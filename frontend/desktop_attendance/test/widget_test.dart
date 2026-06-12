import 'package:desktop_attendance/main.dart';
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
}
