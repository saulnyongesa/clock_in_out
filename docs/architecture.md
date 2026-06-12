# Architecture

## Mono-Repo

All project source lives in one repository:

```text
clock_in_out/
  backend/
  frontend/
    desktop_attendance/
    mobile_registration/
  docs/
```

## Backend

Django will provide:

- Admin dashboard.
- JSON API for Flutter apps.
- Institution setup.
- Trainer management.
- Unit management.
- Attendance sessions.
- Reports and exports.

Recommended Django apps:

- `accounts` - admin users, auth, institution ownership.
- `institutions` - school profile, logo, policies.
- `trainers` - trainer profiles, PIN management, trainer-unit assignment.
- `academics` - terms, units, course metadata if needed.
- `attendance` - clock-in/out sessions, allowance rules, audit photos.
- `reports` - summaries for admin and trainers.

## Frontend

Flutter apps:

- Desktop attendance terminal: Windows/Linux first.
- Mobile registration app: Android first, iOS later if needed.

Both apps should talk to the same Django API.

## Attendance Rounding Policy

Each institution can configure allowance minutes.

Example:

- Unit/class expected duration: 60 minutes.
- Allowance: 10 minutes.
- Trainer clocks out at 50 minutes.
- Backend records 60 minutes because the missing 10 minutes is within allowance.

The backend should always store both:

- actual duration
- credited duration

This keeps reports honest while allowing practical grace.
