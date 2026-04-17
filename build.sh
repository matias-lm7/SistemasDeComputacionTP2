#!/bin/bash
set -e  

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$ROOT_DIR/src"
VENV_DIR="$ROOT_DIR/venv"
LIB_NAME="main.so"

echo "[1/5] Creando entorno virtual de Python..."

if [ ! -d "$VENV_DIR" ]; then
  if ! python3 -m venv "$VENV_DIR"; then
    echo "Error: No se pudo crear el entorno virtual. Asegúrate de tener instalado python3-venv."
    echo "Para instalarlo: sudo apt install python3-venv"
    exit 1
  fi
else
  echo "El entorno virtual ya existe."
fi

source "$VENV_DIR/bin/activate"
echo "Entorno virtual activado."

echo "[2/5] Instalando dependencias de Python..."
pip install --upgrade pip
pip install flask requests matplotlib numpy plotly
echo "Dependencias instaladas."

echo "[3/5] Compilando ensamblador de 32 bits..."
nasm -f elf32 "$SRC_DIR/convert.asm" -o "$SRC_DIR/convert.o"

echo "[4/5] Compilando y enlazando C + ASM en $LIB_NAME (32 bits)..."
gcc -m32 -fPIC -shared "$SRC_DIR/main.c" "$SRC_DIR/convert.o" -o "$SRC_DIR/$LIB_NAME"

echo "[5/5] Compilación completa. Librería compartida creada en: $SRC_DIR/$LIB_NAME"
ls -lh "$SRC_DIR/$LIB_NAME"
