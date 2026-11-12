import 'package:flutter/material.dart';

// ШУТИС-ийн логоны хар хөх өнгө — бүх өнгөний схем үүнээс үүснэ
const kSeedColor = Color(0xFF233A8B);
const kGold = Color(0xFFF5B819);

void main() => runApp(const UniversityApp());

/// Light ба Dark хоёр горимд нэг дүрмээр ThemeData үүсгэнэ
ThemeData buildTheme(Brightness brightness) {
  final scheme = ColorScheme.fromSeed(
    seedColor: kSeedColor,
    brightness: brightness,
  );
  final isDark = brightness == Brightness.dark;

  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    fontFamily: 'Montserrat', // Custom font — апп даяар
    appBarTheme: AppBarTheme(
      backgroundColor: isDark ? scheme.primaryContainer : kSeedColor,
      foregroundColor: isDark ? scheme.onPrimaryContainer : Colors.white,
      elevation: 0,
      centerTitle: false,
      titleTextStyle: TextStyle(
        fontFamily: 'Montserrat',
        fontSize: 18,
        fontWeight: FontWeight.w600,
        color: isDark ? scheme.onPrimaryContainer : Colors.white,
      ),
    ),
    listTileTheme: ListTileThemeData(
      iconColor: scheme.primary,
      titleTextStyle: TextStyle(
        fontFamily: 'Montserrat',
        fontSize: 15,
        fontWeight: FontWeight.w500,
        color: scheme.onSurface,
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: scheme.primary,
        foregroundColor: scheme.onPrimary,
        minimumSize: const Size.fromHeight(48),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        textStyle: const TextStyle(
          fontFamily: 'Montserrat',
          fontSize: 15,
          fontWeight: FontWeight.w600,
        ),
      ),
    ),
  );
}

class UniversityApp extends StatefulWidget {
  const UniversityApp({super.key});

  @override
  State<UniversityApp> createState() => _UniversityAppState();
}

class _UniversityAppState extends State<UniversityApp> {
  ThemeMode _themeMode = ThemeMode.light;

  void _toggleTheme() {
    setState(() {
      _themeMode =
          _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'University Info',
      debugShowCheckedModeBanner: false,
      theme: buildTheme(Brightness.light),
      darkTheme: buildTheme(Brightness.dark),
      themeMode: _themeMode,
      home: UniversityHomePage(
        isDark: _themeMode == ThemeMode.dark,
        onToggleTheme: _toggleTheme,
      ),
    );
  }
}

class UniversityHomePage extends StatelessWidget {
  const UniversityHomePage({
    super.key,
    required this.isDark,
    required this.onToggleTheme,
  });

  final bool isDark;
  final VoidCallback onToggleTheme;

  static const _schools = [
    {'name': 'Мэдээлэл, холбооны технологийн сургууль', 'icon': Icons.computer},
    {'name': 'Барилга, архитектурын сургууль', 'icon': Icons.apartment},
    {'name': 'Бизнесийн удирдлага, хүмүүнлэгийн сургууль', 'icon': Icons.business_center},
    {'name': 'Геологи, уул уурхайн сургууль', 'icon': Icons.terrain},
    {'name': 'Механик, тээврийн сургууль', 'icon': Icons.precision_manufacturing},
    {'name': 'Эрчим хүчний сургууль', 'icon': Icons.bolt},
    {'name': 'Үйлдвэрлэлийн технологи, дизайны сургууль', 'icon': Icons.design_services},
    {'name': 'Хэрэглээний шинжлэх ухааны сургууль', 'icon': Icons.science},
  ];

  void _showMessage(BuildContext context, String text) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text(text)));
  }

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final text = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Лаб №7 - Их сургуулийн апп'),
        actions: [
          IconButton(
            tooltip: isDark ? 'Цайвар горим' : 'Харанхуй горим',
            icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode),
            onPressed: onToggleTheme,
          ),
        ],
      ),
      body: ListView(
        children: [
          // ---------- 1. Толгой хэсэг: кампусын зураг + лого + нэр ----------
          SizedBox(
            height: 210,
            child: Stack(
              fit: StackFit.expand,
              children: [
                Image.asset('assets/images/sict.jpeg', fit: BoxFit.cover),
                // Доод хэсгийг бараан болгож текстийг уншигдахуйц болгоно
                const DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [Color(0x00000000), Color(0xB3000000)],
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Container(
                        width: 64,
                        height: 64,
                        padding: const EdgeInsets.all(6),
                        decoration: const BoxDecoration(
                          color: Colors.white,
                          shape: BoxShape.circle,
                        ),
                        child: Image.asset('assets/images/logo.png'),
                      ),
                      const SizedBox(width: 12),
                      const Expanded(
                        child: Text(
                          'Шинжлэх Ухаан Технологийн Их Сургууль',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.w700,
                            height: 1.3,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // ---------- 2. Товч мэдээлэл ----------
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 4),
            child: Row(
              children: [
                const Icon(Icons.location_city, color: kGold),
                const SizedBox(width: 8),
                Text('Улаанбаатар хот', style: text.bodyMedium),
                const Spacer(),
                const Icon(Icons.language, color: kGold),
                const SizedBox(width: 8),
                Text('www.must.edu.mn', style: text.bodyMedium),
              ],
            ),
          ),

          // ---------- 3. Бүрэлдэхүүн сургуулиуд ----------
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: Text(
              'Бүрэлдэхүүн сургуулиуд',
              style: text.titleMedium?.copyWith(fontWeight: FontWeight.w700),
            ),
          ),
          for (final school in _schools)
            Card(
              margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: scheme.primaryContainer,
                  child: Icon(school['icon'] as IconData,
                      color: scheme.onPrimaryContainer),
                ),
                title: Text(school['name'] as String),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: () => _showMessage(context, school['name'] as String),
              ),
            ),

          // ---------- 4. Товч ----------
          Padding(
            padding: const EdgeInsets.all(16),
            child: ElevatedButton.icon(
              onPressed: () =>
                  _showMessage(context, 'Элсэлтийн мэдээлэл удахгүй нэмэгдэнэ'),
              icon: const Icon(Icons.school),
              label: const Text('Элсэлтийн мэдээлэл'),
            ),
          ),
        ],
      ),
    );
  }
}