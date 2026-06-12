# Clock In Out

Modern trainer attendance system.

This repository is a mono-repo: the Django backend, Flutter desktop app, and Flutter mobile registration app live together so they can evolve as one product.

## Repository Layout

- `backend/` - Django API and admin backend.
- `frontend/desktop_attendance/` - Flutter desktop app for daily trainer clock-in/out and the admin dashboard.
- `frontend/mobile_registration/` - Flutter mobile app for trainer registration and profile/photo capture.
- `docs/` - Product and architecture notes.

## Authentication Direction

Face recognition has been dropped for simplicity and reliability.

The first version will use:

- Trainer ID number.
- Trainer PIN/passcode.
- Mandatory camera snapshot at clock-in and clock-out for audit.
- Admin-managed trainer records.

This keeps setup simple on Windows and Linux while still discouraging proxy attendance.

## Deployment Mapping

See [docs/deployment-mapping.md](docs/deployment-mapping.md) for the full build, test, and LAN deployment roadmap.

## Desktop App Scope

The desktop app is the main operating app for the school.

It will include:

- Trainer clock-in and clock-out.
- Mandatory live camera preview and audit snapshot capture during clock-in and clock-out.
- Admin login.
- Admin dashboard.
- Institution setup: school name, logo, contact details, and policies.
- Trainer management.
- Unit management.
- Trainer-unit assignment.
- Active classes.
- Attendance history.
- Reports.
- Excel report downloads.

The mobile app is focused on trainer registration and profile/photo capture.

## LAN Hosting Setup

The system is designed to run inside a school LAN.

The Django backend will run on one host computer or school server. The school network admin should assign that backend host a static LAN IP address, for example:

```text
192.168.1.50
```

The backend can then be accessed by other computers on the LAN using a URL like:

```text
http://192.168.1.50:8000
```

The superadmin will set this backend URL in the system/frontend configuration. The desktop app must store this URL locally so it knows where to send API requests.

## Backend IP Change Handling

If the backend host receives a new LAN IP, the system should not require reinstalling the frontend app.

The desktop app must include a backend server settings screen where an authorized frontend admin can:

- View the current backend URL.
- Enter a new backend URL.
- Test connection to the new URL.
- Save the new URL locally.
- See online/offline connection status.

Recommended local frontend setting:

```json
{
  "backend_base_url": "http://192.168.1.50:8000"
}
```

When the school network admin changes the backend host IP, they should send the new IP to the admin handling the desktop frontend. That admin updates the backend URL in the desktop app, tests the connection, and saves it.

## Smooth Project Execution Steps

1. Prepare development tools.
   - Install real Python, Django dependencies, Flutter, and Git.
   - Confirm backend and Flutter apps can run.

2. Complete backend foundation.
   - Run migrations.
   - Create superadmin.
   - Confirm Django admin works.
   - Confirm API endpoints respond.

3. Build institution setup.
   - Add school profile, logo, and contact details.
   - Add default class duration and clock-out allowance.
   - Verify settings appear in the desktop app.

4. Build LAN server configuration.
   - Add backend URL setup screen to desktop app.
   - Add connection test.
   - Store selected backend URL locally.
   - Verify app can reconnect after URL change.

5. Build admin dashboard in desktop app.
   - Trainers, units, assignments, active classes, attendance history, and reports.
   - Verify each admin action saves to backend.

6. Build trainer attendance flow.
   - Trainer ID + PIN.
   - Active session detection.
   - Unit selection.
   - Right-side unit stats card.
   - Clock-out with actual and credited minutes.

7. Build mobile registration.
   - Trainer details.
   - Photo capture.
   - PIN setup/reset.
   - Unit assignment.

8. Build Excel reporting.
   - Trainer reports.
   - Unit reports.
   - Date range reports.
   - Payment-focused summaries.
   - Verify exported files open correctly in Excel.

9. Test LAN deployment.
   - Assign backend static IP.
   - Open firewall port.
   - Connect desktop app from another LAN computer.
   - Record attendance and download reports.

10. Finalize backup and recovery.
    - Backup database.
    - Backup uploaded logos/photos.
    - Document restore steps.
