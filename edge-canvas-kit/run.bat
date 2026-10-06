@echo off
REM run.bat -- start the edge-canvas-kit on Windows (ASUS A15). Needs Python 3 + a browser.
REM   run.bat          this device only -> http://127.0.0.1:8765
REM   run.bat --lan    home network (prints a token URL)
REM   run.bat --check  self-tests
cd /d "%~dp0"
set PY=python
where py >nul 2>nul && set PY=py -3
if "%1"=="--check" (
  %PY% selfcheck.py --quick
  goto :eof
)
start "" "http://127.0.0.1:8765/"
%PY% server.py %*
