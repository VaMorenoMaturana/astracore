@echo off
cd /d "%~dp0"

set VENV_DIR=venv

if not exist "%VENV_DIR%" (
    python -m venv %VENV_DIR%
)

call "%VENV_DIR%\Scripts\activate.bat"

echo Instalando/actualizando dependencias...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt

echo Aplicando migraciones...
python manage.py migrate

echo Iniciando servidor local en http://127.0.0.1:8000 ...
python manage.py runserver

pause
