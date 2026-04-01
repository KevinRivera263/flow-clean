@echo off
cd /d %~dp0\..

call venv\Scripts\activate

echo ========================================
echo Actualizando requirements.txt...
echo ========================================

pip freeze > requirements.txt

echo.
echo requirements.txt actualizado.

exit
