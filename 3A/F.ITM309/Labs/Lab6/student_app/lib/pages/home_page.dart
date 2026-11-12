import 'package:flutter/material.dart';

import '../models/student_data.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key, required this.onOpenList});

  final VoidCallback onOpenList;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.school, size: 80, color: Theme.of(context).colorScheme.primary),
            const SizedBox(height: 16),
            const Text('Тавтай морил!', style: TextStyle(fontSize: 24)),
            const SizedBox(height: 8),
            Text('Нийт ${StudentData.students.length} оюутан бүртгэлтэй байна'),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: onOpenList,
              icon: const Icon(Icons.list),
              label: const Text('Жагсаалт харах'),
            ),
          ],
        ),
      ),
    );
  }
}