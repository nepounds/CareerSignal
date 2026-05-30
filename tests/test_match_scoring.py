from careersignal.match_scoring import score_job


def get_score(job):
    result = score_job(job)

    if isinstance(result, dict):
        return result.get("match_score", result.get("score", 0))

    return result


def test_score_job_returns_number_in_expected_range():
    job = {
        "company_name": "Example Company",
        "source_ats": "workday",
        "external_job_id": "123",
        "title": "Financial Analyst",
        "location": "Raleigh, NC",
        "department": "Finance",
        "job_url": "https://example.com/job/123",
        "posted_date": "2026-05-30",
        "date_collected": "2026-05-30",
    }

    score = get_score(job)

    assert isinstance(score, (int, float))
    assert 0 <= score <= 100


def test_score_job_rewards_relevant_analyst_role():
    strong_job = {
        "company_name": "Example Company",
        "source_ats": "workday",
        "external_job_id": "strong-1",
        "title": "Accounting Analyst",
        "location": "Raleigh, NC",
        "department": "Accounting",
        "job_url": "https://example.com/job/strong-1",
        "posted_date": "2026-05-30",
        "date_collected": "2026-05-30",
    }

    weak_job = {
        "company_name": "Example Company",
        "source_ats": "workday",
        "external_job_id": "weak-1",
        "title": "Senior Software Engineer",
        "location": "California",
        "department": "Engineering",
        "job_url": "https://example.com/job/weak-1",
        "posted_date": "2026-05-30",
        "date_collected": "2026-05-30",
    }

    strong_score = get_score(strong_job)
    weak_score = get_score(weak_job)

    assert strong_score > weak_score