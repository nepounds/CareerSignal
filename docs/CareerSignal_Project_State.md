# CareerSignal Project State

## Current Project Status

CareerSignal currently has a working end-to-end job alert pipeline, a completed manual Application Tracker layer, Excel export integration, a Power BI dashboard, weekly Application Tracker email support, and Windows Task Scheduler automation support.

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
17. Application Tracker completed, cleaned up, validated, and ready for portfolio use

* 17A. Application Tracker database foundation completed
* 17B. Application Tracker reusable module completed
* 17C. Manual add-application script completed
* 17D. Manual status-update script completed
* 17E. Application Tracker summary reporting completed
* 17F. Application Tracker Excel export integration completed
* 17G. Weekly Application Tracker email script completed
* 17H. Power BI Application Tracker visuals completed
* 17I. Application Tracker finishing touches completed

Current next step:

* Step 18: GitHub + Portfolio Polish

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

Application Tracker is a manual tracking layer that sits beside the automated job collection pipeline.

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
→ optional weekly scheduled email
```

The Application Tracker is now complete for resume-ready v1.

Step 17I cleaned up temporary demo Application Tracker data, refreshed the Excel export, confirmed Application Tracker sheets, preserved the Power BI source path, validated weekly email preview behavior, preserved the daily email flow, and confirmed the command-line application entry workflow is good enough for v1.

---

## Existing Project Structure

Preserve this structure.

```
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
│       ├── powerbi_overview_dashboard.png
│       └── application_tracker_dashboard.png
├── exports/
│   └── careersignal_export.xlsx
├── logs/
│   ├── careersignal.log
│   ├── scheduled_task.log
│   └── weekly_application_tracker_email.log if weekly scheduling was created
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
│   └── other preview/test scripts created during Workday, scoring, tracker, or audit steps
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
├── run_weekly_application_tracker_email.bat if weekly scheduling was created
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

Some generated files may be ignored by Git, including:

* .env
* logs/
* generated database files
* generated exports
* local Power BI cache files

---

## Important Project Rules

For CareerSignal coding help, always treat this file as the source of truth before suggesting code changes.

Do not invent new function names if an official name already exists.

Before rewriting a core file, explain which other files depend on it.

Keep naming consistent with the official function names in this project state file.

Do not add compatibility wrappers or aliases unless explicitly approved.

Prefer updating dependent scripts to use the current official function names.

Preserve the existing project structure:

* scripts/ contains runnable scripts
* src/careersignal/ contains reusable modules
* data/careersignal.db is the SQLite database
* config/company_config.csv is the company config
* exports/careersignal_export.xlsx is the Excel export used by Power BI
* reports/careersignal_dashboard.pbix is the Power BI dashboard

Do not use:

* data/jobs.db

Do not rename:

* scripts/collect_greenhouse_jobs.py

Even though the script name says Greenhouse, after Workday integration it functions as the main collector runner.

Do not rename this script unless intentionally doing a cleanup/refactor step.

Do not modify the daily job alert email during Application Tracker steps unless explicitly approved.

Do not modify the weekly Application Tracker email unless explicitly working on weekly email behavior.

Do not create a separate Application Tracker workbook unless explicitly approved.

Do not change the Power BI source path unless there is a confirmed source problem and the fix is approved.

Do not use Select-String -Recurse in PowerShell instructions.

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
.env.example
.gitignore
run_careersignal_daily.bat
run_weekly_application_tracker_email.bat if weekly scheduling was created
config/company_config.csv
config/company_ats_audit.csv
config/match_rules.json or config/match_rules.csv if created
data/careersignal.db
docs/CareerSignal_Project_State.md
docs/filtering_strategy.md
docs/screenshots/powerbi_overview_dashboard.png
docs/screenshots/application_tracker_dashboard.png
exports/careersignal_export.xlsx
logs/careersignal.log
logs/scheduled_task.log
logs/weekly_application_tracker_email.log if weekly scheduling was created
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
```

If a future step needs to modify one of these files, explain:

1. Why the file needs to change
2. What depends on it
3. How the change preserves existing behavior

---

## Core Pipeline Status

### SQLite Database

Official database path:

* data/careersignal.db

Do not use:

* data/jobs.db

The main database already supports:

* job storage
* new job detection
* pipeline reporting
* Application Tracker records

Application Tracker also uses:

* data/careersignal.db

Application Tracker table:

* applications

Application Tracker primary key:

* application_id

---

### Greenhouse Collector

Likely file:

* src/careersignal/collectors/greenhouse.py

Existing runner command:

```
python scripts/collect_greenhouse_jobs.py --preview
```

Send real email:

```
python scripts/collect_greenhouse_jobs.py --send
```

Important:

The script name still says collect_greenhouse_jobs.py, but after Workday integration it functions as the main collector runner.

Do not rename this script unless intentionally doing a cleanup/refactor step.

---

### Workday Collector

Likely file:

* src/careersignal/collectors/workday.py

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
* This can wait unless Step 18 polish identifies it as urgent.

---

### Match Scoring

Step 15 is complete and used the Step 14 filtering strategy.

Important distinction:

* Step 14 = decide what CareerSignal should care about
* Step 15 = assign scoring weights and implement/refine scoring logic

Match scoring should preserve:

* score_job(job)

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

Daily email reporting should continue to support preview/test mode and send mode.

Daily job alert email is separate from the weekly Application Tracker email.

Daily job alert email should not be modified during Application Tracker steps unless explicitly approved.

Weekly Application Tracker email script exists:

* scripts/send_weekly_application_tracker_email.py

The weekly Application Tracker email uses:

* preview mode
* send mode
* the applications table
* data/careersignal.db
* the existing .env/email credential pattern where possible

The weekly email does not modify:

* daily job alert behavior
* Excel export
* Power BI
* database schema
* Application Tracker statuses

Weekly Application Tracker email status:

* Script exists.
* Preview mode works if validation passes.
* Send mode is available only through explicit --send.
* Weekly scheduling may exist if run_weekly_application_tracker_email.bat was created and Task Scheduler was configured.
* Preferred weekly schedule is Friday at 4 PM.

Important:

* Do not add Application Tracker stats to the daily job alert email unless explicitly approved.
* Keep the weekly Application Tracker email separate from the daily job alert email.

---

### Logging

Likely file:

* src/careersignal/logging_config.py

Logs should go to:

* logs/careersignal.log

Scheduled daily task logs should go to:

* logs/scheduled_task.log

Weekly Application Tracker scheduled task logs should go to:

* logs/weekly_application_tracker_email.log

A failed company source should not crash the whole run.

Failed sources should be tracked and included in the daily email report where possible.

---

### Excel Export

File:

* scripts/export_to_excel.py

Export output:

* exports/careersignal_export.xlsx

The Excel export feeds the Power BI dashboard.

Do not break this output path without updating the README and Power BI notes.

Step 17F added Application Tracker sheets to the existing workbook.

Step 17I confirmed the Application Tracker sheets still exist after demo data cleanup and export refresh.

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

* exports/careersignal_export.xlsx

The Power BI source path remains unchanged.

No separate tracker workbook should exist unless intentionally approved later.

Application Tracker export behavior:

Applications sheet:

* Full row-level application tracker data from the applications table.
* Expected fields include:

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

Step 17H changed aging labels in export_to_excel.py from:

* ghosting danger zone
* ghosted candidate / should be reviewed

To:

* ghosting candidate
* ghosted

This was done for clearer reporting and better Power BI dashboard presentation.

Step 17I cleanup:

* Temporary demo Application Tracker rows were removed.
* Excel export was rerun after cleanup.
* Application Tracker workbook sheets were confirmed.
* Application Tracker is clean and ready for Step 18 portfolio polish.

---

### Power BI

Power BI report:

* reports/careersignal_dashboard.pbix

Power BI data source:

* exports/careersignal_export.xlsx

After generating a fresh Excel export, refresh Power BI manually:

* Home > Refresh

Current dashboard exists and should not be treated as unstarted.

Step 17H added a dedicated Application Tracker page inside the existing Power BI file.

Step 17I confirmed the Application Tracker dashboard should be refreshed after cleanup using the same Excel source path.

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
* KPI cards use:

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
* Displayed column names:

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
* The Power BI source path remains exports/careersignal_export.xlsx.
* Do not change the Power BI source path unless intentionally working on that issue.

Screenshot:

* docs/screenshots/application_tracker_dashboard.png

Step 17I note:

* Demo Application Tracker data has been cleaned out.
* If the screenshot still shows demo data, replace the screenshot during Step 18 only if needed for portfolio polish.
* If using sample/demo data for portfolio screenshots, clearly separate it from the real local database.

---

### Daily Automation

Step 16 is complete if the project has:

* run_careersignal_daily.bat

and Windows Task Scheduler is configured to run it daily.

The daily automation should run:

```
python scripts\collect_greenhouse_jobs.py --send
python scripts\export_to_excel.py
```

The batch file should:

1. Change into the CareerSignal project folder
2. Activate the virtual environment if needed
3. Set PYTHONPATH=src
4. Run the collector in send mode
5. Run the Excel export
6. Write useful output to logs/scheduled_task.log

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

* Do not close the .bat/cmd window when it appears during the scheduled run.
* Do not run Checkpoint VPN or NordVPN during the scheduled job if they block SMTP traffic.
* If email does not send, check whether VPN or network restrictions blocked smtp.gmail.com on port 587.

---

### Weekly Application Tracker Automation

Weekly Application Tracker email automation is optional but supported.

Weekly email script:

* scripts/send_weekly_application_tracker_email.py

Optional weekly batch file:

* run_weekly_application_tracker_email.bat

Preferred schedule:

* Friday at 4 PM

Recommended weekly batch behavior:

1. Change into the CareerSignal project folder

2. Set PYTHONPATH=src

3. Run:

   ```
   python scripts\send_weekly_application_tracker_email.py --send
   ```

4. Write output to:

   ```
   logs\weekly_application_tracker_email.log
   ```

The weekly task must remain separate from the daily task.

The weekly task should not edit or call:

* run_careersignal_daily.bat

The daily task should remain:

* Daily job collection
* Daily email alert
* Excel export

The weekly task should remain:

* Weekly Application Tracker summary email only

Manual weekly test command if the batch file exists:

```
.\run_weekly_application_tracker_email.bat
```

Weekly log check if the batch file exists:

```
Get-Content .\logs\weekly_application_tracker_email.log -Tail 100
```

Important:

* Do not schedule the weekly email until preview mode works.
* Prefer testing --send manually once before scheduling.
* Do not include secrets in the batch file.
* The batch file should rely on existing .env/email configuration.

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
10. Add extra connectors for ATS platforms used by more than 5 target companies. This can wait.

---

## Step 17 Application Tracker Status

Step 17 is complete.

Goal:

Add a manual application tracking system to CareerSignal that records applications submitted by the user, tracks response outcomes, calculates ghosting/rejection danger zones, summarizes application performance overall and by company, exports Application Tracker sheets to Excel, sends a separate weekly Application Tracker email, and visualizes the tracker in Power BI.

Final Step 17 status:

* Complete
* Cleaned up
* Demo Application Tracker rows removed
* Excel export refreshed
* Application Tracker sheets confirmed
* Weekly email preview/send workflow available
* Optional weekly scheduling supported
* Daily job alert behavior preserved
* Power BI source path preserved
* Command-line application entry confirmed as good enough for resume-ready v1

Application Tracker remains separate from the automated job collector.

Do not modify the daily job alert email unless explicitly approved.

---

### Application Tracker Database Naming

Official database:

* data/careersignal.db

Official Application Tracker table:

* applications

Official Application Tracker primary key:

* application_id

Important:

Earlier planning notes may have referred to the table as application_tracker, but the actual implemented table name is applications.

Use applications going forward unless a future intentional migration renames it.

---

### Step 17A: Application Tracker Database Foundation

Status:

* Complete

Purpose:

Create the database foundation for manually tracking job applications.

Expected database:

* data/careersignal.db

Implemented table:

* applications

Implemented primary key:

* application_id

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

* scripts/init_application_tracker.py

Reusable database setup file:

* src/careersignal/application_tracker_db.py

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

* src/careersignal/application_tracker.py

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

* add_application(...) returns the inserted application_id as an int.
* fetch_application_by_id(...) returns one application record as a dict or None.
* fetch_applications(...) returns a list of application record dicts.

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

* scripts/add_application.py

Expected behavior:

* User runs a command with company, title, date applied, URL/source/notes if available.
* Script validates required input.
* Script calls add_application(...) from src/careersignal/application_tracker.py.
* Script inserts the application into the applications table.
* Script prints a clean confirmation, including the returned application_id.

Example command:

```
python scripts/add_application.py --company "RSM" --title "Audit Associate" --date-applied "2026-06-01" --url "https://example.com/job" --source "company website" --notes "Applied through company portal"
```

Minimal command:

```
python scripts/add_application.py --company "RSM" --title "Audit Associate" --date-applied "2026-06-01"
```

Test insert command:

```
python scripts/add_application.py --company "TEST COMPANY DELETE ME" --title "Fake Test Application" --date-applied "2026-06-01" --url "https://example.com/test-job" --source "manual test" --notes "Delete this after test"
```

PowerShell-safe confirmation query:

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

PowerShell-safe cleanup query:

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

* scripts/update_application_status.py

Expected behavior:

* User provides application_id and new status.
* Script validates status using validate_application_status(...).
* Script calls update_application_status(...) from src/careersignal/application_tracker.py.
* Script updates the matching row in the applications table.
* Script prints a clean confirmation showing application_id, company_name, job_title, old status, and new status.

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

* The script uses existing reusable functions from src/careersignal/application_tracker.py.
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

* scripts/report_applications.py

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

* applications table
* application_id primary key
* data/careersignal.db database
* official functions from src/careersignal/application_tracker.py where practical

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

* scripts/export_to_excel.py

Existing export output preserved:

* exports/careersignal_export.xlsx

Required sheets added:

* Applications
* Application Summary
* Company Application Summary
* Application Aging

Expected behavior:

* Running python scripts/export_to_excel.py still works.
* Existing job export sheets remain intact.
* Application Tracker sheets are added to the same workbook.
* Power BI source path remains unchanged.
* No separate tracker workbook is created.
* No database schema change is made.
* No statuses are automatically changed.
* No daily email behavior is changed.

Application Tracker sheet behavior:

Applications sheet:

* Full row-level application tracker data from the applications table.

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

* data/careersignal.db
* applications table
* application_id primary key
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

PowerShell-safe sheet confirmation command:

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

---

### Step 17G: Weekly Application Tracker Email

Status:

* Complete

Goal:

Add a separate weekly Application Tracker email after reporting and Excel export work.

Implemented file:

* scripts/send_weekly_application_tracker_email.py

Preferred schedule:

* Friday at 4 PM

Important:

The weekly Application Tracker email remains separate from the daily job alert email.

Application Tracker stats were not added to the daily job alert email.

The existing daily email module was not modified during Step 17G.

The existing daily collector script was not modified during Step 17G.

The Excel export was not modified during Step 17G.

Power BI was not modified during Step 17G.

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

Safety behavior:

* Script previews by default if no send flag is provided.
* Script does not send unless --send is explicitly provided.
* Script prints generated email content in preview mode.
* Script uses the existing Application Tracker table: applications.
* Script uses the existing Application Tracker primary key: application_id.
* Script uses the existing database path through the reusable Application Tracker module.
* Script does not change any database schema.
* Script does not mutate application statuses.
* Script does not schedule itself automatically.

Email configuration behavior:

* The script uses environment variables and .env values.
* It supports common email config variable names so the existing email credential pattern can be reused without editing the daily email module.

Supported email config variable names include:

* SMTP_HOST or SMTP_SERVER or EMAIL_HOST
* SMTP_PORT or EMAIL_PORT
* SMTP_USERNAME or EMAIL_USERNAME or EMAIL_SENDER or EMAIL_FROM
* SMTP_PASSWORD or EMAIL_PASSWORD or EMAIL_APP_PASSWORD
* EMAIL_FROM or EMAIL_SENDER
* EMAIL_TO or EMAIL_RECIPIENT or RECIPIENT_EMAIL

Step 17G preserved:

* data/careersignal.db
* applications table
* application_id primary key
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

* reports/careersignal_dashboard.pbix

Supporting screenshot:

* docs/screenshots/application_tracker_dashboard.png

Updated file due to aging label change:

* scripts/export_to_excel.py

Power BI source preserved:

* exports/careersignal_export.xlsx

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
* total applications must be Whole Number and aggregated as Sum.
* Status Mix uses Applications.
* Applications Over Time uses Applications and a cumulative DAX measure.
* Aging Watchlist uses Application Aging only.
* The new page was added to the existing reports/careersignal_dashboard.pbix file.
* Existing job alert/dashboard visuals were intended to remain intact.
* Power BI must be manually refreshed after running python scripts/export_to_excel.py.

Step 17H did not include:

* weekly email scheduling
* automatic database status updates
* new ATS connectors
* Workday link fixes
* job scraper dashboard cleanup
* database schema changes

Known Step 17H cleanup item was resolved in Step 17I:

* Temporary demo Application Tracker rows were cleaned out.
* Excel export was refreshed.
* Power BI should be refreshed after the cleaned export.
* Application Tracker is clean for portfolio handoff.

---

### Step 17I: Application Tracker Finishing Touches

Status:

* Complete

Goal:

Finish the Application Tracker enough to hand it off cleanly into Step 18 GitHub + Portfolio Polish.

Completed finishing items:

1. Demo Application Tracker rows were inspected.
2. Demo Application Tracker rows were removed safely.
3. Confirmation query showed zero demo rows remaining.
4. Excel export was rerun after cleanup.
5. Application Tracker sheets were confirmed in exports/careersignal_export.xlsx.
6. Power BI refresh steps were documented.
7. Weekly Application Tracker email preview command was confirmed.
8. Weekly Application Tracker email send command was preserved as explicit send-only behavior.
9. Optional weekly scheduling approach was documented for Friday at 4 PM.
10. Weekly email scheduling was kept separate from the existing daily run_careersignal_daily.bat.
11. Existing command-line application entry workflow was confirmed as good enough for resume-ready v1.
12. Future improvements were documented instead of built.
13. Final validation commands were documented.
14. Grep/search checks were documented.
15. Git commit guidance was provided.

Application Tracker cleanup command used:

```
@'
import sqlite3

conn = sqlite3.connect("data/careersignal.db")

deleted = conn.execute(
    "DELETE FROM applications WHERE source = ?",
    ("demo data",)
).rowcount

conn.commit()
conn.close()

print(f"Deleted demo rows: {deleted}")
'@ | python -
```

Demo cleanup confirmation command:

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

for row in rows:
    print(dict(row))

conn.close()
'@ | python -
```

Expected cleanup result:

```
Remaining demo rows: 0
```

Excel export refresh command:

```
python scripts/export_to_excel.py
```

Application Tracker sheet confirmation command:

```
@'
from openpyxl import load_workbook

workbook = load_workbook("exports/careersignal_export.xlsx", read_only=True)

print("Workbook sheets:")
for sheet_name in workbook.sheetnames:
    print(f"- {sheet_name}")

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

Weekly Application Tracker preview command:

```
python scripts/send_weekly_application_tracker_email.py --preview
```

Weekly Application Tracker send command:

```
python scripts/send_weekly_application_tracker_email.py --send
```

Daily email preservation command:

```
python scripts/collect_greenhouse_jobs.py --preview
```

Optional weekly batch file if scheduling was created:

* run_weekly_application_tracker_email.bat

Recommended content:

```
@echo off
cd /d "C:\Users\Nathan and Steph\Documents\CareerSignal"

if not exist logs mkdir logs

set PYTHONPATH=src

echo ========================================== >> logs\weekly_application_tracker_email.log
echo CareerSignal weekly application tracker started at %date% %time% >> logs\weekly_application_tracker_email.log

python scripts\send_weekly_application_tracker_email.py --send >> logs\weekly_application_tracker_email.log 2>&1

echo CareerSignal weekly application tracker finished at %date% %time% >> logs\weekly_application_tracker_email.log
echo. >> logs\weekly_application_tracker_email.log
```

Optional weekly Task Scheduler setup:

* Name: CareerSignal Weekly Application Tracker Email

* Trigger: Weekly, Friday, 4:00 PM

* Action: Start a program

* Program/script:

  ```
  C:\Users\Nathan and Steph\Documents\CareerSignal\run_weekly_application_tracker_email.bat
  ```

* Start in:

  ```
  C:\Users\Nathan and Steph\Documents\CareerSignal
  ```

Important Step 17I preservation notes:

* No database schema changes were made.
* No Application Tracker table rename was made.
* No function aliases or compatibility wrappers were added.
* No Streamlit UI was created.
* No automatic ghosting/status mutation was implemented.
* No separate Application Tracker workbook was created.
* No daily job alert behavior was changed.
* No Power BI source path change was made.
* The weekly email remains separate from the daily email.
* The Application Tracker is complete, cleaned, and ready for Step 18.

---

## Future Updates and Fine-Tuning

### Application Dashboard Future Updates

Application Tracker is complete for resume-ready v1.

Future improvements are optional.

1. Cleaner add-application workflow

   * Current method is command line:

     ```
     python scripts/add_application.py --company "RSM" --title "Audit Associate" --date-applied "2026-06-01"
     ```

   * Future improvement may be a guided CLI workflow or form-style prompt.

   * Keep reusable logic in src/careersignal/.

   * Keep runnable scripts in scripts/.

2. CSV import

   * Future option for bulk importing applications from a spreadsheet.
   * Should use the existing add_application logic or a reusable helper.
   * Should not bypass validation.

3. Optional Streamlit UI

   * Future option for prettier local application entry and dashboard viewing.
   * Not required for resume-ready v1.
   * Do not build unless intentionally starting Step 19.

4. Automatic status updates based on days since applying

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

5. Screenshot polish

   * If Application Tracker screenshots still show demo data, update screenshots during Step 18.
   * If using demo screenshots for portfolio presentation, clearly separate local demo data from real project data.

---

### Job Scraper Future Updates

1. Fix the existing job scraper dashboard if it is showing demo companies.

   * This should be cleaned up during Step 18 GitHub + Portfolio Polish.
   * Confirm job scraper visuals use job export tables, not Application Tracker demo data.

2. Add extra connectors for ATS platforms used by more than 5 companies.

   * This can wait.
   * Use the ATS Coverage Audit to decide connector priority.
   * Do not build one-off connectors unless the company is high value.

3. Fix broken Workday links.

   * This can wait.
   * Review Workday source URL handling.
   * Preserve normalized job shape and source_ats = workday.

---

## Current Roadmap

### Step 17: Application Tracker

Status:

* Complete
* Cleaned up
* Portfolio-ready for v1

Completed:

* 17A: Database foundation
* 17B: Reusable module
* 17C: Manual add-application script
* 17D: Manual status-update script
* 17E: Application tracker summary reporting
* 17F: Excel export integration
* 17G: Weekly tracker email script
* 17H: Power BI visuals
* 17I: Finishing touches, cleanup, validation, and optional weekly scheduling setup

Application Tracker v1 is resume-ready.

---

### Step 18: GitHub + Portfolio Polish

Status:

* Current next major phase

Purpose:

Clean README, screenshots, sample outputs, final testing, resume bullets, and portfolio presentation.

Step 18 should update:

* README.md
* docs/CareerSignal_Project_State.md
* docs/screenshots/ if screenshots are added or replaced

Step 18 should not:

* rename official functions
* change database paths
* recreate existing files
* break existing behavior
* change the Power BI source path without documenting it
* expose secrets
* rebuild the Application Tracker
* create a Streamlit UI unless Step 19 is intentionally started
* add automatic status mutation unless explicitly approved

Step 18 validation should confirm:

* preview run works
* send run works
* daily email arrives
* daily email only includes jobs first seen in the past 24 hours
* match scores show correctly
* failed sources show correctly
* Excel export updates
* Application Tracker sheets exist in the Excel export
* weekly Application Tracker email previews correctly
* weekly Application Tracker email sends correctly if intentionally tested
* weekly Application Tracker schedule works if configured
* Power BI refresh works from exports/careersignal_export.xlsx
* Application Tracker Power BI page works
* screenshots exist and are clean
* logs update
* no data/jobs.db references
* no stale application_tracker table SQL
* no old function names
* no secrets staged for Git

Step 18 known action items:

* Polish README for portfolio/resume presentation.
* Add screenshots and sample outputs.
* Confirm Application Tracker screenshots are clean.
* Confirm the Power BI data source pulls from exports/careersignal_export.xlsx.
* Confirm the job scraper dashboard is not accidentally showing old demo companies.
* Check and confirm that match scoring appears correctly in sent emails.
* Make sure sent emails include only jobs first seen in the past 24 hours.
* Circle back to Step 13 Workday URL issues if needed.
* Add the rest of the confirmed Greenhouse companies if ready.
* Add or update notes for the Application Tracker, Excel export sheets, weekly tracker email, and Power BI dashboard.
* Decide whether to mention future enhancements:

  * automatic ghosting status update
  * extra ATS connectors
  * Streamlit UI
  * CSV import
  * cleaner add-application workflow

---

### Step 19: Optional Streamlit UI

Status:

* Optional / later

Only if a prettier local interface is wanted later.

Possible purpose:

* Add applications through a form
* Update statuses through a form
* View tracker summaries locally
* Avoid doing all manual application entry through PowerShell

Nice-to-have, not required.

Do not start Step 19 during Step 18 unless explicitly approved.

---

## Must-Do vs Nice-to-Have

Current must-do path:

* Step 18: GitHub + Portfolio Polish

Application Tracker status:

* Complete for resume-ready v1
* Cleaned up
* Validated
* Ready for portfolio polish

Application Tracker future improvements:

* Cleaner add-application workflow
* CSV import
* Optional Streamlit UI
* Optional automatic status update script

Job Scraper future updates:

* Fix dashboard if it is showing demo companies
* Optional later: add extra ATS connectors for ATS platforms with more than 5 target companies
* Optional later: fix broken Workday links

Nice-to-have:

* Step 19: Optional Streamlit UI
* Automatic status update script
* Additional ATS connectors
* Cleaner application-entry workflow
* More polished Power BI styling

---

## Testing Commands

Useful commands:

```
PYTHONPATH=src python scripts/test_config_loader.py
PYTHONPATH=src python scripts/test_database.py
PYTHONPATH=src python scripts/test_match_scoring.py
PYTHONPATH=src python scripts/test_email_report.py
python scripts/collect_greenhouse_jobs.py --preview
python scripts/export_to_excel.py
python scripts/send_weekly_application_tracker_email.py --preview
```

Windows PowerShell:

```
$env:PYTHONPATH="src"
python scripts/test_config_loader.py
python scripts/test_database.py
python scripts/test_match_scoring.py
python scripts/test_email_report.py
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

Weekly Application Tracker batch test if configured:

```
.\run_weekly_application_tracker_email.bat
```

Weekly Application Tracker log check if configured:

```
Get-Content .\logs\weekly_application_tracker_email.log -Tail 100
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
python scripts/update_application_status.py --id 4 --status interview --notes "Moved to interview during Step 17D test" --date "2026-06-10"
```

Replace 4 with the actual application_id from the test insert.

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

deleted = conn.execute(
    "DELETE FROM applications WHERE source = ?",
    ("demo data",)
).rowcount

conn.commit()
conn.close()

print(f"Deleted demo rows: {deleted}")
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

Compile check:

```
python -m compileall src scripts
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

Do not use Select-String with the -Recurse parameter because this has caused problems on the user's machine.

Use this pattern instead:

```
Get-ChildItem -Recurse -File | Select-String "pattern"
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

The module/file names still use application_tracker, but the actual database table is applications.

Acceptable references:

* src/careersignal/application_tracker.py
* src/careersignal/application_tracker_db.py
* scripts/init_application_tracker.py
* scripts/add_application.py
* scripts/update_application_status.py
* scripts/report_applications.py
* scripts/send_weekly_application_tracker_email.py
* from careersignal.application_tracker import fetch_applications

Stale or suspicious references:

* application_tracker table
* SELECT * FROM application_tracker
* INSERT INTO application_tracker
* UPDATE application_tracker
* DELETE FROM application_tracker

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
git commit -m "Update CareerSignal README"
git push
```

After Application Tracker feature steps, use specific commit messages.

Step 17A:

```
git add .
git commit -m "Add application tracker database foundation"
git push
```

Step 17B:

```
git add .
git commit -m "Add application tracker module"
git push
```

Step 17C:

```
git add .
git commit -m "Add application entry script"
git push
```

Step 17D:

```
git add .
git commit -m "Add application status update script"
git push
```

Step 17E:

```
git add .
git commit -m "Add application tracker reporting"
git push
```

Step 17F:

```
git add scripts/export_to_excel.py
git commit -m "Add application tracker sheets to Excel export"
git push
```

Step 17G:

```
git add scripts/send_weekly_application_tracker_email.py
git commit -m "Add weekly application tracker email"
git push
```

Step 17H:

```
git add reports/careersignal_dashboard.pbix scripts/export_to_excel.py docs/screenshots/application_tracker_dashboard.png
git commit -m "Add application tracker Power BI visuals"
git push
```

Step 17I if weekly batch file was created:

```
git add run_weekly_application_tracker_email.bat docs/CareerSignal_Project_State.md
git commit -m "Finish application tracker cleanup and weekly scheduling setup"
git push
```

Step 17I if only project state was updated:

```
git add docs/CareerSignal_Project_State.md
git commit -m "Update CareerSignal project state"
git push
```

Avoid committing:

* .env
* logs/
* data/careersignal.db if intentionally ignored
* exports/careersignal_export.xlsx if intentionally ignored
* temporary test files
* temporary backup .pbix files
* email passwords
* SMTP secrets

Before committing, always run:

```
git status
git diff --cached
```

Important:

* .pbix files and screenshots are binary, so git diff will not show meaningful line-by-line changes for them.
* git diff --cached should still show text changes for scripts/export_to_excel.py and docs/CareerSignal_Project_State.md.

If updating only the project state file, prefer:

```
git add docs/CareerSignal_Project_State.md
git diff --cached
git commit -m "Update CareerSignal project state"
git push
```

If committing the weekly batch file and project state together, prefer:

```
git add run_weekly_application_tracker_email.bat docs/CareerSignal_Project_State.md
git diff --cached
git commit -m "Finish application tracker cleanup and weekly scheduling setup"
git push
```

If Power BI was refreshed and saved during Step 17I, and the .pbix is intentionally tracked:

```
git add reports/careersignal_dashboard.pbix docs/CareerSignal_Project_State.md
git diff --cached
git commit -m "Refresh application tracker dashboard after cleanup"
git push
```

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
14. During Application Tracker work, do not modify daily job alert behavior unless explicitly approved.
15. During Application Tracker work, keep steps small and separate.
16. During Application Tracker work, use the actual table name applications.
17. During Application Tracker work, use the actual primary key application_id.
18. During Application Tracker work, keep runnable scripts in scripts/.
19. During Application Tracker work, keep reusable logic in src/careersignal/.
20. Do not use Select-String -Recurse in PowerShell instructions.
21. Use Get-ChildItem -Recurse -File | Select-String "pattern" instead.
22. Do not create a separate Application Tracker workbook unless explicitly approved.
23. Do not change the Power BI source path unless explicitly working on that issue.
24. Do not add Application Tracker stats to the daily email unless explicitly approved.
25. Keep the weekly Application Tracker email separate from the daily job alert email.
26. Do not schedule or modify weekly Application Tracker email automation unless explicitly working on that issue.
27. Do not modify Excel export unless explicitly working on Excel export or reporting/dashboard output.
28. Do not modify Power BI unless explicitly working on Power BI or dashboard polish.
29. Treat demo data as temporary unless intentionally keeping it for screenshots.
30. Demo Application Tracker data was cleaned during Step 17I.
31. Before GitHub polish, confirm screenshots and sample outputs are clean or intentionally marked as demo.
32. Application Tracker is complete for resume-ready v1 and should not be rebuilt during Step 18.
33. Future Application Tracker improvements should be treated as optional enhancements, not blockers.

---

## Current Known Truths for Application Tracker

Database:

* data/careersignal.db

Table:

* applications

Primary key:

* application_id

Database setup file:

* src/careersignal/application_tracker_db.py

Reusable logic file:

* src/careersignal/application_tracker.py

Initializer script:

* scripts/init_application_tracker.py

Manual add script:

* scripts/add_application.py

Manual status-update script:

* scripts/update_application_status.py

Summary reporting script:

* scripts/report_applications.py

Weekly email script:

* scripts/send_weekly_application_tracker_email.py

Optional weekly batch file:

* run_weekly_application_tracker_email.bat

Excel export script:

* scripts/export_to_excel.py

Excel export workbook:

* exports/careersignal_export.xlsx

Power BI file:

* reports/careersignal_dashboard.pbix

Application Tracker screenshot:

* docs/screenshots/application_tracker_dashboard.png

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

Current Application Tracker status:

* Complete
* Cleaned up
* Validated
* Resume-ready for v1
* Ready for Step 18 GitHub + Portfolio Polish

Current next planned phase:

* Step 18: GitHub + Portfolio Polish
