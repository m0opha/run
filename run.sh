#!/bin/bash

# Variables
VENV=".env"
SCRIPT="run.py"
BIN_NAME="run.bin"
INSTALL_DIR="$HOME/.config/run"
SYMLINK="$HOME/bin/run"

# Crear entorno virtual
python3 -m venv "$VENV"
source "$VENV/bin/activate"

# Instalar dependencias
pip install --upgrade pip
pip install colorama nuitka

# Compilar con Nuitka
python3 -m nuitka \
  --standalone \
  --output-dir="$INSTALL_DIR" \
  --remove-output \
  --follow-imports \
  --lto=yes \
  --clang \
  --jobs=6 \
  --assume-yes-for-downloads \
  "$SCRIPT"

# Crear bin directory si no existe
mkdir -p "$HOME/bin"

# Crear symlink al ejecutable
ln -sf "$INSTALL_DIR/run.dist/$BIN_NAME" "$SYMLINK"

# Salir del entorno virtual
deactivate