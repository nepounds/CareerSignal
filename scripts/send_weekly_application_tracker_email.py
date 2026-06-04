"""
Send or preview the weekly CareerSignal Application Tracker email.

Step 17G:
- Keeps the weekly Application Tracker email separate from the daily job alert email.
- Uses the existing Application Tracker database table: applications.
- Uses the existing database path: data/careersignal.db.
- Does not modify the daily job alert email.
- Does not modify Excel export.
- Does not modify Power BI.
"""

from __future__ import annotations

import argparse
import os
import smtplib
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from careersignal.application_tracker import fetch_applications  # noqa: E402


SUBJECT = "CareerSignal Weekly Application Tracker Summary"


def load_dotenv_file(env_path: Path) -> None:
    """
    Minimal .env loader.

    This avoids adding a new dependency just for this script.
    Existing environment variables win over .env values.
    """
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def get_env_value(*names: str, default: str | None = None) -> str | None:
    """Return the first non-empty environment variable from a list of possible names."""
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def parse_date(value: Any) -> date | None:
    """
    Parse date-ish values from SQLite rows.

    Handles:
    - None
    - YYYY-MM-DD
    - YYYY-MM-DD HH:MM:SS
    - ISO timestamps
    """
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        pass

    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def start_of_week(today: date) -> date:
    """Return Monday for the week containing today."""
    return today - timedelta(days=today.weekday())


def is_between(value: date | None, start_date: date, end_date: date) -> bool:
    """Return True if value is between start_date and end_date, inclusive."""
    if value is None:
        return False
    return start_date <= value <= end_date


def clean_text(value: Any, fallback: str = "") -> str:
    """Convert None-ish values to a clean string."""
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def status_is_active(status: str) -> bool:
    """Statuses that still represent an active, unresolved application."""
    return status in {"applied", "interview"}


def application_has_response(application: dict[str, Any]) -> bool:
    """
    Determine whether an application has received any response.

    For aging watchlists, we mostly care about applications still sitting in applied status.
    """
    status = clean_text(application.get("status")).lower()

    if status != "applied":
        return True

    response_fields = [
        "first_response_date",
        "interview_date",
        "final_response_date",
    ]

    return any(parse_date(application.get(field)) is not None for field in response_fields)


def get_days_since_applied(application: dict[str, Any], today: date) -> int | None:
    """Return days since date_applied, or None if missing/bad."""
    applied_date = parse_date(application.get("date_applied"))

    if applied_date is None:
        return None

    return (today - applied_date).days


def get_aging_bucket(days_since_applied: int | None) -> str:
    """Return the current aging bucket for an unresolved application."""
    if days_since_applied is None:
        return "unknown"

    if days_since_applied <= 14:
        return "normal waiting period"

    if 15 <= days_since_applied <= 30:
        return "rejection danger zone"

    if 31 <= days_since_applied <= 60:
        return "ghosting danger zone"

    return "61+ day ghosting candidate"


def build_company_summary(applications: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build company-level totals for the weekly email."""
    summary: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "company_name": "",
            "total_applications": 0,
            "active_applications": 0,
            "interviews": 0,
            "acceptances": 0,
            "formal_rejections": 0,
            "ghostings": 0,
            "negative_outcomes": 0,
        }
    )

    for application in applications:
        company_name = clean_text(application.get("company_name"), "Unknown Company")
        status = clean_text(application.get("status")).lower()

        row = summary[company_name]
        row["company_name"] = company_name
        row["total_applications"] += 1

        if status_is_active(status):
            row["active_applications"] += 1

        if status == "interview":
            row["interviews"] += 1
        elif status == "accepted":
            row["acceptances"] += 1
        elif status == "rejected":
            row["formal_rejections"] += 1
            row["negative_outcomes"] += 1
        elif status == "ghosted":
            row["ghostings"] += 1
            row["negative_outcomes"] += 1

    return sorted(
        summary.values(),
        key=lambda row: (
            row["total_applications"],
            row["interviews"],
            row["acceptances"],
            row["negative_outcomes"],
        ),
        reverse=True,
    )


def format_application_line(application: dict[str, Any], today: date | None = None) -> str:
    """Format one application as a readable bullet line."""
    application_id = application.get("application_id")
    company_name = clean_text(application.get("company_name"), "Unknown Company")
    job_title = clean_text(application.get("job_title"), "Unknown Job Title")
    status = clean_text(application.get("status"), "unknown")
    date_applied = clean_text(application.get("date_applied"), "unknown date")

    if today is None:
        return f"- #{application_id}: {company_name} | {job_title} | {status} | applied {date_applied}"

    days_since = get_days_since_applied(application, today)
    if days_since is None:
        return f"- #{application_id}: {company_name} | {job_title} | {status} | applied {date_applied}"

    return (
        f"- #{application_id}: {company_name} | {job_title} | {status} | "
        f"applied {date_applied} | {days_since} days ago"
    )


def format_application_list(
    applications: list[dict[str, Any]],
    today: date | None = None,
    empty_message: str = "- None",
    limit: int = 15,
) -> str:
    """Format a list of applications for the email body."""
    if not applications:
        return empty_message

    lines = [format_application_line(application, today=today) for application in applications[:limit]]

    extra_count = len(applications) - limit
    if extra_count > 0:
        lines.append(f"- Plus {extra_count} more")

    return "\n".join(lines)


def build_weekly_tracker_email_body(applications: list[dict[str, Any]]) -> str:
    """Build the complete weekly Application Tracker email body."""
    today = date.today()
    week_start = start_of_week(today)

    applications_this_week = []
    interviews_this_week = []
    rejections_this_week = []
    ghostings_this_week = []

    rejection_danger_zone = []
    ghosting_danger_zone = []
    sixty_one_plus_candidates = []

    total_applications = len(applications)
    active_applications = 0
    interviews = 0
    acceptances = 0
    formal_rejections = 0
    ghostings = 0
    negative_outcomes = 0

    for application in applications:
        status = clean_text(application.get("status")).lower()
        date_applied = parse_date(application.get("date_applied"))
        first_response_date = parse_date(application.get("first_response_date"))
        interview_date = parse_date(application.get("interview_date"))
        final_response_date = parse_date(application.get("final_response_date"))
        updated_at = parse_date(application.get("updated_at"))

        if status_is_active(status):
            active_applications += 1

        if status == "interview":
            interviews += 1
        elif status == "accepted":
            acceptances += 1
        elif status == "rejected":
            formal_rejections += 1
            negative_outcomes += 1
        elif status == "ghosted":
            ghostings += 1
            negative_outcomes += 1

        if is_between(date_applied, week_start, today):
            applications_this_week.append(application)

        if status == "interview" and (
            is_between(interview_date, week_start, today)
            or is_between(first_response_date, week_start, today)
            or is_between(updated_at, week_start, today)
        ):
            interviews_this_week.append(application)

        if status == "rejected" and (
            is_between(final_response_date, week_start, today)
            or is_between(updated_at, week_start, today)
        ):
            rejections_this_week.append(application)

        if status == "ghosted" and (
            is_between(final_response_date, week_start, today)
            or is_between(updated_at, week_start, today)
        ):
            ghostings_this_week.append(application)

        if status == "applied" and not application_has_response(application):
            days_since = get_days_since_applied(application, today)
            aging_bucket = get_aging_bucket(days_since)

            if aging_bucket == "rejection danger zone":
                rejection_danger_zone.append(application)
            elif aging_bucket == "ghosting danger zone":
                ghosting_danger_zone.append(application)
            elif aging_bucket == "61+ day ghosting candidate":
                sixty_one_plus_candidates.append(application)

    company_summary = build_company_summary(applications)

    company_lines = []
    for row in company_summary:
        company_lines.append(
            "- {company}: {total} total | {active} active | {interviews} interviews | "
            "{rejections} rejected | {ghostings} ghosted | {acceptances} accepted".format(
                company=row["company_name"],
                total=row["total_applications"],
                active=row["active_applications"],
                interviews=row["interviews"],
                rejections=row["formal_rejections"],
                ghostings=row["ghostings"],
                acceptances=row["acceptances"],
            )
        )

    if not company_lines:
        company_lines.append("- None")

    body = f"""CareerSignal Weekly Application Tracker Summary

Report date: {today.isoformat()}
Week covered: {week_start.isoformat()} through {today.isoformat()}

1. This Week
- Applications submitted this week: {len(applications_this_week)}
- Interviews received this week: {len(interviews_this_week)}
- Rejections received this week: {len(rejections_this_week)}
- Ghostings identified this week: {len(ghostings_this_week)}

Applications submitted this week:
{format_application_list(applications_this_week)}

Interviews received this week:
{format_application_list(interviews_this_week)}

Rejections received this week:
{format_application_list(rejections_this_week)}

Ghostings identified this week:
{format_application_list(ghostings_this_week)}

2. Current Totals
- Total applications: {total_applications}
- Active applications: {active_applications}
- Interviews: {interviews}
- Acceptances: {acceptances}
- Formal rejections: {formal_rejections}
- Ghostings: {ghostings}
- Negative outcomes: {negative_outcomes}

3. Aging Watchlist
- Rejection danger zone, 15-30 days with no response: {len(rejection_danger_zone)}
- Ghosting danger zone, 31-60 days with no response: {len(ghosting_danger_zone)}
- 61+ day ghosting candidates: {len(sixty_one_plus_candidates)}

Rejection danger zone:
{format_application_list(rejection_danger_zone, today=today)}

Ghosting danger zone:
{format_application_list(ghosting_danger_zone, today=today)}

61+ day ghosting candidates:
{format_application_list(sixty_one_plus_candidates, today=today)}

4. Company Summary
{chr(10).join(company_lines)}
"""

    return body


def get_email_config() -> dict[str, str | int]:
    """
    Read email config from environment variables.

    Supports several common names so this can match the existing project setup
    without touching the daily email module.
    """
    load_dotenv_file(PROJECT_ROOT / ".env")

    smtp_host = get_env_value("SMTP_HOST", "SMTP_SERVER", "EMAIL_HOST", default="smtp.gmail.com")
    smtp_port_raw = get_env_value("SMTP_PORT", "EMAIL_PORT", default="587")
    smtp_username = get_env_value("SMTP_USERNAME", "EMAIL_USERNAME", "EMAIL_SENDER", "EMAIL_FROM")
    smtp_password = get_env_value("SMTP_PASSWORD", "EMAIL_PASSWORD", "EMAIL_APP_PASSWORD")
    email_from = get_env_value("EMAIL_FROM", "EMAIL_SENDER", "SMTP_USERNAME", "EMAIL_USERNAME")
    email_to = get_env_value("EMAIL_TO", "EMAIL_RECIPIENT", "RECIPIENT_EMAIL")

    missing = []

    if not smtp_host:
        missing.append("SMTP_HOST or SMTP_SERVER or EMAIL_HOST")

    if not smtp_port_raw:
        missing.append("SMTP_PORT or EMAIL_PORT")

    if not smtp_username:
        missing.append("SMTP_USERNAME or EMAIL_USERNAME or EMAIL_SENDER")

    if not smtp_password:
        missing.append("SMTP_PASSWORD or EMAIL_PASSWORD or EMAIL_APP_PASSWORD")

    if not email_from:
        missing.append("EMAIL_FROM or EMAIL_SENDER")

    if not email_to:
        missing.append("EMAIL_TO or EMAIL_RECIPIENT or RECIPIENT_EMAIL")

    if missing:
        missing_text = "\n".join(f"- {item}" for item in missing)
        raise RuntimeError(
            "Missing email configuration. Add these to .env or your environment:\n"
            f"{missing_text}"
        )

    try:
        smtp_port = int(str(smtp_port_raw))
    except ValueError as exc:
        raise RuntimeError(f"SMTP port must be a number. Got: {smtp_port_raw}") from exc

    return {
        "smtp_host": str(smtp_host),
        "smtp_port": smtp_port,
        "smtp_username": str(smtp_username),
        "smtp_password": str(smtp_password),
        "email_from": str(email_from),
        "email_to": str(email_to),
    }


def send_email(subject: str, body: str) -> None:
    """Send the weekly Application Tracker email."""
    config = get_email_config()

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = str(config["email_from"])
    message["To"] = str(config["email_to"])
    message.set_content(body)

    with smtplib.SMTP(str(config["smtp_host"]), int(config["smtp_port"])) as server:
        server.starttls()
        server.login(str(config["smtp_username"]), str(config["smtp_password"]))
        server.send_message(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or send the weekly CareerSignal Application Tracker email."
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--preview",
        action="store_true",
        help="Print the generated weekly tracker email without sending it.",
    )
    mode.add_argument(
        "--send",
        action="store_true",
        help="Send the weekly tracker email.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    applications = fetch_applications()
    body = build_weekly_tracker_email_body(applications)

    if args.send:
        send_email(SUBJECT, body)
        print("Weekly Application Tracker email sent.")
        return

    print("Preview mode. No email was sent.")
    print()
    print(f"Subject: {SUBJECT}")
    print()
    print(body)


if __name__ == "__main__":
    main()