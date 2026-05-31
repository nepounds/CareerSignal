"""
Database setup for the CareerSignal manual application tracker.

Step 17A only creates the application tracker database foundation.
It does not build reporting, email integration, Excel export, or Power BI visuals.
"""

from pathlib import Path
import sqlite3


DATABASE_PATH = Path("data/careersignal.db")


APPLICATIONS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,

    date_applied TEXT NOT NULL,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    job_url TEXT,
    source TEXT,

    status TEXT NOT NULL DEFAULT 'applied'
        CHECK (
            status IN (
                'applied',
                'interview',
                'rejected',
                'accepted',
                'ghosted',
                'withdrawn',
                'closed'
            )
        ),

    first_response_date TEXT,
    interview_date TEXT,
    final_response_date TEXT,

    notes TEXT,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


APPLICATIONS_UPDATED_AT_TRIGGER_SQL = """
CREATE TRIGGER IF NOT EXISTS update_applications_updated_at
AFTER UPDATE ON applications
FOR EACH ROW
BEGIN
    UPDATE applications
    SET updated_at = CURRENT_TIMESTAMP
    WHERE application_id = OLD.application_id;
END;
"""


def initialize_application_tracker(db_path: Path = DATABASE_PATH) -> None:
    """
    Create the manual application tracker table if it does not already exist.

    Args:
        db_path: Path to the CareerSignal SQLite database.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute(APPLICATIONS_TABLE_SQL)
        conn.execute(APPLICATIONS_UPDATED_AT_TRIGGER_SQL)
        conn.commit()