from flask import Flask, request
import redis
import threading
from queue import Queue
import time

app = Flask(__name__)

redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
stream_name = 'task_stream_new'

# Tạo một hàng đợi để lưu trữ các công việc trước khi gửi chúng vào Redis Stream
task_queue = Queue()

# Hàm thực hiện gửi các công việc từ hàng đợi vào Redis Stream
def send_tasks_to_stream():
    while True:
        if not task_queue.empty():
            task = task_queue.get()
            redis_client.xadd(stream_name, {'content': task})
        time.sleep(1)  # Thời gian nghỉ giữa các lần kiểm tra hàng đợi

# Khởi tạo một luồng mới để gửi công việc vào Redis Stream
send_thread = threading.Thread(target=send_tasks_to_stream)
send_thread.daemon = True
send_thread.start()

# Hàm nhận các công việc từ Redis Stream
def receive_tasks_from_stream():
    last_id = '0'

    while True:
        streams = redis_client.xread({stream_name: last_id}, count=1, block=0)  # Chỉ nhận 1 message mỗi lần
        if streams:
            for _, messages in streams:
                for message in messages:
                    last_id = message[0]
                    if 'content' in message[1]:  # Kiểm tra xem message có khóa 'content' không
                        content = message[1]['content']
                        print("Received:", content)  # Thay thế bằng xử lý dữ liệu của bạn
                    else:
                        print("Message does not contain 'content' key:", message)
       


# Khởi tạo một luồng mới để nhận công việc từ Redis Stream
receive_thread = threading.Thread(target=receive_tasks_from_stream)
receive_thread.daemon = True
receive_thread.start()

# Thêm task vào hàng đợi
def add_task(content_input):
    task_queue.put(content_input)

# API gửi message
@app.route('/message')
def index():
    get_value = request.args.get('get', default=1, type=int)
    get_value_str = request.args.get('text', default=1, type=str)

    # Thêm các công việc vào hàng đợi
    for i in range(1, get_value + 1):
        add_task("Message: " + str(i) + " - " + str(get_value_str))

    return str(get_value)

# Sử dụng prometheus_client để xuất các metric
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
