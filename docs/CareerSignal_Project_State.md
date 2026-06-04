# CareerSignal Project State

## Current Project Status

CareerSignal currently has a working end-to-end job alert pipeline and a manual Application Tracker layer.

Completed steps:

1. Project setup and GitHub structure
2. Company config file
3. First ATS collector
4. Standard normalized job format
5. SQLite database
6. New job detection
7. Daily email report
8. Initial match scoring
9. Error handling and logging
10. Excel export
11. Power BI dashboard
12. Workday support
   - 12A. Workday proof of concept
   - 12B. Workday normalization
   - 12C. Workday integration into the main pipeline
13. ATS Coverage Audit started, with unresolved follow-up items
14. Filtering Strategy completed
15. Match Scoring Refinement completed
16. Daily Automation runner added for Windows Task Scheduler
17. Application Tracker started
   - 17A. Application Tracker database foundation completed
   - 17B. Application Tracker reusable module completed
   - 17C. Manual add-application script completed
   - 17D. Manual status-update script completed
   - 17E. Application Tracker summary reporting completed
   - 17F. Application Tracker Excel export integration completed
   - 17G. Weekly Application Tracker email completed

Current next step:

- 17H: Optional Power BI Application Tracker visuals

The main product loop exists:

    company_config.csv
    → supported ATS collector
    → normalized job dictionaries
    → SQLite database
    → new job detection
    → match scoring
    → daily email report
    → Excel export
    → Power BI dashboard
    → Windows Task Scheduler automation

Application Tracker is a manual tracking layer that sits beside the automated job collection pipeline.

Application Tracker loop:

    manual application entry
    → applications table in data/careersignal.db
    → reusable application_tracker.py module
    → manual add/update scripts
    → summary reporting
    → Excel export sheets
    → separate weekly Application Tracker email
    → future Power BI visuals

---

## Existing Project Structure

Preserve this structure.

    CareerSignal/
    ├── config/
    │   ├── company_config.csv
    │   ├── company_ats_audit.csv
    │   └── match_rules.json or match_rules.csv if created
    ├── data/
    │   └── careersignal.db
    ├── docs/
    │   ├── CareerSignal_Project_State.md
    │   ├── filtering_strategy.md
    │   ├── ATS_Coverage_Audit.md or related Step 13 notes if created
    │   └── screenshots/
    │       └── powerbi_overview_dashboard.png
    ├── exports/
    │   └── careersignal_export.xlsx
    ├── logs/
    │   ├── careersignal.log
    │   └── scheduled_task.log
    ├── reports/
    │   └── careersignal_dashboard.pbix
    ├── scripts/
    │   ├── add_application.py
    │   ├── update_application_status.py
    │   ├── report_applications.py
    │   ├── send_weekly_application_tracker_email.py
    │   ├── collect_greenhouse_jobs.py
    │   ├── export_to_excel.py
    │   ├── init_application_tracker.py
    │   ├── preview_workday_jobs.py
    │   ├── test_config_loader.py
    │   ├── test_database.py
    │   ├── test_email_report.py
    │   ├── test_match_scoring.py
    │   └── other preview/test scripts created during Workday, scoring, or tracker steps
    ├── src/
    │   └── careersignal/
    │       ├── __init__.py
    │       ├── application_tracker.py
    │       ├── application_tracker_db.py
    │       ├── config_loader.py
    │       ├── database.py
    │       ├── email_report.py
    │       ├── logging_config.py
    │       ├── match_scoring.py
    │       └── collectors/
    │           ├── __init__.py
    │           ├── greenhouse.py
    │           └── workday.py
    ├── tests/
    ├── run_careersignal_daily.bat
    ├── .env.example
    ├── .gitignore
    ├── README.md
    └── requirements.txt

Some generated files may be ignored by Git, including:

- .env
- logs/
- generated database files
- generated exports
- local Power BI cache files

---

## Important Project Rules

For CareerSignal coding help, always treat this file as the source of truth before suggesting code changes.

Do not invent new function names if an official name already exists.

Before rewriting a core file, explain which other files depend on it.

Keep naming consistent with the official function names in this project state file.

Do not add compatibility wrappers or aliases unless explicitly approved.

Prefer updating dependent scripts to use the current official function names.

Preserve the existing project structure:

- scripts/ contains runnable scripts
- src/careersignal/ contains reusable modules
- data/careersignal.db is the SQLite database
- config/company_config.csv is the company config

Do not use:

- data/jobs.db

Do not rename:

- scripts/collect_greenhouse_jobs.py

Even though the script name says Greenhouse, after Workday integration it functions as the main collector runner.

Do not rename this script unless intentionally doing a cleanup/refactor step.

Do not modify the daily job alert email during Application Tracker steps unless explicitly approved.

Do not modify Power BI during Application Tracker steps unless explicitly working on the Power BI integration step.

Do not modify Excel export during weekly email work unless explicitly approved.

Do not schedule the weekly Application Tracker email unless explicitly approved.

Keep Application Tracker steps small and separate.

---

## Existing Files That Should Not Be Recreated Blindly

These files already exist or have already been worked on.

Do not recreate them from scratch unless they are missing.

    README.md
    requirements.txt
    .env.example
    .gitignore
    run_careersignal_daily.bat
    config/company_config.csv
    config/company_ats_audit.csv
    config/match_rules.json or config/match_rules.csv if created
    data/careersignal.db
    docs/CareerSignal_Project_State.md
    docs/filtering_strategy.md
    exports/careersignal_export.xlsx
    logs/careersignal.log
    logs/scheduled_task.log
    reports/careersignal_dashboard.pbix
    scripts/add_application.py
    scripts/update_application_status.py
    scripts/report_applications.py
    scripts/send_weekly_application_tracker_email.py
    scripts/collect_greenhouse_jobs.py
    scripts/export_to_excel.py
    scripts/init_application_tracker.py
    scripts/preview_workday_jobs.py
    scripts/test_config_loader.py
    scripts/test_database.py
    scripts/test_email_report.py
    scripts/test_match_scoring.py
    src/careersignal/config_loader.py
    src/careersignal/database.py
    src/careersignal/email_report.py
    src/careersignal/logging_config.py
    src/careersignal/match_scoring.py
    src/careersignal/collectors/greenhouse.py
    src/careersignal/collectors/workday.py
    src/careersignal/application_tracker.py
    src/careersignal/application_tracker_db.py

If a future step needs to modify one of these files, explain:

1. Why the file needs to change
2. What depends on it
3. How the change preserves existing behavior

---

## Core Pipeline Status

### SQLite Database

Official database path:

- data/careersignal.db

Do not use:

- data/jobs.db

The main database already supports job storage, new job detection, and pipeline reporting.

Application Tracker also uses:

- data/careersignal.db

Application Tracker table:

- applications

Application Tracker primary key:

- application_id

---

### Greenhouse Collector

Likely file:

- src/careersignal/collectors/greenhouse.py

Existing runner command:

    python scripts/collect_greenhouse_jobs.py --preview

Send real email:

    python scripts/collect_greenhouse_jobs.py --send

Important:

The script name still says collect_greenhouse_jobs.py, but after Workday integration it functions as the main collector runner.

Do not rename this script unless intentionally doing a cleanup/refactor step.

---

### Workday Collector

Likely file:

- src/careersignal/collectors/workday.py

Workday was split into three parts:

- 12A: Workday Proof of Concept
- 12B: Workday Normalization
- 12C: Integrate Workday Connector

All three are considered complete if the current branch has Workday jobs flowing through the same pipeline as Greenhouse.

Workday jobs should use:

    "source_ats": "workday"

Workday jobs must use the official normalized job shape.

---

### Match Scoring

Step 15 is complete and used the Step 14 filtering strategy.

Important distinction:

- Step 14 = decide what CareerSignal should care about
- Step 15 = assign scoring weights and implement/refine scoring logic

Match scoring should preserve:

- score_job(job)

Scores should remain from 0 to 100.

Suggested score bands:

- 80-100: Strong match
- 60-79: Possible match
- 40-59: Weak/stretch match
- 0-39: Low match or likely skip

CareerSignal is not accounting-only.

The filtering and scoring strategy supports multiple job-search lanes:

- Accounting roles
- Finance roles
- General analyst roles
- Business analyst roles
- Operations analyst roles
- Compliance analyst roles
- Data/reporting analyst roles
- Plant supervisor jobs
- Operations supervisor jobs
- Water/wastewater or public utility-adjacent jobs
- Other realistic roles that fit the user's background

---

### Email Reporting

Daily email reporting should continue to support preview/test mode and send mode.

Daily job alert email is separate from the weekly Application Tracker email.

Daily job alert email should not be modified during Application Tracker steps unless explicitly approved.

Weekly Application Tracker email was added in Step 17G as a separate script:

- scripts/send_weekly_application_tracker_email.py

The weekly Application Tracker email uses:

- preview mode
- send mode
- the applications table
- data/careersignal.db
- the existing .env/email credential pattern where possible

The weekly email does not modify:

- daily job alert behavior
- Excel export
- Power BI
- database schema
- Windows Task Scheduler configuration

---

### Logging

Likely file:

- src/careersignal/logging_config.py

Logs should go to:

- logs/careersignal.log

Scheduled task logs should go to:

- logs/scheduled_task.log

A failed company source should not crash the whole run.

Failed sources should be tracked and included in the daily email report where possible.

---

### Excel Export

File:

- scripts/export_to_excel.py

Export output:

- exports/careersignal_export.xlsx

The Excel export feeds the Power BI dashboard.

Do not break this output path without updating the README and Power BI notes.

Step 17F added Application Tracker sheets to the existing workbook.

Existing job export sheets should remain intact.

Application Tracker export sheets now added:

- Applications
- Application Summary
- Company Application Summary
- Application Aging

The export should still run with:

    python scripts/export_to_excel.py

The export should still create or update:

- exports/careersignal_export.xlsx

The Power BI source path remains unchanged.

No separate tracker workbook should exist unless intentionally approved later.

Application Tracker export behavior:

- Applications sheet contains row-level records from the applications table.
- Application Summary sheet contains overall tracker totals.
- Company Application Summary sheet contains company-level tracker totals.
- Application Aging sheet contains waiting-period and ghosting-risk buckets.
- Aging logic reports risk only.
- Aging logic does not automatically change statuses in the database.

Aging rules:

- 0-14 days with no response = active / normal waiting period
- 15-30 days with no response = rejection danger zone
- 31-60 days with no response = ghosting danger zone
- 61+ days with no response = ghosted candidate / should be reviewed

Ghosted applications count as negative outcomes in summary reporting.

---

### Power BI

Power BI report:

- reports/careersignal_dashboard.pbix

Power BI data source:

- exports/careersignal_export.xlsx

After generating a fresh Excel export, refresh Power BI manually:

- Home > Refresh

Current dashboard exists and should not be treated as unstarted.

Application Tracker visuals should come later.

Step 17F did not modify Power BI visuals or the Power BI file.

Step 17G also did not modify Power BI visuals or the Power BI file.

---

### Daily Automation

Step 16 is complete if the project has:

- run_careersignal_daily.bat

and Windows Task Scheduler is configured to run it daily.

The daily automation should run:

    python scripts\collect_greenhouse_jobs.py --send
    python scripts\export_to_excel.py

The batch file should:

1. Change into the CareerSignal project folder
2. Activate the virtual environment if needed
3. Set PYTHONPATH=src
4. Run the collector in send mode
5. Run the Excel export
6. Write useful output to logs/scheduled_task.log

Recommended scheduled run time:

- 7:30 AM daily

Manual test command:

    .\run_careersignal_daily.bat

Useful verification commands:

    Get-Content .\logs\scheduled_task.log -Tail 100
    Get-Content .\logs\careersignal.log -Tail 100
    Get-Item .\data\careersignal.db
    Get-Item .\exports\careersignal_export.xlsx

Known scheduler troubleshooting notes:

- Do not close the .bat/cmd window when it appears during the scheduled run.
- Do not run Checkpoint VPN or NordVPN during the scheduled job if they block SMTP traffic.
- If email does not send, check whether VPN or network restrictions blocked smtp.gmail.com on port 587.

---

## Step 13 ATS Coverage Audit Status

Step 13 is started but not fully resolved.

Step 13 was an audit/planning step, not a clean coding step.

The purpose was to use the master list of target companies to identify:

1. Each company’s career URL
2. Which ATS or career platform each company uses
3. Whether CareerSignal already supports that ATS
4. Whether a new connector is needed
5. Connector priority
6. Notes or unresolved issues

Step 13 follow-up items:

1. Recheck companies with unclear or unreliable career URLs.
2. Confirm ATS type manually for companies marked unknown.
3. Identify which companies are truly Workday or Greenhouse and can be added now.
4. Identify which unsupported ATSs appear often enough to justify new connectors.
5. Do not build connectors for one-off systems unless they are high-value companies.
6. Review companies where search/Gemini produced bad or incorrect career pages.
7. Review companies with redirects, proprietary systems, or confusing career portals.
8. Add the rest of the confirmed Greenhouse companies.
9. Circle back to Workday URL issues.

---

## Step 17 Application Tracker Status

Step 17 is active, with 17A through 17G complete.

Goal:

Add a manual application tracking system to CareerSignal that records applications submitted by the user, tracks response outcomes, calculates ghosting/rejection danger zones, summarizes application performance overall and by company, exports Application Tracker sheets to Excel, and sends a separate weekly Application Tracker email.

Application Tracker remains separate from the automated job collector.

Do not modify the daily job alert email unless explicitly approved.

Do not modify Power BI unless explicitly working on Application Tracker visuals.

---

### Application Tracker Database Naming

Official database:

- data/careersignal.db

Official Application Tracker table:

- applications

Official Application Tracker primary key:

- application_id

Important:

Earlier planning notes may have referred to the table as application_tracker, but the actual implemented table name is applications.

Use applications going forward unless a future intentional migration renames it.

---

### Step 17A: Application Tracker Database Foundation

Status:

- Complete

Purpose:

Create the database foundation for manually tracking job applications.

Expected database:

- data/careersignal.db

Implemented table:

- applications

Implemented primary key:

- application_id

Core fields support:

- application_id
- date_applied
- company_name
- job_title
- job_url
- source
- status
- first_response_date
- interview_date
- final_response_date
- notes
- created_at
- updated_at

Valid statuses:

- applied
- interview
- rejected
- accepted
- ghosted
- withdrawn
- closed

Aging rules:

- 0-14 days with no response = active / normal waiting period
- 15-30 days with no response = rejection danger zone
- 31-60 days with no response = ghosting danger zone
- 61+ days with no response = ghosted candidate / should be reviewed

Reporting rule:

- Ghosted applications should count as negative outcomes/rejections in total outcome reporting.

Initializer script:

- scripts/init_application_tracker.py

Reusable database setup file:

- src/careersignal/application_tracker_db.py

17A does not include:

- manual command-line scripts
- summary reporting
- weekly email
- Excel export
- Power BI visuals
- daily email changes

---

### Step 17B: Application Tracker Reusable Module

Status:

- Complete

Purpose:

Add reusable Python logic for interacting with the Application Tracker table.

Implemented file:

- src/careersignal/application_tracker.py

Official table constant:

    APPLICATION_TRACKER_TABLE = "applications"

Official reusable functions:

- get_current_timestamp
- validate_application_status
- add_application
- update_application_status
- update_application_notes
- update_application_response_dates
- fetch_application_by_id
- fetch_applications

Important function behavior:

- add_application(...) returns the inserted application_id as an int.
- fetch_application_by_id(...) returns one application record as a dict or None.
- fetch_applications(...) returns a list of application record dicts.

17B does not include:

- manual command-line scripts
- summary reporting
- weekly email
- Excel export
- Power BI visuals
- daily email changes

---

### Step 17C: Manual Add-Application Script

Status:

- Complete

Goal:

Create a runnable script for manually adding application records from PowerShell.

Implemented file:

- scripts/add_application.py

Expected behavior:

- User runs a command with company, title, date applied, URL/source/notes if available.
- Script validates required input.
- Script calls add_application(...) from src/careersignal/application_tracker.py.
- Script inserts the application into the applications table.
- Script prints a clean confirmation, including the returned application_id.

Example command:

    python scripts/add_application.py --company "RSM" --title "Audit Associate" --date-applied "2026-06-01" --url "https://example.com/job" --source "company website" --notes "Applied through company portal"

Minimal command:

    python scripts/add_application.py --company "RSM" --title "Audit Associate" --date-applied "2026-06-01"

Test insert command:

    python scripts/add_application.py --company "TEST COMPANY DELETE ME" --title "Fake Test Application" --date-applied "2026-06-01" --url "https://example.com/test-job" --source "manual test" --notes "Delete this after test"

PowerShell-safe confirmation query:

    @'
    import sqlite3

    conn = sqlite3.connect("data/careersignal.db")
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT * FROM applications WHERE company_name = ? ORDER BY application_id DESC",
        ("TEST COMPANY DELETE ME",)
    ).fetchall()

    for row in rows:
        print(dict(row))

    conn.close()
    '@ | python -

PowerShell-safe cleanup query:

    @'
    import sqlite3

    conn = sqlite3.connect("data/careersignal.db")

    conn.execute(
        "DELETE FROM applications WHERE company_name = ?",
        ("TEST COMPANY DELETE ME",)
    )

    conn.commit()
    conn.close()

    print("Deleted fake test application")
    '@ | python -

17C does not include:

- summary reporting
- status updates
- weekly email
- Excel export changes
- Power BI changes
- daily email changes

---

### Step 17D: Manual Status-Update Script

Status:

- Complete

Goal:

Create a runnable script for manually updating an application’s status.

Implemented file:

- scripts/update_application_status.py

Expected behavior:

- User provides application_id and new status.
- Script validates status using validate_application_status(...).
- Script calls update_application_status(...) from src/careersignal/application_tracker.py.
- Script updates the matching row in the applications table.
- Script prints a clean confirmation showing application_id, company_name, job_title, old status, and new status.

Supported command:

    python scripts/update_application_status.py --id 4 --status interview

Optional notes command:

    python scripts/update_application_status.py --id 4 --status rejected --notes "Rejected by email"

Optional date command:

    python scripts/update_application_status.py --id 4 --status interview --date "2026-06-10"

Important implementation notes:

- The script uses existing reusable functions from src/careersignal/application_tracker.py.
- The script does not rewrite the reusable module.
- The script does not modify the daily job alert email.
- The script does not modify Excel export.
- The script does not modify Power BI.
- The script does not build summary reporting.

17D does not include:

- summary reporting
- weekly email
- Excel export changes
- Power BI changes
- daily email changes

---

### Step 17E: Application Tracker Summary Reporting

Status:

- Complete

Goal:

Add summary reporting for Application Tracker.

Implemented file:

- scripts/report_applications.py

Expected reporting:

- total applications
- active applications
- interviews
- acceptances
- formal rejections
- ghostings
- negative outcomes
- totals by company
- interviews by company
- rejections by company
- ghostings by company
- acceptances by company
- application aging buckets

Ghostings count as negative outcomes.

Reporting logic should use:

- applications table
- application_id primary key
- data/careersignal.db database
- official functions from src/careersignal/application_tracker.py where practical

17E does not include:

- weekly email
- Excel export changes
- Power BI changes
- daily job alert email changes

17E is complete because the Application Tracker summary reporting script exists and reporting logic is now available for command-line review.

Run command:

    python scripts/report_applications.py

---

### Step 17F: Excel Export Integration

Status:

- Complete

Goal:

Add Application Tracker sheets to the existing Excel export.

Updated file:

- scripts/export_to_excel.py

Existing export output preserved:

- exports/careersignal_export.xlsx

Required sheets added:

- Applications
- Application Summary
- Company Application Summary
- Application Aging

Expected behavior:

- Running python scripts/export_to_excel.py still works.
- Existing job export sheets remain intact.
- Application Tracker sheets are added to the same workbook.
- Power BI source path remains unchanged.
- No separate tracker workbook is created.
- No database schema change is made.
- No statuses are automatically changed.
- No daily email behavior is changed.
- No Power BI visuals are changed.

Application Tracker sheet behavior:

Applications sheet:

- Full row-level application tracker data from the applications table.
- Expected fields include:
  - application_id
  - date_applied
  - company_name
  - job_title
  - job_url
  - source
  - status
  - first_response_date
  - interview_date
  - final_response_date
  - notes
  - created_at
  - updated_at

Application Summary sheet:

- total applications
- active applications
- interviews
- acceptances
- formal rejections
- ghostings
- negative outcomes

Company Application Summary sheet:

- company_name
- total applications
- active applications
- interviews
- acceptances
- formal rejections
- ghostings
- negative outcomes

Application Aging sheet:

- application_id
- company_name
- job_title
- date_applied
- status
- days_since_applied
- aging_bucket

Aging rules:

- 0-14 days with no response = active / normal waiting period
- 15-30 days with no response = rejection danger zone
- 31-60 days with no response = ghosting danger zone
- 61+ days with no response = ghosted candidate / should be reviewed

Important:

- Application Aging reports aging only.
- It does not mutate the database.
- It does not automatically change statuses to ghosted.
- Ghosted applications count as negative outcomes.

Step 17F preserved:

- data/careersignal.db
- applications table
- application_id primary key
- Greenhouse support
- Workday support
- database behavior
- email behavior
- logging behavior
- match scoring behavior
- Power BI source path
- Windows Task Scheduler behavior

Run command:

    python scripts/export_to_excel.py

PowerShell-safe sheet confirmation command:

    @'
    from openpyxl import load_workbook

    workbook = load_workbook("exports/careersignal_export.xlsx", read_only=True)

    for sheet_name in workbook.sheetnames:
        print(sheet_name)

    required = {
        "Applications",
        "Application Summary",
        "Company Application Summary",
        "Application Aging",
    }

    missing = required - set(workbook.sheetnames)

    if missing:
        print("Missing:", missing)
        raise SystemExit(1)

    print("All Step 17F sheets exist.")
    '@ | python -

---

### Step 17G: Weekly Application Tracker Email

Status:

- Complete

Goal:

Add a separate weekly Application Tracker email after reporting and Excel export work.

Implemented file:

- scripts/send_weekly_application_tracker_email.py

Preferred future schedule:

- Friday at 4 PM

Important:

The weekly Application Tracker email remains separate from the daily job alert email.

Application Tracker stats were not added to the daily job alert email.

The existing daily email module was not modified during Step 17G.

The existing daily collector script was not modified during Step 17G.

The Excel export was not modified during Step 17G.

Power BI was not modified during Step 17G.

Windows Task Scheduler was not modified during Step 17G.

Expected weekly tracker email content:

- applications submitted this week
- interviews received this week
- rejections received this week
- ghostings identified this week
- total applications
- total active applications
- interviews
- acceptances
- formal rejections
- ghostings
- negative outcomes
- rejection danger zone watchlist
- ghosting danger zone watchlist
- 61+ day ghosting candidates
- company response summary

Weekly email subject line:

    CareerSignal Weekly Application Tracker Summary

Preview command:

    python scripts/send_weekly_application_tracker_email.py --preview

Send command:

    python scripts/send_weekly_application_tracker_email.py --send

Safety behavior:

- Script previews by default if no send flag is provided.
- Script does not send unless --send is explicitly provided.
- Script prints generated email content in preview mode.
- Script uses the existing Application Tracker table: applications.
- Script uses the existing Application Tracker primary key: application_id.
- Script uses the existing database path through the reusable Application Tracker module.
- Script does not change any database schema.
- Script does not mutate application statuses.
- Script does not schedule itself yet.

Email configuration behavior:

- The script uses environment variables and .env values.
- It supports common email config variable names so the existing email credential pattern can be reused without editing the daily email module.

Supported email config variable names include:

- SMTP_HOST or SMTP_SERVER or EMAIL_HOST
- SMTP_PORT or EMAIL_PORT
- SMTP_USERNAME or EMAIL_USERNAME or EMAIL_SENDER or EMAIL_FROM
- SMTP_PASSWORD or EMAIL_PASSWORD or EMAIL_APP_PASSWORD
- EMAIL_FROM or EMAIL_SENDER
- EMAIL_TO or EMAIL_RECIPIENT or RECIPIENT_EMAIL

Step 17G preserved:

- data/careersignal.db
- applications table
- application_id primary key
- Greenhouse support
- Workday support
- database behavior
- daily email behavior
- logging behavior
- Excel export behavior
- Power BI source path
- match scoring behavior
- Windows Task Scheduler behavior

Step 17G did not include:

- Power BI Application Tracker visuals
- Windows Task Scheduler setup for the weekly email
- changes to daily job alert email
- changes to Excel export
- database schema changes
- automatic ghosting status updates

Test insert command for fake Step 17G rows:

    @'
    import sqlite3
    from datetime import date, timedelta

    today = date.today()

    fake_rows = [
        {
            "date_applied": today.isoformat(),
            "company_name": "TEST COMPANY DELETE ME",
            "job_title": "Fake Weekly Application",
            "job_url": "https://example.com/weekly",
            "source": "manual test",
            "status": "applied",
            "notes": "Step 17G test row - submitted this week",
        },
        {
            "date_applied": (today - timedelta(days=18)).isoformat(),
            "company_name": "TEST COMPANY DELETE ME",
            "job_title": "Fake Rejection Danger Zone Application",
            "job_url": "https://example.com/rejection-zone",
            "source": "manual test",
            "status": "applied",
            "notes": "Step 17G test row - rejection danger zone",
        },
        {
            "date_applied": (today - timedelta(days=40)).isoformat(),
            "company_name": "TEST COMPANY DELETE ME",
            "job_title": "Fake Ghosting Danger Zone Application",
            "job_url": "https://example.com/ghosting-zone",
            "source": "manual test",
            "status": "applied",
            "notes": "Step 17G test row - ghosting danger zone",
        },
        {
            "date_applied": (today - timedelta(days=70)).isoformat(),
            "company_name": "TEST COMPANY DELETE ME",
            "job_title": "Fake 61 Plus Day Application",
            "job_url": "https://example.com/sixty-one-plus",
            "source": "manual test",
            "status": "applied",
            "notes": "Step 17G test row - 61+ day candidate",
        },
    ]

    conn = sqlite3.connect("data/careersignal.db")

    for row in fake_rows:
        conn.execute(
            """
            INSERT INTO applications (
                date_applied,
                company_name,
                job_title,
                job_url,
                source,
                status,
                notes,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """,
            (
                row["date_applied"],
                row["company_name"],
                row["job_title"],
                row["job_url"],
                row["source"],
                row["status"],
                row["notes"],
            ),
        )

    conn.commit()
    conn.close()

    print("Inserted fake Step 17G test rows.")
    '@ | python -

Test status update command for fake Step 17G rows:

    @'
    import sqlite3
    from datetime import date

    today = date.today().isoformat()

    conn = sqlite3.connect("data/careersignal.db")
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT application_id, job_title
        FROM applications
        WHERE company_name = ?
        ORDER BY application_id DESC
        """,
        ("TEST COMPANY DELETE ME",)
    ).fetchall()

    for row in rows:
        job_title = row["job_title"]
        application_id = row["application_id"]

        if job_title == "Fake Weekly Application":
            conn.execute(
                """
                UPDATE applications
                SET status = ?,
                    first_response_date = ?,
                    interview_date = ?,
                    updated_at = datetime('now')
                WHERE application_id = ?
                """,
                ("interview", today, today, application_id),
            )

        elif job_title == "Fake Rejection Danger Zone Application":
            conn.execute(
                """
                UPDATE applications
                SET status = ?,
                    first_response_date = ?,
                    final_response_date = ?,
                    updated_at = datetime('now')
                WHERE application_id = ?
                """,
                ("rejected", today, today, application_id),
            )

        elif job_title == "Fake Ghosting Danger Zone Application":
            conn.execute(
                """
                UPDATE applications
                SET status = ?,
                    final_response_date = ?,
                    updated_at = datetime('now')
                WHERE application_id = ?
                """,
                ("ghosted", today, application_id),
            )

    conn.commit()
    conn.close()

    print("Updated fake Step 17G test rows.")
    '@ | python -

PowerShell-safe cleanup command for fake Step 17G rows:

    @'
    import sqlite3

    conn = sqlite3.connect("data/careersignal.db")

    conn.execute(
        "DELETE FROM applications WHERE company_name = ?",
        ("TEST COMPANY DELETE ME",)
    )

    conn.commit()
    conn.close()

    print("Deleted fake Step 17G test rows.")
    '@ | python -

PowerShell-safe confirmation after cleanup:

    @'
    import sqlite3

    conn = sqlite3.connect("data/careersignal.db")
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT * FROM applications WHERE company_name = ?",
        ("TEST COMPANY DELETE ME",)
    ).fetchall()

    print(f"Remaining fake rows: {len(rows)}")

    conn.close()
    '@ | python -

Expected cleanup result:

    Remaining fake rows: 0

---

### Step 17H: Power BI Application Tracker Visuals

Status:

- Optional / later

Goal:

Add Application Tracker visuals to Power BI after Excel export sheets are stable.

Possible visuals:

- KPI cards for total applications, interviews, rejections, ghostings, acceptances
- bar chart for applications by company
- bar chart for outcomes by company
- aging table
- status distribution chart
- applications over time

Important:

- Do not modify the Power BI file unless explicitly working on this step.
- Do not change the Power BI source path.
- Use exports/careersignal_export.xlsx as the data source.

---

## Current Roadmap

### Step 17: Application Tracker

Current active step.

Completed:

- 17A: Database foundation
- 17B: Reusable module
- 17C: Manual add-application script
- 17D: Manual status-update script
- 17E: Application tracker summary reporting
- 17F: Excel export integration
- 17G: Weekly tracker email

Current next step:

- 17H: Optional Power BI Application Tracker visuals

Planned:

- 17H: Optional Power BI visuals

---

### Step 18: GitHub + Portfolio Polish

Status:

- Planned, not current

Purpose:

Clean README, screenshots, sample outputs, final testing, resume bullets, and portfolio presentation.

Required before heavily featuring the project on a resume.

Step 18 should update:

- README.md
- docs/CareerSignal_Project_State.md

Step 18 should not:

- rename official functions
- change database paths
- recreate existing files
- break existing behavior
- change the Power BI source path without documenting it
- expose secrets

Step 18 validation should confirm:

- preview run works
- send run works
- email arrives
- email only includes jobs first seen in the past 24 hours
- match scores show correctly
- failed sources show correctly
- Excel export updates
- Application Tracker sheets exist in the Excel export
- weekly Application Tracker email previews correctly
- weekly Application Tracker email sends correctly
- Power BI refresh works from exports/careersignal_export.xlsx
- logs update
- no data/jobs.db references
- no old function names
- no secrets staged for Git

Step 18 known action items:

- Fix or confirm the Power BI data source so it pulls from exports/careersignal_export.xlsx instead of an old test file.
- Check and confirm that match scoring appears correctly in sent emails.
- Make sure sent emails include only jobs first seen in the past 24 hours.
- Circle back to Step 13 Workday URL issues.
- Add the rest of the confirmed Greenhouse companies.
- Polish README for portfolio/resume presentation.
- Add screenshots and sample outputs.
- Add or update notes for the Application Tracker, Excel export sheets, and weekly tracker email.

---

### Step 19: Optional Streamlit UI

Status:

- Optional / later

Only if a prettier local interface is wanted later.

Nice-to-have, not required.

---

## Must-Do vs Nice-to-Have

Current must-do path:

- 18: GitHub + Portfolio Polish

Nice-to-have:

- 17H: Power BI Application Tracker visuals
- 19: Optional Streamlit UI

---

## Testing Commands

Useful commands:

    PYTHONPATH=src python scripts/test_config_loader.py
    PYTHONPATH=src python scripts/test_database.py
    PYTHONPATH=src python scripts/test_match_scoring.py
    PYTHONPATH=src python scripts/test_email_report.py
    python scripts/collect_greenhouse_jobs.py --preview
    python scripts/export_to_excel.py
    python scripts/send_weekly_application_tracker_email.py --preview

Windows PowerShell:

    $env:PYTHONPATH="src"
    python scripts/test_config_loader.py
    python scripts/test_database.py
    python scripts/test_match_scoring.py
    python scripts/test_email_report.py
    python scripts/collect_greenhouse_jobs.py --preview
    python scripts/export_to_excel.py
    python scripts/send_weekly_application_tracker_email.py --preview

Daily automation test:

    .\run_careersignal_daily.bat

Real daily send mode:

    python scripts/collect_greenhouse_jobs.py --send
    python scripts/export_to_excel.py

Weekly Application Tracker email preview:

    python scripts/send_weekly_application_tracker_email.py --preview

Weekly Application Tracker email send:

    python scripts/send_weekly_application_tracker_email.py --send

Application Tracker initializer:

    python scripts/init_application_tracker.py

Application Tracker add-script help:

    python scripts/add_application.py --help

Application Tracker status-update help:

    python scripts/update_application_status.py --help

Application Tracker reporting:

    python scripts/report_applications.py

Application Tracker manual test insert:

    python scripts/add_application.py --company "TEST COMPANY DELETE ME" --title "Fake Test Application" --date-applied "2026-06-01" --url "https://example.com/test-job" --source "manual test" --notes "Delete this after test"

Application Tracker manual status-update test:

    python scripts/update_application_status.py --id 4 --status interview --notes "Moved to interview during Step 17D test" --date "2026-06-10"

Replace 4 with the actual application_id from the test insert.

Application Tracker PowerShell-safe confirmation query:

    @'
    import sqlite3

    conn = sqlite3.connect("data/careersignal.db")
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT * FROM applications WHERE company_name = ? ORDER BY application_id DESC",
        ("TEST COMPANY DELETE ME",)
    ).fetchall()

    for row in rows:
        print(dict(row))

    conn.close()
    '@ | python -

Application Tracker PowerShell-safe cleanup query:

    @'
    import sqlite3

    conn = sqlite3.connect("data/careersignal.db")

    conn.execute(
        "DELETE FROM applications WHERE company_name = ?",
        ("TEST COMPANY DELETE ME",)
    )

    conn.commit()
    conn.close()

    print("Deleted fake test application")
    '@ | python -

Excel export test:

    python scripts/export_to_excel.py

Excel export sheet confirmation:

    @'
    from openpyxl import load_workbook

    workbook = load_workbook("exports/careersignal_export.xlsx", read_only=True)

    for sheet_name in workbook.sheetnames:
        print(sheet_name)

    required = {
        "Applications",
        "Application Summary",
        "Company Application Summary",
        "Application Aging",
    }

    missing = required - set(workbook.sheetnames)

    if missing:
        print("Missing:", missing)
        raise SystemExit(1)

    print("All Step 17F sheets exist.")
    '@ | python -

---

## Required Checks for Future Coding Steps

For every future coding step, include:

1. Files to create/edit
2. Exact code
3. Commands to test
4. Grep/search checks for old names or broken imports
5. Git commit guidance

Important PowerShell note:

Do not use Select-String with the -Recurse parameter because this has caused problems on the user's machine.

Use this pattern instead:

    Get-ChildItem -Recurse -File | Select-String "search text"

Always include checks for:

    Get-ChildItem -Recurse -File | Select-String "data/jobs.db"
    Get-ChildItem -Recurse -File | Select-String "create_tables"
    Get-ChildItem -Recurse -File | Select-String "insert_normalized_jobs"
    Get-ChildItem -Recurse -File | Select-String "fetch_all_jobs"

Also check official function names when relevant:

    Get-ChildItem -Recurse -File | Select-String "build_and_send_daily_report"
    Get-ChildItem -Recurse -File | Select-String "score_job"
    Get-ChildItem -Recurse -File | Select-String "initialize_database"
    Get-ChildItem -Recurse -File | Select-String "insert_or_update_jobs"
    Get-ChildItem -Recurse -File | Select-String "get_jobs_first_seen_in_last_24_hours"

Application Tracker checks when relevant:

    Get-ChildItem -Recurse -File | Select-String "applications"
    Get-ChildItem -Recurse -File | Select-String "application_id"
    Get-ChildItem -Recurse -File | Select-String "application_tracker"
    Get-ChildItem -Recurse -File | Select-String "data/jobs.db"

Important:

The module/file names still use application_tracker, but the actual database table is applications.

Acceptable references:

- src/careersignal/application_tracker.py
- src/careersignal/application_tracker_db.py
- scripts/init_application_tracker.py
- scripts/add_application.py
- scripts/update_application_status.py
- scripts/report_applications.py
- scripts/send_weekly_application_tracker_email.py
- from careersignal.application_tracker import fetch_applications

Stale or suspicious references:

- application_tracker table
- SELECT * FROM application_tracker
- INSERT INTO application_tracker
- UPDATE application_tracker
- DELETE FROM application_tracker

Bad old table SQL checks:

    Get-ChildItem -Recurse -File | Select-String "SELECT \* FROM application_tracker"
    Get-ChildItem -Recurse -File | Select-String "INSERT INTO application_tracker"
    Get-ChildItem -Recurse -File | Select-String "UPDATE application_tracker"
    Get-ChildItem -Recurse -File | Select-String "DELETE FROM application_tracker"

Expected result for bad old table SQL checks:

- No results

Weekly email checks:

    Get-Item .\scripts\send_weekly_application_tracker_email.py
    python scripts/send_weekly_application_tracker_email.py --preview

Daily email preservation check:

    python scripts/collect_greenhouse_jobs.py --preview

Expected result:

- Daily preview still works.
- Weekly preview still works.
- Weekly email remains separate from daily job alert email.

---

## Git Guidance

After project-state updates:

    git add docs/CareerSignal_Project_State.md
    git commit -m "Update CareerSignal project state"
    git push

After README updates:

    git add README.md
    git commit -m "Update CareerSignal README"
    git push

After Application Tracker feature steps, use specific commit messages.

Step 17A:

    git add .
    git commit -m "Add application tracker database foundation"
    git push

Step 17B:

    git add .
    git commit -m "Add application tracker module"
    git push

Step 17C:

    git add .
    git commit -m "Add application entry script"
    git push

Step 17D:

    git add .
    git commit -m "Add application status update script"
    git push

Step 17E:

    git add .
    git commit -m "Add application tracker reporting"
    git push

Step 17F:

    git add scripts/export_to_excel.py
    git commit -m "Add application tracker sheets to Excel export"
    git push

Step 17G:

    git add scripts/send_weekly_application_tracker_email.py
    git commit -m "Add weekly application tracker email"
    git push

Avoid committing:

- .env
- logs/
- data/careersignal.db if intentionally ignored
- exports/careersignal_export.xlsx if intentionally ignored
- temporary test files
- email passwords
- SMTP secrets

Before committing, always run:

    git status
    git diff --cached

If updating only the project state file, prefer:

    git add docs/CareerSignal_Project_State.md
    git diff --cached
    git commit -m "Update CareerSignal project state"
    git push

If committing Step 17G only, prefer:

    git add scripts/send_weekly_application_tracker_email.py
    git diff --cached
    git commit -m "Add weekly application tracker email"
    git push

If committing Step 17G and the updated project state together, prefer:

    git add scripts/send_weekly_application_tracker_email.py docs/CareerSignal_Project_State.md
    git diff --cached
    git commit -m "Add weekly application tracker email"
    git push

---

## Important Reminder for Future ChatGPT Help

Before giving code:

1. Read this file.
2. Do not recreate existing files.
3. Do not rename official functions.
4. Do not change data/careersignal.db.
5. Do not use data/jobs.db.
6. Do not use old function names.
7. Explain dependencies before rewriting core files.
8. Keep new work compatible with the existing pipeline.
9. Preserve Greenhouse and Workday support.
10. Preserve email, Excel, Power BI, logging, and scoring behavior unless asked to change them.
11. Preserve preview mode and send mode.
12. Keep .env and secrets out of GitHub.
13. Keep the response beginner-friendly and step-by-step.
14. During Step 17, do not modify daily job alert behavior unless explicitly approved.
15. During Step 17, keep Application Tracker steps small and separate.
16. During Step 17, use the actual table name applications.
17. During Step 17, use the actual primary key application_id.
18. During Step 17, keep runnable scripts in scripts/.
19. During Step 17, keep reusable logic in src/careersignal/.
20. Do not use Select-String -Recurse in PowerShell instructions.
21. Use Get-ChildItem -Recurse -File | Select-String "pattern" instead.
22. Do not create a separate Application Tracker workbook unless explicitly approved.
23. Do not change the Power BI source path unless explicitly working on that issue.
24. Do not add Application Tracker stats to the daily email unless explicitly approved.
25. Keep the weekly Application Tracker email separate from the daily job alert email at first.
26. Do not schedule the weekly Application Tracker email unless explicitly approved.
27. Do not modify Excel export during weekly email work unless explicitly approved.
28. Do not modify Power BI during weekly email work unless explicitly approved.

---

## Current Known Truths for Application Tracker

Database:

- data/careersignal.db

Table:

- applications

Primary key:

- application_id

Database setup file:

- src/careersignal/application_tracker_db.py

Reusable logic file:

- src/careersignal/application_tracker.py

Initializer script:

- scripts/init_application_tracker.py

Manual add script:

- scripts/add_application.py

Manual status-update script:

- scripts/update_application_status.py

Summary reporting script:

- scripts/report_applications.py

Weekly email script:

- scripts/send_weekly_application_tracker_email.py

Excel export script:

- scripts/export_to_excel.py

Excel export workbook:

- exports/careersignal_export.xlsx

Application Tracker Excel sheets:

- Applications
- Application Summary
- Company Application Summary
- Application Aging

Official reusable functions:

- get_current_timestamp
- validate_application_status
- add_application
- update_application_status
- update_application_notes
- update_application_response_dates
- fetch_application_by_id
- fetch_applications

Current next planned step:

- 17H: Optional Power BI Application Tracker visuals

Current must-do next phase:

- Step 18: GitHub + Portfolio Polish