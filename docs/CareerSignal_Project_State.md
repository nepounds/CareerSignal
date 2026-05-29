# CareerSignal Project State

This file is the source of truth for CareerSignal coding help.

Before suggesting code changes, read this file and preserve the existing project structure, file names, function names, database path, and completed work.

Do not recreate files that already exist unless explicitly instructed.

Do not rename working functions unless absolutely necessary.

Do not add compatibility wrappers or aliases unless explicitly approved.

Prefer updating dependent scripts to use the current official names.

---

## Project Name

`CareerSignal`

CareerSignal is a Python portfolio project that monitors target company career pages, collects job postings, stores results in SQLite, scores jobs against target criteria, exports Excel reports, sends email summaries, and powers a Power BI dashboard.

---

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
8. Match scoring
9. Error handling and logging
10. Excel export
11. Power BI dashboard
    12A. Workday proof of concept
    12B. Workday normalization
    12C. Workday integration into the main pipeline
12. ATS Coverage Audit started, with unresolved follow-up items
13. Filtering Strategy completed
14. Match Scoring Refinement is in progress or next, depending on current chat status

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
```

---

## Current Database Path

Use:

```text
data/careersignal.db
```

Do not use:

```text
data/jobs.db
```

Search check:

```bash
grep -RIn "data/jobs.db" .
```

PowerShell equivalent:

```powershell
Select-String -Path .\* -Pattern "data/jobs.db" -Recurse
```

---

## Existing Project Structure

Preserve this structure.

```text
CareerSignal/
├── config/
│   ├── company_config.csv
│   ├── company_ats_audit.csv
│   └── match_rules.json or match_rules.csv if created during Step 15
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
│   └── careersignal.log
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
│   └── other preview/test scripts created during Workday or scoring steps
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
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

Some generated files may be ignored by Git, including `.env`, logs, generated database files, and generated exports.

---

## Existing Files That Should Not Be Recreated Blindly

These files already exist or have already been worked on.

Do not tell the user to create them from scratch unless the user says they are missing.

```text
README.md
requirements.txt
.env.example
.gitignore
config/company_config.csv
data/careersignal.db
docs/CareerSignal_Project_State.md
docs/filtering_strategy.md
exports/careersignal_export.xlsx
logs/careersignal.log
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
```

If a future step needs to modify one of these files, explain:

1. Why the file needs to change
2. What depends on it
3. What exact code is being changed
4. How to test that nothing broke

---

## Official Normalized Job Shape

Every collector must return job dictionaries with this exact structure:

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

Do not change this shape without explicitly discussing the database, scoring, email, Excel, and Power BI impacts.

---

## Supported ATS Types

Currently supported:

```text
greenhouse
workday
```

Future possible connectors, based on ATS audit needs:

```text
lever
ashby
smartrecruiters
icims
generic_html
```

Only build future connectors if the master company list shows enough need.

Do not build random ATS connectors just because they exist.

---

## Company Config

Primary company config file:

```text
config/company_config.csv
```

Current or expected config fields:

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

Supported `ats_type` values currently:

```text
greenhouse
workday
```

If a new ATS connector is added later, it should use a clean `ats_type` value in this same config file.

---

## Official Function Names

### Database

File:

```text
src/careersignal/database.py
```

Use:

```python
initialize_database()
insert_or_update_jobs(jobs)
get_all_jobs()
get_jobs_first_seen_in_last_24_hours()
insert_run_log(...)
```

Do not use old names:

```python
create_tables()
insert_normalized_jobs()
fetch_all_jobs()
```

Search checks:

```bash
grep -RIn "create_tables" .
grep -RIn "insert_normalized_jobs" .
grep -RIn "fetch_all_jobs" .
```

---

### Match Scoring

File:

```text
src/careersignal/match_scoring.py
```

Official scoring function:

```python
score_job(job)
```

Do not rename this function.

Step 15 may refine the internals of match scoring, add match reasons, or move editable scoring rules into config, but it should preserve `score_job(job)` unless explicitly approved.

---

### Email Report

File:

```text
src/careersignal/email_report.py
```

Official email report function:

```python
build_and_send_daily_report(summary, new_jobs, failed_sources, test_mode=True)
```

Do not rename this function.

Email reporting should continue to support preview/test mode and send mode.

---

### Logging

File:

```text
src/careersignal/logging_config.py
```

Logs should go to:

```text
logs/careersignal.log
```

A failed company source should not crash the whole run.

Failed sources should be tracked and included in the daily email report where possible.

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

Step 11 was completed, though dashboard polish may still be improved later.

---

## Current README Status

README has been updated after Step 14 or should be updated to reflect:

* Greenhouse support
* Workday support
* SQLite database
* new job detection
* match scoring
* email report
* logging
* Excel export
* Power BI dashboard
* ATS coverage audit
* filtering strategy beyond accounting/finance

README polish is still planned for Step 18.

Do not treat README as final portfolio polish yet.

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

### Step 13 Follow-Up Items

These need to be revisited later:

1. Recheck companies with unclear or unreliable career URLs.
2. Confirm ATS type manually for companies marked unknown.
3. Identify which companies are truly Workday or Greenhouse and can be added now.
4. Identify which unsupported ATSs appear often enough to justify new connectors.
5. Do not build connectors for one-off systems unless they are high-value companies.
6. Review companies where search/Gemini produced bad or incorrect career pages.
7. Review companies with redirects, proprietary systems, or confusing career portals.
8. Decide whether `generic_html` is worth building for smaller firms or custom pages.
9. Decide whether Lever, Ashby, SmartRecruiters, or iCIMS should be the next connector based on actual company count.
10. Keep low-priority or unclear companies in an audit file rather than forcing them into `company_config.csv`.

### Step 13 Decision Rule

Only build a new connector if:

```text
- Multiple target companies use the ATS, or
- One very high-priority company uses it, and
- The site appears technically feasible to collect from
```

### Step 13 Buckets

Use these buckets in the audit:

```text
Ready now:
- workday
- greenhouse

Likely future connector:
- lever
- ashby
- smartrecruiters
- icims
- generic_html

Unclear / revisit:
- proprietary portals
- bad career URLs
- redirects
- unknown ATS
- custom career pages

Probably skip for now:
- one-off systems
- broken pages
- companies with no realistic target roles
- companies that require manual searching only
```

### Suggested Step 13 Audit File

Use or create:

```text
config/company_ats_audit.csv
```

Suggested fields:

```text
company_name
career_url
ats_type
supported_now
connector_needed
connector_priority
status
notes
```

Do not assume this file is complete.

---

## Step 14 Filtering Strategy Status

Step 14 is complete.

CareerSignal is not accounting-only.

The filtering strategy supports multiple job-search lanes:

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
Other realistic roles that fit the user’s background
```

Filtering strategy should define:

```text
strong title matches
maybe title matches
weak/stretch title matches
excluded/heavily penalized titles
strong locations
acceptable locations
remote/hybrid rules
North Carolina rules
nearby city/region rules
seniority rules
experience rules
sector-specific rules
```

Filtering strategy is planning/config.

Match scoring refinement is implementation.

---

## Step 15 Match Scoring Refinement Status

Step 15 should use the Step 14 filtering strategy.

Important distinction:

```text
Step 14 = decide what CareerSignal should care about
Step 15 = assign scoring weights and implement/refine scoring logic
```

Step 15 should not recreate existing files if they already exist.

Step 15 should preserve:

```python
score_job(job)
```

Step 15 may update:

```text
src/careersignal/match_scoring.py
scripts/test_match_scoring.py
config/match_rules.json or config/match_rules.csv, if created
README.md, only lightly if needed
```

Step 15 should keep scores from 0 to 100.

Suggested score bands:

```text
80–100: Strong match
60–79: Possible match
40–59: Weak/stretch match
0–39: Low match or likely skip
```

Step 15 should support multiple lanes, not just accounting and finance.

---

## Current Roadmap


### Step 16: Daily Automation

Use Windows Task Scheduler to run CareerSignal automatically and send the daily email report.

### Step 17: Application Tracker

Add saved/applied/interview/rejected/offer/skipped/closed tracking and response-rate reporting.

Nice-to-have, not required for first resume-ready version.

### Step 18: GitHub + Portfolio Polish

Clean README, screenshots, sample outputs, final testing, resume bullets, and portfolio presentation.

Required before adding to resume.

### Step 19: Optional Streamlit UI

Only if a prettier local interface is wanted later.

Nice-to-have, not required.

---

## Must-Do vs Nice-to-Have

Must-do path:

```text
16: Daily Automation
18: GitHub + Portfolio Polish
```

Nice-to-have:

```text
17: Application Tracker
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

If the main runner has been renamed or split later, update this file.

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

---

## Git Guidance

After project-state updates:

```bash
git add docs/CareerSignal_Project_State.md
git commit -m "Update CareerSignal project state"
git push
```

After feature steps, use specific commit messages, such as:

```bash
git add .
git commit -m "Refine match scoring rules"
git push
```

Avoid committing:

```text
.env
logs/
data/careersignal.db if intentionally ignored
exports/careersignal_export.xlsx if intentionally ignored
temporary test files
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
10. Keep the response beginner-friendly and step-by-step.
