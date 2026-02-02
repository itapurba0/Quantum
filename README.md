Quantium starter — local Dash development setup

This repository contains a minimal Dash app and instructions to set up a Python 3.9 virtual environment for development.

Quick checklist

- Fork the upstream repo (https://github.com/vagabond-systems/quantium-starter-repo) and clone your fork.
- Create a Python 3.9 virtual environment inside the project (we use `.venv` here).
- Install dependencies from `requirements.txt` and the Dash testing extras.
- Run the minimal app to verify the environment.

Commands (run in project root):

```bash
# Ensure Python 3.9 is available
python3.9 --version

# Create and activate venv
python3.9 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project deps
pip install -r requirements.txt

# Install dash testing extras
pip install "dash[testing]"

# Run the sample app
python app.py
```

Notes

- If you don't have Python 3.9 installed, install it or adjust the commands to whichever Python 3.x you will use. The project was specified to use Python 3.9.
- The sample `app.py` is a tiny Dash application that uses `pandas`. It will run on http://127.0.0.1:8050 by default.
- Once the venv is active and dependencies installed, open the project in your IDE and point the interpreter to `.venv/bin/python`.

