from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Any

from dotenv import load_dotenv


def build_email_subject(new_jobs_count: int) -> str:
    """
    Build the subject line for the daily email report.
    """

    return f"CareerSignal Daily Briefing — {new_jobs_count} New Jobs"


def shorten_match_notes(match_notes: str | None, max_parts: int = 4) -> str:
    """
    Keep match notes short enough for the daily email preview.
    """

    if not match_notes:
        return ""

    parts = match_notes.split("; ")
    return "; ".join(parts[:max_parts])


def infer_match_notes(job: dict[str, Any]) -> str:
    """
    Build a simple fallback explanation when match_notes is not present.

    This keeps the email useful even when the scoring layer only provides
    a numeric score.
    """

    existing_notes = shorten_match_notes(job.get("match_notes"))

    if existing_notes:
        return existing_notes

    title = str(job.get("title", "") or "")
    location = str(job.get("location", "") or "")
    department = str(job.get("department", "") or "")
    match_score = job.get("match_score", 0)

    title_lower = title.lower()
    location_lower = location.lower()
    department_lower = department.lower()

    reasons = []

    title_terms = [
        "accounting",
        "accountant",
        "finance",
        "financial",
        "analyst",
        "business",
        "operations",
        "compliance",
        "reporting",
        "data",
        "supervisor",
        "plant",
        "utility",
    ]

    matched_title_terms = [
        term for term in title_terms if term in title_lower
    ]

    if matched_title_terms:
        displayed_terms = ", ".join(sorted(set(matched_title_terms))[:3])
        reasons.append(f"title matches target terms: {displayed_terms}")

    department_terms = [
        "accounting",
        "finance",
        "operations",
        "compliance",
        "reporting",
        "data",
    ]

    matched_department_terms = [
        term for term in department_terms if term in department_lower
    ]

    if matched_department_terms:
        displayed_terms = ", ".join(sorted(set(matched_department_terms))[:2])
        reasons.append(f"department aligns with target area: {displayed_terms}")

    if "remote" in location_lower:
        reasons.append("location is remote-friendly")
    elif "nc" in location_lower or "north carolina" in location_lower:
        reasons.append("location is in North Carolina")
    elif "united states" in location_lower:
        reasons.append("location is in the United States")

    try:
        numeric_score = int(match_score)
    except (TypeError, ValueError):
        numeric_score = 0

    if numeric_score >= 80:
        reasons.append("score falls in the strong match range")
    elif numeric_score >= 60:
        reasons.append("score falls in the possible match range")
    elif numeric_score > 0:
        reasons.append("score shows some alignment with target criteria")

    if not reasons:
        return "Matched by configured title, keyword, location, or scoring rules."

    return "; ".join(reasons[:4])


def get_display_job_url(job: dict[str, Any]) -> str:
    """
    Choose the best URL to display in the email.

    Demo screenshot data should avoid obvious fake URLs. If a demo row still
    contains example.com, this tries to fall back to a real company/career URL
    when one is present in the job dictionary.
    """

    job_url = str(job.get("job_url", "") or "").strip()
    career_url = str(job.get("career_url", "") or "").strip()
    job_url_base = str(job.get("job_url_base", "") or "").strip()

    if job_url and "example.com" not in job_url.lower():
        return job_url

    if career_url and "example.com" not in career_url.lower():
        return career_url

    if job_url_base and "example.com" not in job_url_base.lower():
        return job_url_base

    if job_url:
        return job_url

    return "No URL available"


def build_email_body(
    summary: dict[str, Any],
    new_jobs: list[dict[str, Any]],
    failed_sources: list[dict[str, Any]] | None = None,
) -> str:
    """
    Build a clean plain-text daily email report.

    Args:
        summary: Dictionary containing run summary counts.
        new_jobs: List of new job dictionaries.
        failed_sources: List of failed source dictionaries. Can be empty for now.

    Returns:
        Plain-text email body.
    """

    if failed_sources is None:
        failed_sources = []

    companies_checked = summary.get("companies_checked", 0)
    jobs_found = summary.get("jobs_found", 0)
    jobs_inserted = summary.get("jobs_inserted", 0)
    jobs_updated = summary.get("jobs_updated", 0)
    new_jobs_count = summary.get("new_jobs", len(new_jobs))

    lines = []

    lines.append("CareerSignal Daily Briefing")
    lines.append("=" * 29)
    lines.append("")
    lines.append("Summary")
    lines.append("-" * 7)
    lines.append(f"Companies checked: {companies_checked}")
    lines.append(f"Jobs found: {jobs_found}")
    lines.append(f"Jobs inserted: {jobs_inserted}")
    lines.append(f"Jobs updated: {jobs_updated}")
    lines.append(f"New jobs: {new_jobs_count}")
    lines.append("")

    lines.append("New Jobs")
    lines.append("-" * 8)

    if not new_jobs:
        lines.append("No new jobs found in the last 24 hours.")
    else:
        for index, job in enumerate(new_jobs, start=1):
            company_name = job.get("company_name", "Unknown Company")
            title = job.get("title", "Unknown Title")
            location = job.get("location", "Unknown Location")
            job_url = get_display_job_url(job)
            match_score = job.get("match_score", 0)
            match_notes = infer_match_notes(job)

            lines.append(f"{index}. {company_name}")
            lines.append(f"   Match Score: {match_score}/100")
            lines.append(f"   Title: {title}")
            lines.append(f"   Location: {location}")
            lines.append(f"   Why this matched: {match_notes}")
            lines.append(f"   URL: {job_url}")
            lines.append("")

    lines.append("")
    lines.append("Failed Sources")
    lines.append("-" * 14)

    if not failed_sources:
        lines.append("None.")
    else:
        for source in failed_sources:
            company_name = source.get("company_name", "Unknown Company")
            source_ats = source.get("source_ats", "unknown")
            reason = (
                source.get("reason")
                or source.get("error")
                or "No reason provided"
            )

            lines.append(f"- {company_name} ({source_ats}): {reason}")

    lines.append("")
    lines.append("End of report.")

    return "\n".join(lines)


def load_email_settings() -> dict[str, Any]:
    """
    Load email settings from the .env file.

    Returns:
        Dictionary of email settings.
    """

    load_dotenv()

    required_fields = [
        "EMAIL_HOST",
        "EMAIL_PORT",
        "EMAIL_USERNAME",
        "EMAIL_PASSWORD",
        "EMAIL_FROM",
        "EMAIL_TO",
    ]

    missing_fields = []

    for field in required_fields:
        if not os.getenv(field):
            missing_fields.append(field)

    if missing_fields:
        missing_text = ", ".join(missing_fields)
        raise ValueError(f"Missing required email settings: {missing_text}")

    return {
        "host": os.getenv("EMAIL_HOST"),
        "port": int(os.getenv("EMAIL_PORT", "587")),
        "username": os.getenv("EMAIL_USERNAME"),
        "password": os.getenv("EMAIL_PASSWORD"),
        "from_email": os.getenv("EMAIL_FROM"),
        "to_email": os.getenv("EMAIL_TO"),
    }


def send_email_report(
    subject: str,
    body: str,
    test_mode: bool = True,
) -> None:
    """
    Send the email report, or print a preview if test mode is enabled.

    Args:
        subject: Email subject line.
        body: Plain-text email body.
        test_mode: If True, print preview instead of sending.
    """

    if test_mode:
        print("")
        print("=" * 60)
        print("EMAIL PREVIEW")
        print("=" * 60)
        print(f"Subject: {subject}")
        print("")
        print(body)
        print("=" * 60)
        print("")
        return

    settings = load_email_settings()

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings["from_email"]
    message["To"] = settings["to_email"]
    message.set_content(body)

    with smtplib.SMTP(settings["host"], settings["port"]) as server:
        server.starttls()
        server.login(settings["username"], settings["password"])
        server.send_message(message)

    print("Email report sent successfully.")


def build_and_send_daily_report(
    summary: dict[str, Any],
    new_jobs: list[dict[str, Any]],
    failed_sources: list[dict[str, Any]] | None = None,
    test_mode: bool = True,
) -> None:
    """
    Build and send the full daily report.

    This is the main function other CareerSignal scripts should call.
    """

    new_jobs_count = summary.get("new_jobs", len(new_jobs))

    subject = build_email_subject(new_jobs_count)
    body = build_email_body(
        summary=summary,
        new_jobs=new_jobs,
        failed_sources=failed_sources,
    )

    send_email_report(
        subject=subject,
        body=body,
        test_mode=test_mode,
    )
