@echo off
title YouTube Downloader Server

echo ====================================================
echo YouTube Downloader Server Starting...
echo ====================================================
echo.

echo Current Path: %cd%
echo.

python --version
if errorlevel 1 (
    echo [ERROR] Python not installed
    pause
    exit /b 1
)

echo Python OK
echo.

if not exist "youtube_downloader.py" (
    echo [ERROR] youtube_downloader.py not found
    dir
    pause
    exit /b 1
)

echo File OK
echo.

echo Checking packages...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
)

python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 (
    echo Installing yt-dlp...
    pip install yt-dlp
)

echo.
echo ====================================================
echo Starting server...
echo Press Ctrl+C to stop
echo ====================================================
echo.

python youtube_downloader.py

if errorlevel 1 (
    echo.
    echo [ERROR] Server failed!
    pause
)

echo.
echo ====================================================
echo Server stopped
echo ====================================================
pause