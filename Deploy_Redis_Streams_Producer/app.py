from flask import Flask, request
from redis import Redis
from rq import Queue

app = Flask(__name__)
redis_conn = Redis(host='0.0.0.0', port=6379, db=0)
queue = Queue(connection=redis_conn)

# Tên của Redis Stream
stream_name = 'Redis_Streams_AcstOne'

# Tạo Redis Stream (nếu chưa tồn tại)
if not redis_conn.exists(stream_name):
    # Tạo Redis Stream
    redis_conn.xadd(stream_name, {'init': 'start'})

# API just get request from client ( 1 mil transaction per second, no message )
@app.route('/just_send_request', methods=['GET'])
def just_get_request():
    # Không trả về bất kỳ phản hồi nào cho client
    return '', 200

# API just send message and not save ( 100,000 transaction per second, with simple message )
@app.route('/not_save_message', methods=['GET'])
def not_save_message():
    try:
        return "Hello, I got your message", 200
    except Exception as e:
        # Ghi log nếu có lỗi xảy ra
        app.logger.error("Error occurred: %s", str(e))
        return "Error occurred.", 500

# API get + save + reply message ( 10,000 transaction per second, with database process )
@app.route('/save_message', methods=['GET']) 
def save_message():
    get_value = request.args.get('get', default=1, type=int)
    get_value_str = request.args.get('text', default="Default Text", type=str)

    try:
        # Thêm công việc vào Redis Stream
        for i in range(1, get_value + 1):
            message = {'content': f"Message: {i} - {get_value_str}"}
            redis_conn.xadd(stream_name, message)
            
        return "Hello, I saved your message", 200
    except Exception as e:
        # Ghi log nếu có lỗi xảy ra
        app.logger.error("Error occurred: %s", str(e))
        return "Error occurred while adding message to group.", 500

# API sử dụng phương thức POST
@app.route('/post_endpoint', methods=['POST'])
def post_endpoint():
    try:
        # Nhận dữ liệu từ request
        data = request.json
        
        # Lưu dữ liệu vào Redis Stream
        for i, item in enumerate(data):
            message = {'content': f"Message {i+1}: {item}"}
            redis_conn.xadd(stream_name, message)
        
        # Trả về phản hồi cho client
        return "Data saved successfully", 200
    except Exception as e:
        # Ghi log nếu có lỗi xảy ra
        app.logger.error("Error occurred: %s", str(e))
        return "Error occurred while processing the data", 500

# Sử dụng prometheus_client để xuất các metric
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
