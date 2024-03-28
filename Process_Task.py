from flask import Flask, request, jsonify
import redis
import json
import threading

app = Flask(__name__)
redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
queue_name = 'task_queue'

def process_tasks():
    while True:
        task = redis_client.lpop(queue_name)
        if task is not None:
            print("Processing task:", task.decode('utf-8'))
           
            # Thực hiện xử lý công việc ở đây
        else:
            print("No tasks in the queue.")
            break

def start_task_processing():
    threading.Thread(target=process_tasks).start()

@app.route('/process')
def index():
    #get_value = request.args.get('get', default=1, type=int)
    start_task_processing()
    return jsonify({"message": "Task processing started."})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
