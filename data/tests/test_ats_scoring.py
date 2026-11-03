import json

from pyresume.ats_scoring import score_text
from pyresume import ats_scoring


def _ground_truth():
    return {
        "summaries": {
            "personal_data": {
                "name": "Jason Yao",
                "contact": {
                    "email": "Hello@JasonYao.com",
                    "phone": "+1 (949) 335-2639",
                },
            },
            "education": [
                {
                    "name": "New York University",
                    "degree": {"area": "Computer Science"},
                },
            ],
            "skills": {
                "programming": {
                    "Languages": ["Python", "C++"],
                },
            },
        },
        "job_history": [
            {
                "company_name": "Google",
                "positions": [
                    {
                        "title": "Senior Software Engineer",
                        "start_date": "2023-11-01",
                        "end_date": None,
                    },
                ],
            },
        ],
    }


def test_score_text_matches_visible_resume_fields():
    result = score_text(
        "Jason Yao Hello@JasonYao.com +1 (949) 335-2639 "
        "Google Senior Software Engineer November 2023 "
        "New York University Computer Science Python C++",
        _ground_truth(),
    )

    assert result["score"] == 1.0
    assert all(group["coverage"] == 1.0 for group in result["groups"].values())


def test_score_text_reports_missing_fields():
    result = score_text("Jason Yao and Google", _ground_truth())

    assert result["groups"]["contact"]["matched"] == 1
    assert result["groups"]["employment"]["matched"] == 1
    assert result["groups"]["education"]["matched"] == 0
    assert result["groups"]["skills"]["matched"] == 0
    assert result["score"] < 1.0


def test_score_text_matches_month_and_year_dates():
    result = score_text("Senior Software Engineer Nov 2023", _ground_truth())

    assert result["groups"]["employment"]["matched"] == 2


def test_score_text_distinguishes_c_from_cpp():
    result = score_text("C is listed but C++ is not", _ground_truth())

    assert result["groups"]["skills"]["matched"] == 1


def test_score_text_ignores_empty_groups():
    ground_truth = _ground_truth()
    ground_truth["job_history"] = []
    ground_truth["summaries"]["education"] = []
    ground_truth["summaries"]["skills"]["programming"] = {}

    result = score_text(
        "Jason Yao Hello@JasonYao.com +1 (949) 335-2639",
        ground_truth,
    )

    assert result["score"] == 1.0
    assert result["groups"]["employment"]["coverage"] is None


def test_build_report_uses_tier1_only_when_requested(tmp_path, monkeypatch):
    pdf_path = tmp_path / "resume.pdf"
    ground_truth_path = tmp_path / "raw-data.json"
    pdf_path.write_bytes(b"placeholder")
    ground_truth_path.write_text(json.dumps(_ground_truth()))
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

    baseline = ats_scoring.build_report(pdf_path, ground_truth_path)
    all_tiers = ats_scoring.build_report(
        pdf_path, ground_truth_path, include_tier1=True
    )

    assert [parser["name"] for parser in baseline["parsers"]] == ["baseline"]
    assert [parser["name"] for parser in all_tiers["parsers"]] == [
        "baseline",
        "structured",
    ]
