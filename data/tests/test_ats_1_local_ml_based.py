import json

from pyresume import ats_scoring


def test_build_report_includes_local_ml_based_parsers_when_requested(
    tmp_path, monkeypatch, ats_ground_truth
):
    pdf_path = tmp_path / "resume.pdf"
    ground_truth_path = tmp_path / "raw-data.json"
    pdf_path.write_bytes(b"placeholder")
    ground_truth_path.write_text(json.dumps(ats_ground_truth))
    monkeypatch.setattr(
        ats_scoring,
        "TIER0_PARSERS",
        [("baseline", "tier0", lambda _: "Jason Yao")],
    )
    monkeypatch.setattr(
        ats_scoring,
        "TIER1_PARSERS",
        [("structured", "tier1", lambda _: "Google")],
    )

    analysis = ats_scoring.analyze(
        pdf_path, ground_truth_path, ("tier0", "tier1")
    )

    assert [parser.name for parser in analysis.parsers] == ["baseline", "structured"]
    report = ats_scoring.build_report(analysis)
    assert [parser["name"] for parser in report["parsers"]] == [
        "baseline",
        "structured",
    ]
