@echo off
title Nebula Builder
color 0A

echo.
echo  ======================================
echo   Building Nebula.exe ...
echo  ======================================
echo.

pip install -q -r requirements.txt

pyinstaller ^
  --onefile ^
  --console ^
  --name Nebula ^
  --hidden-import win32timezone ^
  --hidden-import pyttsx3.drivers ^
  --hidden-import pyttsx3.drivers.sapi5 ^
  --hidden-import comtypes ^
  --hidden-import comtypes.client ^
  --hidden-import scipy.io.wavfile ^
  --hidden-import sounddevice ^
  --hidden-import numpy ^
  --hidden-import wmi ^
  --hidden-import pythoncom ^
  --hidden-import pywin32 ^
  --collect-submodules pyttsx3 ^
  --collect-submodules comtypes ^
  nebula/main.py

echo.
echo  ======================================
echo   Done!  EXE is at:  dist\Nebula.exe
echo  ======================================
echo.
pause