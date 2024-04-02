from flask import Flask, request
from redis import Redis
from rq import Queue
import time

app = Flask(__name__)

# Kết nối tới Redis
redis_conn = Redis(host='192.168.2.39', port=6379, db=0)

# Tạo một hàng đợi (Queue) để xử lý các message từ Redis Stream
queue = Queue(connection=redis_conn)

# Tên của Redis Stream
stream_name = 'request_logs'

# Tạo Redis Stream nếu chưa tồn tại
if not redis_conn.exists(stream_name):
    redis_conn.xadd(stream_name, {'init': 'start'})

# Route để gửi request
@app.route('/send_request')
def send_request():
    # Lấy thời gian hiện tại
    timestamp = int(time.time() * 1000)
    # Gửi request bằng cách thêm message vào Redis Stream
    redis_conn.xadd(stream_name, {'timestamp': timestamp, 'request': request.url})
    return 'Request sent successfully'

# Worker để xử lý các message từ Redis Stream
def process_request(msg):
    # Xử lý message ở đây, ví dụ in ra nội dung của message
    if len(msg) >= 2 and isinstance(msg[1], dict) and 'timestamp' in msg[1]:
        timestamp = msg[1]['timestamp']
        request_url = msg[1]['request']
        print(f"Received request at {timestamp}: {request_url}")
    else:
        print("Invalid message format")

# Worker process
def worker():
    while True:
        # Lấy message từ Redis Stream
        msg = redis_conn.xread({stream_name: '0'}, count=1)
        if msg:
            # Xử lý message
            process_request(msg[0][1][0])
        else:
            # Nếu không có message nào, chờ 1 giây và thử lại
            time.sleep(1)

# Khởi chạy worker
if __name__ == '__main__':
    worker()
