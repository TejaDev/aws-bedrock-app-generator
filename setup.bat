@echo off
REM AWS Bedrock App Generator - Windows Setup Script
REM This script sets up the project for Windows environments

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   AWS Bedrock App Generator - Setup (Windows)
echo ============================================================
echo.

REM Check Python version
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo DONE: Python %PYTHON_VERSION% found
echo.

REM Check AWS credentials
echo Step 2: Checking AWS credentials...
if not defined AWS_ACCESS_KEY_ID (
    if not exist "%USERPROFILE%\.aws\credentials" (
        echo ERROR: AWS credentials not configured
        echo Please configure AWS credentials:
        echo   1. Run: aws configure
        echo   2. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        echo   3. Create %%USERPROFILE%%\.aws\credentials file
        pause
        exit /b 1
    )
)
echo DONE: AWS credentials found
echo.

REM Create virtual environment
echo Step 3: Setting up Python virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo DONE: Virtual environment created
) else (
    echo INFO: Virtual environment already exists
)
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat
echo DONE: Virtual environment activated
echo.

REM Install dependencies
echo Step 4: Installing dependencies...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -q -r requirements.txt
echo DONE: Dependencies installed
echo.

REM Verify installation
echo Step 5: Verifying installation...
python -c "import boto3; print('  boto3: OK')" 2>nul && (echo DONE: boto3 installed) || (echo WARNING: boto3 check failed)
python -c "import adaptive_app_gen; print('  adaptive_app_gen: OK')" 2>nul && (echo DONE: adaptive_app_gen module OK) || (echo WARNING: adaptive_app_gen check failed)
echo.

echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Activate environment: .venv\Scripts\activate.bat
echo   2. Generate an app:     python cli.py --help
echo   3. Read docs:           type QUICKSTART.md
echo.
pause
