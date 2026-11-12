import 'package:flutter/material.dart';
import 'package:provider/provider.dart';



/// Тоолуурын төлөв — Provider-оор апп даяар дамжина
class CounterModel extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }

  void decrement() {
    _count--;
    notifyListeners();
  }

  void reset() {
    _count = 0;
    notifyListeners();
  }
}

/// Light/Dark горимын төлөв
class ThemeModel extends ChangeNotifier {
  bool _isDarkMode = false;
  bool get isDarkMode => _isDarkMode;

  void toggleTheme() {
    _isDarkMode = !_isDarkMode;
    notifyListeners();
  }
}


void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CounterModel()),
        ChangeNotifierProvider(create: (_) => ThemeModel()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    final themeModel = context.watch<ThemeModel>();
    return MaterialApp(
      title: 'Counter + Theme',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF58A6FF),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF58A6FF),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: themeModel.isDarkMode ? ThemeMode.dark : ThemeMode.light,
      home: const CounterPage(),
    );
  }
}



class CounterPage extends StatelessWidget {
  const CounterPage({super.key});

  /// Нэмэлт даалгавар: утгаас хамаарч өнгө өөрчлөх
  Color _countColor(int count, BuildContext context) {
    if (count >= 10) return Colors.green;
    if (count < 0) return Colors.red;
    return Theme.of(context).colorScheme.primary;
  }

  @override
  Widget build(BuildContext context) {
    final isDark = context.watch<ThemeModel>().isDarkMode;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Лаб №5 - Counter'),
        actions: [
          Row(
            children: [
              Icon(isDark ? Icons.dark_mode : Icons.light_mode, size: 18),
              Switch(
                value: isDark,
                onChanged: (_) => context.read<ThemeModel>().toggleTheme(),
              ),
            ],
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const SizedBox(height: 24),
            Text(
              'Тоолуурын утга (Provider):',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),

            // Зөвхөн энэ хэсэг count өөрчлөгдөхөд дахин зурагдана
            Consumer<CounterModel>(
              builder: (context, model, child) => AnimatedDefaultTextStyle(
                duration: const Duration(milliseconds: 300),
                style: TextStyle(
                  fontSize: 64,
                  fontWeight: FontWeight.bold,
                  color: _countColor(model.count, context),
                ),
                child: Text('${model.count}'),
              ),
            ),
            Consumer<CounterModel>(
              builder: (context, model, child) => Text(
                model.count >= 10
                    ? '10-д хүрлээ!'
                    : model.count < 0
                        ? 'Сөрөг утга'
                        : '',
                style: TextStyle(color: _countColor(model.count, context)),
              ),
            ),
            const SizedBox(height: 20),

            // Хасах / Тэглэх / Нэмэх
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                FloatingActionButton(
                  heroTag: 'inc',
                  onPressed: () => context.read<CounterModel>().increment(),
                  child: const Icon(Icons.add),
                ),
                const SizedBox(width: 16),
                FloatingActionButton(
                  heroTag: 'reset',
                  onPressed: () => context.read<CounterModel>().reset(),
                  child: const Icon(Icons.refresh),
                ),
                const SizedBox(width: 16),
                FloatingActionButton(
                  heroTag: 'dec',
                  onPressed: () => context.read<CounterModel>().decrement(),
                  child: const Icon(Icons.remove),
                ),
              ],
            ),
            const SizedBox(height: 40),
            const Divider(),
            const SizedBox(height: 16),

            
            const LocalCounter(),
          ],
        ),
      ),
    );
  }
}

/// setState ашигласан тоолуур — төлөв нь зөвхөн энэ widget дотор хадгалагдана
class LocalCounter extends StatefulWidget {
  const LocalCounter({super.key});

  @override
  State<LocalCounter> createState() => _LocalCounterState();
}

class _LocalCounterState extends State<LocalCounter> {
  int _count = 0;

  void _increment() {
    setState(() {
      _count++;
    });
  }

  void _decrement() {
    setState(() {
      _count--;
    });
  }

  void _reset() {
    setState(() {
      _count = 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Локал тоолуур (setState)',
                    style: Theme.of(context).textTheme.titleSmall,
                  ),
                  Text(
                    '$_count',
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            IconButton(
              onPressed: _decrement,
              icon: const Icon(Icons.remove),
            ),
            IconButton(
              onPressed: _reset,
              icon: const Icon(Icons.refresh),
            ),
            IconButton.filled(
              onPressed: _increment,
              icon: const Icon(Icons.add),
            ),
          ],
        ),
      ),
    );
  }
}