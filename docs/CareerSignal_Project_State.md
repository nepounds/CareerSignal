# CareerSignal Project State

## Current Project Status

CareerSignal currently has a working end-to-end job alert pipeline, a manual Application Tracker layer, Excel export integration, a Power BI dashboard, Application Tracker Power BI visuals, Windows automation support, GitHub Actions testing, and a polished README.

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

* 12A. Workday proof of concept
* 12B. Workday normalization
* 12C. Workday integration into the main pipeline

13. ATS Coverage Audit started, with unresolved follow-up items
14. Filtering Strategy completed
15. Match Scoring Refinement completed
16. Daily Automation runner added for Windows Task Scheduler
17. Application Tracker completed through Power BI visuals

* 17A. Application Tracker database foundation completed
* 17B. Application Tracker reusable module completed
* 17C. Manual add-application script completed
* 17D. Manual status-update script completed
* 17E. Application Tracker summary reporting completed
* 17F. Application Tracker Excel export integration completed
* 17G. Weekly Application Tracker email script completed
* 17H. Power BI Application Tracker visuals completed
* 17I. Application Tracker finishing touches completed

18. GitHub + Portfolio Polish completed

* `.gitignore` updated
* README updated and pushed
* Application Tracker screenshot added to README
* Demo companies cleaned out
* Excel export verified
* Power BI refreshed and visually checked
* Stale reference checks passed
* Pytest passed
* Ruff passed
* Git working tree clean

Current status:

* CareerSignal is resume-ready and GitHub-ready.
* Main pipeline works.
* Application Tracker works.
* README has been updated to reflect the finished Application Tracker.
* Screenshots are clean and final.
* Git status is clean.

The main product loop exists:

```
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
```

Application Tracker loop:

```
manual application entry
→ applications table in data/careersignal.db
→ reusable application_tracker.py module
→ manual add/update scripts
→ summary reporting
→ Excel export sheets
→ separate weekly Application Tracker email script
→ Power BI Application Tracker dashboard page
```

---

## Existing Project Structure

Preserve this structure.

```
CareerSignal/
├── config/
│   ├── company_config.csv
│   ├── company_ats_audit.csv
│   ├── match_rules.json
│   └── workday_api_url_test_results.csv
├── data/
│   └── .gitkeep
├── docs/
│   ├── CareerSignal_Project_State.md
│   ├── filtering_strategy.md
│   └── screenshots/
│       ├── application_tracker_dashboard.png
│       ├── excel_export_sample.png
│       ├── powerbi_overview_dashboard.png
│       ├── sample_daily_email.png
│       └── task_scheduler_setup.png
├── exports/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── reports/
│   └── careersignal_dashboard.pbix
├── .github/
│   └── workflows/
│       └── tests.yml
├── scripts/
│   ├── add_application.py
│   ├── add_match_scoring_columns.py
│   ├── check_application_tracker.py
│   ├── check_generated_workday_api_urls.py
│   ├── collect_greenhouse_jobs.py
│   ├── export_ready_companies_to_config.py
│   ├── export_to_excel.py
│   ├── generate_company_config_from_audit.py
│   ├── init_application_tracker.py
│   ├── init_database.py
│   ├── preview_workday_jobs.py
│   ├── preview_workday_normalized_jobs.py
│   ├── report_applications.py
│   ├── send_weekly_application_tracker_email.py
│   ├── show_applications.py
│   ├── test_job_normalizer.py
│   ├── test_match_scoring.py
│   ├── test_new_job_detection.py
│   ├── update_application_status.py
│   ├── update_match_scores.py
│   ├── verify_ats_audit.py
│   └── view_database.py
├── src/
│   └── careersignal/
│       ├── __init__.py
│       ├── application_tracker.py
│       ├── application_tracker_db.py
│       ├── config_loader.py
│       ├── database.py
│       ├── email_report.py
│       ├── job_normalizer.py
│       ├── logging_config.py
│       ├── main.py
│       ├── match_scoring.py
│       └── collectors/
│           ├── __init__.py
│           ├── greenhouse.py
│           └── workday.py
├── tests/
│   ├── .gitkeep
│   ├── test_email_report.py
│   └── test_match_scoring.py
├── run_careersignal_daily.bat
├── run_weekly_application_tracker_email.bat
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

Generated/local files should not be committed unless intentionally approved:

* `.env`
* `.venv/`
* `data/careersignal.db`
* `exports/careersignal_export.xlsx`
* `logs/`
* local cache files
* temporary files
* backup files

---

## Important Project Rules

For CareerSignal coding help, always treat this file as the source of truth before suggesting code changes.

Do not invent new function names if an official name already exists.

Before rewriting a core file, explain which other files depend on it.

Keep naming consistent with the official function names in this project state file.

Do not add compatibility wrappers or aliases unless explicitly approved.

Prefer updating dependent scripts to use the current official function names.

Preserve the existing project structure:

* `scripts/` contains runnable scripts.
* `src/careersignal/` contains reusable modules.
* `data/careersignal.db` is the SQLite database.
* `config/company_config.csv` is the company config.
* `exports/careersignal_export.xlsx` is the Excel export used by Power BI.
* `reports/careersignal_dashboard.pbix` is the Power BI dashboard.

Do not use:

* `data/jobs.db`

Do not rename:

* `scripts/collect_greenhouse_jobs.py`

Even though the script name says Greenhouse, after Workday integration it functions as the main collector runner.

Do not rename this script unless intentionally doing a cleanup/refactor step.

Do not modify the daily job alert email unless explicitly approved.

Do not modify the weekly Application Tracker email unless explicitly working on weekly email behavior.

Do not create a separate Application Tracker workbook unless explicitly approved.

Do not change the Power BI source path unless there is a confirmed source problem and the fix is approved.

Do not use `Select-String -Recurse` in PowerShell instructions.

Use this PowerShell pattern instead:

```
Get-ChildItem -Recurse -File | Select-String "search text"
```

---

## Existing Files That Should Not Be Recreated Blindly

These files already exist or have already been worked on.

Do not recreate them from scratch unless they are missing.

```
README.md
requirements.txt
pyproject.toml
.env.example
.gitignore
run_careersignal_daily.bat
run_weekly_application_tracker_email.bat
config/company_config.csv
config/company_ats_audit.csv
config/match_rules.json
config/workday_api_url_test_results.csv
docs/CareerSignal_Project_State.md
docs/filtering_strategy.md
docs/screenshots/application_tracker_dashboard.png
docs/screenshots/excel_export_sample.png
docs/screenshots/powerbi_overview_dashboard.png
docs/screenshots/sample_daily_email.png
docs/screenshots/task_scheduler_setup.png
reports/careersignal_dashboard.pbix
scripts/add_application.py
scripts/add_match_scoring_columns.py
scripts/check_application_tracker.py
scripts/check_generated_workday_api_urls.py
scripts/collect_greenhouse_jobs.py
scripts/export_ready_companies_to_config.py
scripts/export_to_excel.py
scripts/generate_company_config_from_audit.py
scripts/init_application_tracker.py
scripts/init_database.py
scripts/preview_workday_jobs.py
scripts/preview_workday_normalized_jobs.py
scripts/report_applications.py
scripts/send_weekly_application_tracker_email.py
scripts/show_applications.py
scripts/test_job_normalizer.py
scripts/test_new_job_detection.py
scripts/update_application_status.py
scripts/update_match_scores.py
scripts/verify_ats_audit.py
scripts/view_database.py
src/careersignal/application_tracker.py
src/careersignal/application_tracker_db.py
src/careersignal/config_loader.py
src/careersignal/database.py
src/careersignal/email_report.py
src/careersignal/job_normalizer.py
src/careersignal/logging_config.py
src/careersignal/main.py
src/careersignal/match_scoring.py
src/careersignal/collectors/greenhouse.py
src/careersignal/collectors/workday.py
tests/test_email_report.py
tests/test_match_scoring.py
```

If a future step needs to modify one of these files, explain:

1. Why the file needs to change
2. What depends on it
3. How the change preserves existing behavior

---

## Core Pipeline Status

### SQLite Database

Official database path:

* `data/careersignal.db`

Do not use:

* `data/jobs.db`

The main database supports:

* job storage
* duplicate prevention
* first-seen tracking
* last-seen tracking
* new job detection
* match scoring support
* run logging
* Application Tracker records

Application Tracker also uses:

* `data/careersignal.db`

Application Tracker table:

* `applications`

Application Tracker primary key:

* `application_id`

---

### Greenhouse Collector

Likely file:

* `src/careersignal/collectors/greenhouse.py`

Existing runner command:

```
python scripts/collect_greenhouse_jobs.py --preview
```

Send real email:

```
python scripts/collect_greenhouse_jobs.py --send
```

Important:

The script name still says `collect_greenhouse_jobs.py`, but after Workday integration it functions as the main collector runner.

Do not rename this script unless intentionally doing a cleanup/refactor step.

---

### Workday Collector

Likely file:

* `src/careersignal/collectors/workday.py`

Workday was split into three parts:

* 12A: Workday Proof of Concept
* 12B: Workday Normalization
* 12C: Integrate Workday Connector

All three are considered complete if the current branch has Workday jobs flowing through the same pipeline as Greenhouse.

Workday jobs should use:

```
"source_ats": "workday"
```

Workday jobs must use the official normalized job shape.

Known future issue:

* Some Workday links are broken and should be fixed later.

---

### Match Scoring

Step 15 is complete and used the Step 14 filtering strategy.

Important distinction:

* Step 14 = decide what CareerSignal should care about
* Step 15 = assign scoring weights and implement/refine scoring logic

Match scoring should preserve:

* `score_job(job)`

Scores should remain from 0 to 100.

Suggested score bands:

* 80-100: Strong match
* 60-79: Possible match
* 40-59: Weak/stretch match
* 0-39: Low match or likely skip

CareerSignal is not accounting-only.

The filtering and scoring strategy supports multiple job-search lanes:

* Accounting roles
* Finance roles
* General analyst roles
* Business analyst roles
* Operations analyst roles
* Compliance analyst roles
* Data/reporting analyst roles
* Plant supervisor jobs
* Operations supervisor jobs
* Water/wastewater or public utility-adjacent jobs
* Other realistic roles that fit the user's background

---

### Email Reporting

Daily email reporting supports preview/test mode and send mode.

Daily job alert email is separate from the weekly Application Tracker email.

Daily job alert email should not be modified during Application Tracker work unless explicitly approved.

Weekly Application Tracker email script exists:

* `scripts/send_weekly_application_tracker_email.py`

Weekly Application Tracker batch file exists:

* `run_weekly_application_tracker_email.bat`

The weekly Application Tracker email uses:

* preview mode
* send mode
* the `applications` table
* `data/careersignal.db`
* the existing `.env`/email credential pattern where possible

The weekly email does not modify:

* daily job alert behavior
* Excel export
* Power BI
* database schema
* Windows Task Scheduler configuration

The weekly batch file can be run manually. Scheduling it in Windows Task Scheduler is optional and is not currently listed as a planned future update.

---

### Logging

Likely file:

* `src/careersignal/logging_config.py`

Logs should go to:

* `logs/careersignal.log`

Scheduled task logs should go to:

* `logs/scheduled_task.log`

Weekly Application Tracker email logs should go to:

* `logs/weekly_application_tracker_email.log`

A failed company source should not crash the whole run.

Failed sources should be tracked and included in the daily email report where possible.

---

### Excel Export

File:

* `scripts/export_to_excel.py`

Export output:

* `exports/careersignal_export.xlsx`

The Excel export feeds the Power BI dashboard.

Do not break this output path without updating the README and Power BI notes.

Step 17F added Application Tracker sheets to the existing workbook.

Existing job export sheets should remain intact.

Application Tracker export sheets:

* Applications
* Application Summary
* Company Application Summary
* Application Aging

The export should still run with:

```
python scripts/export_to_excel.py
```

The export should still create or update:

* `exports/careersignal_export.xlsx`

The Power BI source path remains unchanged.

No separate tracker workbook should exist unless intentionally approved later.

Application Tracker export behavior:

Applications sheet:

* Full row-level application tracker data from the `applications` table.

Expected fields include:

* application_id
* date_applied
* company_name
* job_title
* job_url
* source
* status
* first_response_date
* interview_date
* final_response_date
* notes
* created_at
* updated_at

Application Summary sheet:

* metric
* value

Expected metric rows include:

* total applications
* active applications
* interviews
* acceptances
* formal rejections
* ghostings
* negative outcomes

Company Application Summary sheet:

* company_name
* total applications
* active applications
* interviews
* acceptances
* formal rejections
* ghostings
* negative outcomes

Application Aging sheet:

* application_id
* company_name
* job_title
* date_applied
* status
* days_since_applied
* aging_bucket

Current reporting/export aging rules:

* Non-applied statuses = responded / closed
* 0-14 days with status applied = active / normal waiting period
* 15-30 days with status applied = rejection danger zone
* 31-60 days with status applied = ghosting candidate
* 61+ days with status applied = ghosted

Important:

* Application Aging reports aging only.
* It does not mutate the database.
* It does not automatically change statuses in the database.
* Ghosted applications count as negative outcomes.

---

### Power BI

Power BI report:

* `reports/careersignal_dashboard.pbix`

Power BI data source:

* `exports/careersignal_export.xlsx`

After generating a fresh Excel export, refresh Power BI manually:

* Home > Refresh

Current dashboard exists and should not be treated as unstarted.

Application Tracker page exists inside the existing Power BI file.

Application Tracker Power BI page title:

* CareerSignal Application Tracker

Application Tracker page visuals:

KPI cards:

* Total
* Active
* Interviews
* Offers
* Rejections
* Ghosted
* Negative

KPI card source:

* Application Summary

Power BI setup note:

* Application Summary is in long format with columns:

  * metric
  * value

KPI cards use:

* value as the card value
* metric as a visual-level filter

KPI card metric mapping:

* Total = metric: total applications
* Active = metric: active applications
* Interviews = metric: interviews
* Offers = metric: acceptances
* Rejections = metric: formal rejections
* Ghosted = metric: ghostings
* Negative = metric: negative outcomes

Charts:

Applications by Company:

* Source: Company Application Summary
* Axis: company_name
* Value: total applications
* Aggregation: Sum
* Important: total applications must be treated as Whole Number in Power Query, not text.

Status Mix:

* Source: Applications
* Legend: status
* Values: application_id
* Aggregation: Count

Applications Over Time:

* Source: Applications
* X-axis: date_applied
* Y-axis: Cumulative Applications measure
* Current visual behaves as cumulative application growth.
* Suggested title if renamed later: Application Growth

Cumulative Applications DAX measure:

```
Cumulative Applications =
VAR CurrentDate = MAX('Applications'[date_applied])
RETURN
CALCULATE(
    COUNTROWS('Applications'),
    FILTER(
        ALL('Applications'),
        'Applications'[date_applied] <= CurrentDate
    )
)
```

Aging Watchlist table:

* Source: Application Aging
* Fields:

  * company_name
  * job_title
  * date_applied
  * status
  * days_since_applied
  * aging_bucket

Displayed column names:

* Company
* Job Title
* Date Applied
* Status
* Days Waiting
* Aging Bucket

Important Power BI notes:

* Each visual should generally use fields from one table/query unless relationships are intentionally configured.
* The Aging Watchlist table should use only the Application Aging table.
* The Applications by Company chart should use only the Company Application Summary table.
* The KPI cards should use only the Application Summary table.
* The Power BI data source path remains `exports/careersignal_export.xlsx`.

Screenshot:

* `docs/screenshots/application_tracker_dashboard.png`

The screenshot is final and included in the README.

---

### Daily Automation

Step 16 is complete if the project has:

* `run_careersignal_daily.bat`

and Windows Task Scheduler is configured to run it daily.

The daily automation should run:

```
python scripts\collect_greenhouse_jobs.py --send
python scripts\export_to_excel.py
```

The batch file should:

1. Change into the CareerSignal project folder
2. Activate the virtual environment if needed
3. Set `PYTHONPATH=src`
4. Run the collector in send mode
5. Run the Excel export
6. Write useful output to `logs/scheduled_task.log`

Recommended scheduled run time:

* 7:30 AM daily

Manual test command:

```
.\run_careersignal_daily.bat
```

Useful verification commands:

```
Get-Content .\logs\scheduled_task.log -Tail 100
Get-Content .\logs\careersignal.log -Tail 100
Get-Item .\data\careersignal.db
Get-Item .\exports\careersignal_export.xlsx
```

Known scheduler troubleshooting notes:

* Do not close the `.bat`/cmd window when it appears during the scheduled run.
* Do not run Checkpoint VPN or NordVPN during the scheduled job if they block SMTP traffic.
* If email does not send, check whether VPN or network restrictions blocked `smtp.gmail.com` or the configured SMTP host on port 587.

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

Step 13 follow-up items that still matter:

1. Identify which unsupported ATSs appear often enough to justify new connectors.
2. Add extra connectors for ATS platforms used by more than 5 target companies.
3. Review and fix broken Workday links.

Do not build connectors for one-off systems unless they are high-value companies.

---

## Step 17 Application Tracker Status

Step 17 is complete.

Goal:

Add a manual application tracking system to CareerSignal that records applications submitted by the user, tracks response outcomes, calculates ghosting/rejection danger zones, summarizes application performance overall and by company, exports Application Tracker sheets to Excel, sends a separate weekly Application Tracker email, and visualizes the tracker in Power BI.

Application Tracker remains separate from the automated job collector.

Do not modify the daily job alert email unless explicitly approved.

---

### Application Tracker Database Naming

Official database:

* `data/careersignal.db`

Official Application Tracker table:

* `applications`

Official Application Tracker primary key:

* `application_id`

Important:

Earlier planning notes may have referred to the table as `application_tracker`, but the actual implemented table name is `applications`.

Use `applications` going forward unless a future intentional migration renames it.

---

### Step 17A: Application Tracker Database Foundation

Status:

* Complete

Purpose:

Create the database foundation for manually tracking job applications.

Expected database:

* `data/careersignal.db`

Implemented table:

* `applications`

Implemented primary key:

* `application_id`

Core fields support:

* application_id
* date_applied
* company_name
* job_title
* job_url
* source
* status
* first_response_date
* interview_date
* final_response_date
* notes
* created_at
* updated_at

Valid statuses:

* applied
* interview
* rejected
* accepted
* ghosted
* withdrawn
* closed

Initializer script:

* `scripts/init_application_tracker.py`

Reusable database setup file:

* `src/careersignal/application_tracker_db.py`

17A did not include:

* manual command-line scripts
* summary reporting
* weekly email
* Excel export
* Power BI visuals
* daily email changes

---

### Step 17B: Application Tracker Reusable Module

Status:

* Complete

Purpose:

Add reusable Python logic for interacting with the Application Tracker table.

Implemented file:

* `src/careersignal/application_tracker.py`

Official table constant:

```
APPLICATION_TRACKER_TABLE = "applications"
```

Official reusable functions:

* get_current_timestamp
* validate_application_status
* add_application
* update_application_status
* update_application_notes
* update_application_response_dates
* fetch_application_by_id
* fetch_applications

Important function behavior:

* `add_application(...)` returns the inserted `application_id` as an int.
* `fetch_application_by_id(...)` returns one application record as a dict or None.
* `fetch_applications(...)` returns a list of application record dicts.

17B did not include:

* manual command-line scripts
* summary reporting
* weekly email
* Excel export
* Power BI visuals
* daily email changes

---

### Step 17C: Manual Add-Application Script

Status:

* Complete

Goal:

Create a runnable script for manually adding application records from PowerShell.

Implemented file:

* `scripts/add_application.py`

Expected behavior:

* User runs a command with company, title, date applied, URL/source/notes if available.
* Script validates required input.
* Script calls `add_application(...)` from `src/careersignal/application_tracker.py`.
* Script inserts the application into the `applications` table.
* Script prints a clean confirmation, including the returned `application_id`.

Example command:

```
python scripts/add_application.py --company "RSM" --title "Audit Associate" --date-applied "2026-06-01" --url "https://example.com/job" --source "company website" --notes "Applied through company portal"
```

Minimal command:

```
python scripts/add_application.py --company "RSM" --title "Audit Associate" --date-applied "2026-06-01"
```

17C did not include:

* summary reporting
* status updates
* weekly email
* Excel export changes
* Power BI changes
* daily email changes

---

### Step 17D: Manual Status-Update Script

Status:

* Complete

Goal:

Create a runnable script for manually updating an application’s status.

Implemented file:

* `scripts/update_application_status.py`

Expected behavior:

* User provides `application_id` and new status.
* Script validates status using `validate_application_status(...)`.
* Script calls `update_application_status(...)` from `src/careersignal/application_tracker.py`.
* Script updates the matching row in the `applications` table.
* Script prints a clean confirmation showing `application_id`, `company_name`, `job_title`, old status, and new status.

Supported command:

```
python scripts/update_application_status.py --id 4 --status interview
```

Optional notes command:

```
python scripts/update_application_status.py --id 4 --status rejected --notes "Rejected by email"
```

Optional date command:

```
python scripts/update_application_status.py --id 4 --status interview --date "2026-06-10"
```

Important implementation notes:

* The script uses existing reusable functions from `src/careersignal/application_tracker.py`.
* The script does not rewrite the reusable module.
* The script does not modify the daily job alert email.
* The script does not modify Excel export.
* The script does not modify Power BI.
* The script does not build summary reporting.

17D did not include:

* summary reporting
* weekly email
* Excel export changes
* Power BI changes
* daily email changes

---

### Step 17E: Application Tracker Summary Reporting

Status:

* Complete

Goal:

Add summary reporting for Application Tracker.

Implemented file:

* `scripts/report_applications.py`

Expected reporting:

* total applications
* active applications
* interviews
* acceptances
* formal rejections
* ghostings
* negative outcomes
* totals by company
* interviews by company
* rejections by company
* ghostings by company
* acceptances by company
* application aging buckets

Ghostings count as negative outcomes.

Reporting logic should use:

* `applications` table
* `application_id` primary key
* `data/careersignal.db` database
* official functions from `src/careersignal/application_tracker.py` where practical

Run command:

```
python scripts/report_applications.py
```

17E did not include:

* weekly email
* Excel export changes
* Power BI changes
* daily job alert email changes

---

### Step 17F: Excel Export Integration

Status:

* Complete

Goal:

Add Application Tracker sheets to the existing Excel export.

Updated file:

* `scripts/export_to_excel.py`

Existing export output preserved:

* `exports/careersignal_export.xlsx`

Required sheets added:

* Applications
* Application Summary
* Company Application Summary
* Application Aging

Expected behavior:

* Running `python scripts/export_to_excel.py` still works.
* Existing job export sheets remain intact.
* Application Tracker sheets are added to the same workbook.
* Power BI source path remains unchanged.
* No separate tracker workbook is created.
* No database schema change is made.
* No statuses are automatically changed.
* No daily email behavior is changed.

Application Tracker sheet behavior:

Applications sheet:

* Full row-level application tracker data from the `applications` table.

Application Summary sheet:

* metric
* value

Company Application Summary sheet:

* company_name
* total applications
* active applications
* interviews
* acceptances
* formal rejections
* ghostings
* negative outcomes

Application Aging sheet:

* application_id
* company_name
* job_title
* date_applied
* status
* days_since_applied
* aging_bucket

Current aging rules:

* Non-applied statuses = responded / closed
* 0-14 days with status applied = active / normal waiting period
* 15-30 days with status applied = rejection danger zone
* 31-60 days with status applied = ghosting candidate
* 61+ days with status applied = ghosted

Important:

* Application Aging reports aging only.
* It does not mutate the database.
* It does not automatically change statuses in the database.
* Ghosted applications count as negative outcomes.

Step 17F preserved:

* `data/careersignal.db`
* `applications` table
* `application_id` primary key
* Greenhouse support
* Workday support
* database behavior
* email behavior
* logging behavior
* match scoring behavior
* Power BI source path
* Windows Task Scheduler behavior

Run command:

```
python scripts/export_to_excel.py
```

---

### Step 17G: Weekly Application Tracker Email

Status:

* Complete script
* Manual weekly batch file exists

Goal:

Add a separate weekly Application Tracker email after reporting and Excel export work.

Implemented file:

* `scripts/send_weekly_application_tracker_email.py`

Manual batch file:

* `run_weekly_application_tracker_email.bat`

Important:

The weekly Application Tracker email remains separate from the daily job alert email.

Application Tracker stats were not added to the daily job alert email.

The existing daily email module was not modified during Step 17G.

The existing daily collector script was not modified during Step 17G.

The Excel export was not modified during Step 17G.

Power BI was not modified during Step 17G.

Windows Task Scheduler was not modified during Step 17G.

Expected weekly tracker email content:

* applications submitted this week
* interviews received this week
* rejections received this week
* ghostings identified this week
* total applications
* total active applications
* interviews
* acceptances
* formal rejections
* ghostings
* negative outcomes
* rejection danger zone watchlist
* ghosting candidate watchlist
* ghosted items
* company response summary

Weekly email subject line:

```
CareerSignal Weekly Application Tracker Summary
```

Preview command:

```
python scripts/send_weekly_application_tracker_email.py --preview
```

Send command:

```
python scripts/send_weekly_application_tracker_email.py --send
```

Manual batch command:

```
.\run_weekly_application_tracker_email.bat
```

Safety behavior:

* Script previews by default if no send flag is provided.
* Script does not send unless `--send` is explicitly provided.
* Script prints generated email content in preview mode.
* Script uses the existing Application Tracker table: `applications`.
* Script uses the existing Application Tracker primary key: `application_id`.
* Script uses the existing database path through the reusable Application Tracker module.
* Script does not change any database schema.
* Script does not mutate application statuses.
* Script does not schedule itself.

Email configuration behavior:

* The script uses environment variables and `.env` values.
* It supports common email config variable names so the existing email credential pattern can be reused without editing the daily email module.

Supported email config variable names include:

* SMTP_HOST or SMTP_SERVER or EMAIL_HOST
* SMTP_PORT or EMAIL_PORT
* SMTP_USERNAME or EMAIL_USERNAME or EMAIL_SENDER or EMAIL_FROM
* SMTP_PASSWORD or EMAIL_PASSWORD or EMAIL_APP_PASSWORD
* EMAIL_FROM or EMAIL_SENDER
* EMAIL_TO or EMAIL_RECIPIENT or RECIPIENT_EMAIL

Step 17G preserved:

* `data/careersignal.db`
* `applications` table
* `application_id` primary key
* Greenhouse support
* Workday support
* database behavior
* daily email behavior
* logging behavior
* Excel export behavior
* Power BI source path
* match scoring behavior
* Windows Task Scheduler behavior

Step 17G did not include:

* Power BI Application Tracker visuals
* Windows Task Scheduler setup for the weekly email
* changes to daily job alert email
* changes to Excel export
* database schema changes
* automatic ghosting status updates

---

### Step 17H: Power BI Application Tracker Visuals

Status:

* Complete

Goal:

Add Application Tracker visuals to Power BI after Excel export sheets are stable.

Updated file:

* `reports/careersignal_dashboard.pbix`

Supporting screenshot:

* `docs/screenshots/application_tracker_dashboard.png`

Updated file due to aging label change:

* `scripts/export_to_excel.py`

Power BI source preserved:

* `exports/careersignal_export.xlsx`

Dedicated page added:

* Application Tracker

Dashboard title:

* CareerSignal Application Tracker

Visuals added:

KPI cards:

* Total
* Active
* Interviews
* Offers
* Rejections
* Ghosted
* Negative

Charts:

* Applications by Company
* Status Mix
* Applications Over Time / cumulative application growth

Table:

* Aging Watchlist

Important implementation notes:

* KPI cards use the Application Summary sheet.
* Application Summary has metric/value layout.
* Each KPI card uses value and filters by metric.
* Applications by Company uses Company Application Summary.
* `total applications` must be Whole Number and aggregated as Sum.
* Status Mix uses Applications.
* Applications Over Time uses Applications and a cumulative DAX measure.
* Aging Watchlist uses Application Aging only.
* The new page was added to the existing `reports/careersignal_dashboard.pbix` file.
* Existing job alert/dashboard visuals were intended to remain intact.
* Power BI must be manually refreshed after running `python scripts/export_to_excel.py`.

Step 17H did not include:

* automatic database status updates
* new ATS connectors
* Workday link fixes
* database schema changes

---

### Step 17I: Application Tracker Finishing Touches

Status:

* Complete

Purpose:

Finish Application Tracker cleanup and prepare the project for GitHub polish.

Completed:

* Demo companies cleaned out.
* Application Tracker screenshot finalized.
* Power BI dashboard refreshed cleanly.
* Application Tracker Excel export sheets confirmed.
* Weekly Application Tracker email batch file exists.
* README later updated during Step 18 to reflect the finished Application Tracker.

Known result:

* Application Tracker is complete and clean.
* Demo application data is not left in the live database.
* Power BI visuals are present and clean.

Remaining Application Dashboard future update:

* Change status updates to auto based on days since applying.
* This can wait.

---

## Step 18: GitHub + Portfolio Polish

Status:

* Complete

Purpose:

Clean README, screenshots, sample outputs, final testing, GitHub safety, and portfolio presentation.

Updated:

* `README.md`
* `.gitignore`
* `docs/CareerSignal_Project_State.md`

Confirmed:

* Git status clean before README work.
* `.gitignore` updated and pushed.
* README updated and pushed.
* README now includes the Application Tracker.
* README now includes the Application Tracker dashboard screenshot.
* README future improvements narrowed to only the desired future updates.
* Demo data checks returned 0 rows for companies, run logs, and applications.
* Excel export ran successfully.
* Application Tracker sheets exist in the Excel export.
* Power BI refreshed and looks good.
* Screenshots are good.
* Stale reference checks passed.
* Pytest passed.
* Ruff passed.
* Git status clean after README push.

Step 18 validation results:

```
pytest tests
→ 5 passed

ruff check src scripts tests
→ All checks passed

git status
→ nothing to commit, working tree clean
```

Stale reference checks passed for:

* `data/jobs.db`
* old `application_tracker` table SQL
* old function names:

  * create_tables
  * insert_normalized_jobs
  * fetch_all_jobs

Demo data checks passed:

* companies.company_name = 0 demo/example/test rows
* run_logs.company_name = 0 demo/example/test rows
* applications.company_name = 0 demo/example/test rows

README now presents CareerSignal as:

* automated job discovery
* SQLite storage
* match scoring
* daily email reporting
* Excel export
* Power BI dashboard
* manual Application Tracker
* weekly Application Tracker email
* GitHub Actions testing
* Ruff linting
* Windows automation

Step 18 did not include:

* new ATS connectors
* Workday link fixes
* automatic application status changes
* hosted deployment
* Streamlit UI

---

## Future Updates and Fine-Tuning

Only the following future updates are currently planned.

### Application Dashboard Future Update

1. Change status updates to auto based on days since applying.

   * This can wait.
   * Do not silently mutate the database without an intentional step.
   * Preferred safe approach:

     * Add a reporting/display status first, or
     * Add a separate script that marks 61+ day applied rows as ghosted only when intentionally run.
   * Avoid hidden automatic status changes unless clearly documented.

Current desired future logic if implemented later:

* 0-14 days with status applied = active / normal waiting period
* 15-30 days with status applied = rejection danger zone
* 31-60 days with status applied = ghosting candidate
* 61+ days with status applied = status can be reviewed or automatically changed to ghosted, if explicitly approved

### Job Scraper Future Updates

1. Add extra connectors for ATS platforms used by more than 5 target companies.

   * This can wait.
   * Use the ATS Coverage Audit to decide connector priority.
   * Do not build one-off connectors unless the company is high value.

2. Fix broken Workday links.

   * This can wait.
   * Review Workday source URL handling.
   * Preserve normalized job shape and `source_ats = workday`.

---

## Current Roadmap

### Step 17: Application Tracker

Status:

* Complete

Completed:

* 17A: Database foundation
* 17B: Reusable module
* 17C: Manual add-application script
* 17D: Manual status-update script
* 17E: Application tracker summary reporting
* 17F: Excel export integration
* 17G: Weekly tracker email script
* 17H: Power BI visuals
* 17I: Finishing touches

### Step 18: GitHub + Portfolio Polish

Status:

* Complete

Completed:

* `.gitignore` cleanup
* README polish
* Application Tracker screenshot added to README
* demo data cleanup confirmation
* Excel export confirmation
* Power BI refresh confirmation
* stale reference checks
* pytest validation
* Ruff validation
* final Git cleanliness check

### Next Planned Work

No urgent next step is required.

Only future updates:

* Application Dashboard: auto status updates based on days since applying
* Job Scraper: extra ATS connectors for ATS platforms with more than 5 target companies
* Job Scraper: broken Workday link fixes

---

## Testing Commands

Useful commands:

```
python scripts/collect_greenhouse_jobs.py --preview
python scripts/export_to_excel.py
python scripts/send_weekly_application_tracker_email.py --preview
```

Windows PowerShell:

```
$env:PYTHONPATH="src"
python scripts/collect_greenhouse_jobs.py --preview
python scripts/export_to_excel.py
python scripts/send_weekly_application_tracker_email.py --preview
```

Daily automation test:

```
.\run_careersignal_daily.bat
```

Real daily send mode:

```
python scripts/collect_greenhouse_jobs.py --send
python scripts/export_to_excel.py
```

Weekly Application Tracker email preview:

```
python scripts/send_weekly_application_tracker_email.py --preview
```

Weekly Application Tracker email send:

```
python scripts/send_weekly_application_tracker_email.py --send
```

Weekly Application Tracker manual batch file:

```
.\run_weekly_application_tracker_email.bat
```

Application Tracker initializer:

```
python scripts/init_application_tracker.py
```

Application Tracker add-script help:

```
python scripts/add_application.py --help
```

Application Tracker status-update help:

```
python scripts/update_application_status.py --help
```

Application Tracker reporting:

```
python scripts/report_applications.py
```

Application Tracker manual test insert:

```
python scripts/add_application.py --company "TEST COMPANY DELETE ME" --title "Fake Test Application" --date-applied "2026-06-01" --url "https://example.com/test-job" --source "manual test" --notes "Delete this after test"
```

Application Tracker manual status-update test:

```
python scripts/update_application_status.py --id 4 --status interview --notes "Moved to interview during test" --date "2026-06-10"
```

Replace 4 with the actual `application_id` from the test insert.

Application Tracker PowerShell-safe confirmation query:

```
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
```

Application Tracker PowerShell-safe cleanup query:

```
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
```

Excel export test:

```
python scripts/export_to_excel.py
```

Excel export sheet confirmation:

```
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

print("All Application Tracker sheets exist.")
'@ | python -
```

Temporary demo data cleanup command:

```
@'
import sqlite3

conn = sqlite3.connect("data/careersignal.db")

conn.execute(
    "DELETE FROM applications WHERE source = ?",
    ("demo data",)
)

conn.commit()
conn.close()

print("Deleted temporary demo application rows.")
'@ | python -
```

Temporary demo data cleanup confirmation:

```
@'
import sqlite3

conn = sqlite3.connect("data/careersignal.db")
conn.row_factory = sqlite3.Row

rows = conn.execute(
    "SELECT * FROM applications WHERE source = ?",
    ("demo data",)
).fetchall()

print(f"Remaining demo rows: {len(rows)}")

conn.close()
'@ | python -
```

Expected cleanup result:

```
Remaining demo rows: 0
```

Project validation:

```
pytest tests
ruff check src scripts tests
git status
```

---

## Required Checks for Future Coding Steps

For every future coding step, include:

1. Files to create/edit
2. Exact code
3. Commands to test
4. Grep/search checks for old names or broken imports
5. Git commit guidance

Important PowerShell note:

Do not use `Select-String` with the `-Recurse` parameter because this has caused problems on the user's machine.

Use this pattern instead:

```
Get-ChildItem -Recurse -File | Select-String "search text"
```

Always include checks for:

```
Get-ChildItem -Recurse -File | Select-String "data/jobs.db"
Get-ChildItem -Recurse -File | Select-String "create_tables"
Get-ChildItem -Recurse -File | Select-String "insert_normalized_jobs"
Get-ChildItem -Recurse -File | Select-String "fetch_all_jobs"
```

Also check official function names when relevant:

```
Get-ChildItem -Recurse -File | Select-String "build_and_send_daily_report"
Get-ChildItem -Recurse -File | Select-String "score_job"
Get-ChildItem -Recurse -File | Select-String "initialize_database"
Get-ChildItem -Recurse -File | Select-String "insert_or_update_jobs"
Get-ChildItem -Recurse -File | Select-String "get_jobs_first_seen_in_last_24_hours"
```

Application Tracker checks when relevant:

```
Get-ChildItem -Recurse -File | Select-String "applications"
Get-ChildItem -Recurse -File | Select-String "application_id"
Get-ChildItem -Recurse -File | Select-String "application_tracker"
Get-ChildItem -Recurse -File | Select-String "data/jobs.db"
```

Important:

The module/file names still use `application_tracker`, but the actual database table is `applications`.

Acceptable references:

* `src/careersignal/application_tracker.py`
* `src/careersignal/application_tracker_db.py`
* `scripts/init_application_tracker.py`
* `scripts/add_application.py`
* `scripts/update_application_status.py`
* `scripts/report_applications.py`
* `scripts/send_weekly_application_tracker_email.py`
* `from careersignal.application_tracker import fetch_applications`

Stale or suspicious references:

* `application_tracker` table
* `SELECT * FROM application_tracker`
* `INSERT INTO application_tracker`
* `UPDATE application_tracker`
* `DELETE FROM application_tracker`

Bad old table SQL checks:

```
Get-ChildItem -Recurse -File | Select-String "SELECT \* FROM application_tracker"
Get-ChildItem -Recurse -File | Select-String "INSERT INTO application_tracker"
Get-ChildItem -Recurse -File | Select-String "UPDATE application_tracker"
Get-ChildItem -Recurse -File | Select-String "DELETE FROM application_tracker"
```

Expected result for bad old table SQL checks:

* No results

Weekly email checks:

```
Get-Item .\scripts\send_weekly_application_tracker_email.py
python scripts/send_weekly_application_tracker_email.py --preview
```

Daily email preservation check:

```
python scripts/collect_greenhouse_jobs.py --preview
```

Expected result:

* Daily preview still works.
* Weekly preview still works.
* Weekly email remains separate from daily job alert email.

Power BI / Excel export checks:

```
python scripts/export_to_excel.py

@'
from openpyxl import load_workbook

workbook = load_workbook("exports/careersignal_export.xlsx", read_only=True)

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

print("All Application Tracker sheets exist.")
'@ | python -
```

---

## Git Guidance

After project-state updates:

```
git add docs/CareerSignal_Project_State.md
git commit -m "Update CareerSignal project state"
git push
```

After README updates:

```
git add README.md
git commit -m "Update README for application tracker"
git push
```

After `.gitignore` updates:

```
git add .gitignore
git commit -m "Update gitignore for local cache files"
git push
```

After final GitHub polish:

```
git add README.md docs/CareerSignal_Project_State.md .gitignore
git commit -m "Polish CareerSignal for GitHub"
git push
```

Avoid committing:

* `.env`
* `.venv/`
* `logs/`
* `data/careersignal.db`
* `exports/careersignal_export.xlsx`
* temporary test files
* temporary backup `.pbix` files
* email passwords
* SMTP secrets

Before committing, always run:

```
git status
git diff --cached
```

Important:

* `.pbix` files and screenshots are binary, so `git diff` will not show meaningful line-by-line changes for them.
* `git diff --cached` should still show text changes for scripts, README, and project state files.

If updating only the project state file, prefer:

```
git add docs/CareerSignal_Project_State.md
git diff --cached
git commit -m "Update CareerSignal project state"
git push
```

---

## Important Reminder for Future ChatGPT Help

Before giving code:

1. Read this file.
2. Do not recreate existing files.
3. Do not rename official functions.
4. Do not change `data/careersignal.db`.
5. Do not use `data/jobs.db`.
6. Do not use old function names.
7. Explain dependencies before rewriting core files.
8. Keep new work compatible with the existing pipeline.
9. Preserve Greenhouse and Workday support.
10. Preserve email, Excel, Power BI, logging, and scoring behavior unless asked to change them.
11. Preserve preview mode and send mode.
12. Keep `.env` and secrets out of GitHub.
13. Keep the response beginner-friendly and step-by-step.
14. During Application Tracker work, do not modify daily job alert behavior unless explicitly approved.
15. During Application Tracker work, keep steps small and separate.
16. During Application Tracker work, use the actual table name `applications`.
17. During Application Tracker work, use the actual primary key `application_id`.
18. During Application Tracker work, keep runnable scripts in `scripts/`.
19. During Application Tracker work, keep reusable logic in `src/careersignal/`.
20. Do not use `Select-String -Recurse` in PowerShell instructions.
21. Use `Get-ChildItem -Recurse -File | Select-String "pattern"` instead.
22. Do not create a separate Application Tracker workbook unless explicitly approved.
23. Do not change the Power BI source path unless explicitly working on that issue.
24. Do not add Application Tracker stats to the daily email unless explicitly approved.
25. Keep the weekly Application Tracker email separate from the daily job alert email.
26. Do not modify Excel export unless explicitly working on Excel export or reporting/dashboard output.
27. Do not modify Power BI unless explicitly working on Power BI or dashboard polish.
28. Treat demo data as temporary unless intentionally keeping it for screenshots.
29. Before GitHub polish, confirm demo companies are cleaned out or clearly separated from real/demo portfolio outputs.
30. Do not add future roadmap items unless the user explicitly approves them.

---

## Current Known Truths for Application Tracker

Database:

* `data/careersignal.db`

Table:

* `applications`

Primary key:

* `application_id`

Database setup file:

* `src/careersignal/application_tracker_db.py`

Reusable logic file:

* `src/careersignal/application_tracker.py`

Initializer script:

* `scripts/init_application_tracker.py`

Manual add script:

* `scripts/add_application.py`

Manual status-update script:

* `scripts/update_application_status.py`

Summary reporting script:

* `scripts/report_applications.py`

Weekly email script:

* `scripts/send_weekly_application_tracker_email.py`

Weekly email batch file:

* `run_weekly_application_tracker_email.bat`

Excel export script:

* `scripts/export_to_excel.py`

Excel export workbook:

* `exports/careersignal_export.xlsx`

Power BI file:

* `reports/careersignal_dashboard.pbix`

Application Tracker screenshot:

* `docs/screenshots/application_tracker_dashboard.png`

Application Tracker Excel sheets:

* Applications
* Application Summary
* Company Application Summary
* Application Aging

Official reusable functions:

* get_current_timestamp
* validate_application_status
* add_application
* update_application_status
* update_application_notes
* update_application_response_dates
* fetch_application_by_id
* fetch_applications

Current aging labels for reporting/export:

* active / normal waiting period
* rejection danger zone
* ghosting candidate
* ghosted
* responded / closed
* missing or invalid application date

Current project status:

* Resume-ready
* GitHub-ready
* Portfolio-ready
* No urgent next coding step required
