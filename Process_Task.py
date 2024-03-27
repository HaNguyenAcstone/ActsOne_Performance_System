from flask import Flask, request

import redis

app = Flask(__name__)
redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
queue_name = 'task_queue'

# Add Task theo cơ chế Messege queue theo redis 
def add_task(content_Input):
    redis_client.rpush(queue_name, content_Input)

# Hàm lưu vào Redis Data
def insert_data(key, value):
    redis_client.set(key, value)

# Xử lý các công việc
def process_tasks():
    # Code xử lý các công việc ở đây
    return "Tasks processed successfully."

@app.route('/process_tasks', methods=['GET'])
def trigger_process_tasks():
    get_param = request.args.get('get')
    if get_param == '1':
        message = process_tasks()  # Gọi hàm xử lý công việc và nhận giá trị message
        return message  # Trả về giá trị message
    else:
        return "Invalid request."

if __name__ == '__main__':
    app.run(debug=True, port=5002)
