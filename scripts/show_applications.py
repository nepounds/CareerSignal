import sqlite3


def main() -> None:
    conn = sqlite3.connect("data/careersignal.db")

    rows = conn.execute("""
        SELECT
            application_id,
            date_applied,
            company_name,
            job_title,
            status,
            source,
            notes
        FROM applications
        ORDER BY application_id;
    """).fetchall()

    if not rows:
        print("No applications found.")
        return

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()