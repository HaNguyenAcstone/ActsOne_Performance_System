import redis
import time

# Kết nối tới Redis server
redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)

# Tên của hàng đợi
queue_name = 'task_queue'

def add_task(task):
    """Thêm một nhiệm vụ vào hàng đợi."""
    redis_client.rpush(queue_name, task)

def process_tasks():
    """Xử lý các nhiệm vụ từ hàng đợi."""
    while True:
        # Lấy nhiệm vụ từ hàng đợi
        task = redis_client.lpop(queue_name)
        if task is not None:
            # Xử lý nhiệm vụ (trong ví dụ này, chúng ta chỉ in ra)
            print("Processing task:", task.decode('utf-8'))
            # Giả lập thời gian xử lý
            time.sleep(1)
        else:
            print("No tasks in the queue.")
            break

# Thêm một số nhiệm vụ vào hàng đợi
add_task("Task 1")
add_task("Task 2")
add_task("Task 3")

# Xử lý các nhiệm vụ từ hàng đợi
process_tasks()
