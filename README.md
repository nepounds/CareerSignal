# CareerSignal

CareerSignal is a Python/SQL career intelligence pipeline that monitors target company career pages, collects job postings, stores them in SQLite, scores jobs against target criteria, sends daily email reports, exports Excel reports, and supports Power BI dashboard reporting.

The project was built as a portfolio project to show practical Python, SQL, automation, data pipeline, reporting, and business analysis skills.

## Project Summary

CareerSignal helps reduce manual job searching by checking configured company career pages and surfacing new jobs that match defined target roles, locations, and keywords.

The pipeline currently supports:

* Greenhouse job boards
* Workday job boards
* Company-level configuration
* Normalized job records
* SQLite job storage
* New job detection
* Match scoring
* Daily email reports
* Error handling and logging
* Excel export
* Power BI dashboard reporting
* Windows Task Scheduler automation

## How It Works

```text
Windows Task Scheduler
→ run_careersignal_daily.bat
→ Python collection runner
→ Greenhouse / Workday collectors
→ normalized job records
→ SQLite database
→ new job detection
→ match scoring
→ daily email report
→ Excel export
→ Power BI dashboard
```

### 1. Task Scheduler

Windows Task Scheduler runs the project automatically each day using:

```text
run_careersignal_daily.bat
```

The batch file runs the main collection script in send mode and then refreshes the Excel export.

### 2. Python Collection Runner

The main runner is:

```text
scripts/collect_greenhouse_jobs.py
```

Even though the filename references Greenhouse, the script currently functions as the main collection runner for supported ATS types.

Preview mode:

```powershell
python scripts/collect_greenhouse_jobs.py --preview
```

Send mode:

```powershell
python scripts/collect_greenhouse_jobs.py --send
```

### 3. Greenhouse and Workday Collectors

CareerSignal currently supports two ATS types:

```text
greenhouse
workday
```

Collector modules live in:

```text
src/careersignal/collectors/
```

Each collector returns normalized job dictionaries so the rest of the pipeline can process jobs consistently.

### 4. SQLite Database

CareerSignal stores collected jobs in:

```text
data/careersignal.db
```

The database is used to:

* Store job postings
* Avoid duplicate job records
* Track first-seen and last-seen dates
* Identify jobs first seen in the past 24 hours
* Support reporting and exports

### 5. Match Scoring

Jobs are scored against target criteria such as title, keywords, location, seniority, and fit.

The scoring system supports multiple job-search lanes, not only accounting roles.

Examples of supported lanes include:

* Accounting roles
* Finance roles
* General analyst roles
* Business analyst roles
* Operations analyst roles
* Compliance analyst roles
* Data/reporting analyst roles
* Plant supervisor roles
* Operations supervisor roles
* Water/wastewater or public utility-adjacent roles

Suggested score bands:

```text
80-100: Strong match
60-79: Possible match
40-59: Weak/stretch match
0-39: Low match or likely skip
```

### 6. Daily Email Report

CareerSignal can send a daily email report that includes:

* Run summary
* Newly discovered matching jobs
* Match scores
* Failed sources, if any
* Collection status

Send mode:

```powershell
python scripts/collect_greenhouse_jobs.py --send
```

### 7. Excel Export

CareerSignal exports job data to:

```text
exports/careersignal_export.xlsx
```

Manual export command:

```powershell
python scripts/export_to_excel.py
```

The Excel file is used as the data source for the Power BI dashboard.

### 8. Power BI Dashboard

The Power BI report is stored in:

```text
reports/careersignal_dashboard.pbix
```

The dashboard should pull from:

```text
exports/careersignal_export.xlsx
```

Power BI Desktop requires manual refresh unless the report is published and configured with scheduled refresh separately.

Refresh manually in Power BI Desktop:

```text
Home > Refresh
```

## Current Features

* Greenhouse ATS support
* Workday ATS support
* Company configuration through CSV
* Normalized job format
* SQLite database storage
* Duplicate job prevention
* New job detection
* Match scoring
* Daily email report
* Failed-source reporting
* Error handling and logging
* Excel export
* Power BI dashboard
* Windows Task Scheduler automation
* Filtering strategy for multiple job-search lanes

## Project Structure

```text
CareerSignal/
├── config/
│   ├── company_config.csv
│   ├── company_ats_audit.csv
│   └── match_rules.json or match_rules.csv
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
│       ├── config_loader.py
│       ├── database.py
│       ├── email_report.py
│       ├── logging_config.py
│       ├── match_scoring.py
│       └── collectors/
│           ├── greenhouse.py
│           └── workday.py
├── run_careersignal_daily.bat
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

### 1. Clone the repository

```powershell
git clone <repository-url>
cd CareerSignal
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install requirements

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```powershell
copy .env.example .env
```

Then update `.env` with your local email settings.

Do not commit `.env`.

### 5. Confirm company configuration

Company settings live in:

```text
config/company_config.csv
```

Supported ATS values are:

```text
greenhouse
workday
```

## Common Commands

Set `PYTHONPATH` in PowerShell:

```powershell
$env:PYTHONPATH="src"
```

Run tests:

```powershell
python scripts/test_config_loader.py
python scripts/test_database.py
python scripts/test_match_scoring.py
python scripts/test_email_report.py
```

Preview job collection:

```powershell
python scripts/collect_greenhouse_jobs.py --preview
```

Send the daily email report:

```powershell
python scripts/collect_greenhouse_jobs.py --send
```

Export to Excel:

```powershell
python scripts/export_to_excel.py
```

Run the daily automation manually:

```powershell
.\run_careersignal_daily.bat
```

Check logs:

```powershell
Get-Content .\logs\careersignal.log -Tail 100
Get-Content .\logs\scheduled_task.log -Tail 100
```

## Screenshots

Recommended screenshots for GitHub:

```text
docs/screenshots/powerbi_overview_dashboard.png
docs/screenshots/sample_daily_email.png
docs/screenshots/excel_export_sample.png
docs/screenshots/task_scheduler_setup.png
```

Suggested README image section:

```markdown
## Screenshots

### Power BI Dashboard

![Power BI dashboard](docs/screenshots/powerbi_overview_dashboard.png)

### Daily Email Report

![Sample daily email](docs/screenshots/sample_daily_email.png)

### Excel Export

![Excel export sample](docs/screenshots/excel_export_sample.png)

### Task Scheduler Setup

![Task Scheduler setup](docs/screenshots/task_scheduler_setup.png)
```

Only use screenshots with fake, sample, or non-sensitive data.

## Known Limitations

* Power BI Desktop requires manual refresh unless the report is published and scheduled refresh is configured separately.
* Some ATS platforms are not supported yet.
* The Step 13 ATS coverage audit still has unresolved follow-up items.
* Workday URLs may require manual review because Workday career sites can vary by company.
* Application tracking is planned but not included in this version.
* Generated local files may contain private data and should not be committed unless converted to sample data.

## Future Improvements

* Resolve remaining Step 13 ATS audit items.
* Add more supported ATS connectors only when enough target companies justify them.
* Add an application tracker for saved, applied, interview, rejected, offer, skipped, and closed statuses.
* Improve Power BI dashboard pages.
* Add optional Streamlit UI.

## GitHub Safety Notes

Do not commit:

```text
.env
.venv/
logs/
data/careersignal.db
exports/careersignal_export.xlsx
email passwords
SMTP secrets
private job exports
temporary test files
```

Safe files to commit generally include:

```text
README.md
requirements.txt
.env.example
.gitignore
run_careersignal_daily.bat
config/company_config.csv if it contains no private data
config/company_ats_audit.csv if it contains no private data
docs/
reports/careersignal_dashboard.pbix if it does not contain private data
scripts/
src/
tests/
```

## Final Validation Checklist

Before treating the project as resume-ready, confirm:

* Preview run works.
* Send run works.
* Email arrives.
* Email only includes jobs first seen in the past 24 hours.
* Match scores show correctly in the email.
* Failed sources show correctly in the email when a source fails.
* Excel export updates.
* Power BI refresh works from `exports/careersignal_export.xlsx`.
* Logs update.
* No references to `data/jobs.db` remain.
* No old function names remain.
* No secrets are staged for Git.
* README screenshots use sample or non-sensitive data.

## Portfolio Summary

CareerSignal demonstrates:

* Python scripting
* SQL and SQLite database design
* Data normalization
* API-style data collection
* Error handling and logging
* Match scoring logic
* Email automation
* Excel reporting
* Power BI reporting
* Windows Task Scheduler automation
* Git/GitHub project organization

## Resume Bullet Options

* Built CareerSignal, a Python/SQL job intelligence pipeline that collects postings from Greenhouse and Workday career sites, stores normalized job data in SQLite, scores role fit, and sends automated daily email reports.
* Designed a configurable job-monitoring system using Python, SQLite, Excel exports, Power BI, and Windows Task Scheduler to automate job discovery and reporting.
* Created a portfolio data pipeline that normalizes job postings, prevents duplicate records, detects newly posted roles, applies match scoring, logs failed sources, and exports data for dashboard reporting.
* Developed an automated career tracking workflow with Python collectors, SQL-backed storage, daily email reporting, Excel output, and Power BI visualization.
