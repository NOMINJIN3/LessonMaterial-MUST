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
  final int year; // Курс
}

const students = [
  Student(id: 1, name: 'Оюунаа', major: 'Программ хангамж', year: 2),
  Student(id: 2, name: 'Бат-Эрдэнэ', major: 'Кибер аюулгүй байдал', year: 3),
  Student(id: 3, name: 'Сараа', major: 'Дата шинжлэх ухаан', year: 1),
  Student(id: 4, name: 'Тэмүүлэн', major: 'Компьютерийн ухаан', year: 4),
  Student(id: 5, name: 'Номин', major: 'Мэдээллийн систем', year: 2),
];
