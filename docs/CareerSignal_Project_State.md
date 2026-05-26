# CareerSignal Project State

## Purpose of This Document

This document is the internal source of truth for the CareerSignal project.

Use this file to preserve official file names, function names, folder structure, database paths, workflow decisions, and project status.

This is not meant to replace the README.

- `README.md` is the public-facing project explanation.
- `docs/CareerSignal_Project_State.md` is the internal development map.

The main reason this file exists is to prevent accidental backtracking, duplicate names, broken imports, old database paths, and inconsistent project structure.

---

# 1. Project Overview

CareerSignal is a Python portfolio project that tracks job postings from target companies and helps identify relevant accounting, finance, analyst, and business roles.

The project is designed to:

- Load target companies from a config file.
- Collect jobs from supported ATS platforms.
- Normalize job data into one official shape.
- Store jobs in SQLite.
- Detect newly discovered jobs.
- Score jobs based on match quality.
- Send daily email reports.
- Export job data to Excel.
- Support a Power BI dashboard.
- Eventually support multiple ATS sources, including Greenhouse and Workday.

---

# 2. Current Project Phase

The project is currently in:

```text
Step 12: Workday Connector
```

Step 12 is split into three separate parts:

```text
Step 12A: Workday Proof of Concept
Step 12B: Workday Normalization
Step 12C: Integrate Workday Connector
```

Current active step:

```text
Step 12B: Workday Normalization
```

---

# 3. Official Project Structure

Use this structure unless there is a strong reason to change it.

```text
CareerSignal/
├── config/
│   └── company_config.csv
│
├── data/
│   └── careersignal.db
│
├── docs/
│   └── CareerSignal_Project_State.md
│
├── exports/
│   └── careersignal_export.xlsx
│
├── logs/
│   └── careersignal.log
│
├── reports/
│   └── careersignal_dashboard.pbix
│
├── scripts/
│   ├── collect_greenhouse_jobs.py
│   ├── export_to_excel.py
│   ├── preview_workday_jobs.py
│   └── preview_workday_normalized_jobs.py
│
├── src/
│   └── careersignal/
│       ├── __init__.py
│       ├── config_loader.py
│       ├── database.py
│       ├── email_report.py
│       ├── match_scoring.py
│       └── collectors/
│           ├── __init__.py
│           └── workday.py
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

Notes:

- `scripts/` contains runnable scripts.
- `src/careersignal/` contains reusable project modules.
- `src/careersignal/collectors/` contains ATS-specific collector modules.
- `data/` contains the SQLite database.
- `config/` contains company settings.
- `logs/` contains log files.
- `exports/` contains Excel exports.
- `reports/` contains Power BI files.
- `docs/` contains internal project documentation.

---

# 4. Official Database Path

The official SQLite database path is:

```text
data/careersignal.db
```

Do not use:

```text
data/jobs.db
```

If `data/jobs.db` appears anywhere, it is an old name and should be corrected.

---

# 5. Official Normalized Job Shape

Every job from every ATS must eventually become this exact normalized job dictionary shape:

```python
{
    "company_name": str,
    "source_ats": str,
    "external_job_id": str,
    "title": str,
    "location": str,
    "department": str,
    "job_url": str,
    "posted_date": str,
    "date_collected": str,
}
```

Official field names:

```text
company_name
source_ats
external_job_id
title
location
department
job_url
posted_date
date_collected
```

Rules:

- Do not rename these fields.
- Do not add extra fields to the normalized job object unless the database, Excel export, email report, and Power BI are intentionally updated together.
- Missing text fields should safely become empty strings.
- Missing dates may be `None` when appropriate.
- `date_collected` should represent when CareerSignal collected the job.
- `posted_date` should represent when the job was posted, if the ATS provides that information.

---

# 6. Official Database Functions

Official database file:

```text
src/careersignal/database.py
```

Official database functions:

```python
initialize_database()
insert_or_update_jobs(jobs)
get_all_jobs()
get_jobs_first_seen_in_last_24_hours()
insert_run_log(...)
```

Rules:

- Preserve these function names.
- Do not rename working database functions unless absolutely necessary.
- Do not create duplicate versions with similar names.
- Do not create a new database path.
- Do not insert Workday jobs into SQLite during Step 12B.
- Workday database insertion begins in Step 12C.

---

# 7. Official Match Scoring Function

Official match scoring file:

```text
src/careersignal/match_scoring.py
```

Official function:

```python
score_job(job)
```

Rules:

- Preserve this function name.
- Match scoring should operate on normalized job dictionaries.
- Do not change match scoring during Step 12B.
- Workday jobs should eventually be scoreable because they will match the official normalized job shape.

---

# 8. Official Email Report Function

Official email report file:

```text
src/careersignal/email_report.py
```

Official function:

```python
build_and_send_daily_report(summary, new_jobs, failed_sources, test_mode=True)
```

Rules:

- Preserve this function name and signature.
- Do not change email reporting during Step 12B.
- Workday jobs should not be included in daily email reports until Step 12C.

---

# 9. Official Greenhouse Runner

Official Greenhouse runner file:

```text
scripts/collect_greenhouse_jobs.py
```

Official commands:

```bash
python scripts/collect_greenhouse_jobs.py --preview
python scripts/collect_greenhouse_jobs.py --send
```

Rules:

- Preserve these commands.
- Do not break Greenhouse while adding Workday.
- Greenhouse is the currently working main ATS pipeline.
- Workday should stay isolated during Step 12B.

---

# 10. Official Excel Export

Official Excel export file:

```text
scripts/export_to_excel.py
```

Official Excel output:

```text
exports/careersignal_export.xlsx
```

Rules:

- Do not change Excel export during Step 12B.
- Excel export should continue reading from the official SQLite database.
- Workday data should not appear in Excel until Step 12C integration is complete.

---

# 11. Official Power BI Dashboard

Official Power BI file:

```text
reports/careersignal_dashboard.pbix
```

Official Power BI data source:

```text
exports/careersignal_export.xlsx
```

Rules:

- Do not change Power BI during Step 12B.
- Power BI should continue using the Excel export.
- Workday data should not flow into Power BI until Step 12C.

---

# 12. Official Company Config

Official company config file:

```text
config/company_config.csv
```

Purpose:

The config file stores target company information used by collectors.

Rules:

- Do not add Workday configuration during Step 12B unless explicitly starting Step 12C.
- Greenhouse config should keep working.
- Workday integration into config happens during Step 12C.

---

# 13. Completed Steps

## Step 1: Project Setup

Completed.

The project has:

- Basic folder structure.
- Git tracking.
- GitHub repository.
- `.gitignore`.
- Project files organized into folders.

Important folders:

```text
scripts/
src/careersignal/
data/
config/
logs/
exports/
reports/
docs/
```

---

## Step 2: Company Config Loader

Completed.

Official config file:

```text
config/company_config.csv
```

Official reusable module:

```text
src/careersignal/config_loader.py
```

Purpose:

- Load company information from CSV.
- Keep company data separate from code.
- Allow the project to support multiple companies.

Rules:

- Do not hardcode long-term company lists inside runnable scripts.
- Use config loading when integrating collectors into the main pipeline.

---

## Step 3: Greenhouse ATS Collector

Completed.

Official runner:

```text
scripts/collect_greenhouse_jobs.py
```

Official commands:

```bash
python scripts/collect_greenhouse_jobs.py --preview
python scripts/collect_greenhouse_jobs.py --send
```

Purpose:

- Fetch jobs from Greenhouse-supported companies.
- Normalize jobs.
- Support preview and send modes.
- Feed the existing main pipeline.

Rules:

- Do not break this runner while adding Workday.
- Preserve preview/send behavior.

---

## Step 4: Job Data Normalization

Completed.

CareerSignal uses one official normalized job shape.

Official normalized job shape:

```python
{
    "company_name": str,
    "source_ats": str,
    "external_job_id": str,
    "title": str,
    "location": str,
    "department": str,
    "job_url": str,
    "posted_date": str,
    "date_collected": str,
}
```

Purpose:

- Make every ATS output look the same.
- Let database, scoring, email, Excel, and Power BI work with one standard format.

Rules:

- Every ATS connector must return this shape.
- Greenhouse and Workday should both normalize to this same format.

---

## Step 5: SQLite Database

Completed.

Official file:

```text
src/careersignal/database.py
```

Official database path:

```text
data/careersignal.db
```

Official database functions:

```python
initialize_database()
insert_or_update_jobs(jobs)
get_all_jobs()
get_jobs_first_seen_in_last_24_hours()
insert_run_log(...)
```

Purpose:

- Store discovered jobs.
- Avoid duplicate job records.
- Track first seen and last seen dates.
- Support new job detection.
- Support exports and reports.

Rules:

- Do not use `data/jobs.db`.
- Do not create a second SQLite database.
- Do not insert Workday jobs during Step 12B.

---

## Step 6: New Job Detection

Completed.

Purpose:

- Existing jobs update their `last_seen_date`.
- New jobs are inserted with `first_seen_date` and `last_seen_date`.
- The project can identify jobs first seen in the last 24 hours.
- Duplicate job records should be avoided.

Official function:

```python
get_jobs_first_seen_in_last_24_hours()
```

Rules:

- New job detection should continue working for Greenhouse.
- Workday should not be added to new job detection until Step 12C.

---

## Step 7: Daily Email Report

Completed.

Official file:

```text
src/careersignal/email_report.py
```

Official function:

```python
build_and_send_daily_report(summary, new_jobs, failed_sources, test_mode=True)
```

Purpose:

- Build daily email reports.
- Include summary information.
- Include new jobs.
- Include failed sources.
- Support test mode.

Rules:

- Do not change this during Step 12B.
- Workday email reporting starts during Step 12C.

---

## Step 8: Error Handling and Logging

Completed.

Official logs folder:

```text
logs/
```

Typical log file:

```text
logs/careersignal.log
```

Purpose:

- Record successful runs.
- Record failed sources.
- Avoid full pipeline crashes when one source fails.
- Make debugging easier.

Rules:

- Keep logging consistent.
- Do not create random log folders.
- New collectors should eventually use the same logging pattern when integrated.

---

## Step 9: Excel Export

Completed.

Official file:

```text
scripts/export_to_excel.py
```

Official output:

```text
exports/careersignal_export.xlsx
```

Purpose:

- Export SQLite job data to Excel.
- Create a clean file for review.
- Feed the Power BI dashboard.

Rules:

- Keep the output path stable.
- Do not change Excel export during Step 12B.
- Workday data should only appear here after database integration in Step 12C.

---

## Step 10: Power BI Dashboard

Completed.

Official Power BI file:

```text
reports/careersignal_dashboard.pbix
```

Official data source:

```text
exports/careersignal_export.xlsx
```

Purpose:

- Visualize job data.
- Show match quality.
- Show role/company/location patterns.
- Turn the project into something visually useful for a portfolio.

Rules:

- Power BI should read from Excel export.
- Do not change dashboard source paths unnecessarily.
- Do not change Power BI during Step 12B.

---

## Step 11: Power BI Polish / Dashboard Update

Completed.

Purpose:

- Improve dashboard presentation.
- Make the project more portfolio-friendly.
- Improve visuals, layout, and usefulness.

Rules:

- Keep Power BI connected to:

```text
exports/careersignal_export.xlsx
```

- Do not update Power BI again during Step 12B unless there is a specific reason.

---

## Step 12A: Workday Proof of Concept

Completed.

Current proof-of-concept script:

```text
scripts/preview_workday_jobs.py
```

Purpose:

- Fetch jobs from one Workday career site.
- Preview raw Workday job results.
- Learn Workday’s response shape.
- Keep Workday completely separate from the main pipeline.

Rules:

- This step was only about proving that Workday jobs can be fetched.
- This script should not insert jobs into SQLite.
- This script should not send emails.
- This script should not export to Excel.
- This script should not modify Power BI.

---

# 14. Current Step: Step 12B Workday Normalization

Current active step:

```text
Step 12B: Workday Normalization
```

Goal:

Convert raw Workday job results into CareerSignal’s official normalized job shape.

Planned reusable module:

```text
src/careersignal/collectors/workday.py
```

Planned preview script:

```text
scripts/preview_workday_normalized_jobs.py
```

Step 12B should:

- Fetch raw Workday jobs.
- Convert raw Workday jobs into official normalized job dictionaries.
- Set `source_ats` to `"workday"`.
- Extract a stable `external_job_id` if possible.
- Extract title.
- Extract location.
- Extract department if available.
- Extract posted date if available.
- Build a clean job URL.
- Add `date_collected`.
- Validate that every normalized Workday job has the exact official fields.
- Stay isolated from the main pipeline.

Step 12B should not:

- Insert Workday jobs into SQLite.
- Change `config/company_config.csv`.
- Change daily email reporting.
- Change match scoring.
- Change Excel export.
- Change Power BI.
- Break the Greenhouse collector.
- Replace the existing main runner.

Success criteria:

```text
Raw Workday jobs can be fetched.
Raw Workday jobs can be normalized.
Every normalized Workday job has the official CareerSignal fields.
No Workday jobs are inserted into SQLite yet.
The Greenhouse preview command still works.
```

---

# 15. Future Step: Step 12C Workday Integration

Future step:

```text
Step 12C: Integrate Workday Connector
```

Goal:

Connect Workday to the full CareerSignal pipeline.

Step 12C will eventually connect Workday to:

```text
config/company_config.csv
data/careersignal.db
src/careersignal/database.py
src/careersignal/match_scoring.py
src/careersignal/email_report.py
scripts/export_to_excel.py
exports/careersignal_export.xlsx
reports/careersignal_dashboard.pbix
```

Step 12C will likely involve:

- Adding Workday companies to `company_config.csv`.
- Updating the runner logic to choose collectors by ATS.
- Calling the Workday collector from the main pipeline.
- Inserting normalized Workday jobs into SQLite.
- Scoring Workday jobs.
- Including Workday jobs in daily email reports.
- Including Workday jobs in Excel exports.
- Refreshing Power BI with Workday data.

Rules:

- Do not do Step 12C work during Step 12B.
- Only integrate after normalized Workday jobs are proven stable.

---

# 16. Workday Connector Plan

## Step 12A

Status:

```text
Done
```

Purpose:

- Fetch raw Workday jobs.
- Preview the raw response.
- Avoid touching the main CareerSignal pipeline.

Official script:

```text
scripts/preview_workday_jobs.py
```

---

## Step 12B

Status:

```text
Current
```

Purpose:

- Normalize Workday jobs into CareerSignal’s official format.

Planned module:

```text
src/careersignal/collectors/workday.py
```

Planned preview script:

```text
scripts/preview_workday_normalized_jobs.py
```

Expected main reusable function:

```python
fetch_and_normalize_workday_jobs(...)
```

Expected helper functions may include:

```python
fetch_workday_raw_jobs(...)
normalize_workday_job(...)
normalize_workday_jobs(...)
extract_workday_external_job_id(...)
extract_workday_title(...)
extract_workday_location(...)
extract_workday_department(...)
extract_workday_posted_date(...)
build_workday_job_url(...)
validate_normalized_job_shape(...)
```

Rules:

- These functions may be adjusted if needed.
- Keep the function names plain and consistent.
- Do not rename working project-wide functions.

---

## Step 12C

Status:

```text
Later
```

Purpose:

- Integrate Workday into the main CareerSignal pipeline.

Rules:

- This is when Workday touches SQLite, email, Excel, and Power BI.
- Do not do it during Step 12B.

---

# 17. Important Commands

## Check Project State

```bash
cat docs/CareerSignal_Project_State.md
```

## Greenhouse Preview

```bash
python scripts/collect_greenhouse_jobs.py --preview
```

## Greenhouse Send

```bash
python scripts/collect_greenhouse_jobs.py --send
```

## Excel Export

```bash
python scripts/export_to_excel.py
```

## Workday Raw Preview

```bash
python scripts/preview_workday_jobs.py
```

## Workday Normalized Preview

Command shape:

```bash
python scripts/preview_workday_normalized_jobs.py \
  --api-url "PASTE_WORKDAY_API_URL_HERE" \
  --company-name "Example Company" \
  --job-url-base "PASTE_PUBLIC_WORKDAY_CAREER_BASE_URL_HERE" \
  --limit 10
```

PowerShell shape:

```powershell
python scripts/preview_workday_normalized_jobs.py `
  --api-url "PASTE_WORKDAY_API_URL_HERE" `
  --company-name "Example Company" `
  --job-url-base "PASTE_PUBLIC_WORKDAY_CAREER_BASE_URL_HERE" `
  --limit 10
```

---

# 18. Important Grep Checks

Use these checks to catch old names, broken imports, or accidental integration.

## Check for old database path

```bash
grep -RIn "data/jobs.db" .
```

Expected:

```text
No results
```

## Check for official database path

```bash
grep -RIn "data/careersignal.db" .
```

Expected:

Relevant files may mention this.

## Check for database insertion calls

```bash
grep -RIn "insert_or_update_jobs" .
```

During Step 12B:

- Existing pipeline files may contain this.
- New Workday normalization files should not call it.

## Check for old or duplicate function names

```bash
grep -RIn "get_new_jobs\|send_daily_report\|jobs.db" .
```

If old names appear, review them carefully.

## Check Workday isolation during Step 12B

```bash
grep -RIn "insert_or_update_jobs\|build_and_send_daily_report\|score_job\|export_to_excel" src/careersignal/collectors scripts/preview_workday_normalized_jobs.py
```

Expected during Step 12B:

```text
No results
```

Or no concerning results.

## Check Greenhouse still works

```bash
python scripts/collect_greenhouse_jobs.py --preview
```

Expected:

Greenhouse preview still runs.

---

# 19. Git Workflow

Before changes:

```bash
git status
```

Review changes:

```bash
git diff
```

Stage specific files:

```bash
git add path/to/file
```

Commit:

```bash
git commit -m "Clear commit message"
```

Push:

```bash
git push
```

After commit:

```bash
git status
```

Expected clean result:

```text
nothing to commit, working tree clean
```

Rules:

- Commit each logical step separately.
- Do not mix unrelated changes in one commit.
- Do not commit temporary files.
- Do not commit the SQLite database unless intentionally deciding to track it.
- Do not commit local secrets, API keys, passwords, or `.env` files.

---

# 20. Git Commit History Guidance

Use commit messages like:

```text
Add company config loader
Add Greenhouse job collector
Normalize job data
Add SQLite job storage
Add new job detection
Add daily email report
Add logging and error handling
Add Excel export
Update Power BI dashboard
Add Workday proof of concept
Add Workday job normalization
Integrate Workday collector
```

For Step 12B, preferred commit message:

```text
Add Workday job normalization
```

---

# 21. Naming Rules

Preserve these official names.

## Database

```python
initialize_database()
insert_or_update_jobs(jobs)
get_all_jobs()
get_jobs_first_seen_in_last_24_hours()
insert_run_log(...)
```

## Match Scoring

```python
score_job(job)
```

## Email Report

```python
build_and_send_daily_report(summary, new_jobs, failed_sources, test_mode=True)
```

## Greenhouse Runner

```bash
python scripts/collect_greenhouse_jobs.py --preview
python scripts/collect_greenhouse_jobs.py --send
```

## Excel Export

```text
scripts/export_to_excel.py
exports/careersignal_export.xlsx
```

## Database Path

```text
data/careersignal.db
```

Do not use:

```text
data/jobs.db
```

---

# 22. Anti-Backtracking Rules

Before adding or changing code:

1. Check this project state file.
2. Check existing function names.
3. Check existing file names.
4. Search before inventing a new name.
5. Do not rename working functions casually.
6. Do not create duplicate scripts that do almost the same thing.
7. Do not change database paths.
8. Do not change output paths unless the whole pipeline is updated.
9. Do not touch Greenhouse when working on isolated Workday normalization.
10. Do not integrate before the isolated step works.

Useful search command:

```bash
grep -RIn "function_or_file_name_here" .
```

---

# 23. Separation of Concerns

Keep responsibilities separate.

## Collectors

Collectors should:

- Fetch jobs.
- Normalize jobs.
- Return normalized dictionaries.

Collectors should not:

- Send emails.
- Export Excel files.
- Update Power BI.
- Handle dashboard logic.

## Database Module

Database code should:

- Initialize database.
- Insert or update jobs.
- Query jobs.
- Log runs.

Database code should not:

- Fetch jobs from ATS platforms.
- Send emails.
- Build dashboards.

## Email Module

Email code should:

- Build email content.
- Send reports.
- Support test mode.

Email code should not:

- Fetch jobs.
- Normalize jobs.
- Directly scrape ATS platforms.

## Export Script

Excel export should:

- Read from SQLite.
- Create Excel output.
- Save to the official export path.

Excel export should not:

- Fetch jobs from ATS platforms.
- Send emails.

## Power BI

Power BI should:

- Read the Excel export.
- Visualize job data.

Power BI should not:

- Be required for job collection.
- Be required for normalization.
- Be required for email reports.

---

# 24. Current Known Good Commands

These commands should remain valid.

```bash
python scripts/collect_greenhouse_jobs.py --preview
python scripts/collect_greenhouse_jobs.py --send
python scripts/export_to_excel.py
```

After Step 12B, this should also work:

```bash
python scripts/preview_workday_normalized_jobs.py \
  --api-url "PASTE_WORKDAY_API_URL_HERE" \
  --company-name "Example Company" \
  --job-url-base "PASTE_PUBLIC_WORKDAY_CAREER_BASE_URL_HERE" \
  --limit 10
```

---

# 25. Files That Should Not Be Changed During Step 12B

Unless there is a specific bug unrelated to Workday normalization, do not change these during Step 12B:

```text
src/careersignal/database.py
src/careersignal/match_scoring.py
src/careersignal/email_report.py
scripts/collect_greenhouse_jobs.py
scripts/export_to_excel.py
config/company_config.csv
reports/careersignal_dashboard.pbix
exports/careersignal_export.xlsx
data/careersignal.db
```

Step 12B should mainly affect:

```text
src/careersignal/collectors/__init__.py
src/careersignal/collectors/workday.py
scripts/preview_workday_normalized_jobs.py
docs/CareerSignal_Project_State.md
```

---

# 26. Files That May Be Changed During Step 12C

Step 12C may affect:

```text
config/company_config.csv
scripts/collect_greenhouse_jobs.py
src/careersignal/collectors/workday.py
src/careersignal/database.py
src/careersignal/match_scoring.py
src/careersignal/email_report.py
scripts/export_to_excel.py
exports/careersignal_export.xlsx
reports/careersignal_dashboard.pbix
```

But only after Step 12B normalization is working.

---

# 27. Portfolio Purpose

CareerSignal should look useful to employers because it shows:

- Python scripting.
- API/data fetching.
- CSV config loading.
- Data normalization.
- SQLite database design.
- New record detection.
- Error handling.
- Logging.
- Email reporting.
- Excel export.
- Power BI dashboarding.
- Git/GitHub workflow.
- Project documentation.
- Incremental development.
- Real-world business use case.

This project is especially meant to support applications for roles involving:

- Accounting.
- Finance.
- FP&A.
- Business analysis.
- Data analysis.
- Operations analysis.
- Reporting.
- Entry-level analyst work.

---

# 28. README vs Project State

## README.md

Purpose:

- Public project overview.
- Recruiter-friendly.
- Explains what the project does.
- Explains how to run main commands.
- Explains tech stack.
- Shows project value.

Tone:

```text
Clean, professional, concise.
```

## docs/CareerSignal_Project_State.md

Purpose:

- Internal development source of truth.
- Tracks official names.
- Tracks step status.
- Prevents accidental backtracking.
- Helps continue work across ChatGPT sessions.

Tone:

```text
Practical, detailed, boring on purpose.
```

The README should not become bloated with every internal rule.

The project state file can be detailed because it is meant for development control.

---

# 29. Current Status Summary

Current status:

```text
Step 12A is done.
Step 12B is active.
Step 12C is later.
```

Current goal:

```text
Normalize Workday jobs into the official CareerSignal job shape.
```

Current guardrail:

```text
Do not integrate Workday into the main pipeline yet.
```

Current success condition:

```text
A preview script prints normalized Workday jobs, and every job has the official fields exactly.
```

---

# 30. Final Rule

When unsure, do the boring safe thing:

```text
Search existing names.
Preserve working functions.
Keep the current step isolated.
Test before integrating.
Commit cleanly.
```

Do not get clever and accidentally create CareerSignal 2: Electric Dumbass.