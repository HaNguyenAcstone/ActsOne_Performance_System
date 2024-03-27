import time
import redis
from flask import Flask, request

app = Flask(__name__)
redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
queue_name = 'task_queue'

def process_tasks():
    while True:
        task = redis_client.lpop(queue_name)
        if task is not None:
            print("Processing task:", task.decode('utf-8'))
            time.sleep(1)
        else:
            print("No tasks in the queue.")
            break

@app.route('/process_tasks', methods=['GET'])
def trigger_process_tasks():
    get_param = request.args.get('get')
    if get_param == '1':
        process_tasks()
        return "Tasks processed successfully."
    else:
        return "Invalid request."

if __name__ == '__main__':
    app.run(debug=True)
