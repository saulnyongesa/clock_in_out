# Deployment Mapping

This document maps the steps for building, testing, and deploying the Clock In Out system smoothly.

## Target Deployment

The system is designed for a school LAN.

- Django backend runs on one host computer or school server.
- The network admin assigns a static LAN IP to the backend host.
- Flutter desktop apps connect to that LAN IP.
- The superadmin sets the backend server IP inside the system configuration.
- If the backend host receives a new IP, the frontend admin updates the frontend server address so apps communicate with the backend again.

Example backend URL:

```text
http://192.168.1.50:8000
```

## Phase 1: Foundation

Goal: Make the project runnable end to end.

Steps:

1. Install real Python and Flutter on the development machine.
2. Create and activate the backend virtual environment.
3. Install backend requirements.
4. Run Django migrations.
5. Create Django superuser.
6. Start backend server.
7. Start Flutter desktop app.
8. Confirm the desktop app can reach the backend health/API endpoint.

Working check:

- Backend opens in browser.
- Django admin opens.
- Flutter app launches.
- Flutter app shows backend connection status.
- Backend monitor opens and shows usable LAN backend URLs.

## Phase 2: Institution Setup

Goal: Allow system branding and school policies to be configured.

Steps:

1. Build institution profile screen in desktop admin dashboard.
2. Add school name, logo, phone, email, address, and default class duration.
3. Add clock-out allowance minutes.
4. Save settings to Django backend.
5. Display school logo/name in desktop app header.
6. Verify the setup screen in Flutter web before packaging the desktop app.

Working check:

- Superadmin can update school details.
- Logo appears on the desktop app.
- Clock-out allowance is saved and used by attendance logic.

## Phase 3: Network/IP Configuration

Goal: Make LAN deployment reliable even if the backend IP changes.

Steps:

1. Add backend server URL setting in the desktop app.
2. Store the backend URL locally on the desktop machine.
3. Add a connection test button.
4. Add clear online/offline status in the app.
5. Allow frontend admin to update the backend URL when the LAN IP changes.
6. Keep last working IP visible for troubleshooting.

Working check:

- Desktop app can switch from one backend URL to another.
- Invalid IP shows a clear connection error.
- Valid IP reconnects without reinstalling the app.

## Phase 4: Admin Dashboard In Desktop App

Goal: Move system management into the desktop application.

Steps:

1. Add admin login.
2. Add dashboard summary: trainers, units, active classes, today hours.
3. Add institution setup screen.
4. Add trainer management screen.
5. Add unit management screen.
6. Add trainer-unit assignment screen.
7. Add attendance history screen.
8. Add active classes screen with admin force clock-out.
9. Add reports screen.
10. Add Excel report download/export.

Working check:

- Admin can manage all core data from the desktop app.
- Reports download as Excel files.
- Admin actions update backend data immediately.

## Phase 5: Trainer Attendance Flow

Goal: Make daily clock-in/out fast and reliable.

Steps:

1. Trainer enters ID number.
2. Trainer enters PIN.
3. Backend verifies trainer.
4. App checks active session.
5. If active session exists, open active unit screen.
6. If no active session exists, show assigned units.
7. Trainer selects unit.
8. App shows the live camera preview and captures a mandatory clock-in snapshot.
9. Backend records clock-in.
10. App shows right-side unit stats card.
11. Trainer clocks out.
12. App shows the live camera preview and captures a mandatory clock-out snapshot.
13. Backend records actual and credited minutes.

Working check:

- Trainer cannot clock into two classes at once.
- Trainer cannot clock in or clock out without the camera preview and audit snapshot.
- Active trainer returns directly to clock-out screen.
- Unit stats are correct after clock-in and clock-out.
- Grace allowance credits the expected minutes when applicable.

## Phase 6: Mobile Registration

Goal: Register trainers from mobile devices.

Steps:

1. Add admin login to mobile app.
2. Add trainer profile form.
3. Add profile photo capture.
4. Add PIN setup/reset.
5. Add unit assignment.
6. Submit trainer data to backend.

Working check:

- Trainer created from mobile appears in desktop admin dashboard.
- Trainer can immediately clock in from desktop terminal.

## Phase 7: Reports

Goal: Produce usable payment and monitoring reports.

Steps:

1. Add trainer attendance report.
2. Add unit report.
3. Add term report.
4. Add date range filters.
5. Add active/incomplete sessions report.
6. Add Excel export endpoints in Django.
7. Add Excel download buttons in desktop admin dashboard.

Working check:

- Excel files open correctly.
- Report totals match database attendance sessions.
- Actual minutes and credited minutes are both visible.

## Phase 8: LAN Deployment

Goal: Install the system at a school.

Steps:

1. Choose backend host computer/server.
2. Network admin assigns static LAN IP.
3. Install backend dependencies.
4. Configure `.env` on backend.
5. Run migrations and create superadmin.
6. Start backend service.
7. Open firewall port for backend.
8. Install desktop app on attendance/admin machines.
9. Superadmin or frontend admin sets backend URL in desktop app.
10. Test trainer login, clock-in, clock-out, and report export.

Working check:

- Other LAN computers can open backend URL.
- Desktop app connects using assigned IP.
- Admin dashboard works.
- Attendance records save.
- Excel reports download.

## Phase 9: Backup And Recovery

Goal: Protect school attendance data.

Steps:

1. Add database backup command.
2. Add media backup for logos and trainer photos.
3. Document restore steps.
4. Schedule regular backups.

Working check:

- Backup file is created.
- Restore test works on another machine.

## Phase 10: Final Acceptance

Goal: Confirm the system is ready for real use.

Checklist:

- Institution details configured.
- Backend IP configured in frontend.
- Admin can manage trainers.
- Admin can manage units.
- Admin can assign units to trainers.
- Trainer can clock in.
- Trainer can clock out.
- Grace allowance works.
- Active sessions are visible.
- Reports export to Excel.
- Desktop app reconnects after backend IP change.
- Backup process is documented.
