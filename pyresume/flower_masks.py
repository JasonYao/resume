import argparse
from html.parser import HTMLParser
import math
from pathlib import Path
import subprocess


POINTS_TO_CM = 2.54 / 72
MASK_PADDING_CM = 0.2


class _BBoxParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pages = []
        self.lines = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "page":
            self.pages.append(
                (float(attributes["width"]), float(attributes["height"]))
            )
        elif tag == "line" and all(
            name in attributes for name in ("xmin", "ymin", "xmax", "ymax")
        ):
            self.lines.append(
                tuple(float(attributes[name]) for name in ("xmin", "ymin", "xmax", "ymax"))
            )


def mask_regions_from_bbox(bbox_html, padding=MASK_PADDING_CM):
    parser = _BBoxParser()
    parser.feed(bbox_html)
    if len(parser.pages) != 1:
        raise ValueError(f"Expected a single-page PDF, found {len(parser.pages)} pages")
    if not parser.lines:
        raise ValueError("The PDF contains no measurable text lines")

    page_width_pt, page_height_pt = parser.pages[0]
    page_width_cm = page_width_pt * POINTS_TO_CM
    page_height_cm = page_height_pt * POINTS_TO_CM
    regions = []
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
    return regions


def _format_regions(regions):
    lua_regions = ["return {"]
    tex_regions = []
    for x0, y0, x1, y1 in regions:
        lua_regions.append(f"  {{ {x0:.3f}, {y0:.3f}, {x1:.3f}, {y1:.3f} }},")
        tex_regions.append(
            f"\\resumeFlowerMaskBox{{{x0:.3f}cm}}{{{y0:.3f}cm}}"
            f"{{{x1:.3f}cm}}{{{y1:.3f}cm}}"
        )
    lua_regions.append("}")
    return "\n".join(lua_regions) + "\n", "\n".join(tex_regions) + "\n"


def generate_flower_masks(pdf_path):
    result = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    regions = mask_regions_from_bbox(result.stdout)
    lua_content, tex_content = _format_regions(regions)
    Path("resume_flower_masks.lua").write_text(lua_content)
    Path("resume_flower_masks_preview.tex").write_text(tex_content)


def main():
    parser = argparse.ArgumentParser(description="Measure text regions for flower masks")
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    generate_flower_masks(args.pdf)


if __name__ == "__main__":
    main()
