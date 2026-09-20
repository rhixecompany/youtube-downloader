@echo off
REM YouTube CLI wrapper — Windows batch (.bat)
REM Interactive by default; non-interactive with --non-interactive
REM Example interactive: youtube-downloader.bat
REM Example non-interactive: youtube-downloader.bat --non-interactive "https://youtube.com/watch?v=xxx"

setlocal enabledelayedexpansion

REM Check for --non-interactive flag and URL argument
set NON_INTERACTIVE=0
set PROVIDED_URL=

REM Loop through arguments
:loop_args
if "%~1"=="" goto :done_args
if "%~1"=="--non-interactive" (
    set NON_INTERACTIVE=1
) else (
    if not defined PROVIDED_URL (
        set PROVIDED_URL=%~1
    )
)
shift
goto loop_args
:done_args

if %NON_INTERACTIVE%==1 (
    if defined PROVIDED_URL (
        echo Running non-interactive mode with URL: %PROVIDED_URL%
        python main_noplaylist.py %PROVIDED_URL%
    ) else (
        echo Non-interactive mode selected but no URL provided. Please pass URL after --non-interactive.
        exit /b 1
    )
) else (
    if defined PROVIDED_URL (
        echo URL provided: %PROVIDED_URL%
        python main_noplaylist.py %PROVIDED_URL%
    ) else (
        echo Running interactive mode (default). Enter a video URL:
        set /p url=URL:
        if "!url!"=="" (
            echo No URL entered. Exiting.
            exit /b 1
        )
        python main_noplaylist.py !url!
    )
)
