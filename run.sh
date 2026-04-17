#!/bin/bash
set -e 

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$ROOT_DIR/venv"
APP_FILE="$ROOT_DIR/src/main.py"

echo ""
echo "Iniciando la app Flask..."

if [ ! -d "$VENV_DIR" ]; then
  echo "Error: No se encontró el entorno virtual en $VENV_DIR"
  echo "Ejecutá primero el script de build."
  exit 1
fi

source "$VENV_DIR/bin/activate"
echo "Entorno virtual activado."

echo "Ejecutando: python $APP_FILE"
python "$APP_FILE"
