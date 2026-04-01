@echo off
cd /d %~dp0\..

call venv\Scripts\activate

echo ========================================
echo Limpiando compilaciones anteriores...
echo ========================================

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist FlowClean.spec del /f /q FlowClean.spec

echo ========================================
echo Generando EXE...
echo ========================================

pyinstaller --noconfirm --clean --onefile --windowed --name FlowClean --icon=assets\flowclean_icon.ico --add-data "assets;assets" src\main.py

echo.
echo EXE generado en dist\FlowClean.exe
exit