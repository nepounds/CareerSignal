@echo off
setlocal

REM ============================================================
REM CareerSignal Daily Automation Runner
REM Runs the daily collector in send mode, then refreshes Excel.
REM ============================================================

REM Move into the CareerSignal project folder.
cd /d "C:\Users\Nathan and Steph\Documents\CareerSignal"

REM Make sure local project modules can be imported.
set PYTHONPATH=src

REM Create logs folder if it does not exist.
if not exist "logs" mkdir "logs"

REM Write a visible start marker to the scheduled task log.
echo ============================================================ >> "logs\scheduled_task.log"
echo CareerSignal daily run started at %date% %time% >> "logs\scheduled_task.log"

REM Activate the virtual environment if it exists.
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
    echo Virtual environment activated. >> "logs\scheduled_task.log"
) else (
    echo WARNING: .venv\Scripts\activate.bat not found. Using system Python. >> "logs\scheduled_task.log"
)

REM Run the main collector in send mode.
echo Running collector in send mode... >> "logs\scheduled_task.log"
python scripts\collect_greenhouse_jobs.py --send >> "logs\scheduled_task.log" 2>&1

REM Capture collector result.
if errorlevel 1 (
    echo ERROR: Collector failed at %date% %time% >> "logs\scheduled_task.log"
    exit /b 1
)

REM Run Excel export.
echo Running Excel export... >> "logs\scheduled_task.log"
python scripts\export_to_excel.py >> "logs\scheduled_task.log" 2>&1

REM Capture export result.
if errorlevel 1 (
    echo ERROR: Excel export failed at %date% %time% >> "logs\scheduled_task.log"
    exit /b 1
)

echo CareerSignal daily run finished successfully at %date% %time% >> "logs\scheduled_task.log"
echo. >> "logs\scheduled_task.log"

endlocal
exit /b 0