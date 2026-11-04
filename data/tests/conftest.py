import pytest


@pytest.fixture
def ats_ground_truth():
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
