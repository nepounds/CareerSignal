@echo off
cd /d "C:\Users\Nathan and Steph\Documents\CareerSignal"

if not exist logs mkdir logs

set PYTHONPATH=src

echo ========================================== >> logs\weekly_application_tracker_email.log
echo CareerSignal weekly application tracker started at %date% %time% >> logs\weekly_application_tracker_email.log

python scripts\send_weekly_application_tracker_email.py --send >> logs\weekly_application_tracker_email.log 2>&1

echo CareerSignal weekly application tracker finished at %date% %time% >> logs\weekly_application_tracker_email.log
echo. >> logs\weekly_application_tracker_email.log