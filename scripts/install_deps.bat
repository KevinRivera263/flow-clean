@echo off
cd /d %~dp0\..

call venv\Scripts\activate

echo ========================================
echo Instalando dependencias...
echo ========================================

pip install -r requirements.txt

echo.
echo Proceso finalizado.
exit