import concurrent.futures
from django.shortcuts import render
from .models import Task
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
import requests
from background_task import background
import json


logger = logging.getLogger(__name__)

global task_limit
task_limit = 20


@login_required
def process_number(request):
    tasks = Task.objects.filter(user=request.user)
    user_tasks = {}

    for task in tasks:
        user_tasks[task.id] = {
            'is_running': task.is_running,
            'is_finished': task.is_finished,
            'result': task.result,
        }

    return render(request, 'tasksolver/detail.html', {'tasks': user_tasks})


# def fetch(session, url, data, task_id):
#     try:
#         with session.post(url, json=data, headers={'Content-Type': 'application/json'}) as response:
#             response.raise_for_status()
#             logger.info(f"Task ID {task_id} processed successfully.")
#     except Exception as e:
#         logger.error(f"Error processing Task ID {task_id}: {str(e)}")


# @background(schedule=2)
# def nginx_caller():
#     logger.info("Checking for new tasks...")
#     url = 'http://localhost:80/process_number/'
#
#     try:
#         tasks = Task.objects.filter(is_running=False, is_finished=False)
#         if tasks:
#             logger.info(f'*********** TASKS ')
#             logger.info(f"TASK LENGTH: {tasks.count()}")
#
#             jsons = [{'task_id': task.id, 'number': task.number} for task in tasks]
#
#             with ThreadPoolExecutor(max_workers=5) as executor:
#                 with requests.Session() as session:
#                     executor.map(lambda data: fetch(session, url, **data), jsons)
#                     executor.shutdown(wait=True)
#
#             logger.info(f'*********** POST OK ')
#         else:
#             logger.info('No available tasks found in the database.')
#         return JsonResponse({'status': 'success'})
#     except Exception as e:
#         logger.error(f'*********** START OF ERROR ***********')
#         logger.error(f'Error occurred while calling nginx: {str(e)}')
#         logger.error(f'*********** END OF ERROR ***********')
#         return JsonResponse({'status': 'error', 'error': str(e)})

@background(schedule=1)
def nginx_caller():
    logger.info("Checking for new tasks...")
    url = 'http://localhost:80/process_number/'

    try:
        tasks = Task.objects.filter(is_running=False, is_finished=False)
        if tasks:
            logger.info(f'*********** TASKS ')
            logger.info(f"TASK LENGTH: {tasks.count()}")

            jsons = [{'task_id': task.id, 'number': task.number} for task in tasks]

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(send_request, url, data): data for data in jsons}
                concurrent.futures.wait(futures)

                for future in concurrent.futures.as_completed(futures):
                    data = futures[future]
                    try:
                        response = future.result()
                        logger.info(f"Task ID {data['task_id']} processed successfully.")
                    except Exception as e:
                        logger.error(f"Error processing Task ID {data['task_id']}: {str(e)}")

            logger.info(f'*********** POST OK ')
        else:
            logger.info('No available tasks found in the database.')
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f'*********** START OF ERROR ***********')
        logger.error(f'Error occurred while calling nginx: {str(e)}')
        logger.error(f'*********** END OF ERROR ***********')
        return JsonResponse({'status': 'error', 'error': str(e)})


def send_request(url, data):
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response
    except Exception as e:
        raise Exception(f"Error sending request: {str(e)}")

# @background(schedule=1)
# def nginx_caller():
#     logger.info("Checking for new tasks...")
#     url = 'http://localhost:80/process_number/'
#
#     try:
#         task = Task.objects.filter(is_running=False, is_finished=False).first()
#         if task:
#             logger.info(f"NEW TASK: {task.id}")
#             logger.info(f"Task number: {task.number}")
#             logger.info(f"Is running: {task.is_running}")
#             logger.info(f"Is finished: {task.is_finished}")
#
#             body = {'task_id': task.id, 'number': task.number}
#
#             x = requests.post(url, json=body, headers={'Content-Type': 'application/json'})
#             logger.info(f'*********** POST OK ')
#         else:
#             logger.info('No available tasks found in the database.')
#         return JsonResponse({'status': 'success'})
#     except Exception as e:
#         logger.error(f'*********** START OF ERROR ***********')
#         logger.error(f'Error occurred while calling nginx: {str(e)}')
#         logger.error(f'*********** END OF ERROR ***********')
#         return JsonResponse({'status': 'error', 'error': str(e)})


def add_task(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        number = data['number']

        if 1 <= int(number) <= 1000000000:
            logger.info(f'ADDING TASK WITH NEW NUMBER: {number}')
            logger.info(f'REQUEST BODY: {data}')

            tasks = Task.objects.filter(user=request.user)

            if tasks.count() < task_limit:
                task = Task(number=number, user=request.user, is_running=False, is_finished=False,
                            completion_percentage=0, result=-1)
                task.save()
            else:
                response = {
                    'status': 'error',
                    'message': 'You have reached the maximum number of tasks (20).',
                }
                return JsonResponse(response, status=400)

            tasks = Task.objects.filter(user=request.user)

            logging.debug(f'Generated Task ID: {task.id}')
            logging.debug(f'Generated Task Number: {task.number}')
            logging.debug(f'Generated Task User: {task.user}')
            logging.debug(f'Generated Task is_running: {task.is_running}')
            logging.debug(f'Generated Task is_finished: {task.is_finished}')
            logging.debug(f'Generated Task completion_percentage: {task.completion_percentage}')
            logging.debug(f'Generated Task result: {task.result}')

            task_status = {}
            for task in tasks:
                task_status[task.id] = {
                    'is_running': task.is_running,
                    'is_finished': task.is_finished,
                    'result': task.result,
                }

            return JsonResponse({'task_status': task_status,
                                 'form_input': number,
                                 'count': tasks.count(),
                                 'number_of_tasks_left': task_limit - tasks.count(),
                                 'message': ''})
        else:
            response_data = {
                'status': 'error',
                'message': 'Invalid input: Number must be between 1 and 1,000,000,000 (1B).',
            }
            return JsonResponse(response_data, status=400)
    else:
        response_data = {
            'status': 'error',
            'message': 'Invalid request method',
        }
        return JsonResponse(response_data, status=400)


def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
        tasks = Task.objects.filter(user=request.user)
        task_data = [{'id': t.id, 'number': t.number, 'is_running': t.is_running} for t in tasks]
        return JsonResponse({
            'tasks': task_data,
            'deleted': True,
            'message': 'Invalid input: Number must be between 1 and 1,000,000,000 (1B).',
        })
    except Task.DoesNotExist:
        return JsonResponse({
            'deleted': False,
            'message': 'Task not found'
        }, status=404)


def check_task_status(request):
    tasks = Task.objects.filter(user=request.user)
    count = tasks.count()
    tasks_left = task_limit - count
    if not tasks:
        return JsonResponse({'task_status': [], 'count': count, 'number_of_tasks_left': tasks_left})

    task_status = {}

    for task in tasks:
        task_status[task.id] = {
            'number': task.number,
            'is_running': task.is_running,
            'is_finished': task.is_finished,
            'completion_percentage': task.completion_percentage,
            'result': task.result,
        }

    return JsonResponse({
        'task_status': task_status,
        'count': count,
        'number_of_tasks_left': tasks_left,
        'message': '',
    })
