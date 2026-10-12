// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:hello_flutter/main.dart';

void main() {
  testWidgets('displays the hello Flutter page', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const HelloFlutterApp());

    expect(find.text('Hello, Flutter!'), findsOneWidget);
    expect(find.text('Лаб №1 - Hello Flutter'), findsOneWidget);
    expect(find.byIcon(Icons.flutter_dash), findsOneWidget);
  });
}
