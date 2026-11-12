import 'package:flutter/material.dart';

const kPrimaryColor = Color(0xFF58A6FF);

void main() => runApp(const RegistrationFormApp());

class RegistrationFormApp extends StatelessWidget {
  const RegistrationFormApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: kPrimaryColor)),
        home: const RegistrationPage(),
      );
}

class RegistrationPage extends StatefulWidget {
  const RegistrationPage({super.key});

  @override
  State<RegistrationPage> createState() => _RegistrationPageState();
}

class _RegistrationPageState extends State<RegistrationPage> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _confirm = TextEditingController();

  double _age = 18;
  bool _notifications = true;
  bool _obscure = true;

  @override
  void dispose() {
    for (final c in [_name, _email, _password, _confirm]) {
      c.dispose();
    }
    super.dispose();
  }

  // ---------- Validator-ууд ----------
  String? _validateName(String? v) => v!.trim().isEmpty
      ? 'Нэрээ оруулна уу'
      : v.trim().length < 2 ? 'Нэр дор хаяж 2 тэмдэгт байх' : null;

  String? _validateEmail(String? v) => v!.trim().isEmpty
      ? 'И-мэйл оруулна уу'
      : !RegExp(r'^[\w.+-]+@[\w-]+\.[\w.-]+$').hasMatch(v.trim())
          ? 'И-мэйл формат буруу'
          : null;

  String? _validatePassword(String? v) => v!.isEmpty
      ? 'Нууц үг оруулна уу'
      : v.length < 6
          ? 'Дор хаяж 6 тэмдэгт байх'
          : !RegExp(r'\d').hasMatch(v) ? 'Дор хаяж 1 тоо агуулсан байх' : null;

  String? _validateConfirm(String? v) => v!.isEmpty
      ? 'Нууц үгээ давтан оруулна уу'
      : v != _password.text ? 'Нууц үг таарахгүй байна' : null;

  // ---------- Илгээх ----------
  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Алдаатай талбаруудыг засна уу'),
        backgroundColor: Colors.red,
      ));
      return;
    }

    await showDialog<void>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Амжилттай бүртгэгдлээ!'),
        content: Text('Нэр: ${_name.text.trim()}\n'
            'И-мэйл: ${_email.text.trim()}\n' 
            'Нас: ${_age.round()}\n'
            'Мэдэгдэл: ${_notifications ? "Тийм" : "Үгүй"}'),
        actions: [TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('OK'))],
      ),
    );
    if (mounted) _reset();
  }

  void _reset() {
    _formKey.currentState!.reset();
    for (final c in [_name, _email, _password, _confirm]) {
      c.clear();
    }
    setState(() {
      _age = 18;
      _notifications = true;
    });
  }

  // ---------- UI ----------
  Widget _field(TextEditingController c, String label, FormFieldValidator<String> validator,
          {bool password = false, TextInputType? keyboard}) =>
      Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: TextFormField(
          controller: c,
          obscureText: password && _obscure,
          keyboardType: keyboard,
          validator: validator,
          decoration: InputDecoration(
            labelText: label,
            border: const OutlineInputBorder(),
            suffixIcon: password
                ? IconButton(
                    icon: Icon(_obscure ? Icons.visibility : Icons.visibility_off),
                    onPressed: () => setState(() => _obscure = !_obscure),
                  )
                : null,
          ),
        ),
      );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Лаб №4 - Бүртгүүлэх'),
        backgroundColor: kPrimaryColor,
        foregroundColor: Colors.white,
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _field(_name, 'Нэр', _validateName),
            _field(_email, 'И-мэйл', _validateEmail, keyboard: TextInputType.emailAddress),
            _field(_password, 'Нууц үг', _validatePassword, password: true),
            _field(_confirm, 'Нууц үг давтах', _validateConfirm, password: true),

            Text('Нас: ${_age.round()}'),
            Slider(
              value: _age,
              min: 10,
              max: 80,
              divisions: 70,
              label: '${_age.round()}',
              onChanged: (v) => setState(() => _age = v),
            ),

            SwitchListTile(
              title: const Text('Мэдэгдэл хүлээн авах'),
              value: _notifications,
              onChanged: (v) => setState(() => _notifications = v),
            ),

            // Checkbox-ийг FormField-д ороосон тул validate()/reset()-д хамрагдана
            FormField<bool>(
              initialValue: false,
              validator: (v) => v! ? null : 'Үйлчилгээний нөхцөлийг зөвшөөрнө үү',
              builder: (field) => CheckboxListTile(
                title: const Text('Үйлчилгээний нөхцөлтэй танилцсан'),
                value: field.value,
                onChanged: field.didChange,
                subtitle: field.hasError
                    ? Text(field.errorText!, style: const TextStyle(color: Colors.red))
                    : null,
              ),
            ),
            const SizedBox(height: 16),

            ElevatedButton(onPressed: _submit, child: const Text('Бүртгүүлэх')),
            TextButton(onPressed: _reset, child: const Text('Цэвэрлэх')),
          ],
        ),
      ),
    );
  }
}