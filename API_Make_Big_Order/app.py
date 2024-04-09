from flask import Flask, request, jsonify
from confluent_kafka import Producer
import socket

app = Flask(__name__)

# Topic Use 
topic_Use = 'my-topic'
# Connect with Kafka Producer
conf = {"bootstrap.servers": "kafka-service:9092", "client.id": socket.gethostname()}
producer = Producer(conf)

# # API POST
# @app.route('/send-message', methods=['POST'])
# def send_message():
#     data = request.json
#     # Sử dụng tên chủ đề cố định
#     key = data.get('key', 'message')  # Sử dụng giá trị mặc định 'message' nếu không được cung cấp
#     value = data.get('value', '')     # Sử dụng chuỗi trống làm giá trị mặc định nếu không được cung cấp

#     try:
#         producer.produce(topic_Use, key=key, value=value)
#         producer.flush()  # Đảm bảo rằng tin nhắn được gửi ngay lập tức
#         return jsonify({'success': True, 'message': 'Message sent successfully'}), 200
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

# API GET
@app.route('/send-big-message', methods=['GET'])
def send_big_message():
    key = request.args.get('key', 'message')

    try:
        num_orders = int(request.args.get('value', ''))
        for order_number in range(1, num_orders + 1):
            value = str(order_number)
            producer.produce(topic_Use, key=key, value=value)
        producer.flush()
        return jsonify({'success': True, 'message': f'{num_orders} messages sent successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Run ---------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)