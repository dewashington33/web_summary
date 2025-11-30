# End-to-end Python project setup on Windows 11 with PowerShell

This is a complete, reproducible walkthrough—from installing Python and pip to building your `web_summary` project, installing dependencies, and verifying everything works. Follow each step in order inside PowerShell.

---

## Prerequisites on Windows 11

- **PowerShell:** Use Windows PowerShell or PowerShell 7.
- **Admin rights:** Not required, but helpful if you change system-wide PATH.

---

## Install Python and ensure pip

### Download and install Python

- **Download:** Get the latest stable Windows installer from python.org.
- **Installer options:**
  - **Add to PATH:** Check “Add Python to PATH.”
  - **Customize installation:** Ensure both **pip** and **venv** are selected.
  - **Disable App Execution Aliases (optional):** If multiple Pythons exist, go to “App execution aliases” settings and turn off Python aliases to avoid conflicts.

### Verify Python and pip in PowerShell

- **Check versions:**
  ```powershell
  python --version
  python -m pip --version
  ```
- **If `python` works but `pip` fails:**
  ```powershell
  python -m ensurepip --upgrade
  python -m pip install --upgrade pip
  ```
  \*\*Even if pip shows the version the first time, make sure you run the upgrade to get the latest version.

### Confirm PATH and executable locations

- **See which Python runs:**
  ```powershell
  Get-Command python | Format-List *
  ```
- **List Python and pip paths:**
  ```powershell
  where.exe python
  where.exe pip
  ```
- **Typical install paths (user install):**
  - Python: `C:\Users\<You>\AppData\Local\Programs\Python\Python3xx\python.exe`
  - Scripts: `C:\Users\<You>\AppData\Local\Programs\Python\Python3xx\Scripts\`

### Add Scripts to PATH (if `pip` not found)

- **Temporary (current session):**
  ```powershell
  $scripts = "$env:LOCALAPPDATA\Programs\Python\Python3xx\Scripts"
  $env:Path += ";$scripts"
  ```
- **Permanent (recommended):**
  - **System Settings → Environment Variables → Path → Edit → New**
  - Add: `C:\Users\<You>\AppData\Local\Programs\Python\Python3xx\Scripts`
  - Restart PowerShell.

---

## Create the project and virtual environment

### Create root folder and enter it

```powershell
New-Item -ItemType Directory -Path "C:\Projects\web_summary"
Set-Location "C:\Projects\web_summary"
```

### Create and activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

- **Indicator:** Your prompt shows `(venv)` when active.
- **Deactivate later:** `deactivate`

---

## Create the package structure and files

### Create package folder and files

```powershell
New-Item -ItemType Directory -Path "web_summary"
New-Item -ItemType File -Path "web_summary\__init__.py"
New-Item -ItemType File -Path "web_summary\main.py"
New-Item -ItemType File -Path "web_summary\scraper.py"
```

### Create tests and support files

```powershell
New-Item -ItemType Directory -Path "tests"
New-Item -ItemType File -Path "tests\test_scraper.py"
New-Item -ItemType File -Path "README.md"
New-Item -ItemType File -Path ".gitignore"
```

- **.gitignore contents:**
  ```
  venv/
  .venv/
  __pycache__/
  *.pyc
  .pytest_cache/
  .env
  .env.*
  ```

---

## Install project dependencies

### Install and freeze dependencies

```powershell
pip install openai beautifulsoup4 requests
pip freeze > requirements.txt
```

- **Packages:**
  - **openai:** for `main.py`
  - **beautifulsoup4:** for `scraper.py` HTML parsing
  - **requests:** for HTTP calls in `scraper.py`
  - **python-dotenv:** to load variables from `.env`

### Reproducible reinstall later

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Using uv (faster alternative to pip)

You can keep the existing `requirements.txt` and virtualenv, and just use uv for faster installs. Or adopt uv fully with a lockfile for reproducible builds.

### Install uv (Windows PowerShell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### Option A: Use uv with requirements.txt (no repo change)

```powershell
# Create and activate a venv as usual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies (fast)
uv pip install -r requirements.txt

# Optional: enforce an exact match to requirements.txt
uv pip sync requirements.txt
```

### Option B: Full uv workflow with lockfile (reproducible)

```powershell
# Initialize project (creates pyproject.toml)
uv init --package web_summary

# Create a uv-managed venv
uv venv
& .\.venv\Scripts\Activate.ps1

# Import existing requirements OR add packages individually
uv add -r requirements.txt
# Example (if starting fresh):
# uv add openai beautifulsoup4 requests

# Install from lock
uv sync

# Run (without manual activation if preferred)
uv run python web_summary\main.py
```

Notes:

- Commit `uv.lock` to version control.
- Ensure `.venv/` remains in `.gitignore` (already listed above).

## Run and test

### Run your scripts

```powershell
python .\web_summary\main.py
python .\web_summary\scraper.py
```

### Optional: use pytest

```powershell
pip install pytest
pytest
```

---

## Optional: initialize Git

```powershell
git init
git add .
git commit -m "Initial project setup for web_summary"
```

---

## Final project layout

```
web_summary/
│
├── venv/                  # Virtual environment
├── web_summary/           # Package folder
│   ├── __init__.py
│   ├── main.py            # Uses OpenAI
│   └── scraper.py         # Uses BeautifulSoup + requests
│
├── tests/                 # Unit tests
│   └── test_scraper.py
│
├── requirements.txt       # Dependencies (pinned)
├── README.md              # Documentation
└── .gitignore             # Ignore venv, caches, pyc
```

---

## Add a .env to store environment variables and secrets

Place a `.env` file in the project root to keep API keys and configuration out of source code. The `.gitignore` section above already ignores `.env` and `.env.*` so it won’t be pushed.

Example `.env` contents (edit as needed):

```dotenv
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
LLM_PROVIDER=ollama   # or openai, gemini
LLM_MODEL=            # optional: for openai/gemini (e.g., gpt-5-nano or gemini-2.5-pro)
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2
```

Create `.env` on Windows PowerShell:

```powershell
@"
OPENAI_API_KEY=sk-your-key
GEMINI_API_KEY=your-gemini-key
LLM_PROVIDER=openai
LLM_MODEL=
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2
"@ | Set-Content -Encoding UTF8 .env
```

Use the values at runtime in one of two ways:

- PowerShell (current session only):
  ```powershell
  $env:OPENAI_API_KEY = "sk-your-key"
  $env:LLM_PROVIDER = "openai"   # or gemini, ollama
  $env:LLM_MODEL = "gpt-5-nano"  # for openai; use "gemini-2.5-pro" for gemini
  ```
- python-dotenv (already included): load `.env` automatically in your entrypoint (e.g., `web_summary/main.py`):
  ```python
  from dotenv import load_dotenv
  load_dotenv()  # loads variables from .env into the environment
  ```

Git safety:

- If `.env` was accidentally committed once, stop tracking while keeping the local file:
  ```powershell
  git rm --cached .env
  git commit -m "Stop tracking .env"
  ```

## Troubleshooting quick reference

- **Label:** Pip not found  
  **Fix:** `python -m ensurepip --upgrade` then add the Scripts folder to PATH and restart PowerShell.

- **Label:** Wrong Python runs  
  **Fix:** Check “App execution aliases” in Windows settings; turn off Python aliases. Use full path or ensure desired Python is first in PATH.

- **Label:** Activation script blocked  
  **Fix:** If `Activate.ps1` is blocked by policy, run PowerShell as admin and:

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

  Then re-run activation.

- **Label:** Mixing global and venv pip  
  **Fix:** Prefer `python -m pip install ...` to guarantee you’re using the venv’s pip.

---
