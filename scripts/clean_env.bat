@echo off
echo Cleaning Nebula development environment...

REM Python cache
rmdir /s /q apps\backend\__pycache__ 2>nul
rmdir /s /q apps\backend\nebula\__pycache__ 2>nul

REM PyInstaller build
rmdir /s /q apps\backend\build 2>nul
rmdir /s /q apps\backend\dist 2>nul
del /f /q apps\backend\*.spec 2>nul

REM Node / Electron
rmdir /s /q apps\desktop\node_modules 2>nul
rmdir /s /q apps\desktop\ui\node_modules 2>nul
rmdir /s /q apps\desktop\dist 2>nul
rmdir /s /q apps\desktop\ui\dist 2>nul

echo Environment cleaned successfully.
pause
