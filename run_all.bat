@echo off
echo Starting Omni-Retail System...

start "Omni-Backend" cmd /k "call run_backend.bat"

echo Waiting for backend...
timeout /t 5

echo Starting Frontend...
cd omni-retail-web
npm run dev
