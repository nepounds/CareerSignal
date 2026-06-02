"""
Manual status-update script for the CareerSignal Application Tracker.

Step 17D only updates an existing application status.
It does not build reports, weekly emails, Excel export changes, or Power BI changes.
"""

from __future__ import annotations

import argparse
import inspect
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from careersignal.application_tracker import (  # noqa: E402
    fetch_application_by_id,
    update_application_notes,
    update_application_response_dates,
    update_application_status,
    validate_application_status,
)


FIRST_RESPONSE_STATUSES = {
    "interview",
    "rejected",
    "accepted",
    "ghosted",
    "withdrawn",
    "closed",
}

FINAL_RESPONSE_STATUSES = {
    "rejected",
    "accepted",
    "ghosted",
    "withdrawn",
    "closed",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manually update the status of an existing job application."
    )

    parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="Application ID to update.",
    )

    parser.add_argument(
        "--status",
        required=True,
        help=(
            "New application status. Valid statuses: applied, interview, rejected, "
            "accepted, ghosted, withdrawn, closed."
        ),
    )

    parser.add_argument(
        "--notes",
        default=None,
        help="Optional notes to save with this application.",
    )

    parser.add_argument(
        "--date",
        default=None,
        help=(
            "Optional response date in YYYY-MM-DD format. "
            "For interview, this updates interview_date. "
            "For rejected, accepted, ghosted, withdrawn, or closed, this updates final_response_date. "
            "For first-response statuses, it may also update first_response_date if supported by the module."
        ),
    )

    return parser.parse_args()


def call_response_date_update(application_id: int, status: str, response_date: str) -> None:
    """
    Call update_application_response_dates using only keyword arguments supported
    by the current reusable module.

    This keeps Step 17D from rewriting src/careersignal/application_tracker.py.
    """

    signature = inspect.signature(update_application_response_dates)
    supported_parameters = set(signature.parameters)

    kwargs: dict[str, object] = {}

    if "application_id" in supported_parameters:
        kwargs["application_id"] = application_id
    else:
        # Fallback for a positional-only style signature.
        kwargs = {}

    if status in FIRST_RESPONSE_STATUSES and "first_response_date" in supported_parameters:
        kwargs["first_response_date"] = response_date

    if status == "interview" and "interview_date" in supported_parameters:
        kwargs["interview_date"] = response_date

    if status in FINAL_RESPONSE_STATUSES and "final_response_date" in supported_parameters:
        kwargs["final_response_date"] = response_date

    if kwargs:
        update_application_response_dates(**kwargs)
        return

    # If the function does not support the expected keyword names, skip date automation.
    print(
        "Date argument was provided, but update_application_response_dates(...) "
        "does not appear to support the expected date keyword arguments. "
        "Status was still updated."
    )


def main() -> None:
    args = parse_args()

    new_status = args.status.strip().lower()
    validate_application_status(new_status)

    existing_application = fetch_application_by_id(args.id)

    if existing_application is None:
        raise SystemExit(f"No application found with application_id {args.id}.")

    old_status = existing_application.get("status", "")

    update_application_status(args.id, new_status)

    if args.notes:
        update_application_notes(args.id, args.notes)

    if args.date:
        call_response_date_update(args.id, new_status, args.date)

    updated_application = fetch_application_by_id(args.id)

    if updated_application is None:
        raise SystemExit(
            "Status update may have failed. Could not reload the application after update."
        )

    print()
    print("Application status updated")
    print("--------------------------")
    print(f"application_id: {updated_application.get('application_id')}")
    print(f"company_name:   {updated_application.get('company_name')}")
    print(f"job_title:      {updated_application.get('job_title')}")
    print(f"old_status:     {old_status}")
    print(f"new_status:     {updated_application.get('status')}")

    if args.notes:
        print(f"notes:          {updated_application.get('notes')}")

    if args.date:
        print(f"date argument:  {args.date}")


if __name__ == "__main__":
    main()