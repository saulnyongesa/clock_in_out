# Product Summary

## Goal

Build a modern trainer attendance system for institutions that pay trainers based on teaching hours.

## Main Roles

- Admin: configures institution details, trainers, units, policies, and reports.
- Trainer: clocks in and out for assigned units.

## Admin Setup

Admin should be able to configure:

- School/institution name.
- Logo.
- Location/address.
- Email and phone.
- Clock-out allowance minutes.
- Academic terms.
- Units and expected teaching hours.
- Trainers and assigned units.

## Trainer Desktop Flow

1. Trainer enters ID number.
2. Trainer enters PIN/passcode.
3. App checks whether trainer has an active class.
4. If already clocked in, go directly to active unit screen.
5. Show unit stats card and clock-out button.
6. If not clocked in, trainer selects unit to teach.
7. App shows a small live camera preview and captures a clock-in audit snapshot.
8. App starts attendance session.
9. Right-side stats card shows:
   - unit name/code
   - expected weekly hours
   - expected term hours
   - completed hours
   - remaining hours
   - progress percentage
10. On clock-out, app again shows the live camera preview and captures a clock-out audit snapshot.
11. Backend records taught minutes.
12. If configured allowance applies, backend can round to full expected class duration.

## Trainer Mobile Registration Flow

1. Admin or authorized staff opens registration app.
2. Capture trainer details.
3. Capture trainer photo for profile/audit, not face matching.
4. Set or reset trainer PIN.
5. Assign trainer to one or more units.

## Simpler Identity Model

The system will not use face recognition.

Instead:

- Trainer ID + PIN verifies the trainer.
- Device must show a small live camera preview and capture an audit snapshot during clock-in and clock-out.
- Admin can review suspicious entries from reports.
