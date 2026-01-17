@echo off
set NEXT_TURBO=0
echo [STATUS] Cleaning up existing sessions...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /F /PID %%a 2>nul
echo [STATUS] Starting Omni-Retail Ecosystem...

:: Start Backend
start "OmniBackend" cmd /k "python src/server.py"

:: Start Frontend
echo [STATUS] Starting Frontend UI...
npm run dev

echo Ecosystem is active.
