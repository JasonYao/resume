from ..resume_data import BIOGRAPHY

LINKEDIN_SUMMARY_CHARACTER_LIMIT = 2000


def test_bio_conforms_to_linkedin_character_limit():
    assert len(BIOGRAPHY) < LINKEDIN_SUMMARY_CHARACTER_LIMIT
