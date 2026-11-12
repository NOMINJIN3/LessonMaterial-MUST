import 'package:flutter/material.dart';

import '../models/student_data.dart';

class StudentDetailPage extends StatelessWidget {
  const StudentDetailPage({super.key});

  @override
  Widget build(BuildContext context) {
    // Жагсаалтаас дамжуулсан оюутныг уншина
    final student = ModalRoute.of(context)!.settings.arguments as Student;

    return Scaffold(
      appBar: AppBar(
        title: Text(student.name),
        backgroundColor: Theme.of(context).colorScheme.primary,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: CircleAvatar(
                radius: 40,
                child: Text(student.name[0], style: const TextStyle(fontSize: 32)),
              ),
            ),
            const SizedBox(height: 24),
            Text('ID: ${student.id}', style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 8),
            Text('Мэргэжил: ${student.major}', style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 8),
            Text('Курс: ${student.year}', style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 32),
            Row(
              children: [
                // Үр дүнгүй энгийн буцах
                OutlinedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Буцах'),
                ),
                const SizedBox(width: 12),
                // Нэмэлт даалгавар: "таалагдсан" үр дүнтэй буцах
                FilledButton.icon(
                  onPressed: () => Navigator.pop(context, true),
                  icon: const Icon(Icons.favorite),
                  label: const Text('Таалагдлаа'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}