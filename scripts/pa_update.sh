#!/usr/bin/env bash
set -euo pipefail

# PythonAnywhere update script
# Usage: run this in a Bash console on PythonAnywhere to pull the latest code,
# install deps, run migrations (if present), and reload the web app.

REPO_DIR="${HOME}/Phola_park_app"
WSGI_FILE="/var/www/shabanguj_pythonanywhere_com_wsgi.py"
VENV_PATH=""

echo "[pa_update] Starting update script"

if [ ! -d "$REPO_DIR" ]; then
  echo "[pa_update] Repo not found at $REPO_DIR — cloning..."
  git clone https://github.com/Shabangujj/Phola_park_app.git "$REPO_DIR"
fi

cd "$REPO_DIR"

echo "[pa_update] Fetching latest from origin"
git fetch --all --prune

echo "[pa_update] Checking out main and pulling"
git checkout main || git checkout -b main
git reset --hard origin/main

echo "[pa_update] Detecting virtualenv from WSGI file ($WSGI_FILE)"
if [ -f "$WSGI_FILE" ]; then
  VENV_PATH=$(grep -oE "/home/[a-zA-Z0-9._-]+/.virtualenvs/[^"]+" "$WSGI_FILE" || true)
  if [ -z "$VENV_PATH" ]; then
    VENV_PATH=$(grep -oE "/home/[a-zA-Z0-9._-]+/venv[^"]*" "$WSGI_FILE" || true)
  fi
fi

# fallback: if user has a single virtualenv under ~/.virtualenvs, use it
if [ -z "$VENV_PATH" ] && [ -d "${HOME}/.virtualenvs" ]; then
  count=$(ls -1 ${HOME}/.virtualenvs 2>/dev/null | wc -l || true)
  if [ "$count" -eq 1 ]; then
    VENV_NAME=$(ls -1 ${HOME}/.virtualenvs | head -n1)
    VENV_PATH="${HOME}/.virtualenvs/${VENV_NAME}"
  fi
fi

PY_CMD=python3
if [ -n "$VENV_PATH" ] && [ -f "$VENV_PATH/bin/activate" ]; then
  echo "[pa_update] Activating virtualenv: $VENV_PATH"
  # shellcheck source=/dev/null
  source "$VENV_PATH/bin/activate"
  PY_CMD=python
else
  echo "[pa_update] Virtualenv not auto-detected. Using system python."
  echo "[pa_update] If this is wrong, edit this script and set VENV_PATH to your venv (e.g. /home/youruser/.virtualenvs/myenv)"
fi

echo "[pa_update] Installing dependencies from requirements.txt"
$PY_CMD -m pip install --upgrade pip
if [ -f requirements.txt ]; then
  $PY_CMD -m pip install -r requirements.txt
else
  echo "[pa_update] No requirements.txt found"
fi

echo "[pa_update] Installing project in editable mode (pip install -e .)"
$PY_CMD -m pip install -e . || true

# Attempt migrations if Flask-Migrate appears to be used
if [ -d migrations ] || $PY_CMD -c "import flask_migrate" >/dev/null 2>&1; then
  echo "[pa_update] Running database migrations (flask db upgrade)"
  export FLASK_APP=phola_park_app
  $PY_CMD -m flask db upgrade || echo "[pa_update] flask db upgrade failed or not configured"
fi

# Ensure uploads/static directories exist
echo "[pa_update] Ensuring static/uploads exist"
mkdir -p phola_park_app/static/uploads
chmod 755 phola_park_app/static/uploads || true

# Reload the web app by touching the WSGI file (PythonAnywhere will reload)
if [ -f "$WSGI_FILE" ]; then
  echo "[pa_update] Touching WSGI file to trigger reload: $WSGI_FILE"
  touch "$WSGI_FILE"
else
  echo "[pa_update] WSGI file not found at $WSGI_FILE — please reload the app from the PythonAnywhere Web tab"
fi

echo "[pa_update] Update complete. Current commit:" 
git rev-parse --short HEAD

echo "[pa_update] Done"
