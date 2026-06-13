# Product Summary

## Goal

Build a web-based trainer attendance system for schools that pay trainers based on teaching hours.

## Main Roles

- Superadmin/Admin: configures school details, trainers, units, policies, and reports.
- Trainer: clocks in and out for assigned units.

## Web Admin Setup

Admin can configure:

- School/institution name.
- Logo.
- Location/address.
- Email and phone.
- Clock-out allowance minutes.
- Default class duration.
- Academic terms.
- Units and expected teaching hours.
- Trainers and assigned units.

## Trainer Browser Flow

1. Trainer opens `/trainer/clock/`, which is separate from the admin dashboard.
2. Trainer enters ID number.
3. Browser shows a small live camera preview.
4. System captures mandatory clock-in snapshot.
5. Backend uses the ID number to load that trainer only, then DeepFace verifies the live snapshot against the registered trainer photo.
6. Trainer selects assigned unit.
7. Backend records clock-in.
8. Unit stats show expected hours, completed hours, remaining hours, and progress.
9. If trainer already has an active class, system goes directly to active session.
10. Trainer clocks out with mandatory camera preview and DeepFace verification.
11. Backend records actual minutes and credited minutes.
12. If allowance applies, credited minutes can round up to expected class duration.

## Identity Model

- Trainer ID filters the lookup to one trainer.
- DeepFace verifies the live snapshot against the registered trainer photo.
- Mandatory camera snapshots discourage proxy attendance.
- Admin can review snapshots in reports/history.

## Future Apps

Mobile or desktop apps can be added later.

They must use the same Django API endpoints and keep Django as the source of truth.
