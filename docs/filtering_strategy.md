# CareerSignal Filtering Strategy

## Purpose

This document defines the broad filtering strategy for CareerSignal.

Step 14 defines what kinds of jobs should be considered relevant.

Step 15 will later convert these rules into numeric scoring weights inside:

```text
src/careersignal/match_scoring.py
```

Current goal: keep the filter broad enough to avoid missing good jobs, even if some unrelated jobs slip into the daily email.

## Source of Truth

Use the official project state document before making code changes:

```text
docs/CareerSignal_Project_State.md
```

Official database path:

```text
data/careersignal.db
```

Do not use:

```text
data/jobs.db
```

Official scoring function:

```python
score_job(job)
```

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

## Step 14 vs. Step 15

### Step 14: Filtering Strategy

Defines:

- job lanes
- title keyword buckets
- location buckets
- seniority buckets
- experience rules
- sector-specific rules
- exclusions

This step should mainly create documentation and config files.

### Step 15: Match Scoring Refinement

Turns the Step 14 strategy into actual scoring logic.

Step 15 may update:

```text
src/careersignal/match_scoring.py
```

Step 14 should not rewrite match scoring unless absolutely necessary.

## Main Job Lanes

CareerSignal should support these lanes:

1. Accounting
2. Finance
3. General Analyst
4. Business Analyst
5. Operations Analyst
6. Compliance
7. Data / Reporting
8. Supervisor / Plant / Utility
9. Government / Public Sector Adjacent
10. Manufacturing / Plant Operations
11. Consulting / Advisory
12. Other Realistic Stretch Roles

## Filtering Philosophy

CareerSignal should be inclusive.

It is better to include a few unrelated jobs in the email than to miss a good job.

Broad words like these should be allowed:

```text
associate
analyst
specialist
coordinator
assistant
staff
accountant
finance
accounting
operations
compliance
reporting
data
business
plant
supervisor
utility
water
wastewater
```

The system should only heavily penalize or exclude obvious bad fits.

## Title Buckets

### Strong Title Matches

Strong matches usually belong directly to one of the target job lanes.

Examples:

```text
staff accountant
junior accountant
accounting analyst
accounting associate
audit associate
tax associate
financial analyst
finance analyst
fp&a analyst
budget analyst
business analyst
operations analyst
compliance analyst
reporting analyst
data analyst
plant supervisor
operations supervisor
production supervisor
water treatment supervisor
wastewater supervisor
utility supervisor
```

### Maybe Title Matches

Maybe matches are broad but useful.

Examples:

```text
associate
analyst
specialist
coordinator
assistant
staff
finance associate
accounting specialist
billing specialist
payroll specialist
operations specialist
business specialist
compliance specialist
regulatory specialist
reporting specialist
data specialist
project coordinator
program coordinator
claims analyst
quality specialist
implementation analyst
```

### Weak / Stretch Title Matches

Weak matches may still be useful, especially for realistic stretch roles.

Examples:

```text
customer operations
client operations
business support
administrative analyst
case analyst
grant analyst
records analyst
documentation specialist
facilities coordinator
environmental technician
field operations specialist
scheduler
dispatcher
team lead
shift lead
```

### Exclude or Heavily Penalize

These should usually score poorly.

Examples:

```text
director
senior director
vice president
vp
chief financial officer
chief accounting officer
chief operating officer
executive
partner
principal
senior manager
software engineer
software developer
data engineer
machine learning engineer
data scientist
registered nurse
rn
physician
therapist
pharmacist
teacher
professor
driver
warehouse associate
retail associate
food service
security officer
```

## Location Buckets

### Strong Locations

```text
north carolina
nc
raleigh
durham
chapel hill
research triangle
triangle
cary
morrisville
apex
garner
clayton
smithfield
selma
benson
goldsboro
wilson
kinston
clinton
franklinton
greenville
rocky mount
fayetteville
wake county
johnston county
wayne county
```

### Acceptable Locations

```text
charlotte
greensboro
winston-salem
high point
burlington
wilmington
new bern
jacksonville
remote - north carolina
remote, nc
hybrid - nc
remote - united states
united states remote
hybrid
```

### Remote and Hybrid Rules

Strong:

```text
remote - north carolina
remote, nc
hybrid - raleigh
hybrid - durham
hybrid - nc
```

Medium:

```text
remote - united states
united states remote
hybrid
```

Low or exclude:

```text
remote but restricted to another state
on-site outside north carolina
hybrid outside north carolina
```

## Seniority Buckets

### High Fit

```text
entry level
junior
trainee
associate
assistant
coordinator
staff
analyst
specialist
```

### Medium Fit

```text
senior analyst
senior accountant
experienced associate
supervisor
lead
```

### Low Fit

```text
manager
senior specialist
senior supervisor
```

### Exclude or Heavily Penalize

```text
senior manager
director
senior director
vice president
vp
chief
executive
partner
principal
```

## Experience Rules

### Strong Fit

```text
0-2 years
0 to 2 years
1-2 years
1 to 2 years
1-3 years
1 to 3 years
2-4 years
2 to 4 years
entry level
recent graduate
```

### Medium Fit

```text
3-5 years
3 to 5 years
2-5 years
2 to 5 years
```

### Penalty

```text
5+ years
5 or more years
7+ years
10+ years
manager experience required
supervisory experience required
```

### Credential Rules

Positive:

```text
bachelor
accounting degree
finance degree
business degree
related field
```

Penalty:

```text
cpa required
mba required
master's required
big 4 required
```

Neutral or mild positive:

```text
cpa preferred
mba preferred
public accounting preferred
```

## Sector-Specific Rules

### Public Accounting Firms

Good matches:

```text
audit associate
tax associate
assurance associate
advisory associate
risk advisory associate
client accounting services associate
```

Penalize:

```text
manager
senior manager
director
partner
principal
cpa required
```

### Corporate Accounting / Finance

Good matches:

```text
staff accountant
accounting analyst
financial analyst
finance analyst
cost accountant
budget analyst
billing analyst
revenue analyst
```

### Healthcare / Insurance

Good matches:

```text
claims analyst
compliance analyst
finance analyst
business analyst
reporting analyst
reimbursement analyst
provider data analyst
operations analyst
quality analyst
```

Penalize:

```text
nurse
rn
physician
therapist
pharmacist
clinical director
```

### Government / Public Sector

Good matches:

```text
budget analyst
accountant
finance officer
program analyst
administrative analyst
compliance analyst
utility analyst
public works analyst
procurement analyst
grant analyst
```

### Utilities / Water Operations

Good matches:

```text
water plant operator
wastewater plant operator
utility supervisor
water treatment supervisor
environmental compliance specialist
public works analyst
utility billing analyst
operations supervisor
plant supervisor
chief operator
```

### Manufacturing / Plant Operations

Good matches:

```text
production supervisor
plant supervisor
operations supervisor
quality analyst
inventory analyst
supply chain analyst
manufacturing analyst
cost accountant
production planner
materials analyst
```

Penalize:

```text
plant manager
general manager
maintenance mechanic
machine operator
forklift operator
warehouse associate
```

### Consulting / Advisory

Good matches:

```text
associate consultant
business analyst
risk advisory associate
technology risk associate
accounting advisory associate
operations consultant
implementation analyst
```

Penalize:

```text
mba required
travel 80%
manager
senior manager
```

## Example Scoring Outcomes for Step 15

### High-Fit Examples

```text
Staff Accountant | Raleigh, NC
Financial Analyst | Remote - North Carolina
Business Analyst | Durham, NC
Compliance Analyst | Raleigh, NC
Operations Analyst | Clayton, NC
Plant Supervisor | Smithfield, NC
Reporting Analyst | Remote - United States
```

### Medium-Fit Examples

```text
Senior Accountant | Raleigh, NC
Senior Business Analyst | Remote - United States
Operations Specialist | Charlotte, NC
Project Coordinator | Durham, NC
Procurement Analyst | Greensboro, NC
Quality Specialist | Wilson, NC
```

### Low-Fit Examples

```text
Finance Manager | Raleigh, NC
Senior Operations Manager | Remote - United States
Plant Manager | Goldsboro, NC
Business Analyst | Hybrid - Georgia
Data Analyst | On-site New York
```

### Excluded or Near-Excluded Examples

```text
Director of Finance | Raleigh, NC
VP of Operations | Remote
Software Engineer | Raleigh, NC
Registered Nurse | Durham, NC
Warehouse Associate | Clayton, NC
Retail Sales Associate | Raleigh, NC
Machine Learning Engineer | Remote
```

## Future Step 15 Notes

Step 15 should use this document and `config/match_rules.json` to update:

```text
src/careersignal/match_scoring.py
```

The scoring logic should probably reward:

- strong title matches
- acceptable title matches
- North Carolina locations
- remote or hybrid flexibility
- realistic seniority
- reasonable experience requirements
- accounting, finance, analyst, compliance, operations, data, utility, and plant relevance

The scoring logic should penalize:

- director, VP, executive, partner, and principal titles
- jobs outside North Carolina unless remote
- hard CPA requirements
- hard MBA requirements
- software engineering and clinical roles
- very high experience requirements