"""Reusable database logic for the CareerSignal application tracker."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from careersignal.application_tracker_db import DATABASE_PATH


APPLICATION_TRACKER_TABLE = "applications"

VALID_APPLICATION_STATUSES = {
    "applied",
    "interview",
    "rejected",
    "accepted",
    "ghosted",
    "withdrawn",
    "closed",
}


def get_current_timestamp() -> str:
    """Return the current timestamp in ISO format for application records."""
    return datetime.now().isoformat(timespec="seconds")


def validate_application_status(status: str) -> None:
    """Validate an application status before writing to the database."""
    if status not in VALID_APPLICATION_STATUSES:
        valid_statuses = ", ".join(sorted(VALID_APPLICATION_STATUSES))
        raise ValueError(
            f"Invalid application status: {status}. "
            f"Valid statuses are: {valid_statuses}"
        )


def add_application(
    date_applied: str,
    company_name: str,
    job_title: str,
    job_url: str | None = None,
    source: str | None = None,
    status: str = "applied",
    first_response_date: str | None = None,
    interview_date: str | None = None,
    final_response_date: str | None = None,
    notes: str | None = None,
    db_path: Path = DATABASE_PATH,
) -> int:
    """Add a new application record and return its application_id."""
    validate_application_status(status)

    timestamp = get_current_timestamp()

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO {APPLICATION_TRACKER_TABLE} (
                date_applied,
                company_name,
                job_title,
                job_url,
                source,
                status,
                first_response_date,
                interview_date,
                final_response_date,
                notes,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date_applied,
                company_name,
                job_title,
                job_url,
                source,
                status,
                first_response_date,
                interview_date,
                final_response_date,
                notes,
                timestamp,
                timestamp,
            ),
        )
        connection.commit()

        return int(cursor.lastrowid)


def update_application_status(
    application_id: int,
    status: str,
    db_path: Path = DATABASE_PATH,
) -> None:
    """Update the status for an existing application record."""
    validate_application_status(status)

    timestamp = get_current_timestamp()

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            UPDATE {APPLICATION_TRACKER_TABLE}
            SET status = ?,
                updated_at = ?
            WHERE application_id = ?
            """,
            (status, timestamp, application_id),
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise ValueError(f"No application found with application_id: {application_id}")


def update_application_notes(
    application_id: int,
    notes: str | None,
    db_path: Path = DATABASE_PATH,
) -> None:
    """Update notes for an existing application record."""
    timestamp = get_current_timestamp()

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            UPDATE {APPLICATION_TRACKER_TABLE}
            SET notes = ?,
                updated_at = ?
            WHERE application_id = ?
            """,
            (notes, timestamp, application_id),
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise ValueError(f"No application found with application_id: {application_id}")


def update_application_response_dates(
    application_id: int,
    first_response_date: str | None = None,
    interview_date: str | None = None,
    final_response_date: str | None = None,
    db_path: Path = DATABASE_PATH,
) -> None:
    """Update response-related dates for an existing application record."""
    timestamp = get_current_timestamp()

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            UPDATE {APPLICATION_TRACKER_TABLE}
            SET first_response_date = ?,
                interview_date = ?,
                final_response_date = ?,
                updated_at = ?
            WHERE application_id = ?
            """,
            (
                first_response_date,
                interview_date,
                final_response_date,
                timestamp,
                application_id,
            ),
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise ValueError(f"No application found with application_id: {application_id}")


def fetch_application_by_id(
    application_id: int,
    db_path: Path = DATABASE_PATH,
) -> dict[str, Any] | None:
    """Fetch one application record by application_id."""
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(
            f"""
            SELECT
                application_id,
                date_applied,
                company_name,
                job_title,
                job_url,
                source,
                status,
                first_response_date,
                interview_date,
                final_response_date,
                notes,
                created_at,
                updated_at
            FROM {APPLICATION_TRACKER_TABLE}
            WHERE application_id = ?
            """,
            (application_id,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    return dict(row)


def fetch_applications(
    status: str | None = None,
    company_name: str | None = None,
    db_path: Path = DATABASE_PATH,
) -> list[dict[str, Any]]:
    """Fetch application records, optionally filtered by status and company."""
    if status is not None:
        validate_application_status(status)

    query = f"""
        SELECT
            application_id,
            date_applied,
            company_name,
            job_title,
            job_url,
            source,
            status,
            first_response_date,
            interview_date,
            final_response_date,
            notes,
            created_at,
            updated_at
        FROM {APPLICATION_TRACKER_TABLE}
    """

    filters: list[str] = []
    parameters: list[Any] = []

    if status is not None:
        filters.append("status = ?")
        parameters.append(status)

    if company_name is not None:
        filters.append("company_name = ?")
        parameters.append(company_name)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY date_applied DESC, application_id DESC"

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        rows = cursor.fetchall()

    return [dict(row) for row in rows]