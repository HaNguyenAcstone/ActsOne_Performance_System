from flask import Flask, request

app = Flask(__name__)

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

# Sử dụng prometheus_client để xuất các metric
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
