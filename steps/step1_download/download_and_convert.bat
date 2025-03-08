@echo off
if "%~1"=="" (
    echo Usage: download_and_convert.bat [YouTube URL]
    exit /b 1
)

python download_subs.py "%~1"
if errorlevel 1 (
    echo Failed to download subtitles
    exit /b 1
)

python convert_vtt_to_txt.py output/sub.en.vtt
if errorlevel 1 (
    echo Failed to convert subtitles
    exit /b 1
)

echo Process completed successfully 