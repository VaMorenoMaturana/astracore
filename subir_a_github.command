#!/bin/zsh
set -e
cd "$(dirname "$0")"

echo "==> Estado actual del repositorio:"
git status

echo ""
read "MENSAJE?Escribe el mensaje del commit y presiona Enter: "

if [ -z "$MENSAJE" ]; then
  MENSAJE="Actualizacion rapida $(date '+%Y-%m-%d %H:%M')"
fi

git add -A
git commit -m "$MENSAJE" || echo "No hay cambios nuevos para commitear."
git push origin main

echo ""
echo "==> Listo. Cambios subidos a GitHub."
read "?Presiona Enter para cerrar esta ventana..."
