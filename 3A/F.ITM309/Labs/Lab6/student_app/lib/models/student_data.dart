class Student {
  const Student({
    required this.id,
    required this.name,
    required this.major,
    required this.year,
  });

  final int id;
  final String name;
  final String major;
  final int year;
}

class StudentData {
  static const List<Student> students = [
    Student(id: 1, name: 'Оюунаа', major: 'Программ хангамж', year: 3),
    Student(id: 2, name: 'Бат-Эрдэнэ', major: 'Кибер аюулгүй байдал', year: 2),
    Student(id: 3, name: 'Сараа', major: 'Дата шинжлэх ухаан', year: 1),
  ];
}
