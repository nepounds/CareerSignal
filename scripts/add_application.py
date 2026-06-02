"""
Manual application entry script for CareerSignal.

Step 17C goal:
- Add one application record from the command line.
- Use reusable logic from src/careersignal/application_tracker.py.
- Do not build summaries, reports, status updates, email changes, Excel export changes, or Power BI changes.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


# Allow this script to run from PowerShell without requiring the user
# to manually set PYTHONPATH every single time.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


try:
    from careersignal.application_tracker import add_application
except ImportError as exc:
    raise SystemExit(
        "Could not import add_application from careersignal.application_tracker.\n"
        "Run this command to inspect available function names:\n\n"
        "python -c \"import inspect; import careersignal.application_tracker as app; "
        "print([name for name, obj in inspect.getmembers(app, inspect.isfunction) "
        "if not name.startswith('_')])\"\n\n"
        f"Original import error: {exc}"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manually add a job application to the CareerSignal application tracker."
    )

    parser.add_argument(
        "--company",
        required=True,
        help='Company name, such as "RSM".',
    )

    parser.add_argument(
        "--title",
        required=True,
        help='Job title, such as "Audit Associate".',
    )

    parser.add_argument(
        "--date-applied",
        required=True,
        help='Date applied in YYYY-MM-DD format, such as "2026-06-01".',
    )

    parser.add_argument(
        "--url",
        default="",
        help="Optional job posting URL.",
    )

    parser.add_argument(
        "--source",
        default="",
        help='Optional source, such as "company website", "LinkedIn", or "Handshake".',
    )

    parser.add_argument(
        "--notes",
        default="",
        help="Optional notes about the application.",
    )

    return parser.parse_args()


def validate_required_text(value: str, field_name: str) -> str:
    cleaned_value = value.strip()

    if not cleaned_value:
        raise ValueError(f"{field_name} cannot be blank.")

    return cleaned_value


def validate_date_applied(value: str) -> str:
    cleaned_value = value.strip()

    try:
        datetime.strptime(cleaned_value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(
            "--date-applied must use YYYY-MM-DD format, like 2026-06-01."
        ) from exc

    return cleaned_value


def main() -> None:
    args = parse_args()

    try:
        company_name = validate_required_text(args.company, "--company")
        job_title = validate_required_text(args.title, "--title")
        date_applied = validate_date_applied(args.date_applied)

        job_url = args.url.strip()
        source = args.source.strip()
        notes = args.notes.strip()

        inserted_application = add_application(
            company_name=company_name,
            job_title=job_title,
            date_applied=date_applied,
            job_url=job_url,
            source=source,
            notes=notes,
        )

    except TypeError as exc:
        raise SystemExit(
            "add_application was found, but the argument names may not match this script.\n"
            "Inspect the function signature with:\n\n"
            "python -c \"import inspect; from careersignal.application_tracker import add_application; "
            "print(inspect.signature(add_application))\"\n\n"
            f"Original error: {exc}"
        ) from exc

    except ValueError as exc:
        raise SystemExit(f"Input error: {exc}") from exc

    print()
    print("Application added successfully.")
    print("-------------------------------")
    print(f"Company:      {company_name}")
    print(f"Job title:    {job_title}")
    print(f"Date applied: {date_applied}")
    print(f"Job URL:      {job_url or '(blank)'}")
    print(f"Source:       {source or '(blank)'}")
    print(f"Notes:        {notes or '(blank)'}")

    if inserted_application is not None:
        print(f"Application ID: {inserted_application}")


if __name__ == "__main__":
    main()