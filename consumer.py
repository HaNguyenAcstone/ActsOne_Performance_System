from redis import Redis
from rq import Worker

# Kết nối tới Redis
redis_conn = Redis(host='192.168.2.39', port=6379, db=0)

# Tạo một Worker để xử lý các message từ tất cả các nhóm trong Redis Stream
worker = Worker([], connection=redis_conn)  # Đối số queues trống

# Khởi động Worker để bắt đầu xử lý các message từ tất cả các nhóm
while True:
    worker.work(burst=True)
