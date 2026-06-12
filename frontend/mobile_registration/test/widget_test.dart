import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_registration/main.dart';

void main() {
  testWidgets('registration form renders trainer fields', (tester) async {
    await tester.pumpWidget(const MobileRegistrationApp());

    expect(find.text('Register Trainer'), findsOneWidget);
    expect(find.text('Full Name'), findsOneWidget);
    expect(find.text('ID Number'), findsOneWidget);
    expect(find.text('Trainer PIN'), findsOneWidget);
  });
}
