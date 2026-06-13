# Deployment Mapping

This roadmap is now web-first. The complete system runs in Django and is accessed through a browser on the school LAN.

## Phase 1: Foundation

Goal: Make Django runnable and reachable.

Steps:

1. Install Python.
2. Create/activate virtual environment.
3. Install requirements.
4. Run migrations.
5. Create superuser.
6. Start Django with `0.0.0.0:8000`.
7. Open backend monitor.
8. Confirm health endpoint and network endpoint work.

Working check:

- `/api/health/` returns `200`.
- `/api/network/` returns LAN URLs.
- `/` monitor page opens.
- `/admin/` opens.

## Phase 2: Web System Setup

Goal: Configure school identity and policies from the browser.

Steps:

1. Build `/app/setup/`.
2. Load current institution setup through `/api/institution-setup/current/`.
3. Save school name, email, phone, address, default class minutes, and clock-out allowance.
4. Show detected LAN URLs on setup page.
5. Add logo upload support.
6. Display school branding across web pages.
7. Keep trainer clocking separate at `/trainer/clock/`.

Working check:

- Setup page loads existing data.
- Admin can save changes.
- Saved values are returned by API.
- LAN URLs are visible.
- Trainer clock page is not inside the admin dashboard shell.

## Phase 3: Web Admin Dashboard

Goal: Manage the full system from browser pages.

Steps:

1. Build dashboard summary.
2. Add trainer management pages.
3. Add unit management pages.
4. Add trainer-unit assignment pages.
5. Add active classes page.
6. Add attendance history page.
7. Keep Django admin available for superadmin fallback.

Working check:

- Admin can manage trainers and units without using Flutter/mobile apps.
- All pages use Django templates and vanilla JS.
- Trainer-unit assignment works from `/app/assignments/`.

## Phase 4: Trainer Clock-In/Clock-Out

Goal: Complete the daily trainer workflow in the browser.

Steps:

1. Trainer enters ID number.
2. Browser opens camera preview.
3. Clock-in snapshot is mandatory.
4. Backend uses DeepFace to verify the snapshot against the registered photo for that ID number.
5. Trainer selects assigned unit.
6. Backend records clock-in.
7. Active session page shows unit stats.
8. Clock-out snapshot and DeepFace verification are mandatory.
9. Backend records actual and credited minutes.

Working check:

- Trainer cannot clock in without snapshot.
- Trainer cannot clock into two classes at once.
- Active trainer goes directly to active session screen.
- Grace allowance works.

## Phase 5: Reports

Goal: Produce Excel-ready admin reports.

Steps:

1. Trainer attendance report.
2. Unit report.
3. Trainer summary report.
4. Payment-focused summary using credited minutes.
5. Date range filters.
6. Excel export endpoints.
7. Browser download buttons.

Working check:

- Excel files open correctly.
- Actual and credited minutes are visible.
- Totals match attendance records.

## Phase 6: LAN Deployment

Goal: Install at a school.

Steps:

1. Choose backend host/server.
2. Network admin assigns static LAN IP.
3. Configure firewall for port `8000`.
4. Start Django service.
5. Open monitor page on LAN IP.
6. Complete setup from browser.
7. Test clock-in/out from another LAN computer.

Working check:

- `http://LAN-IP:8000/` opens from another computer.
- Setup page saves.
- Attendance records save.
- Reports download.

## Phase 7: Backup And Recovery

Goal: Protect school attendance data.

Steps:

1. Back up database.
2. Back up uploaded media.
3. Document restore steps.
4. Schedule regular backups.

Working check:

- Backup file is created.
- Restore test works.

## Future Phase: Optional Apps

Desktop/mobile apps may be built later.

Rules:

- Apps must use existing APIs.
- Apps must not replace the web system.
- Attendance rules remain in Django.
