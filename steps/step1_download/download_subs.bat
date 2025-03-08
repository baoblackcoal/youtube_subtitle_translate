@echo off
if "%~1"=="" (
    echo Usage: download_subs.bat [YouTube URL]
    exit /b 1
)
if not exist output mkdir output
echo Downloading subtitles from: %~1
echo Output directory: %CD%\output
yt-dlp --verbose --skip-download --write-auto-sub --sub-lang en --paths output --output "sub" "%~1"
if exist "output\sub.en.vtt" (
    echo Subtitles downloaded successfully to: %CD%\output\sub.en.vtt
) else (
    echo Failed to download subtitles
    exit /b 1
) 