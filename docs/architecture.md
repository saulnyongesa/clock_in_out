# Architecture

## Current Direction

Clock In Out is a Django web system.

Django provides:

- Server-rendered browser pages.
- Vanilla JavaScript interactions.
- JSON API endpoints.
- Django admin.
- LAN monitor page.
- Attendance business rules.

Future desktop or mobile apps can be added later as API clients, but the web system must remain complete and usable on its own.

## Repository Layout

```text
clock_in_out/
  backend/
    config/
    institutions/
    academics/
    trainers/
    attendance/
    templates/
  docs/
```

## Backend Apps

- `institutions` - school profile, logo, contact information, allowance policy.
- `academics` - terms and units.
- `trainers` - trainer profiles, reference photos, DeepFace verification, unit assignment.
- `attendance` - clock-in/out sessions, mandatory audit photos, credited minutes.
- `config` - project settings, URLs, monitor pages, web entry pages.

## Frontend Approach

The frontend is Django templates plus vanilla JavaScript.

Rules:

- Use template pages for navigation and layout.
- Keep admin pages separate from trainer-facing clock pages.
- Use `fetch` for API calls.
- Keep endpoints reusable for future apps.
- Keep JavaScript small and page-specific.
- Avoid React, Vue, Flutter, or other frontend frameworks for the web version.

## LAN/IP Handling

At startup, Django dynamically adds local access hosts:

- localhost
- 127.0.0.1
- hostname
- detected LAN IPs

The monitor page and `/api/network/` show the URLs that LAN users and future apps can use.

## Web Areas

- `/app/` - admin dashboard and management pages.
- `/app/setup/` - school setup and LAN/IP details.
- `/trainer/clock/` - trainer-facing clock terminal.
- `/` - backend monitor.

## Attendance Rounding Policy

Each institution can configure allowance minutes.

Example:

- Unit/class expected duration: 60 minutes.
- Allowance: 10 minutes.
- Trainer clocks out at 50 minutes.
- Backend records 60 credited minutes because the missing 10 minutes is within allowance.

The backend stores:

- actual duration
- credited duration

Reports should show both.
