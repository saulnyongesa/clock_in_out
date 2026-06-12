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
  String connectionStatus = 'Not tested';
  bool isCheckingConnection = false;

  @override
  void dispose() {
    backendUrlController.dispose();
    idController.dispose();
    pinController.dispose();
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
          Expanded(
            flex: 3,
            child: Padding(
              padding: const EdgeInsets.all(32),
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
                  Row(
                    children: [
                      FilledButton.icon(
                        onPressed:
                            isCheckingConnection ? null : testBackendConnection,
                        icon: const Icon(Icons.wifi_tethering),
                        label: const Text('Test Connection'),
                      ),
                      const SizedBox(width: 12),
                      Expanded(child: Text(connectionStatus)),
                    ],
                  ),
                  const Spacer(),
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
                  const Spacer(),
                ],
              ),
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
