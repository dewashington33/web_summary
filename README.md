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
  __pycache__/
  *.pyc
  .pytest_cache/
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

### Reproducible reinstall later

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

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

\*\*Add the .env file to the root of the project

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
