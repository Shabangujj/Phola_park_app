@echo off
REM start_app.bat — assumes venv is in phola_park_app\venv
REM Change path if your venv location is different.

REM Move to script directory (folder containing this .bat)
cd /d "%~dp0"

REM Activate the virtualenv (Windows)
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Could not find venv\Scripts\activate.bat — make sure virtualenv is at phola_park_app\venv
)

REM Run the app module
python -m phola_park_app.app

pause
