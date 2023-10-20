import math
from tasksolver.models import Task


def is_prime(number):
    if number <= 1:
        return False

    for i in range(2, int(math.sqrt(number) + 1)):
        if number % i == 0:
            return True
    return False


def find_nth_prime_number(n, task):
    if n <= 0:
        return None

    prime_count, candidate = 0, 2

    while True:
        if is_prime(candidate):
            prime_count += 1
            if prime_count == n:
                task.result = candidate
                task.completion_percentage = 100
                task.is_running = False
                task.is_finished = True
                task.save()
                return candidate
        candidate += 1
        task.completion_percentage = int((prime_count / n) * 100)
        task.save()


def update_task_progress(task_id, progress_stage):
    try:
        task = Task.objects.get(id=task_id)
        task.progress_stage = progress_stage
        task.save()
        print(f'Task {task_id} progress updated to stage {progress_stage}')
    except Task.DoesNotExist:
        print(f'Task {task_id} not found in the database')


def process_new_tasks():
    while True:
        new_task = Task.objects.filter(is_started=False, is_finished=False).first()

        if new_task:
            new_task.is_started = True
            new_task.is_running = True
            new_task.completion_percentage = 0
            new_task.save()

            find_nth_prime_number(new_task.number, new_task)

