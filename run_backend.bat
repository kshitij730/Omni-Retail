@echo off
echo Starting Omni-Retail Agent Backend...
cd /d "%~dp0"
call python -m uvicorn src.server:app --reload --host 0.0.0.0 --port 8000
pause
