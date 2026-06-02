# CareerSignal Project State

## Current Project Status

CareerSignal currently has a working end-to-end pipeline.

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
17. Application Tracker started

    * 17A. Application Tracker database foundation completed
    * 17B. Application Tracker reusable module completed

Current step:

```text
17C: Application Tracker manual add-application script
```

The main product loop exists:

```text
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

Application Tracker is a new manual tracking layer that sits beside the automated job collection pipeline.

Application Tracker loop:

```text
manual application entry
→ application_tracker table in data/careersignal.db
→ reusable application_tracker.py module
→ manual add/update scripts
→ summary reporting
→ future Excel export
→ future weekly email
→ future Power BI visuals
```

---

## Existing Project Structure

Preserve this structure.

```text
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
│   ├── collect_greenhouse_jobs.py
│   ├── export_to_excel.py
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
│       ├── application_tracker_db.py, if created in Step 17A
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
```

Some generated files may be ignored by Git, including `.env`, logs, generated database files, generated exports, and local Power BI cache files.

---

## Important Project Rules

For CareerSignal coding help, always treat this file as the source of truth before suggesting code changes.

Do not invent new function names if an official name already exists.

Before rewriting a core file, explain which other files depend on it.

Keep naming consistent with the official function names in this project state file.

Do not add compatibility wrappers or aliases unless explicitly approved.

Prefer updating dependent scripts to use the current official function names.

Preserve the existing project structure:

```text
scripts/ contains runnable scripts
src/careersignal/ contains reusable modules
data/careersignal.db is the SQLite database
config/company_config.csv is the company config
```

Do not use:

```text
data/jobs.db
```

Do not rename:

```text
scripts/collect_greenhouse_jobs.py
```

Even though the script name says Greenhouse, after Workday integration it functions as the main collector runner.

---

## Existing Files That Should Not Be Recreated Blindly

These files already exist or have already been worked on.

Do not recreate them from scratch unless they are missing.

```text
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
scripts/collect_greenhouse_jobs.py
scripts/export_to_excel.py
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
```

If a future step needs to modify one of these files, explain:

1. Why the file needs to change
2. What depends on it
3. How the change preserves existing behavior

---

## Core Pipeline Status

### SQLite Database

Official database path:

```text
data/careersignal.db
```

Do not use:

```text
data/jobs.db
```

The main database already supports job storage, new job detection, and pipeline reporting.

Application Tracker also uses:

```text
data/careersignal.db
```

---

### Greenhouse Collector

Likely file:

```text
src/careersignal/collectors/greenhouse.py
```

Existing runner command:

```bash
python scripts/collect_greenhouse_jobs.py --preview
```

Send real email:

```bash
python scripts/collect_greenhouse_jobs.py --send
```

Important:

The script name still says `collect_greenhouse_jobs.py`, but after Workday integration it may function as the main collector runner. Do not rename this script unless intentionally doing a cleanup/refactor step.

---

### Workday Collector

Likely file:

```text
src/careersignal/collectors/workday.py
```

Workday was split into three parts:

```text
12A: Workday Proof of Concept
12B: Workday Normalization
12C: Integrate Workday Connector
```

All three are considered complete if the current branch has Workday jobs flowing through the same pipeline as Greenhouse.

Workday jobs should use:

```python
"source_ats": "workday"
```

Workday jobs must use the official normalized job shape.

---

### Match Scoring

Step 15 is complete and used the Step 14 filtering strategy.

Important distinction:

```text
Step 14 = decide what CareerSignal should care about
Step 15 = assign scoring weights and implement/refine scoring logic
```

Match scoring should preserve:

```python
score_job(job)
```

Scores should remain from 0 to 100.

Suggested score bands:

```text
80-100: Strong match
60-79: Possible match
40-59: Weak/stretch match
0-39: Low match or likely skip
```

CareerSignal is not accounting-only.

The filtering and scoring strategy supports multiple job-search lanes:

```text
Accounting roles
Finance roles
General analyst roles
Business analyst roles
Operations analyst roles
Compliance analyst roles
Data/reporting analyst roles
Plant supervisor jobs
Operations supervisor jobs
Water/wastewater or public utility-adjacent jobs
Other realistic roles that fit the user's background
```

---

### Email Reporting

Email reporting should continue to support preview/test mode and send mode.

Daily job alert email should not be modified during Application Tracker steps unless explicitly approved.

Application Tracker weekly email should come later, after tracker reporting works.

---

### Logging

Likely file:

```text
src/careersignal/logging_config.py
```

Logs should go to:

```text
logs/careersignal.log
```

Scheduled task logs should go to:

```text
logs/scheduled_task.log
```

A failed company source should not crash the whole run.

Failed sources should be tracked and included in the daily email report where possible.

---

### Excel Export

File:

```text
scripts/export_to_excel.py
```

Export output:

```text
exports/careersignal_export.xlsx
```

The Excel export feeds the Power BI dashboard.

Do not break this output path without updating the README and Power BI notes.

Application Tracker export sheets should come later, after tracker scripts and reporting are stable.

---

### Power BI

Power BI report:

```text
reports/careersignal_dashboard.pbix
```

Power BI data source:

```text
exports/careersignal_export.xlsx
```

After generating a fresh Excel export, refresh Power BI manually:

```text
Home > Refresh
```

Current dashboard exists and should not be treated as unstarted.

Application Tracker visuals should come later.

---

### Daily Automation

Step 16 is complete if the project has:

```text
run_careersignal_daily.bat
```

and Windows Task Scheduler is configured to run it daily.

The daily automation should run:

```bat
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

```text
7:30 AM daily
```

Manual test command:

```powershell
.\run_careersignal_daily.bat
```

Useful verification commands:

```powershell
Get-Content .\logs\scheduled_task.log -Tail 100
Get-Content .\logs\careersignal.log -Tail 100
Get-Item .\data\careersignal.db
Get-Item .\exports\careersignal_export.xlsx
```

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

Step 17 is now active.

Goal:

Add a manual application tracking system to CareerSignal that records applications submitted by the user, tracks response outcomes, calculates ghosting/rejection danger zones, and summarizes application performance overall and by company.

Application Tracker should remain separate from the automated job collector at first.

Do not modify the daily job alert email yet.

Do not build weekly email yet.

Do not build Power BI visuals yet.

Do not update Excel export yet unless working on the specific export step later.

---

### Step 17A: Application Tracker Database Foundation

Status:

```text
Complete
```

Purpose:

Create the database foundation for manually tracking job applications.

Expected database:

```text
data/careersignal.db
```

Expected table:

```text
application_tracker
```

Core fields should support:

```text
date_applied
company_name
job_title
job_url
source
status
response dates
notes
created_at
updated_at
```

Valid statuses should include:

```text
applied
interview
rejected
accepted
ghosted
withdrawn
closed
```

Aging rules:

```text
0-14 days with no response = active / normal waiting period
15-30 days with no response = rejection danger zone
31-60 days with no response = ghosting danger zone
61+ days with no response = ghosted
```

Reporting rule:

```text
Ghosted applications should count as negative outcomes/rejections in total outcome reporting.
```

---

### Step 17B: Application Tracker Reusable Module

Status:

```text
Complete
```

Purpose:

Add the reusable Python logic for interacting with the Application Tracker table.

Expected file:

```text
src/careersignal/application_tracker.py
```

The module should contain reusable database helper logic for things like:

```text
adding application records
validating statuses
updating application statuses
updating application details or notes
fetching application records
using data/careersignal.db
```

17B should not include:

```text
manual command-line scripts
summary reporting
weekly email
Excel export
Power BI visuals
daily email changes
```

---

### Step 17C: Manual Add-Application Script

Status:

```text
Current next step
```

Goal:

Create a runnable script for manually adding application records from PowerShell.

Expected file:

```text
scripts/add_application.py
```

The script should use the reusable functions from:

```text
src/careersignal/application_tracker.py
```

Expected behavior:

```text
User runs a command with company, title, date applied, URL/source/notes if available.
Script validates input.
Script inserts the application into application_tracker.
Script prints the inserted record or confirmation.
```

Example future command:

```powershell
python scripts/add_application.py --company "RSM" --title "Audit Associate" --date-applied "2026-06-01" --url "https://example.com/job" --source "company website"
```

Keep 17C small.

Do not build reporting in 17C.

Do not build status update script in 17C unless explicitly approved.

---

### Step 17D: Manual Status-Update Script

Status:

```text
Planned
```

Goal:

Create a runnable script for manually updating an application’s status.

Expected file:

```text
scripts/update_application_status.py
```

Expected behavior:

```text
User provides application ID and new status.
Script validates status.
Script updates status and relevant response date fields.
Script prints confirmation.
```

Example future command:

```powershell
python scripts/update_application_status.py --id 4 --status interview --date "2026-06-10"
```

---

### Step 17E: Application Tracker Summary Reporting

Status:

```text
Planned
```

Goal:

Add summary reporting for Application Tracker.

Expected reporting:

```text
total applications
active applications
interviews
acceptances
formal rejections
ghostings
negative outcomes
totals by company
interviews by company
rejections by company
ghostings by company
acceptances by company
application aging buckets
```

Ghostings should count as negative outcomes.

Possible file:

```text
scripts/report_applications.py
```

or reusable reporting functions inside:

```text
src/careersignal/application_tracker.py
```

Only add reporting after 17C and 17D are stable.

---

### Step 17F: Excel Export Integration

Status:

```text
Planned
```

Goal:

Add Application Tracker sheets to the existing Excel export.

Existing export file:

```text
scripts/export_to_excel.py
```

Existing output:

```text
exports/careersignal_export.xlsx
```

Possible future sheets:

```text
Applications
Application Summary
Company Application Summary
Application Aging
```

Do not change the Power BI source path.

---

### Step 17G: Weekly Application Tracker Email

Status:

```text
Planned
```

Goal:

Add a separate weekly Application Tracker email after reporting works.

Preferred schedule:

```text
Friday at 4 PM
```

Do not add Application Tracker stats to the daily job alert email at first.

The weekly email may include:

```text
applications this week
total active applications
interviews received
rejections received
new ghostings
applications entering rejection danger zone
applications entering ghosting danger zone
company response summary
```

---

### Step 17H: Power BI Application Tracker Visuals

Status:

```text
Optional / later
```

Goal:

Add Application Tracker visuals to Power BI after Excel export sheets are stable.

Possible visuals:

```text
KPI cards for total applications, interviews, rejections, ghostings, acceptances
bar chart for applications by company
bar chart for outcomes by company
aging table
status distribution chart
applications over time
```

---

## Current Roadmap

### Step 17: Application Tracker

Current active step.

Completed:

```text
17A: Database foundation
17B: Reusable module
```

Current next step:

```text
17C: Manual add-application script
```

Planned:

```text
17D: Manual status-update script
17E: Summary reporting
17F: Excel export integration
17G: Weekly tracker email
17H: Optional Power BI visuals
```

---

### Step 18: GitHub + Portfolio Polish

Status:

```text
Planned, not current
```

Purpose:

Clean README, screenshots, sample outputs, final testing, resume bullets, and portfolio presentation.

Required before heavily featuring the project on a resume.

Step 18 should update:

```text
README.md
docs/CareerSignal_Project_State.md
```

Step 18 should not rename official functions, change database paths, recreate existing files, or break existing behavior.

Step 18 validation should confirm:

```text
preview run works
send run works
email arrives
email only includes jobs first seen in the past 24 hours
match scores show correctly
failed sources show correctly
Excel export updates
Power BI refresh works from exports/careersignal_export.xlsx
logs update
no data/jobs.db references
no old function names
no secrets staged for Git
```

Step 18 known action items:

```text
Fix or confirm the Power BI data source so it pulls from exports/careersignal_export.xlsx instead of an old test file.
Check and confirm that match scoring appears correctly in sent emails.
Make sure sent emails include only jobs first seen in the past 24 hours.
Circle back to Step 13 Workday URL issues.
Add the rest of the Greenhouse companies.
Polish README for portfolio/resume presentation.
Add screenshots and sample outputs.
```

---

### Step 19: Optional Streamlit UI

Status:

```text
Optional / later
```

Only if a prettier local interface is wanted later.

Nice-to-have, not required.

---

## Must-Do vs Nice-to-Have

Current must-do path:

```text
17C: Manual add-application script
17D: Manual status-update script
17E: Application tracker summary reporting
18: GitHub + Portfolio Polish
```

Nice-to-have:

```text
17F: Excel export integration
17G: Weekly tracker email
17H: Power BI Application Tracker visuals
19: Optional Streamlit UI
```

---

## Testing Commands

Useful commands:

```bash
PYTHONPATH=src python scripts/test_config_loader.py
PYTHONPATH=src python scripts/test_database.py
PYTHONPATH=src python scripts/test_match_scoring.py
PYTHONPATH=src python scripts/test_email_report.py
python scripts/collect_greenhouse_jobs.py --preview
python scripts/export_to_excel.py
```

Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python scripts/test_config_loader.py
python scripts/test_database.py
python scripts/test_match_scoring.py
python scripts/test_email_report.py
python scripts/collect_greenhouse_jobs.py --preview
python scripts/export_to_excel.py
```

Daily automation test:

```powershell
.\run_careersignal_daily.bat
```

Real send mode:

```powershell
python scripts/collect_greenhouse_jobs.py --send
python scripts/export_to_excel.py
```

Future Application Tracker tests may include:

```powershell
python scripts/add_application.py --help
python scripts/update_application_status.py --help
python scripts/report_applications.py
```

Only use those after the scripts exist.

---

## Required Checks for Future Coding Steps

For every future coding step, include:

1. Files to create/edit
2. Exact code
3. Commands to test
4. Grep/search checks for old names or broken imports
5. Git commit guidance

Always include checks for:

```bash
grep -RIn "data/jobs.db" .
grep -RIn "create_tables" .
grep -RIn "insert_normalized_jobs" .
grep -RIn "fetch_all_jobs" .
```

PowerShell equivalent:

```powershell
Select-String -Path .\* -Pattern "data/jobs.db" -Recurse
Select-String -Path .\* -Pattern "create_tables" -Recurse
Select-String -Path .\* -Pattern "insert_normalized_jobs" -Recurse
Select-String -Path .\* -Pattern "fetch_all_jobs" -Recurse
```

Also check official function names when relevant:

```bash
grep -RIn "build_and_send_daily_report" .
grep -RIn "score_job" .
grep -RIn "initialize_database" .
grep -RIn "insert_or_update_jobs" .
grep -RIn "get_jobs_first_seen_in_last_24_hours" .
```

PowerShell:

```powershell
Select-String -Path .\* -Pattern "build_and_send_daily_report" -Recurse
Select-String -Path .\* -Pattern "score_job" -Recurse
Select-String -Path .\* -Pattern "initialize_database" -Recurse
Select-String -Path .\* -Pattern "insert_or_update_jobs" -Recurse
Select-String -Path .\* -Pattern "get_jobs_first_seen_in_last_24_hours" -Recurse
```

Application Tracker checks when relevant:

```bash
grep -RIn "application_tracker" .
grep -RIn "data/jobs.db" .
```

PowerShell:

```powershell
Select-String -Path .\* -Pattern "application_tracker" -Recurse
Select-String -Path .\* -Pattern "data/jobs.db" -Recurse
```

---

## Git Guidance

After project-state updates:

```bash
git add docs/CareerSignal_Project_State.md
git commit -m "Update CareerSignal project state"
git push
```

After README updates:

```bash
git add README.md
git commit -m "Update CareerSignal README"
git push
```

After Application Tracker feature steps, use specific commit messages, such as:

```bash
git add .
git commit -m "Add application tracker database foundation"
git push
```

```bash
git add .
git commit -m "Add application tracker module"
git push
```

```bash
git add .
git commit -m "Add application entry script"
git push
```

Avoid committing:

```text
.env
logs/
data/careersignal.db if intentionally ignored
exports/careersignal_export.xlsx if intentionally ignored
temporary test files
email passwords
SMTP secrets
```

---

## Important Reminder for Future ChatGPT Help

Before giving code:

1. Read this file.
2. Do not recreate existing files.
3. Do not rename official functions.
4. Do not change `data/careersignal.db`.
5. Do not use old function names.
6. Explain dependencies before rewriting core files.
7. Keep new work compatible with the existing pipeline.
8. Preserve Greenhouse and Workday support.
9. Preserve email, Excel, Power BI, logging, and scoring behavior unless the user asks to change them.
10. Preserve preview mode and send mode.
11. Keep `.env` and secrets out of GitHub.
12. Keep the response beginner-friendly and step-by-step.
13. During Step 17, do not modify daily job alert behavior unless explicitly approved.
14. During Step 17, keep Application Tracker steps small and separate.
