from flask import Flask, request
from redis import Redis
from rq import Queue

app = Flask(__name__)

redis_conn = Redis(host='192.168.2.39', port=6379, db=0)
queue = Queue(connection=redis_conn)

# Tên của Redis Stream
stream_name = 'task_stream_new'

# Tên nhóm mà bạn muốn gửi message vào
group_name = 'group1'

# Tạo Redis Stream (nếu chưa tồn tại)
if not redis_conn.exists(stream_name):
    # Tạo Redis Stream
    redis_conn.xadd(stream_name, {'init': 'start'})

# Tạo hoặc kết nối message vào nhóm group1 trong Redis Stream
try:
    if not redis_conn.xinfo_groups(stream_name):
        redis_conn.xgroup_create(stream_name, group_name, id='0', mkstream=True)
    else:
        redis_conn.xgroup_setid(stream_name, group_name, '0')
except Exception as e:
    app.logger.error("Error while creating or connecting to group '%s': %s", group_name, str(e))

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
