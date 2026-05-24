# CareerSignal

CareerSignal is a Python portfolio project that tracks job postings from target companies and sends alerts when new matching jobs appear.

## Project Goal

The goal of this project is to help job seekers monitor companies they care about instead of manually checking each career page every day.

## Planned Features

- Store a list of target companies
- Check company career pages for new job postings
- Filter jobs by location, title, and keywords
- Save discovered jobs in a local SQLite database
- Avoid sending duplicate alerts
- Send email alerts when new matching jobs are found

## Tech Stack

- Python
- SQLite
- Requests
- BeautifulSoup
- python-dotenv
- GitHub

## Project Structure

```text
CareerSignal/
├── config/
│   └── company_config.csv
├── scripts/
│   └── test_config_loader.py
├── src/
│   └── careersignal/
│       ├── __init__.py
│       ├── config_loader.py
│       └── main.py
├── data/
├── logs/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the project

```bash
python src/careersignal/main.py
```

Expected output:

```text
CareerSignal is running.
```

## Environment Variables

Copy `.env.example` to `.env` and fill in your real settings.

Do not commit `.env` to GitHub.

## Company Config

CareerSignal uses a CSV file to store target company information.

Config file location:

```text
config/company_config.csv
```

Current config fields:

- `company_name`
- `ats_type`
- `career_url`
- `target_locations`
- `keywords`
- `job_title_keywords`
- `excluded_keywords`
- `active`

The config loader is located here:

```text
src/careersignal/config_loader.py
```

To test the config loader in PowerShell:

```powershell
$env:PYTHONPATH="src"
python scripts/test_config_loader.py
```

The test should print all companies marked as active in `company_config.csv`.

## Current Status

Step 2 complete: company configuration file added, with a Python loader that reads active companies from the CSV.

## Future Improvements

- Add scraper for one test company
- Add SQLite database setup
- Add duplicate job detection
- Add email alerts
- Add scheduled runs