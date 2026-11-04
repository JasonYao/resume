from pyresume.ats_scoring import score_text


def test_score_text_matches_visible_resume_fields(ats_ground_truth):
    result = score_text(
        "Jason Yao Hello@JasonYao.com +1 (949) 335-2639 "
        "Google Senior Software Engineer November 2023 "
        "New York University Computer Science Python C++",
        ats_ground_truth,
    )

    assert result["score"] == 1.0
    assert all(group["coverage"] == 1.0 for group in result["groups"].values())


def test_score_text_reports_missing_fields(ats_ground_truth):
    result = score_text("Jason Yao and Google", ats_ground_truth)

    assert result["groups"]["contact"]["matched"] == 1
    assert result["groups"]["employment"]["matched"] == 1
    assert result["groups"]["education"]["matched"] == 0
    assert result["groups"]["skills"]["matched"] == 0
    assert result["score"] < 1.0


def test_score_text_matches_month_and_year_dates(ats_ground_truth):
    result = score_text("Senior Software Engineer Nov 2023", ats_ground_truth)

    assert result["groups"]["employment"]["matched"] == 2


def test_score_text_distinguishes_c_from_cpp(ats_ground_truth):
    result = score_text("C is listed but C++ is not", ats_ground_truth)

    assert result["groups"]["skills"]["matched"] == 1


def test_score_text_ignores_empty_groups(ats_ground_truth):
    ats_ground_truth["job_history"] = []
    ats_ground_truth["summaries"]["education"] = []
    ats_ground_truth["summaries"]["skills"]["programming"] = {}

    result = score_text(
        "Jason Yao Hello@JasonYao.com +1 (949) 335-2639",
        ats_ground_truth,
    )

    assert result["score"] == 1.0
    assert result["groups"]["employment"]["coverage"] == 0.0
