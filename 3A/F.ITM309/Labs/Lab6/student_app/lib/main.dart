import 'package:flutter/material.dart';
import 'models/student_data.dart';
import 'pages/student_detail_page.dart';
void main() {
runApp(const StudentApp());
}
class StudentApp extends StatelessWidget {
const StudentApp({super.key});
@override
Widget build(BuildContext context) {
return MaterialApp(
title: 'Student App',
theme: ThemeData(primarySwatch: Colors.blue),
initialRoute: '/',
routes: {
'/': (context) => const MainNavigation(),
'/detail': (context) => const StudentDetailPage(),
},
);
}
}
// BottomNavigationBar-тай үндсэн скелет
class MainNavigation extends StatefulWidget {
const MainNavigation({super.key});
@override
State<MainNavigation> createState() => _MainNavigationState();
}
class _MainNavigationState extends State<MainNavigation> {
int _currentIndex = 0;
final List<Widget> _pages = const [
StudentListPage(),
Center(child: Text('Мэдэгдлийн хуудас')),
Center(child: Text('Профайлын хуудас')),
];
@override
Widget build(BuildContext context) {
return Scaffold(
appBar: AppBar(title: const Text('Лаб №6 - Student App')),
drawer: Drawer(
child: ListView(
children: [
const DrawerHeader(
decoration: BoxDecoration(color: Colors.blue),
child: Text('Цэс', style: TextStyle(
color: Colors.white, fontSize: 22)),
),
ListTile(leading: const Icon(Icons.settings),
title: const Text('Тохиргоо'),
onTap: () => Navigator.pop(context),
),
ListTile(
leading: const Icon(Icons.info),
title: const Text('Тухай апп'),
onTap: () => Navigator.pop(context),
),
],
),
),
body: _pages[_currentIndex],
bottomNavigationBar: BottomNavigationBar(
currentIndex: _currentIndex,
onTap: (index) => setState(() => _currentIndex = index),
items: const [
BottomNavigationBarItem(
icon: Icon(Icons.list), label: 'Жагсаалт'),
BottomNavigationBarItem(
icon: Icon(Icons.notifications), label: 'Мэдэгдэл'),
BottomNavigationBarItem(
icon: Icon(Icons.person), label: 'Профайл'),
],
),
);
}
}
class StudentListPage extends StatelessWidget {
const StudentListPage({super.key});
static const _students = StudentData.students;
@override
Widget build(BuildContext context) {
return ListView.builder(
itemCount: _students.length,
itemBuilder: (context, index) {
final student = _students[index];
return ListTile(
leading: const CircleAvatar(child: Icon(Icons.person)),
title: Text(student.name),
subtitle: Text(student.major),
onTap: () {
Navigator.pushNamed(
context, '/detail', arguments: student);
},);
},
);
}
}
