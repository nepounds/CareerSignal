from careersignal.email_report import build_email_body, build_email_subject


def test_build_email_subject_includes_new_job_count():
    subject = build_email_subject(3)

    assert "CareerSignal" in subject
    assert "3" in subject


def test_build_email_body_includes_summary_and_job_details():
    summary = {
        "companies_checked": 5,
        "jobs_found": 12,
        "jobs_inserted": 2,
        "jobs_updated": 10,
        "new_jobs": 1,
    }

    new_jobs = [
        {
            "company_name": "Example Company",
            "title": "Accounting Analyst",
            "location": "Raleigh, NC",
            "job_url": "https://example.com/jobs/123",
            "match_score": 92,
            "match_notes": "title matches accounting; location is in North Carolina",
        }
    ]

    body = build_email_body(
        summary=summary,
        new_jobs=new_jobs,
        failed_sources=[],
    )

    assert "CareerSignal Daily Briefing" in body
    assert "Companies checked: 5" in body
    assert "Jobs found: 12" in body
    assert "New jobs: 1" in body
    assert "Example Company" in body
    assert "Accounting Analyst" in body
    assert "Raleigh, NC" in body
    assert "Match Score: 92/100" in body
    assert "Why this matched:" in body
    assert "https://example.com/jobs/123" in body


def test_build_email_body_includes_failed_sources():
    summary = {
        "companies_checked": 1,
        "jobs_found": 0,
        "jobs_inserted": 0,
        "jobs_updated": 0,
        "new_jobs": 0,
    }

    failed_sources = [
        {
            "company_name": "Broken Company",
            "source_ats": "workday",
            "reason": "HTTP error",
        }
    ]

    body = build_email_body(
        summary=summary,
        new_jobs=[],
        failed_sources=failed_sources,
    )

    assert "No new jobs found in the last 24 hours." in body
    assert "Broken Company" in body
    assert "workday" in body
    assert "HTTP error" in body