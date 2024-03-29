from flask import Flask, request
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
stream_name = 'task_stream'

# Thêm task vào Redis Stream
def add_task(content_input):
    redis_client.xadd(stream_name, {'content': content_input})

# API gửi message
@app.route('/message')
def index():
    get_value = request.args.get('get', default=1, type=int)
    get_value_str = request.args.get('text', default=1, type=str)

    # Insert tự động dữ liệu vào stream
    for i in range(1, get_value):
        add_task("Message: " + str(i) + " - " + str(get_value_str))

    return str(get_value)

# Sử dụng prometheus_client để xuất các metric
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
