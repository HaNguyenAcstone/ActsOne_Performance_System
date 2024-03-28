from flask import Flask, send_file
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time
from flask import Flask, request, jsonify
import redis


app = Flask(__name__)
metrics = PrometheusMetrics(app) # Dùng để ghi Logs
redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
queue_name = 'task_queue'

# Add Task theo cơ chế Messege queue theo redis 
def add_task(content_Input):
    redis_client.rpush(queue_name, content_Input)

@app.route('/endpoint1')
def endpoint1():
    time.sleep(1)
    # Đường dẫn của hình ảnh bạn muốn trả về
    image_path = 'images/2.png'  # Thay đổi đường dẫn tới hình ảnh thực tế của bạn

    # Trả về hình ảnh như là phản hồi
    return send_file(image_path, mimetype='image/png')

# Api gửi message        
@app.route('/message')
def index():
    get_value = request.args.get('get', default=1, type=int)
    get_value_str = request.args.get('text', default=1, type=str)


    #if get_value > 0 and get_value != "":
    # Insert tự động dữ liệu vào queue
    for i in range(1, get_value):

        # Add Task theo cơ chế Messege queue theo redis 
        add_task("Message: " + str(i) + " - " + str(get_value_str))
       
    return format(get_value)


# Sử dụng prometheus_client để xuất các metric
@app.route('/metrics')
def export_metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
