## PythonAnywhere deployment helper

This repository includes a small script to update the deployed app on PythonAnywhere.

Usage on PythonAnywhere (Bash console):

1. Open a Bash console on PythonAnywhere (Web → Consoles → Bash).
2. Run:

   bash ~/Phola_park_app/scripts/pa_update.sh

The script will:
- clone the repo if not present
- pull the latest changes from main
- try to detect and activate the webapp virtualenv
- install/update dependencies and install the project in editable mode
- run Flask-Migrate upgrades (if configured)
- ensure static/uploads exists
- touch the WSGI file to trigger a reload

GitHub Actions (optional):
- A workflow template is provided at .github/workflows/deploy-to-pa.yml.
- To use it you must add the following repository secrets in GitHub:
  - PA_HOST: your PythonAnywhere SSH host (e.g. ssh.pythonanywhere.com)
  - PA_USER: your PythonAnywhere username (e.g. shabanguj)
  - PA_KEY: private SSH key (PEM) for the user with SSH access to PythonAnywhere
  - PA_PORT: optional (default SSH port 22)

Notes:
- PythonAnywhere SSH access is only available for paid accounts. If you don't have SSH, run the script manually in a Bash console.
- If the script cannot detect your virtualenv, edit scripts/pa_update.sh and set VENV_PATH accordingly.
