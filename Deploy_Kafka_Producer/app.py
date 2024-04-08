from flask import Flask, request, jsonify
from confluent_kafka import Producer
import socket

app = Flask(__name__)

# Topic Use 
topic_Use = 'my-topic'
# Connect with Kafka Producer
conf = {"bootstrap.servers": "kafka-broker-2:9093", "client.id": socket.gethostname()}
producer = Producer(conf)

# API POST
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    # Sử dụng tên chủ đề cố định
    key = data.get('key', 'message')  # Sử dụng giá trị mặc định 'message' nếu không được cung cấp
    value = data.get('value', '')     # Sử dụng chuỗi trống làm giá trị mặc định nếu không được cung cấp

    try:
        producer.produce(topic_Use, key=key, value=value)
        producer.flush()  # Đảm bảo rằng tin nhắn được gửi ngay lập tức
        return jsonify({'success': True, 'message': 'Message sent successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API GET
# Test: http://192.168.10.133:30002/get-message?key=test_key&value=test_value
@app.route('/get-message', methods=['GET'])
def get_message():

    # Sử dụng tên chủ đề cố định
    key = request.args.get('key', 'message')  # Sử dụng giá trị mặc định 'message' nếu không được cung cấp
    value = request.args.get('value', '')     # Sử dụng chuỗi trống làm giá trị mặc định nếu không được cung cấp

    try:
        producer.produce(topic_Use, key=key, value=value)
        producer.flush()
        return jsonify({'success': True, 'message': 'Message sent successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Run ---------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


