import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

// Dart хэлний үндэс: хувьсагч, төрөл, функц
const String userName = 'Ц.Номинжин';
const String major = 'Мэдээллийн технологийн инженер';
const String className = 'IT-3 анги, ШУТИС-Мэдээлэл,Холбооны Технологийн Сургууль';
const int followers = 128;
const int following = 97;
const int posts = 42;
const double gpa = 3.2;
const bool isStudent = true;
var email = 'ts.nominjin2006@example.mn'; // var — төрлийг автоматаар тодорхойлно

String greet(String name) {
  return 'Сайн байна уу, $name!';
}

// Үндсэн өнгө
const Color accent = Color(0xFF00BFFF);

void main() {
  runApp(const ProfileCardApp());
}

class ProfileCardApp extends StatelessWidget {
  const ProfileCardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Profile Card',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: accent),
        textTheme: GoogleFonts.nunitoTextTheme(),
      ),
      home: const ProfileCardPage(),
    );
  }
}

class ProfileCardPage extends StatelessWidget {
  const ProfileCardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Лаб №2 - Profile Card'),
        backgroundColor: accent,
        foregroundColor: Colors.white,
        centerTitle: true,
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFFE6F9FF), Color(0xFFB3ECFF)],
          ),
        ),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: SizedBox(
              height: 700, // картын тогтмол өндөр — хүссэнээрээ өөрчилж болно
              child: Card(
              elevation: 8,
              shadowColor: accent.withValues(alpha: 0.4),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(24),
              ),
              child: Padding(
                padding: const EdgeInsets.fromLTRB(24, 32, 24, 24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly, // агуулгыг тэгш тараана
                  children: [
                    const CircleAvatar(
                      radius: 62,
                      backgroundColor: accent,
                      child: CircleAvatar(
                        radius: 57,
                        backgroundImage: AssetImage('assets/profile_picture.jpg'),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      userName,
                      style: const TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.w800,
                        color: Color(0xFF00455C),
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      major,
                      style: TextStyle(fontSize: 16, color: Colors.grey[700]),
                    ),
                    const SizedBox(height: 10),
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.school, size: 18, color: accent),
                        const SizedBox(width: 6),
                        Flexible(
                          child: Text(
                            className,
                            textAlign: TextAlign.center,
                            style: TextStyle(fontSize: 14, color: Colors.grey[600]),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '${greet(userName)}  •  GPA: $gpa  •  ${isStudent ? 'Оюутан' : 'Төгссөн'}',
                      style: const TextStyle(fontSize: 13, color: accent),
                    ),
                    const Padding(
                      padding: EdgeInsets.symmetric(vertical: 20),
                      child: Divider(),
                    ),
                    Row(
                      children: [
                        const Expanded(
                          child: _StatItem(label: 'Дагагч', value: '$followers'),
                        ),
                        _divider(),
                        const Expanded(
                          child: _StatItem(label: 'Дагаж буй', value: '$following'),
                        ),
                        _divider(),
                        const Expanded(
                          child: _StatItem(label: 'Нийтлэл', value: '$posts'),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 1, vertical: 12),
                      decoration: BoxDecoration(
                        color: const Color(0xFFE6F9FF),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                    const SizedBox(height: 10),
                          const Icon(Icons.email_outlined, size: 18, color: accent),
                          const SizedBox(width: 8),
                          Flexible(
                            child: Text(email, style: const TextStyle(fontSize: 14)),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _divider() => SizedBox(
        height: 60,
        child: VerticalDivider(color: Colors.grey[300], thickness: 1),
      );
}

class _StatItem extends StatelessWidget {
  final String label;
  final String value;

  const _StatItem({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Color(0xFF00455C),
          ),
        ),
        const SizedBox(height: 2),
        Text(label, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
      ],
    );
  }
}