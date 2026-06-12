import 'package:flutter/material.dart';

void main() {
  runApp(const MobileRegistrationApp());
}

class MobileRegistrationApp extends StatelessWidget {
  const MobileRegistrationApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Trainer Registration',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0E7A5F)),
        useMaterial3: true,
      ),
      home: const TrainerRegistrationScreen(),
    );
  }
}

class TrainerRegistrationScreen extends StatelessWidget {
  const TrainerRegistrationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Register Trainer')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const CircleAvatar(
            radius: 48,
            child: Icon(Icons.person_add_alt_1, size: 42),
          ),
          const SizedBox(height: 24),
          const TextField(
            decoration: InputDecoration(
              labelText: 'Full Name',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          const TextField(
            decoration: InputDecoration(
              labelText: 'ID Number',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          const TextField(
            keyboardType: TextInputType.phone,
            decoration: InputDecoration(
              labelText: 'Phone',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          const TextField(
            obscureText: true,
            decoration: InputDecoration(
              labelText: 'Trainer PIN',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 20),
          OutlinedButton.icon(
            onPressed: null,
            icon: const Icon(Icons.camera_alt_outlined),
            label: const Text('Capture Profile Photo'),
          ),
          const SizedBox(height: 12),
          const FilledButton(onPressed: null, child: Text('Save Trainer')),
        ],
      ),
    );
  }
}
