import redis

# Kết nối đến Redis
redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
queue_name = 'task_queue'

# Sử dụng phương thức llen để đếm số lượng giá trị trong task_queue
num_items = redis_client.llen(queue_name)

print("Số lượng giá trị trong task_queue:", num_items)
