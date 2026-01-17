@echo off
echo ==========================================
echo      Omni-Retail System Setup & Run
echo ==========================================

IF "%GOOGLE_API_KEY%"=="" (
    echo [WARNING] GOOGLE_API_KEY is not set!
    echo Please set it using: set GOOGLE_API_KEY=AIzaSyAYG46ctTLxyti5S0K_XuNqhejd0A13Opc
    echo The system may fail without it.
    pause
)

echo [1/4] Installing Python Dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

echo [2/4] Generating Synthetic Data...
python setup_dbs.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo [3/4] Installing Frontend Dependencies...
cd omni-retail-web
call npm install
cd ..
if %errorlevel% neq 0 exit /b %errorlevel%

echo [4/4] Starting System...
call run_all.bat
