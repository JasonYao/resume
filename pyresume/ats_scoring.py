import argparse
from collections.abc import Callable
from difflib import SequenceMatcher
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
            "coverage": len(matched) / total if total else None,
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


def _extract_pdftotext(pdf_path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _extract_pdfplumber(pdf_path: Path) -> str:
    import pdfplumber

    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text(layout=True) or "" for page in pdf.pages)


def _extract_docling(pdf_path: Path) -> str:
    from docling.document_converter import DocumentConverter

    document = DocumentConverter().convert(str(pdf_path)).document
    return document.export_to_markdown()


def _extract_unstructured(pdf_path: Path) -> str:
    from unstructured.partition.pdf import partition_pdf

    elements = partition_pdf(filename=str(pdf_path), strategy="fast")
    return "\n".join(str(element) for element in elements)


TIER0_PARSERS: list[tuple[str, str, Callable[[Path], str]]] = [
    ("pdftotext-layout", "tier0", _extract_pdftotext),
    ("pdfplumber-layout", "tier0", _extract_pdfplumber),
]
TIER1_PARSERS: list[tuple[str, str, Callable[[Path], str]]] = [
    ("docling", "tier1", _extract_docling),
    ("unstructured", "tier1", _extract_unstructured),
]


def build_report(
    pdf_path: Path, ground_truth_path: Path, include_tier1: bool = False
) -> dict:
    ground_truth = json.loads(ground_truth_path.read_text())
    parsers = []
    selected_parsers = [*TIER0_PARSERS]
    if include_tier1:
        selected_parsers.extend(TIER1_PARSERS)
    for name, tier, extractor in selected_parsers:
        text = extractor(pdf_path)
        score = score_text(text, ground_truth)
        parsers.append({
            "name": name,
            "tier": tier,
            **score,
        })
    return {
        "pdf": str(pdf_path),
        "ground_truth": str(ground_truth_path),
        "metric": "weighted expected-field text coverage (not field extraction precision)",
        "weights": GROUP_WEIGHTS,
        "parsers": parsers,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score PDF text extraction against the resume source JSON."
    )
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("ats-report.json"))
    parser.add_argument(
        "--include-tier1",
        action="store_true",
        help="Also run the heavyweight Docling and Unstructured parsers.",
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF does not exist: {args.pdf}")
    if not args.ground_truth.is_file():
        parser.error(f"Ground-truth JSON does not exist: {args.ground_truth}")

    report = build_report(args.pdf, args.ground_truth, args.include_tier1)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    for result in report["parsers"]:
        print(f'{result["name"]}: {result["score"]:.1%}')


if __name__ == "__main__":
    main()
