import 'package:flutter/material.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(24),
      children: const [
        Center(child: CircleAvatar(radius: 48, child: Icon(Icons.person, size: 48))),
        SizedBox(height: 16),
        Center(child: Text('Номинжин', style: TextStyle(fontSize: 22))),
        SizedBox(height: 24),
        ListTile(leading: Icon(Icons.email), title: Text('ts.nominjin2006@gmail.com')),
        ListTile(leading: Icon(Icons.school), title: Text('Мобайл хөгжүүлэлт')),
        ListTile(leading: Icon(Icons.assignment), title: Text('Лабораторийн ажил №6')),
      ],
    );
  }
}