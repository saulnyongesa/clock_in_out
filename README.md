# Clock In Out

Modern web-based trainer attendance system for schools.

The system is now web-first: Django serves both the backend API and the browser interface. Future desktop or mobile apps can be added later by consuming the same API endpoints.

## Repository Layout

- `backend/` - Django web app, templates, API endpoints, admin, and attendance backend.
- `docs/` - Product, architecture, and deployment notes.

## Current Web Pages

- Public landing page: `http://127.0.0.1:8000/`
- Main dashboard: `http://127.0.0.1:8000/app/`
- System setup: `http://127.0.0.1:8000/app/setup/`
- Trainers: `http://127.0.0.1:8000/app/trainers/`
- Units: `http://127.0.0.1:8000/app/units/`
- Assignments: `http://127.0.0.1:8000/app/assignments/`
- Active classes: `http://127.0.0.1:8000/app/active-classes/`
- Attendance history: `http://127.0.0.1:8000/app/attendance/`
- Reports: `http://127.0.0.1:8000/app/reports/`
- Backend monitor: `http://127.0.0.1:8000/app/system/monitor/`
- Trainer clock in/out: `http://127.0.0.1:8000/trainer/clock/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Core Direction

The system uses:

- Trainer ID number.
- DeepFace verification against the trainer photo registered for that ID.
- Mandatory camera preview and audit snapshot at clock-in and clock-out.
- Admin-managed trainer records.
- Web templates with vanilla JavaScript.
- API endpoints that future apps can reuse.

## Web And API Design

Django templates provide the browser UI. Vanilla JavaScript communicates with Django API endpoints using `fetch`.

Admin and trainer pages are intentionally separate:

- Admin system: `/app/`
- Trainer terminal: `/trainer/clock/`
- Public entry: `/`

Current API endpoints include:

- Health check: `/api/health/`
- LAN/network info: `/api/network/`
- Institution setup: `/api/institution-setup/current/`
- Institutions API: `/api/institutions/`
- Units API: `/api/units/`
- Trainers API: `/api/trainers/`
- Trainer face verification: `/api/trainers/verify-face/`
- Attendance sessions API: `/api/attendance-sessions/`

Report downloads:

- Attendance Excel: `/app/reports/export/attendance/`
- Trainer Summary Excel: `/app/reports/export/trainers/`
- Unit Summary Excel: `/app/reports/export/units/`

Future mobile or desktop apps should use these same endpoints instead of creating separate backend logic.

## LAN Hosting Setup

The system is designed to run inside a school LAN.

The Django backend/web system runs on one host computer or school server. The school network admin should assign that host a static LAN IP address, for example:

```text
192.168.1.50
```

The web system can then be opened from other computers on the LAN:

```text
http://192.168.1.50:8000
```

The backend automatically allows access through:

- `localhost`
- `127.0.0.1`
- the backend computer hostname
- detected LAN IP addresses

If needed, extra hostnames/IPs can be added with the `DJANGO_ALLOWED_HOSTS` environment variable.

## Backend Monitor

The backend monitor page shows:

- backend online status
- institution count
- trainer count
- unit count
- active class count
- detected LAN IP addresses
- backend URLs for future frontend clients

Open:

```text
http://127.0.0.1:8000/app/system/monitor/
```

JSON network data:

```text
http://127.0.0.1:8000/api/network/
```

## Development Setup

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Then open:

```text
http://127.0.0.1:8000/app/
```

## Camera Access On LAN

Trainer face verification and clock-in/clock-out audit photos require browser camera access.

Modern browsers allow camera capture only from a secure context:

- `http://localhost:8000` or `http://127.0.0.1:8000` on the backend computer.
- HTTPS URLs on other LAN computers, for example `https://192.168.1.50`.

If a trainer opens `http://192.168.1.50:8000/trainer/clock/` from another computer, the browser may block the camera as "not secure". For school-wide LAN use, configure HTTPS for the Django host or place Django behind an HTTPS reverse proxy on the assigned static IP.

Trainer login flow:

1. Enter trainer ID number.
2. Click Next to open the camera preview.
3. Verify face against the registered reference photo.
4. Open the trainer dashboard to clock in or clock out.

## Optional DeepFace Install

The system can use DeepFace for stronger trainer face verification when it is installed. DeepFace downloads TensorFlow, which is a large Windows package and may fail on slow connections.

Base setup works without DeepFace by using a lightweight local photo verifier. To enable DeepFace later:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install --default-timeout 1000 --retries 10 -r requirements-ml.txt
```

If DeepFace is installed successfully, the trainer verification API will use it automatically. If it is not installed, the API falls back to the lightweight verifier instead of blocking clock-in/out.

## Future App Room

Desktop and mobile apps may be added later if needed.

When that happens:

- Keep Django as the source of truth.
- Reuse existing API endpoints.
- Do not duplicate attendance/business rules in the app.
- Keep the web system fully functional even if apps are added.
