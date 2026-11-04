import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from pyresume import ats_scoring


def test_load_preconditions_reads_inputs(tmp_path, ats_ground_truth):
    pdf_path = tmp_path / "resume.pdf"
    ground_truth_path = tmp_path / "raw-data.json"
    pdf_path.write_bytes(b"pdf data")
    ground_truth_path.write_text(json.dumps(ats_ground_truth))

    pdf, ground_truth = ats_scoring.load_preconditions(pdf_path, ground_truth_path)

    assert pdf == b"pdf data"
    assert ground_truth == ats_ground_truth


def test_parse_args_defaults_to_all_tiers():
    assert ats_scoring.parse_args([
        "--pdf", "resume.pdf",
        "--ground-truth", "raw-data.json",
    ]) == (
        Path("resume.pdf"),
        Path("raw-data.json"),
        (0, 1),
        ats_scoring.DEFAULT_OUTPUT_PATH,
        ats_scoring.DEFAULT_SUMMARY_PATH,
    )


def test_analyze_selects_light_tier_and_returns_data(ats_ground_truth):
    parser_functions = [
        ("baseline", 0, lambda _: "Jason Yao", lambda: "1.0"),
        ("structured", 1, lambda _: "Google", lambda: "2.0"),
    ]

    analysis = ats_scoring.analyze(
        b"pdf data", ats_ground_truth, (0,), parser_functions
    )

    assert [parser.name for parser in analysis.parsers] == ["baseline"]
    assert next(
        group for group in analysis.parsers[0].groups if group.name == "contact"
    ).matched == 1
    assert analysis.parsers[0].duration_seconds >= 0.0
    report = ats_scoring.build_report(
        analysis, Path("resume.pdf"), Path("raw-data.json")
    )
    assert [parser["name"] for parser in report["parsers"]] == ["baseline"]
    assert report["parsers"][0]["version"] == "1.0"
    assert report["parsers"][0]["duration_seconds"] == analysis.parsers[0].duration_seconds
    assert ats_scoring.build_summary(report) == {
        "parsers": [
            {
                "parser": "baseline",
                "version": "1.0",
                "score": report["parsers"][0]["score"],
                "duration_seconds": report["parsers"][0]["duration_seconds"],
            }
        ],
    }


def test_analyze_requires_at_least_one_parser(ats_ground_truth):
    with pytest.raises(ValueError, match="At least one parser"):
        ats_scoring.analyze(b"pdf data", ats_ground_truth, (0,), [])


def test_group_analysis_uses_zero_coverage_when_empty():
    group = ats_scoring.GroupAnalysis("employment", 0, 0, 0.0, ())

    assert group.coverage == 0.0
    with pytest.raises(FrozenInstanceError):
        group.coverage = 1.0


def test_parser_analysis_rejects_negative_duration():
    with pytest.raises(ValueError, match="duration must be finite and nonnegative"):
        ats_scoring.ParserAnalysis(
            name="baseline",
            tier=0,
            version="1.0",
            score=1.0,
            duration_seconds=-0.001,
            groups=(ats_scoring.GroupAnalysis("contact", 1, 1, 1.0, ()),),
        )


def test_parser_analysis_rejects_infinite_duration():
    with pytest.raises(ValueError, match="duration must be finite and nonnegative"):
        ats_scoring.ParserAnalysis(
            name="baseline",
            tier=0,
            version="1.0",
            score=1.0,
            duration_seconds=float("inf"),
            groups=(ats_scoring.GroupAnalysis("contact", 1, 1, 1.0, ()),),
        )


def test_dump_writes_detailed_and_top_line_json(tmp_path, capsys):
    output_path = tmp_path / "report.json"
    summary_path = tmp_path / "summary.json"
    report = {"parsers": [{"name": "baseline", "score": 1.0}]}
    summary = {
        "parsers": [{
            "parser": "baseline",
            "version": "1.0",
            "score": 1.0,
            "duration_seconds": 0.125,
        }]
    }

    ats_scoring.dump(report, summary, output_path, summary_path)

    assert json.loads(output_path.read_text()) == report
    assert json.loads(summary_path.read_text()) == summary
    assert output_path.read_text().startswith('{\n    "parsers"')
    assert capsys.readouterr().out == ""
