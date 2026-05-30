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
    12A. Workday proof of concept
    12B. Workday normalization
    12C. Workday integration into the main pipeline
12. ATS Coverage Audit started, with unresolved follow-up items
13. Filtering Strategy completed
14. Match Scoring Refinement completed
15. Daily Automation runner added for Windows Task Scheduler

Current step:

```text
18: GitHub + Portfolio Polish
```

Skipped for now:

```text
17: Application Tracker
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

---

## Current README Status

README is being polished during Step 18 to present CareerSignal as a resume-ready Python/SQL career intelligence pipeline.

README should reflect:

* Greenhouse support
* Workday support
* SQLite database
* New job detection
* Match scoring
* Email report
* Logging
* Excel export
* Power BI dashboard
* ATS coverage audit
* Filtering strategy beyond accounting/finance
* Windows Task Scheduler automation
* Known limitations
* Future improvements
* Screenshot recommendations
* Final validation checklist
* Resume bullet options

After Step 18, README should be treated as the main GitHub-facing project overview.

---

## Current Roadmap

### Step 17: Application Tracker

Add saved/applied/interview/rejected/offer/skipped/closed tracking and response-rate reporting.

Nice-to-have, not required for first resume-ready version.

Skipped for now.

---

### Step 18: GitHub + Portfolio Polish

Clean README, screenshots, sample outputs, final testing, resume bullets, and portfolio presentation.

Current active step.

Required before heavily featuring the project on a resume.

---

### Step 19: Optional Streamlit UI

Only if a prettier local interface is wanted later.

Nice-to-have, not required.

---

## Step 18 GitHub + Portfolio Polish Status

Step 18 focuses on presentation and validation, not major feature development.

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
```
