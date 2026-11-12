import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

// ---------------------------------------------------------------------------
// API тохиргоо
// ---------------------------------------------------------------------------
const kBaseUrl = 'https://jsonplaceholder.typicode.com';
const kTimeout = Duration(seconds: 10);

// ---------------------------------------------------------------------------
// Model классууд — JSON-г Dart объект руу хөрвүүлнэ
// ---------------------------------------------------------------------------
class Article {
  final int id;
  final int userId;
  final String title;
  final String description;

  Article({
    required this.id,
    required this.userId,
    required this.title,
    required this.description,
  });

  /// JSON → Article. Талбар дутуу ирвэл анхдагч утга өгнө.
  factory Article.fromJson(Map<String, dynamic> json) {
    return Article(
      id: json['id'] ?? 0,
      userId: json['userId'] ?? 0,
      title: json['title'] ?? 'Гарчиггүй',
      description: json['body'] ?? '',
    );
  }

  /// JSONPlaceholder зураггүй тул мэдээ бүрт id-аар тогтмол зураг онооно
  String get imageUrl => 'https://picsum.photos/seed/news$id/600/400';
}

class Comment {
  final String name;
  final String email;
  final String body;

  Comment({required this.name, required this.email, required this.body});

  factory Comment.fromJson(Map<String, dynamic> json) {
    return Comment(
      name: json['name'] ?? '',
      email: json['email'] ?? '',
      body: json['body'] ?? '',
    );
  }
}

// ---------------------------------------------------------------------------
// API service — http.get → statusCode шалгах → jsonDecode → List<Model>
// ---------------------------------------------------------------------------
Future<List<Article>> fetchArticles() async {
  final response =
      await http.get(Uri.parse('$kBaseUrl/posts')).timeout(kTimeout);

  if (response.statusCode == 200) {
    final List data = jsonDecode(response.body);
    return data.map((e) => Article.fromJson(e)).toList();
  } else {
    throw Exception('Сервер ${response.statusCode} алдаа буцаалаа');
  }
}

Future<List<Comment>> fetchComments(int postId) async {
  final response = await http
      .get(Uri.parse('$kBaseUrl/posts/$postId/comments'))
      .timeout(kTimeout);

  if (response.statusCode == 200) {
    final List data = jsonDecode(response.body);
    return data.map((e) => Comment.fromJson(e)).toList();
  } else {
    throw Exception('Сервер ${response.statusCode} алдаа буцаалаа');
  }
}

/// Алдааг хэрэглэгчид ойлгомжтой текст болгоно
String friendlyError(Object? error) {
  if (error is TimeoutException) return 'Хүсэлтийн хугацаа дууслаа (10 сек).';
  final text = error.toString();
  if (text.contains('SocketException') || text.contains('ClientException')) {
    return 'Интернэт холболтоо шалгана уу.';
  }
  return text.replaceFirst('Exception: ', '');
}

// ---------------------------------------------------------------------------
// Апп
// ---------------------------------------------------------------------------
void main() => runApp(const NewsApp());

class NewsApp extends StatelessWidget {
  const NewsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'News App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.red),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.red,
          foregroundColor: Colors.white,
        ),
      ),
      home: const NewsListPage(),
    );
  }
}

// ---------------------------------------------------------------------------
// 1. Мэдээний жагсаалт — FutureBuilder-ийн 3 төлөв
// ---------------------------------------------------------------------------
class NewsListPage extends StatefulWidget {
  const NewsListPage({super.key});

  @override
  State<NewsListPage> createState() => _NewsListPageState();
}

class _NewsListPageState extends State<NewsListPage> {
  // build() дотор биш, initState-д нэг удаа үүсгэнэ
  late Future<List<Article>> _futureArticles;

  @override
  void initState() {
    super.initState();
    _futureArticles = fetchArticles();
  }

  void _reload() {
    setState(() => _futureArticles = fetchArticles());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Лаб №8 - Мэдээ'),
        actions: [
          IconButton(
            tooltip: 'Шинэчлэх',
            icon: const Icon(Icons.refresh),
            onPressed: _reload,
          ),
        ],
      ),
      body: FutureBuilder<List<Article>>(
        future: _futureArticles,
        builder: (context, snapshot) {
          // Төлөв 1: ачаалж буй
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Мэдээ ачаалж байна...'),
                ],
              ),
            );
          }

          // Төлөв 2: алдаатай
          if (snapshot.hasError) {
            return ErrorView(
              message: friendlyError(snapshot.error),
              onRetry: _reload,
            );
          }

          // Төлөв 3: амжилттай (хоосон байж болно)
          final articles = snapshot.data ?? [];
          if (articles.isEmpty) {
            return const Center(child: Text('Мэдээ олдсонгүй'));
          }

          return RefreshIndicator(
            onRefresh: () async {
              _reload();
              try {
                await _futureArticles;
              } catch (_) {}
            },
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(vertical: 6),
              itemCount: articles.length,
              itemBuilder: (context, index) =>
                  ArticleCard(article: articles[index]),
            ),
          );
        },
      ),
    );
  }
}

class ArticleCard extends StatelessWidget {
  const ArticleCard({super.key, required this.article});

  final Article article;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        // Нэмэлт: дэлгэрэнгүй хуудас руу шилжих
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => NewsDetailPage(article: article)),
        ),
        child: Padding(
          padding: const EdgeInsets.all(10),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Hero(
                tag: 'image-${article.id}',
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: NetImage(url: article.imageUrl, width: 84, height: 84),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      article.title,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: text.titleSmall?.copyWith(fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      article.description,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: text.bodySmall,
                    ),
                    const SizedBox(height: 6),
                    Text(
                      'Мэдээ #${article.id}',
                      style: text.labelSmall?.copyWith(color: Colors.red),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// 2. Дэлгэрэнгүй хуудас (нэмэлт даалгавар) — сэтгэгдлийг мөн API-аас татна
// ---------------------------------------------------------------------------
class NewsDetailPage extends StatefulWidget {
  const NewsDetailPage({super.key, required this.article});

  final Article article;

  @override
  State<NewsDetailPage> createState() => _NewsDetailPageState();
}

class _NewsDetailPageState extends State<NewsDetailPage> {
  late Future<List<Comment>> _futureComments;

  @override
  void initState() {
    super.initState();
    _futureComments = fetchComments(widget.article.id);
  }

  @override
  Widget build(BuildContext context) {
    final article = widget.article;
    final text = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(title: Text('Мэдээ #${article.id}')),
      body: ListView(
        children: [
          Hero(
            tag: 'image-${article.id}',
            child: NetImage(
                url: article.imageUrl, width: double.infinity, height: 220),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  article.title,
                  style: text.titleLarge?.copyWith(fontWeight: FontWeight.w700),
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    const Icon(Icons.person, size: 18, color: Colors.red),
                    const SizedBox(width: 6),
                    Text('Нийтлэгч #${article.userId}', style: text.labelLarge),
                  ],
                ),
                const SizedBox(height: 12),
                Text(article.description, style: text.bodyLarge),
                const Divider(height: 32),
                Text(
                  'Сэтгэгдэл',
                  style: text.titleMedium?.copyWith(fontWeight: FontWeight.w700),
                ),
              ],
            ),
          ),
          FutureBuilder<List<Comment>>(
            future: _futureComments,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Padding(
                  padding: EdgeInsets.all(24),
                  child: Center(child: CircularProgressIndicator()),
                );
              }
              if (snapshot.hasError) {
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Text(
                    'Сэтгэгдэл ачаалж чадсангүй: ${friendlyError(snapshot.error)}',
                    style: const TextStyle(color: Colors.red),
                  ),
                );
              }
              final comments = snapshot.data ?? [];
              return Column(
                children: [
                  for (final c in comments)
                    ListTile(
                      leading: CircleAvatar(
                        child: Text(c.email.isNotEmpty
                            ? c.email[0].toUpperCase()
                            : '?'),
                      ),
                      title: Text(c.name,
                          maxLines: 1, overflow: TextOverflow.ellipsis),
                      subtitle: Text(c.body),
                    ),
                  const SizedBox(height: 16),
                ],
              );
            },
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Туслах widget-үүд
// ---------------------------------------------------------------------------

/// Интернэтээс зураг ачаалж, алдаа гарвал саарал дүрс харуулна
class NetImage extends StatelessWidget {
  const NetImage({
    super.key,
    required this.url,
    required this.width,
    required this.height,
  });

  final String url;
  final double width;
  final double height;

  @override
  Widget build(BuildContext context) {
    return Image.network(
      url,
      width: width,
      height: height,
      fit: BoxFit.cover,
      loadingBuilder: (context, child, progress) => progress == null
          ? child
          : Container(
              width: width,
              height: height,
              color: Colors.grey.shade200,
              alignment: Alignment.center,
              child: const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              ),
            ),
      errorBuilder: (context, error, stack) => Container(
        width: width,
        height: height,
        color: Colors.grey.shade300,
        alignment: Alignment.center,
        child: const Icon(Icons.image_not_supported, color: Colors.grey),
      ),
    );
  }
}

/// FutureBuilder-ийн алдаатай төлөв
class ErrorView extends StatelessWidget {
  const ErrorView({super.key, required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.wifi_off, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            const Text(
              'Мэдээ татаж чадсангүй',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 20),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Дахин оролдох'),
            ),
          ],
        ),
      ),
    );
  }
}