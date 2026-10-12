import heapq
from collections import deque


class Task:
    """Даалгаврын үндсэн класс (Base Task)"""

    def __init__(self, task_id, description, priority=1):
        self.task_id = task_id
        self.description = description
        self.priority = priority  
        self.status = "Pending"  

    def get_id(self):
        return self.task_id

    def get_priority(self):
        return self.priority

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return f"[{self.task_id}] {self.description} | Status: {self.status} | Priority: {self.priority}"


class DataProcessingTask(Task):
    """Өгөгдөл боловсруулах даалгаврын SubClass"""

    def __init__(self, task_id, description, data_path, priority=1):
        super().__init__(task_id, description, priority)
        self.data_path = data_path

    def __str__(self):
        return super().__str__() + f" | Data: {self.data_path}"


# Даалгавар 2: Шинэ subClass нэмсэн (ModelEvaluationTask)
class ModelEvaluationTask(Task):
    """Загварын үнэлгээний даалгаврын SubClass"""

    def __init__(self, task_id, description, model_name, accuracy_threshold, priority=1):
        super().__init__(task_id, description, priority)
        self.model_name = model_name
        self.accuracy_threshold = accuracy_threshold

    def __str__(self):
        return super().__str__() + f" | Model: {self.model_name} (Threshold: {self.accuracy_threshold})"


class TaskHistory:
    """Дууссан болон цуцлагдсан ажлуудыг хадгалах Стек (LIFO)"""

    def __init__(self):
        self._history = deque()

    def add_history(self, task):
        self._history.append(task)

    # Даалгавар 6: Алдааны зохицуулалт ба хоосон эсэхийг шалгах
    def undo_last(self):
        """Сүүлийн ажлыг стекээс буцаан гаргаж авах"""
        try:
            if not self._history:
                raise IndexError("Стек хоосон байна! Буцаах ажил олдсонгүй.")
            return self._history.pop()
        except IndexError as e:
            print(f"[Алдаа]: {e}")
            return None


class TaskQueue:
    """Даалгаврыг удирдах дараалал (Queue & Priority Queue)"""

    def __init__(self):
        self.queue = deque()
        self.history = TaskHistory()

    def add_task(self, task):
        """Даалгавар нэмэх"""
        self.queue.append(task)
        print(f"Даалгавар нэмэгдлээ: {task.task_id}")

    # Даалгавар 4: Даалгаврыг цуцлах функц
    def cancel_task(self, task_id):
        """Даалгаврыг ID-аар нь хайж цуцлах"""
        for task in self.queue:
            if task.get_id() == task_id:
                task.set_status("Cancelled")
                self.queue.remove(task)
                self.history.add_history(task)
                print(f"Даалгавар [{task_id}] амжилттай цуцлагдлаа.")
                return True
        print(f"Цуцлах боломжгүй: [{task_id}] ID-тай даалгавар олдсонгүй.")
        return False

    # Даалгавар 5: Тэргүүлэх чиглэлээр эрэмбэлэх (Priority Sort)
    def sort_by_priority(self):
        """FIFO-гээс илүү давуу эрх (Priority)-ээр эрэмбэлэх"""
        sorted_list = sorted(self.queue, key=lambda x: x.get_priority())
        self.queue = deque(sorted_list)
        print("--> Даалгавруудыг priority-гоор эрэмбэллээ.")

    # Даалгавар 3 & 6: Гүйцэтгэлийг сайжруулах ба Алдаа зохицуулалт
    def _execute_task(self, task):
        """Даалгаврын төрлөөс хамаарч өөр өөр боловсруулалт хийх"""
        try:
            task.set_status("Running")
            print(f"\n[Ажиллуулж байна]: {task}")

            if isinstance(task, DataProcessingTask):
                if not task.data_path:
                    raise ValueError("Файлын зам олдсонгүй!")
                print(f"  -> '{task.data_path}' файл дээр өгөгдлийн цэвэрлэгээ ба боловсруулалт хийж байна...")

            elif isinstance(task, ModelEvaluationTask):
                if task.accuracy_threshold < 0 or task.accuracy_threshold > 1:
                    raise ValueError("Нөхцөлт нарийвчлалын утга 0-1 хооронд байх ёстой!")
                print(f"  -> '{task.model_name}' загварыг {task.accuracy_threshold} босгоор үнэлж байна...")

            else:
                print("  -> Ерөнхий даалгаврыг ажиллуулж байна...")

            task.set_status("Completed")
            self.history.add_history(task)
            print(f"[Амжилттай дууслаа]: {task.task_id}")

        except Exception as e:
            task.set_status("Failed")
            print(f"[Алдаа гарлаа] Даалгавар {task.task_id} бүтэлгүйтлээ! Шалтгаан: {e}")

    def process_all_tasks(self):
        """Дараалалд байгаа бүх даалгавруудыг боловсруулах"""
        print("\n--- Даалгавруудыг ажиллуулж эхэллээ ---")
        while self.queue:
            task = self.queue.popleft()
            self._execute_task(task)


# ==========================================
# Тест хийх ба Код ажиллуулах хэсэг
# ==========================================
if __name__ == "__main__":
    t_queue = TaskQueue()

    # Даалгавруудыг үүсгэн нэмэх
    task1 = Task("T101", "Лог файл цэвэрлэх", priority=3)
    task2 = DataProcessingTask("T102", "Датасет бэлтгэх", "data/reviews.csv", priority=1)
    task3 = ModelEvaluationTask("T103", "LLM Загвар үнэлэх", "GPT-4o", 0.85, priority=2)
    task4 = DataProcessingTask("T104", "Алдаатай даалгавар тест", "", priority=1)  # Алдаа заах ёстой (Empty path)

    t_queue.add_task(task1)
    t_queue.add_task(task2)
    t_queue.add_task(task3)
    t_queue.add_task(task4)

    # Даалгавар цуцлах тест
    t_queue.cancel_task("T101")

    # Тэргүүлэх чиглэлээр эрэмбэлэх тест
    t_queue.sort_by_priority()

    # Даалгавруудыг ажиллуулах
    t_queue.process_all_tasks()

    # Стекээс Undo хийж буцаах тест
    print("\n--- Стекийн тест (Undo) ---")
    last_task = t_queue.history.undo_last()
    if last_task:
        print(f"Сүүлд хийгдсэн ажил: {last_task}")
