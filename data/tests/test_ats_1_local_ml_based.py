from pathlib import Path

from pyresume import ats_scoring


def test_parse_args_accepts_multiple_tiers():
    pdf_path, ground_truth_path, tiers, output_path = ats_scoring.parse_args([
        "--pdf", "resume.pdf",
        "--ground-truth", "raw-data.json",
        "--included-tiers", "0", "1",
    ])

    assert tiers == (0, 1)
    assert pdf_path == Path("resume.pdf")
    assert ground_truth_path == Path("raw-data.json")
    assert output_path == ats_scoring.DEFAULT_OUTPUT_PATH


def test_analyze_includes_local_ml_based_tier_when_requested(ats_ground_truth):
    parser_functions = [
        ("baseline", 0, lambda _: "Jason Yao"),
        ("structured", 1, lambda _: "Google"),
    ]

    analysis = ats_scoring.analyze(
        b"pdf data", ats_ground_truth, (0, 1), parser_functions
    )

    assert [parser.name for parser in analysis.parsers] == [
        "baseline",
        "structured",
    ]
    report = ats_scoring.build_report(
        analysis, Path("resume.pdf"), Path("raw-data.json")
    )
    assert [parser["name"] for parser in report["parsers"]] == [
        "baseline",
        "structured",
    ]
