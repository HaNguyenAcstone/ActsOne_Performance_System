from flask import Flask, request
from redis import Redis
from rq import Queue
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge
import psutil

app = Flask(__name__)
metrics = PrometheusMetrics(app) # Dùng để ghi Logs
redis_conn = Redis(host='192.168.10.133', port=6379, db=0)
queue = Queue(connection=redis_conn)

# Tên của Redis Stream
stream_name = 'Redis_Streams_AcstOne'

# Tạo Redis Stream (nếu chưa tồn tại)
if not redis_conn.exists(stream_name):
    # Tạo Redis Stream
    redis_conn.xadd(stream_name, {'init': 'start'})

# Metrics cho CPU
cpu_usage_metric = Gauge('cpu_usage_percent', 'CPU usage percent')

# Metrics cho RAM
ram_usage_metric = Gauge('ram_usage_percent', 'RAM usage percent')

# Metrics cho băng thông (nếu có)

# API just get request from client ( 1 mil transaction per second, no message )
@app.route('/just_get_request')
def just_get_request():

    # Thu thập thông tin về CPU và RAM
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent

    try:
        # Cập nhật metrics cho CPU và RAM
        cpu_usage_metric.set(cpu_percent)
        ram_usage_metric.set(ram_percent)

    except Exception as e:
        # Ghi log nếu có lỗi xảy ra
        app.logger.error("Error while updating metrics: %s", str(e))

    # Không trả về bất kỳ phản hồi nào cho client
    return '', 204

# API just send message and not save ( 100,000 transaction per second, with simple message )
@app.route('/not_save_message')
def not_save_message():

    # Thu thập thông tin về CPU và RAM
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent

    try:

        # Cập nhật metrics cho CPU và RAM
        cpu_usage_metric.set(cpu_percent)
        ram_usage_metric.set(ram_percent)

        return str("Hello, I got your message")

    except Exception as e:
        # Ghi log nếu có lỗi xảy ra
        app.logger.error("Error while adding task to Redis Stream: %s", str(e))
        return "Error occurred while adding message to group.", 500

# API get + save + reply message ( 10,000 transaction per second, with database process )
@app.route('/save_message') 
def save_message():
    get_value = request.args.get('get', default=1, type=int)
    get_value_str = request.args.get('text', default=1, type=str)

    # Thu thập thông tin về CPU và RAM
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent

    try:
        # Thêm công việc vào Redis Stream
        for i in range(1, get_value):
            message = {'content': "Message: " + str(i) + " - " + str(get_value_str)}
            redis_conn.xadd(stream_name, message)

        # Cập nhật metrics cho CPU và RAM
        cpu_usage_metric.set(cpu_percent)
        ram_usage_metric.set(ram_percent)

        return str("Hello, I saved your message")

    except Exception as e:
        # Ghi log nếu có lỗi xảy ra
        app.logger.error("Error while adding task to Redis Stream: %s", str(e))
        return "Error occurred while adding message to group.", 500

# Sử dụng prometheus_client để xuất các metric
@app.route('/metrics')
@metrics.do_not_track()
def export_metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Sử dụng prometheus_client để xuất các metric
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
