import argparse
from collections.abc import Callable
from dataclasses import dataclass
from difflib import SequenceMatcher
from importlib.metadata import version as package_version
from io import BytesIO
import json
from pathlib import Path
import re
import subprocess
import unicodedata

from dateutil.parser import isoparse


GROUP_WEIGHTS = {
    "contact": 0.3,
    "employment": 0.4,
    "education": 0.2,
    "skills": 0.1,
}
DEFAULT_OUTPUT_PATH = Path("ats-report.json")
DEFAULT_SUMMARY_PATH = Path("ats-summary.json")


@dataclass(frozen=True)
class MissingField:
    # Ground-truth field label, such as "email".
    field: str
    # Expected value that was not found, such as "person@example.com".
    value: str


@dataclass(frozen=True)
class GroupAnalysis:
    # Dimension being scored, such as "contact".
    name: str
    # Number of expected values found; integer range is 0 through total.
    matched: int
    # Number of expected values; nonnegative integer.
    total: int
    # Matched / total in [0.0, 1.0]; zero when total is zero (no fields).
    coverage: float
    # Expected values not found, e.g. (MissingField("email", "..."),); empty means none.
    missing: tuple[MissingField, ...]

    def __post_init__(self) -> None:
        if self.total < 0 or not 0 <= self.matched <= self.total:
            raise ValueError("Group counts must satisfy 0 <= matched <= total")
        if len(self.missing) != self.total - self.matched:
            raise ValueError("Missing values must account for unmatched fields")
        if not 0.0 <= self.coverage <= 1.0:
            raise ValueError("Group coverage must be between 0 and 1")
        expected_coverage = self.matched / self.total if self.total else 0.0
        if self.coverage != expected_coverage:
            raise ValueError("Group coverage must match its counts")


@dataclass(frozen=True)
class ParserAnalysis:
    # Parser identifier, such as "pdftotext-layout".
    name: str
    # Parser tier: 0 (lightweight) or 1 (local ML-based).
    tier: int
    # Installed parser version, such as "25.02.0".
    version: str
    # Weighted expected-field coverage in [0.0, 1.0].
    score: float
    # Per-dimension results, e.g. (GroupAnalysis("contact", ...),).
    groups: tuple[GroupAnalysis, ...]

    def __post_init__(self) -> None:
        if self.tier not in (0, 1):
            raise ValueError("Parser tier must be 0 or 1")
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Parser score must be between 0 and 1")
        if not self.groups:
            raise ValueError("A parser result must contain at least one group")


@dataclass(frozen=True)
class ATSAnalysis:
    # Per-parser results, e.g. (ParserAnalysis("pdftotext-layout", ...),).
    parsers: tuple[ParserAnalysis, ...]

    def __post_init__(self) -> None:
        if not self.parsers:
            raise ValueError("An analysis must contain at least one parser")


def main() -> None:
    pdf_path, ground_truth_path, active_tiers, output_path, summary_path = parse_args()
    pdf, ground_truth = load_preconditions(pdf_path, ground_truth_path)
    analysis = analyze(
        pdf, ground_truth, active_tiers, [*TIER0_PARSERS, *TIER1_PARSERS]
    )
    report = build_report(analysis, pdf_path, ground_truth_path)
    summary = build_summary(report)
    dump(report, summary, output_path, summary_path)


def parse_args(
    argv: list[str] | None = None,
) -> tuple[Path, Path, tuple[int, ...], Path, Path]:
    parser = argparse.ArgumentParser(
        description="Score PDF text extraction against the resume source JSON."
    )
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument(
        "--included-tiers",
        nargs="+",
        type=int,
        choices=(0, 1),
        default=(0, 1),
        help="Parser tiers to run (0: lightweight, 1: local ML-based).",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_PATH)
    args = parser.parse_args(argv)

    return (
        args.pdf,
        args.ground_truth,
        tuple(args.included_tiers),
        args.output,
        args.summary_output,
    )


def load_preconditions(
    pdf_path: Path, ground_truth_path: Path
) -> tuple[bytes, dict]:
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF does not exist: {pdf_path}")
    if not ground_truth_path.is_file():
        raise FileNotFoundError(f"Ground-truth JSON does not exist: {ground_truth_path}")
    return pdf_path.read_bytes(), json.loads(ground_truth_path.read_text())


def analyze(
    pdf: bytes,
    ground_truth: dict,
    active_tiers: tuple[int, ...],
    parsers: list[tuple[str, int, Callable[[bytes], str], Callable[[], str]]],
) -> ATSAnalysis:
    if len(parsers) < 1:
        raise ValueError("At least one parser must be configured")
    results = []
    for name, tier, extractor, get_version in parsers:
        if tier not in active_tiers:
            continue
        text = extractor(pdf)
        score = score_text(text, ground_truth)
        results.append(ParserAnalysis(
            name=name,
            tier=tier,
            version=get_version(),
            score=score["score"],
            groups=tuple(
                GroupAnalysis(
                    name=group_name,
                    matched=result["matched"],
                    total=result["total"],
                    coverage=result["coverage"],
                    missing=tuple(
                        MissingField(**item) for item in result["missing"]
                    ),
                )
                for group_name, result in score["groups"].items()
            ),
        ))
    return ATSAnalysis(tuple(results))


def build_report(
    analysis: ATSAnalysis, pdf_path: Path, ground_truth_path: Path
) -> dict:
    return {
        "pdf": str(pdf_path),
        "ground_truth": str(ground_truth_path),
        "metric": "weighted expected-field text coverage (not field extraction precision)",
        "weights": GROUP_WEIGHTS,
        "parsers": [
            {
                "name": parser.name,
                "tier": parser.tier,
                "version": parser.version,
                "score": parser.score,
                "groups": {
                    group.name: {
                        "matched": group.matched,
                        "total": group.total,
                        "coverage": group.coverage,
                        "missing": [
                            {"field": item.field, "value": item.value}
                            for item in group.missing
                        ],
                    }
                    for group in parser.groups
                },
            }
            for parser in analysis.parsers
        ],
    }


def build_summary(report: dict) -> dict:
    return {
        "parsers": [
            {
                "parser": parser["name"],
                "version": parser["version"],
                "score": parser["score"],
            }
            for parser in report["parsers"]
        ],
    }


def dump(
    report: dict, summary: dict, output_path: Path, summary_path: Path
) -> None:
    output_path.write_text(json.dumps(report, indent=4) + "\n")
    summary_path.write_text(json.dumps(summary, indent=4) + "\n")


def _expected_fields(ground_truth: dict) -> dict[str, list[dict[str, str]]]:
    summaries = ground_truth["summaries"]
    contact = summaries["personal_data"]["contact"]

    fields = {
        "contact": [
            {"field": "name", "value": summaries["personal_data"]["name"]},
            {"field": "email", "value": contact["email"]},
            {"field": "phone", "value": contact["phone"]},
        ],
        "employment": [],
        "education": [],
        "skills": [],
    }

    for company in ground_truth["job_history"]:
        fields["employment"].append({
            "field": "employer",
            "value": company["company_name"],
        })
        for position in company["positions"]:
            fields["employment"].append({
                "field": "job title",
                "value": position["title"],
            })
            for date_field in ("start_date", "end_date"):
                value = position[date_field]
                if value:
                    fields["employment"].append({
                        "field": date_field.replace("_", " "),
                        "value": value,
                        "kind": "date",
                    })

    for education in summaries["education"]:
        fields["education"].append({
            "field": "school",
            "value": education["name"],
        })
        degree = education.get("degree", {})
        if degree.get("area"):
            fields["education"].append({
                "field": "degree area",
                "value": degree["area"],
            })

    for category in summaries["skills"]["programming"].values():
        if isinstance(category, list):
            fields["skills"].extend(
                {"field": "skill", "value": skill} for skill in category
            )

    return fields


def _normalized_tokens(value: str) -> list[str]:
    # NFKD decomposes compatibility forms and accents so they tokenize consistently.
    # Unlike NFC/NFKC, it exposes combining marks for removal; it also decomposes
    # compatibility forms (such as ligatures) that can differ in PDF extraction.
    normalized = unicodedata.normalize("NFKD", value).casefold()
    normalized = "".join(
        character for character in normalized
        if not unicodedata.combining(character)
    )
    return re.findall(r"[a-z0-9]+[+#]*", normalized)


def _date_matches(value: str, text_tokens: list[str]) -> bool:
    parsed = isoparse(value)
    month = parsed.strftime("%B").casefold()
    abbreviated_month = parsed.strftime("%b").casefold()
    year = str(parsed.year)
    text = " ".join(text_tokens)
    month_aliases = {
        "september": "sep",
        "june": "jun",
        "july": "jul",
    }
    abbreviated_month = month_aliases.get(month, abbreviated_month)
    return (
        f"{month} {year}" in text
        or f"{abbreviated_month} {year}" in text
        or f"{year} {month}" in text
        or f"{year} {abbreviated_month}" in text
    )


def _contains_value(value: str, text_tokens: list[str], kind: str = "") -> bool:
    if kind == "date":
        return _date_matches(value, text_tokens)

    expected = _normalized_tokens(value)
    if not expected or not text_tokens:
        return False
    width = len(expected)
    for start in range(max(1, len(text_tokens) - width + 1)):
        candidate = text_tokens[start:start + width]
        if len(candidate) == width and candidate == expected:
            return True
        if width > 1 and len(candidate) == width:
            if SequenceMatcher(None, " ".join(expected), " ".join(candidate)).ratio() >= 0.9:
                return True
    return False


def score_text(text: str, ground_truth: dict) -> dict:
    text_tokens = _normalized_tokens(text)
    expected = _expected_fields(ground_truth)
    groups = {}
    for group_name, fields in expected.items():
        matched = []
        missing = []
        for item in fields:
            entry = {"field": item["field"], "value": item["value"]}
            (matched if _contains_value(
                item["value"], text_tokens, item.get("kind", "")
            ) else missing).append(entry)
        total = len(fields)
        groups[group_name] = {
            "matched": len(matched),
            "total": total,
            "coverage": len(matched) / total if total else 0.0,
            "missing": missing,
        }

    active_groups = [
        (group, result)
        for group, result in groups.items()
        if result["total"]
    ]
    active_weight = sum(GROUP_WEIGHTS[group] for group, _ in active_groups)
    weighted_score = (
        sum(
            GROUP_WEIGHTS[group] * result["coverage"]
            for group, result in active_groups
        ) / active_weight
        if active_weight
        else 0.0
    )
    return {"score": weighted_score, "groups": groups}


def _pdftotext_version() -> str:
    result = subprocess.run(
        ["pdftotext", "-v"], capture_output=True, text=True, check=True
    )
    match = re.search(r"version\s+([^\s]+)", result.stderr + result.stdout)
    if not match:
        raise RuntimeError("Could not determine pdftotext version")
    return match.group(1)


def _package_version(package_name: str) -> Callable[[], str]:
    return lambda: package_version(package_name)


def _extract_pdftotext(pdf: bytes) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", "-", "-"],
        check=True,
        capture_output=True,
        input=pdf,
    )
    return result.stdout.decode("utf-8", errors="replace")


def _extract_pdfplumber(pdf: bytes) -> str:
    import pdfplumber

    with pdfplumber.open(BytesIO(pdf)) as document:
        return "\n".join(
            page.extract_text(layout=True) or "" for page in document.pages
        )


def _extract_docling(pdf: bytes) -> str:
    from docling.document_converter import DocumentConverter
    from docling.datamodel.base_models import DocumentStream

    source = DocumentStream(name="resume.pdf", stream=BytesIO(pdf))
    document = DocumentConverter().convert(source).document
    return document.export_to_markdown()


def _extract_unstructured(pdf: bytes) -> str:
    from unstructured.partition.pdf import partition_pdf

    elements = partition_pdf(file=BytesIO(pdf), strategy="fast")
    return "\n".join(str(element) for element in elements)


TIER0_PARSERS: list[
    tuple[str, int, Callable[[bytes], str], Callable[[], str]]
] = [
    ("pdftotext-layout", 0, _extract_pdftotext, _pdftotext_version),
    ("pdfplumber-layout", 0, _extract_pdfplumber, _package_version("pdfplumber")),
]
TIER1_PARSERS: list[
    tuple[str, int, Callable[[bytes], str], Callable[[], str]]
] = [
    ("docling", 1, _extract_docling, _package_version("docling")),
    ("unstructured", 1, _extract_unstructured, _package_version("unstructured")),
]
if __name__ == "__main__":
    main()
