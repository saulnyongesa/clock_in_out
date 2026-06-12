# Backend

Django backend for Clock In Out.

Python is not currently available on PATH in this shell, so this folder starts as source scaffolding. Once Python is installed, initialize the Django project here.

Planned command:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
django-admin startproject config .
python manage.py startapp institutions
python manage.py startapp trainers
python manage.py startapp academics
python manage.py startapp attendance
python manage.py startapp reports
```
