@echo off
:: ═══════════════════════════════════════════════════════════
::  AUTO STOCK UPDATER — Runs daily via Windows Task Scheduler
::  Fetches latest data and refreshes Power BI CSVs
:: ═══════════════════════════════════════════════════════════

:: ── Edit these paths ─────────────────────────────────────
SET PYTHON_PATH=python
SET SCRIPT_DIR=%~dp0
SET SCRIPT="%SCRIPT_DIR%fetch_clean_stocks.py"
SET LOG_FILE="%SCRIPT_DIR%powerbi_data\scheduler.log"

:: ── Run pipeline ─────────────────────────────────────────
echo [%DATE% %TIME%] Starting stock pipeline... >> %LOG_FILE%
%PYTHON_PATH% %SCRIPT% >> %LOG_FILE% 2>&1

IF %ERRORLEVEL% EQU 0 (
    echo [%DATE% %TIME%] SUCCESS >> %LOG_FILE%
) ELSE (
    echo [%DATE% %TIME%] FAILED with code %ERRORLEVEL% >> %LOG_FILE%
)
