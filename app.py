from flask import Flask, request
from redis import Redis
from rq import Queue
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge

app = Flask(__name__)
metrics = PrometheusMetrics(app) # Dùng để ghi Logs
redis_conn = Redis(host='192.168.10.133', port=32368, db=0)
queue = Queue(connection=redis_conn)

# Tên của Redis Stream
stream_name = 'Redis_Streams_AcstOne'

# Tạo Redis Stream (nếu chưa tồn tại)
if not redis_conn.exists(stream_name):
    # Tạo Redis Stream
    redis_conn.xadd(stream_name, {'init': 'start'})

# Metrics cho băng thông (nếu có)

# API just get request from client ( 1 mil transaction per second, no message )
@app.route('/just_get_request')
def just_get_request():
    # Không trả về bất kỳ phản hồi nào cho client
    return '', 204

# API just send message and not save ( 100,000 transaction per second, with simple message )
@app.route('/not_save_message')
def not_save_message():

    try:
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

    try:
        # Thêm công việc vào Redis Stream
        for i in range(1, get_value):
            message = {'content': "Message: " + str(i) + " - " + str(get_value_str)}
            redis_conn.xadd(stream_name, message)

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
