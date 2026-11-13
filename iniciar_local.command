#!/bin/zsh
set -e
cd "$(dirname "$0")"

VENV_DIR="venv"

echo "==> Verificando entorno virtual..."
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "==> Instalando/actualizando dependencias..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt

echo "==> Aplicando migraciones..."
python manage.py migrate

LAN_IP=""
for interface in en0 en1; do
  LAN_IP="$(ipconfig getifaddr "$interface" 2>/dev/null || true)"
  if [ -n "$LAN_IP" ]; then
    break
  fi
done

export DEV_ALLOWED_HOSTS="localhost,127.0.0.1"
if [ -n "$LAN_IP" ]; then
  export DEV_ALLOWED_HOSTS="$DEV_ALLOWED_HOSTS,$LAN_IP"
  echo "==> En esta Mac: http://127.0.0.1:8000"
  echo "==> En dispositivos de la misma red: http://$LAN_IP:8000"
else
  echo "==> No se pudo detectar la IP de red. El acceso por red podría no estar disponible."
  echo "==> En esta Mac: http://127.0.0.1:8000"
fi

echo "==> Iniciando servidor local para la red..."
python manage.py runserver 0.0.0.0:8000

echo ""
read "?Presiona Enter para cerrar esta ventana..."
