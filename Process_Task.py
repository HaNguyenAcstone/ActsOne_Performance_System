import redis
import json

redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)  # Connect to DB0

def process_tasks():
    tasks = redis_client.lrange('task_queue', 0, -1)  # Retrieve all elements of the list
    task_list = [{'task': task.decode('utf-8')} for task in tasks]
    print(json.dumps(task_list, indent=4))  # Print all tasks as a JSON array with indentation

if __name__ == '__main__':
    process_tasks()
