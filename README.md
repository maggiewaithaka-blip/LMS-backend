# ECCGD Backend (Django) — Scaffold

This repository contains a Django backend scaffold mapped from a Moodle architecture to Django apps.

Quick start (Windows PowerShell):

1. Create virtual environment and activate

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run migrations and start dev server

```powershell
python manage.py migrate
python manage.py runserver
```

Notes:
- This scaffold provides app folders and base models per the Moodle→Django mapping. Fill in business logic, serializers, views and tests next.

If you want, I can now run migrations and a smoke test locally (I may need your confirmation and a configured Python environment in the workspace).
