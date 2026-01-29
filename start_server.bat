@echo off
chcp 65001 >nul
title YouTube 다운로더 서버

echo ====================================================
echo YouTube 다운로더 서버 시작 중...
echo ====================================================
echo.

REM 현재 디렉토리 확인
echo 현재 경로: %cd%
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python을 설치하고 다시 실행하세요.
    pause
    exit /b 1
)

echo Python 확인 완료
echo.

REM youtube_downloader.py 파일 존재 확인
if not exist "youtube_downloader.py" (
    echo [오류] youtube_downloader.py 파일을 찾을 수 없습니다.
    echo 파일이 현재 폴더에 있는지 확인하세요.
    pause
    exit /b 1
)

echo youtube_downloader.py 파일 확인 완료
echo.

REM 필요한 패키지 확인
echo 필요한 패키지 확인 중...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Flask가 설치되어 있지 않습니다. 설치 중...
    pip install flask
)

python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 (
    echo yt-dlp가 설치되어 있지 않습니다. 설치 중...
    pip install yt-dlp
)

echo.
echo ====================================================
echo 서버를 시작합니다...
echo 종료하려면 Ctrl+C를 누르세요
echo ====================================================
echo.

REM 1초 대기 (안전성)
timeout /t 1 /nobreak >nul

REM 서버 실행
python youtube_downloader.py

REM 서버 종료 시
echo.
echo ====================================================
echo 서버가 종료되었습니다.
echo ====================================================
pause
