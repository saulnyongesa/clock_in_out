import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const DesktopAttendanceApp());
}

class DesktopAttendanceApp extends StatelessWidget {
  const DesktopAttendanceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Clock In Out',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0E7A5F)),
        useMaterial3: true,
      ),
      home: const AttendanceTerminalScreen(),
    );
  }
}

class AttendanceTerminalScreen extends StatefulWidget {
  const AttendanceTerminalScreen({super.key});

  @override
  State<AttendanceTerminalScreen> createState() =>
      _AttendanceTerminalScreenState();
}

class _AttendanceTerminalScreenState extends State<AttendanceTerminalScreen> {
  final backendUrlController = TextEditingController(
    text: 'http://127.0.0.1:8000',
  );
  final idController = TextEditingController();
  final pinController = TextEditingController();
  final schoolNameController = TextEditingController();
  final schoolEmailController = TextEditingController();
  final schoolPhoneController = TextEditingController();
  final schoolAddressController = TextEditingController();
  final defaultClassMinutesController = TextEditingController(text: '60');
  final allowanceMinutesController = TextEditingController(text: '10');
  int selectedSection = 0;
  String connectionStatus = 'Not tested';
  bool isCheckingConnection = false;

  @override
  void dispose() {
    backendUrlController.dispose();
    idController.dispose();
    pinController.dispose();
    schoolNameController.dispose();
    schoolEmailController.dispose();
    schoolPhoneController.dispose();
    schoolAddressController.dispose();
    defaultClassMinutesController.dispose();
    allowanceMinutesController.dispose();
    super.dispose();
  }

  Future<void> testBackendConnection() async {
    setState(() {
      isCheckingConnection = true;
      connectionStatus = 'Checking...';
    });

    final baseUrl = backendUrlController.text.trim().replaceAll(
          RegExp(r'/$'),
          '',
        );

    try {
      final response = await http
          .get(Uri.parse('$baseUrl/api/health/'))
          .timeout(const Duration(seconds: 5));

      setState(() {
        connectionStatus = response.statusCode == 200
            ? 'Online: backend reachable'
            : 'Error: HTTP ${response.statusCode}';
      });
    } catch (_) {
      setState(() {
        connectionStatus = 'Offline: backend not reachable';
      });
    } finally {
      setState(() {
        isCheckingConnection = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: selectedSection,
            onDestinationSelected: (index) {
              setState(() {
                selectedSection = index;
              });
            },
            labelType: NavigationRailLabelType.all,
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.schedule),
                label: Text('Clock'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.admin_panel_settings),
                label: Text('Admin'),
              ),
            ],
          ),
          const VerticalDivider(width: 1),
          Expanded(
            flex: 3,
            child: selectedSection == 0
                ? ClockSection(
                    backendUrlController: backendUrlController,
                    idController: idController,
                    pinController: pinController,
                    isCheckingConnection: isCheckingConnection,
                    connectionStatus: connectionStatus,
                    onTestConnection: testBackendConnection,
                  )
                : AdminSetupSection(
                    schoolNameController: schoolNameController,
                    schoolEmailController: schoolEmailController,
                    schoolPhoneController: schoolPhoneController,
                    schoolAddressController: schoolAddressController,
                    defaultClassMinutesController:
                        defaultClassMinutesController,
                    allowanceMinutesController: allowanceMinutesController,
                  ),
          ),
          Container(
            width: 380,
            color: const Color(0xFFF3F7F5),
            padding: const EdgeInsets.all(24),
            child: const Column(
              children: [
                CameraPreviewPanel(),
                SizedBox(height: 16),
                Expanded(child: UnitStatsCard()),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ClockSection extends StatelessWidget {
  const ClockSection({
    required this.backendUrlController,
    required this.idController,
    required this.pinController,
    required this.isCheckingConnection,
    required this.connectionStatus,
    required this.onTestConnection,
    super.key,
  });

  final TextEditingController backendUrlController;
  final TextEditingController idController;
  final TextEditingController pinController;
  final bool isCheckingConnection;
  final String connectionStatus;
  final VoidCallback onTestConnection;

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 680),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Clock In Out',
              style: TextStyle(fontSize: 32, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 8),
            const Text('Trainer attendance terminal'),
            const SizedBox(height: 28),
            TextField(
              controller: backendUrlController,
              decoration: const InputDecoration(
                labelText: 'Backend Server URL',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 12,
              runSpacing: 8,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                FilledButton.icon(
                  onPressed: isCheckingConnection ? null : onTestConnection,
                  icon: const Icon(Icons.wifi_tethering),
                  label: const Text('Test Connection'),
                ),
                Text(connectionStatus),
              ],
            ),
            const SizedBox(height: 56),
            TextField(
              controller: idController,
              decoration: const InputDecoration(
                labelText: 'Trainer ID Number',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: pinController,
              obscureText: true,
              decoration: const InputDecoration(
                labelText: 'PIN',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            FilledButton(onPressed: () {}, child: const Text('Continue')),
          ],
        ),
      ),
    );
  }
}

class AdminSetupSection extends StatelessWidget {
  const AdminSetupSection({
    required this.schoolNameController,
    required this.schoolEmailController,
    required this.schoolPhoneController,
    required this.schoolAddressController,
    required this.defaultClassMinutesController,
    required this.allowanceMinutesController,
    super.key,
  });

  final TextEditingController schoolNameController;
  final TextEditingController schoolEmailController;
  final TextEditingController schoolPhoneController;
  final TextEditingController schoolAddressController;
  final TextEditingController defaultClassMinutesController;
  final TextEditingController allowanceMinutesController;

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 820),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Admin Setup',
              style: TextStyle(fontSize: 32, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 8),
            const Text('Institution branding and attendance policy'),
            const SizedBox(height: 28),
            OutlinedButton.icon(
              onPressed: null,
              icon: const Icon(Icons.image_outlined),
              label: const Text('Upload School Logo'),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: schoolNameController,
              decoration: const InputDecoration(
                labelText: 'School Name',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: schoolEmailController,
                    decoration: const InputDecoration(
                      labelText: 'School Email',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: TextField(
                    controller: schoolPhoneController,
                    decoration: const InputDecoration(
                      labelText: 'School Phone',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            TextField(
              controller: schoolAddressController,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: 'Address',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: defaultClassMinutesController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Default Class Minutes',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: TextField(
                    controller: allowanceMinutesController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Clock-out Allowance Minutes',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            FilledButton.icon(
              onPressed: null,
              icon: const Icon(Icons.save_outlined),
              label: const Text('Save Institution Setup'),
            ),
          ],
        ),
      ),
    );
  }
}

class CameraPreviewPanel extends StatelessWidget {
  const CameraPreviewPanel({super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      child: AspectRatio(
        aspectRatio: 16 / 9,
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: const Color(0xFF17211D),
            borderRadius: BorderRadius.circular(12),
          ),
          child: const Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.videocam, color: Colors.white, size: 32),
              SizedBox(height: 6),
              Text(
                'Camera preview required',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                ),
              ),
              SizedBox(height: 3),
              Text(
                'Snapshot will be captured at clock-in and clock-out',
                textAlign: TextAlign.center,
                style: TextStyle(color: Color(0xFFC7D8D0), fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class UnitStatsCard extends StatelessWidget {
  const UnitStatsCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Unit Stats', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 16),
            const Text('Select a trainer and unit to view teaching progress.'),
            const SizedBox(height: 24),
            const LinearProgressIndicator(value: 0),
            const SizedBox(height: 12),
            const Text('Completed: 0.0 hrs'),
            const Text('Remaining: 0.0 hrs'),
          ],
        ),
      ),
    );
  }
}
