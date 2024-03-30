from flask import Flask, request
from redis import Redis
from rq import Queue

app = Flask(__name__)

redis_conn = Redis(host='192.168.10.133', port=6379, db=0)
queue = Queue(connection=redis_conn)

# Tên của Redis Stream
stream_name = 'Redis_Streams_AcstOne'

# Tạo Redis Stream (nếu chưa tồn tại)
if not redis_conn.exists(stream_name):
    # Tạo Redis Stream
    redis_conn.xadd(stream_name, {'init': 'start'})


# API gửi message
@app.route('/message')
def index():
    get_value = request.args.get('get', default=1, type=int)
    get_value_str = request.args.get('text', default=1, type=str)

    try:
        # Thêm công việc vào Redis Stream
        for i in range(1, get_value):
            message = {'content': "Message: " + str(i) + " - " + str(get_value_str)}
            redis_conn.xadd(stream_name, message)

        return str(get_value)

    except Exception as e:
        # Ghi log nếu có lỗi xảy ra
        app.logger.error("Error while adding task to Redis Stream: %s", str(e))
        return "Error occurred while adding message to group.", 500

# Sử dụng prometheus_client để xuất các metric
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
