import 'package:desktop_attendance/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('desktop terminal renders connection and camera panels',
      (tester) async {
    await tester.pumpWidget(const DesktopAttendanceApp());

    expect(find.text('Clock In Out'), findsOneWidget);
    expect(find.text('Backend Server URL'), findsOneWidget);
    expect(find.text('Camera preview required'), findsOneWidget);
    expect(find.text('Unit Stats'), findsOneWidget);
  });

  testWidgets('admin setup section renders institution fields', (tester) async {
    await tester.pumpWidget(const DesktopAttendanceApp());

    await tester.tap(find.byIcon(Icons.admin_panel_settings));
    await tester.pumpAndSettle();

    expect(find.text('Admin Setup'), findsOneWidget);
    expect(find.text('School Name'), findsOneWidget);
    expect(find.text('Default Class Minutes'), findsOneWidget);
    expect(find.text('Clock-out Allowance Minutes'), findsOneWidget);
  });
}
