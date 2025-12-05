from ..resume_data import BIOGRAPHY

# See https://github.com/JasonYao/resume/issues/39#issuecomment-1780577908
# for more information on LinkedIn character limits
LINKEDIN_SUMMARY_CHARACTER_LIMIT = 2600


def test_bio_conforms_to_linkedin_character_limit():
  assert len(BIOGRAPHY) < LINKEDIN_SUMMARY_CHARACTER_LIMIT
