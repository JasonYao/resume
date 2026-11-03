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
    )


def test_analyze_selects_light_tier_and_returns_data(ats_ground_truth):
    parser_functions = [
        ("baseline", 0, lambda _: "Jason Yao"),
        ("structured", 1, lambda _: "Google"),
    ]

    analysis = ats_scoring.analyze(
        b"pdf data", ats_ground_truth, (0,), parser_functions
    )

    assert [parser.name for parser in analysis.parsers] == ["baseline"]
    assert next(
        group for group in analysis.parsers[0].groups if group.name == "contact"
    ).matched == 1
    report = ats_scoring.build_report(
        analysis, Path("resume.pdf"), Path("raw-data.json")
    )
    assert [parser["name"] for parser in report["parsers"]] == ["baseline"]


def test_analyze_requires_at_least_one_parser(ats_ground_truth):
    with pytest.raises(ValueError, match="At least one parser"):
        ats_scoring.analyze(b"pdf data", ats_ground_truth, (0,), [])


def test_group_analysis_uses_zero_coverage_when_empty():
    group = ats_scoring.GroupAnalysis("employment", 0, 0, 0.0, ())

    assert group.coverage == 0.0
    with pytest.raises(FrozenInstanceError):
        group.coverage = 1.0


def test_dump_uses_four_space_json_indentation(tmp_path, capsys):
    output_path = tmp_path / "report.json"
    report = {"parsers": [{"name": "baseline", "score": 1.0}]}

    ats_scoring.dump(report, output_path)

    assert output_path.read_text() == (
        '{\n'
        '    "parsers": [\n'
        '        {\n'
        '            "name": "baseline",\n'
        '            "score": 1.0\n'
        '        }\n'
        '    ]\n'
        '}\n'
    )
    assert capsys.readouterr().out == "baseline: 100.0%\n"
