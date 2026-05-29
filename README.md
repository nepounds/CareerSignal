# CareerSignal

CareerSignal is a Python portfolio project that monitors job postings from target companies, stores the results in SQLite, scores each job against custom career criteria, sends daily email reports, exports Excel reports, and supports a Power BI dashboard.

The project was built to solve a real job-search problem: instead of manually checking dozens of company career pages every day, CareerSignal collects and organizes relevant postings automatically.

---

## Project Status

CareerSignal currently has a working end-to-end pipeline.

Completed features include:

* Company configuration file
* Greenhouse job collection
* Workday job collection
* Standard normalized job format
* SQLite database storage
* New job detection
* Daily email report
* Error handling and logging
* Excel export
* Power BI dashboard support
* ATS coverage audit planning
* Filtering strategy
* Match scoring refinement
* Windows Task Scheduler automation runner

---

## What CareerSignal Does

CareerSignal follows this general workflow:

```text
Target companies
→ ATS collectors
→ normalized job records
→ SQLite database
→ new job detection
→ match scoring
→ daily email report
→ Excel export
→ Power BI dashboard
```

The system is designed to help track jobs across multiple target lanes, including:

* Accounting roles
* Finance roles
* General analyst roles
* Business analyst roles
* Operations analyst roles
* Compliance analyst roles
* Data/reporting analyst roles
* Plant supervisor roles
* Operations supervisor roles
* Water/wastewater or utility-adjacent roles
* Other realistic roles that fit the user’s background

This is not an accounting-only project.

---

## Current Supported ATS Platforms

CareerSignal currently supports:

```text
greenhouse
workday
```

Future possible ATS connectors may include:

```text
lever
ashby
smartrecruiters
icims
generic_html
```

Those are not built yet. Future connectors should only be added if enough target companies use them or if one very high-priority company makes the connector worth building.

---

## Project Structure

```text
CareerSignal/
├── config/
│   ├── company_config.csv
│   ├── company_ats_audit.csv
│   └── match_rules.json
├── data/
│   └── careersignal.db
├── docs/
│   ├── CareerSignal_Project_State.md
│   ├── filtering_strategy.md
│   └── screenshots/
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
│   └── test_match_scoring.py
├── src/
│   └── careersignal/
│       ├── __init__.py
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

Some generated files may be ignored by Git, including `.env`, logs, local database files, and generated exports.

---

## Main Files

### Company Config

```text
config/company_config.csv
```

This file stores the companies CareerSignal should check.

Current supported `ats_type` values:

```text
greenhouse
workday
```

Expected config fields include:

```text
company
ats_type
career_url
workday_api_url
job_url_base
target_location
keywords
job_title_keywords
excluded_keywords
is_active
```

---

### Database

CareerSignal uses SQLite.

Current database path:

```text
data/careersignal.db
```

The project should not use:

```text
data/jobs.db
```

---

### Main Collector Runner

The current main runner is:

```text
scripts/collect_greenhouse_jobs.py
```

The file name still says Greenhouse because that was the first collector built, but the runner now supports both Greenhouse and Workday through the shared pipeline.

Preview mode:

```bash
python scripts/collect_greenhouse_jobs.py --preview
```

Send mode:

```bash
python scripts/collect_greenhouse_jobs.py --send
```

Preview mode is used for testing without sending the real daily email.

Send mode is used for the real daily run.

---

### Excel Export

CareerSignal exports job data to Excel:

```bash
python scripts/export_to_excel.py
```

Default output:

```text
exports/careersignal_export.xlsx
```

This export supports the Power BI dashboard.

---

### Power BI Dashboard

Power BI report file:

```text
reports/careersignal_dashboard.pbix
```

Power BI data source:

```text
exports/careersignal_export.xlsx
```

After running a fresh Excel export, refresh the dashboard manually in Power BI:

```text
Home > Refresh
```

---

## Daily Automation

CareerSignal can be automated with Windows Task Scheduler.

The daily automation should run:

```bat
python scripts\collect_greenhouse_jobs.py --send
python scripts\export_to_excel.py
```

The project includes a batch runner:

```text
run_careersignal_daily.bat
```

The batch file should:

1. Change into the CareerSignal project folder
2. Activate the virtual environment if available
3. Set `PYTHONPATH=src`
4. Run the collector in send mode
5. Run the Excel export
6. Write scheduled-task output to:

```text
logs/scheduled_task.log
```

Recommended daily run time:

```text
7:30 AM
```

If the computer is usually asleep in the morning, a midday time may be more reliable.

---

## Environment Variables

CareerSignal uses a local `.env` file for private settings.

The `.env` file should not be committed to GitHub.

A safe example file may be tracked instead:

```text
.env.example
```

The real `.env` may include settings such as:

```text
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USERNAME=
EMAIL_PASSWORD=
EMAIL_FROM=
EMAIL_TO=
```

Secrets should stay local.

---

## Logging

Main application log:

```text
logs/careersignal.log
```

Scheduled task log:

```text
logs/scheduled_task.log
```

The goal is for one failed company source to be logged without crashing the entire daily run.

Failed sources should be included in the daily email report when possible.

---

## Match Scoring

CareerSignal scores jobs from 0 to 100.

Suggested score bands:

```text
80-100: Strong match
60-79: Possible match
40-59: Weak/stretch match
0-39: Low match or likely skip
```

The scoring system supports multiple job lanes, not just accounting and finance.

Official scoring function:

```python
score_job(job)
```

This function should not be renamed unless the rest of the project is intentionally updated.

---

## Testing Commands

From PowerShell:

```powershell
$env:PYTHONPATH="src"

python scripts/test_config_loader.py
python scripts/test_database.py
python scripts/test_match_scoring.py
python scripts/test_email_report.py
python scripts/collect_greenhouse_jobs.py --preview
python scripts/export_to_excel.py
```

To test the real daily send flow:

```powershell
python scripts/collect_greenhouse_jobs.py --send
python scripts/export_to_excel.py
```

To test the automation runner:

```powershell
.\run_careersignal_daily.bat
```

---

## Search Checks

Use these checks to avoid old names and broken paths.

Git Bash:

```bash
grep -RIn "data/jobs.db" .
grep -RIn "create_tables" .
grep -RIn "insert_normalized_jobs" .
grep -RIn "fetch_all_jobs" .
```

PowerShell:

```powershell
Select-String -Path .\* -Pattern "data/jobs.db" -Recurse
Select-String -Path .\* -Pattern "create_tables" -Recurse
Select-String -Path .\* -Pattern "insert_normalized_jobs" -Recurse
Select-String -Path .\* -Pattern "fetch_all_jobs" -Recurse
```

Those old names should not appear in active project code.

---

## Current Roadmap

### Step 17: Application Tracker

Possible future feature.

This would add tracking for jobs that were:

* Saved
* Applied
* Interviewed
* Rejected
* Offered
* Skipped
* Closed

This is useful, but not required for the first resume-ready version.

---

### Step 18: GitHub and Portfolio Polish

Required before adding the project heavily to a resume.

Planned polish work:

* Clean README
* Add screenshots
* Add sample outputs
* Confirm GitHub-safe files
* Final test run
* Resume bullets
* Portfolio explanation

---

### Step 19: Optional Streamlit UI

Optional future feature.

This could provide a local dashboard-style interface, but it is not required because the project already has Excel and Power BI reporting.

---

## Skills Demonstrated

CareerSignal demonstrates practical experience with:

* Python scripting
* API collection
* ATS data collection
* Data normalization
* SQLite databases
* SQL-backed persistence
* Email automation
* Error handling and logging
* Excel export
* Power BI dashboard support
* Match scoring logic
* Config-driven design
* Windows automation
* Git/GitHub project organization
* AI-assisted development workflow

---

## Portfolio Summary

CareerSignal is a job-posting monitoring and reporting tool built with Python, SQLite, Excel, and Power BI. It collects postings from supported ATS platforms, stores normalized job records, detects new jobs, scores postings against custom criteria, sends daily email summaries, and exports data for dashboard reporting.

The project is designed as a practical business automation and analytics portfolio project.
