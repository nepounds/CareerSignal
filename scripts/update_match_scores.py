import sqlite3
from pathlib import Path

from careersignal.match_scoring import score_job


DATABASE_PATH = Path("data/careersignal.db")


def get_all_jobs(cursor):
    cursor.execute(
        """
        SELECT
            id,
            company_name,
            source_ats,
            external_job_id,
            title,
            location,
            department,
            job_url,
            posted_date,
            date_collected
        FROM jobs
        """
    )

    rows = cursor.fetchall()

    jobs = []

    for row in rows:
        jobs.append(
            {
                "id": row[0],
                "company_name": row[1],
                "source_ats": row[2],
                "external_job_id": row[3],
                "title": row[4],
                "location": row[5],
                "department": row[6],
                "job_url": row[7],
                "posted_date": row[8],
                "date_collected": row[9],
            }
        )

    return jobs


def update_job_score(cursor, job_id, match_score, match_notes):
    cursor.execute(
        """
        UPDATE jobs
        SET
            match_score = ?,
            match_notes = ?
        WHERE id = ?
        """,
        (match_score, match_notes, job_id),
    )


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DATABASE_PATH}")

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    jobs = get_all_jobs(cursor)

    print(f"Found {len(jobs)} jobs to score.")

    for job in jobs:
        result = score_job(job)

        update_job_score(
            cursor=cursor,
            job_id=job["id"],
            match_score=result["match_score"],
            match_notes=result["match_notes"],
        )

        print(
            f"{result['match_score']:>3} | "
            f"{job.get('company_name')} | "
            f"{job.get('title')} | "
            f"{job.get('location')}"
        )

    connection.commit()
    connection.close()

    print("Match scores updated.")


if __name__ == "__main__":
    main()