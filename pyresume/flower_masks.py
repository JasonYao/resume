from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
import math
from pathlib import Path
import subprocess


POINTS_TO_CM = 2.54 / 72
MASK_PADDING_CM = 0.2
RegionCoordinates = tuple[float, float, float, float]


def main() -> None:
    pdf_path = parse_arguments()
    regions = isolate_regions(pdf_path)
    dump(regions)


def parse_arguments() -> Path:
    parser = argparse.ArgumentParser(description="Measure text regions for flower masks")
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    return args.pdf


def isolate_regions(pdf_path: Path) -> MeasuredRegions:
    result = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return mask_regions_from_bbox(result.stdout)


def dump(regions: MeasuredRegions) -> None:
    lua_content, tex_content = _format_regions(regions)
    Path("resume_flower_masks.lua").write_text(lua_content)
    Path("resume_flower_masks_preview.tex").write_text(tex_content)


@dataclass(frozen=True)
class MeasuredRegions:
    page_width_cm: float
    page_height_cm: float
    regions: tuple[RegionCoordinates, ...]

    def __post_init__(self) -> None:
        if not math.isfinite(self.page_width_cm) or self.page_width_cm <= 0:
            raise ValueError("Page width must be finite and positive")
        if not math.isfinite(self.page_height_cm) or self.page_height_cm <= 0:
            raise ValueError("Page height must be finite and positive")
        if not self.regions:
            raise ValueError("At least one measurable text region is required")
        for x0, y0, x1, y1 in self.regions:
            if not all(math.isfinite(value) for value in (x0, y0, x1, y1)):
                raise ValueError("Region coordinates must be finite")
            if not (0 <= x0 < x1 <= self.page_width_cm):
                raise ValueError("Region must fit within the page width")
            if not (0 <= y0 < y1 <= self.page_height_cm):
                raise ValueError("Region must fit within the page height")


class _BBoxParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.pages: list[tuple[float, float]] = []
        self.lines: list[RegionCoordinates] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag == "page":
            self.pages.append((
                float(attributes["width"] or ""),
                float(attributes["height"] or ""),
            ))
        elif tag == "line" and all(
            name in attributes for name in ("xmin", "ymin", "xmax", "ymax")
        ):
            values = tuple(
                attributes[name] for name in ("xmin", "ymin", "xmax", "ymax")
            )
            if all(value is not None for value in values):
                self.lines.append(tuple(float(value) for value in values))


def mask_regions_from_bbox(
    bbox_html: str, padding: float = MASK_PADDING_CM
) -> MeasuredRegions:
    parser = _BBoxParser()
    parser.feed(bbox_html)
    if len(parser.pages) != 1:
        raise ValueError(f"Expected a single-page PDF, found {len(parser.pages)} pages")
    if not parser.lines:
        raise ValueError("The PDF contains no measurable text lines")

    page_width_pt, page_height_pt = parser.pages[0]
    page_width_cm = round(page_width_pt * POINTS_TO_CM, 3)
    page_height_cm = round(page_height_pt * POINTS_TO_CM, 3)
    regions: list[RegionCoordinates] = []
    for x_min, y_min, x_max, y_max in parser.lines:
        if not all(math.isfinite(value) for value in (x_min, y_min, x_max, y_max)):
            continue
        x0 = max(0, x_min * POINTS_TO_CM - padding)
        y0 = max(0, page_height_cm - y_max * POINTS_TO_CM - padding)
        x1 = min(page_width_cm, x_max * POINTS_TO_CM + padding)
        y1 = min(page_height_cm, page_height_cm - y_min * POINTS_TO_CM + padding)
        if x0 < x1 and y0 < y1:
            regions.append(tuple(round(value, 3) for value in (x0, y0, x1, y1)))
    if not regions:
        raise ValueError("The PDF contains no valid measurable text lines")
    return MeasuredRegions(page_width_cm, page_height_cm, tuple(regions))


def _format_regions(regions: MeasuredRegions) -> tuple[str, str]:
    lua_regions = ["return {"]
    tex_regions = []
    for x0, y0, x1, y1 in regions.regions:
        lua_regions.append(f"  {{ {x0:.3f}, {y0:.3f}, {x1:.3f}, {y1:.3f} }},")
        tex_regions.append(
            f"\\resumeFlowerMaskBox{{{x0:.3f}cm}}{{{y0:.3f}cm}}"
            f"{{{x1:.3f}cm}}{{{y1:.3f}cm}}"
        )
    lua_regions.append("}")
    return "\n".join(lua_regions) + "\n", "\n".join(tex_regions) + "\n"


if __name__ == "__main__":
    main()
