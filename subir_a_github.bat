@echo off
cd /d "%~dp0"

git status

set /p MENSAJE="Escribe el mensaje del commit: "

if "%MENSAJE%"=="" set MENSAJE=Actualizacion rapida %date% %time%

git add -A
git commit -m "%MENSAJE%"
git push origin main

echo Listo. Cambios subidos a GitHub.
pause
