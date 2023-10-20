import os
import psycopg2
from flask import Flask, g, request
from flask import jsonify
from psycopg2 import sql
import math
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

DATABASE_NAME = 'webdevtask'
DATABASE_USER = 'webdevtask'
DATABASE_PASSWORD = '123456789'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432

conn = psycopg2.connect(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    port=DATABASE_PORT,
)


def is_prime(number):
    if number < 2:
        return False

    upper_bound = int(math.sqrt(number) + 1)
    for i in range(2, upper_bound):
        if number % i == 0:
            return False
    return True


def find_nth_prime_number(n, id, conn):
    try:
        with conn.cursor() as cursor:
            update_is_running = sql.SQL('UPDATE tasksolver_task SET is_running = %s WHERE id = %s;')
            cursor.execute(update_is_running, (True, id))
            conn.commit()

            print("**************** Committed!")
    except Exception as e:
        print("Error occurred while updating database:", str(e))
        conn.rollback()

    prime_count, candidate, iteration_count = 0, 2, 0
    previous_percent = -1
    while True:
        if is_prime(candidate):
            prime_count += 1
            if prime_count == n:
                write_final_result(candidate, id, conn)
                conn.commit()
                return candidate

        iteration_count += 1
        candidate += 1
        current_percent = int((candidate / n) * 100)

        if current_percent != previous_percent and 0 <= current_percent <= 100:
            status = update_db(current_percent, id, conn)
            if status == 'error':
                print("THERE WAS AN ERROR WHILE UPDATING DB...")
                break
            previous_percent = current_percent
    return None


def update_db(percentage, id, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL('SELECT id FROM tasksolver_task WHERE id = %s;'), (id,))
            existing_row = cursor.fetchone()

            if existing_row:
                update_query = sql.SQL('UPDATE tasksolver_task SET completion_percentage = %s WHERE id = %s;')
                cursor.execute(update_query, (percentage, id))
                conn.commit()
                print("**************** ITERATIONS")
                get_data_by_id = sql.SQL('SELECT * FROM tasksolver_task WHERE id = %s;')
                cursor.execute(get_data_by_id, (id,))
                row = cursor.fetchone()
                print("ID\tnumber\tuser\tis_running\tis_finished\tresult\t%")
                res_row = [str(i) for i in row] if row else []
                print('\t'.join(res_row))
                return 'success'
            else:
                print(f"TASK ID {id} DOES NOT EXIST IN DB.")
                return 'error'
    except Exception as e:
        print("Error occurred while updating database:", str(e))

    try:
        with conn.cursor() as cursor:
            print("**************** ITERATIONS")
            get_data_by_id = sql.SQL('SELECT * FROM tasksolver_task WHERE id = %s;')
            cursor.execute(get_data_by_id, (id,))
            row = cursor.fetchone()
            print("ID\tnumber\tuser\tis_running\tis_finished\tresult\t%")
            res_row = [str(i) for i in row] if row else []
            print('\t'.join(res_row))
    except Exception as e:
        print("Error occurred while updating database:", str(e))


def write_final_result(result, id, conn):
    try:
        with conn.cursor() as cursor:
            update_query = sql.SQL('UPDATE tasksolver_task SET result = %s, is_running = %s, is_finished = %s WHERE id = %s;')
            print("**************** WRITING FINAL RESULT")
            print("**************** RESULT:", result)
            print("**************** ID:", id)
            cursor.execute(update_query, (result, False, True, id))
            conn.commit()
    except Exception as e:
        print("Error occurred while updating/querying database:", str(e))


@app.route('/process_number/', methods=['POST'])
def process_number():
    data = request.get_json()
    print(f'Processing number: {data}')
    id = data['task_id']
    number = int(data['number'])
    global conn
    result = find_nth_prime_number(number, id, conn)
    conn.commit()

    return jsonify({'status': 'success', 'result': result})


@app.route('/home', methods=['GET'])
def home():
    return jsonify({'status': 'success', 'result': 'Hello world!', 'served_from': str(os.getpid())})


if __name__ == '__main__':
    app.run(debug=True)
