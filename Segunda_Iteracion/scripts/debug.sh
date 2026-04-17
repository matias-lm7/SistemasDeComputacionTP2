#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/src"
DEBUG_DIR="$ROOT_DIR/debug"
BUILD_DIR="$ROOT_DIR/build"

echo "Creando directorios de build y debug..."
mkdir -p "$BUILD_DIR" "$DEBUG_DIR"

echo "1/2) Compilando ensamblador de 32 bits convert.asm ➜ $BUILD_DIR/convert.o"
nasm -f elf32 -g -F dwarf \
     "$SRC_DIR/convert.asm" \
     -o "$BUILD_DIR/convert.o"

echo "2/2) Compilando debug/debug.c + enlazando ➜ $DEBUG_DIR/debug"
gcc -m32 -g -fno-omit-frame-pointer -no-pie \
    "$ROOT_DIR/debug/debug.c" \
    "$BUILD_DIR/convert.o" \
    -o "$DEBUG_DIR/debug"

echo "Ejecutable para debug listo en: $DEBUG_DIR/debug"

gdb -tui ./debug/debug
