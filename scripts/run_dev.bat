@echo off
cd /d %~dp0\..

call venv\Scripts\activate

echo ========================================
echo Iniciando Flow Clean en modo desarrollo...
echo ========================================

python src\main.py

exit