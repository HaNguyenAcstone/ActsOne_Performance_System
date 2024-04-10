# from flask import Flask, request, jsonify
# from confluent_kafka import Producer
# import socket

# app = Flask(__name__)

# # Topic Use 
# topic_Use = 'my-topic'
# # Connect with Kafka Producer
# conf = {"bootstrap.servers": "kafka-service:9092", "client.id": socket.gethostname()}
# producer = Producer(conf)

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
# # Test: http://192.168.10.133:30002/get-message?key=test_key&value=test_value
# @app.route('/get-message', methods=['GET'])
# def get_message():

#     # Sử dụng tên chủ đề cố định
#     key = request.args.get('key', 'message')  # Sử dụng giá trị mặc định 'message' nếu không được cung cấp
#     value = request.args.get('value', '')     # Sử dụng chuỗi trống làm giá trị mặc định nếu không được cung cấp

#     try:
#         producer.produce(topic_Use, key=key, value=value)
#         producer.flush()
#         return jsonify({'success': True, 'message': 'Message sent successfully'}), 200
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

# # Run ---------------------------
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# ------------------------------------------------------------------ 

from flask import Flask, request, jsonify
from confluent_kafka import Producer
import socket
import queue
import threading

app = Flask(__name__)

# Topic to use
topic_to_use = 'my-topic'

# Connect with Kafka Producer
conf = {"bootstrap.servers": "192.168.2.45:9092", "client.id": socket.gethostname()}
producer = Producer(conf)

# Message queue
message_queue = queue.Queue()

# Function to process messages from queue and send them to Kafka
def process_messages():
    while True:
        try:
            key, value = message_queue.get(timeout=0.2)  # Get message from the queue
            producer.produce(topic_to_use, key=key, value=value)
            producer.flush()  # Ensure message is sent immediately
            message_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f'Error processing message: {e}')

# Start the thread to process messages
message_thread = threading.Thread(target=process_messages)
message_thread.daemon = True
message_thread.start()

# API POST
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    key = data.get('key', 'message')
    value = data.get('value', '')

    try:
        message_queue.put((key, value))  # Put message into the queue
        return jsonify({'success': True, 'message': 'Message added to queue'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API GET
@app.route('/get-message', methods=['GET'])
def get_message():
    try:
        key = request.args.get('key', 'default_key')
        value = request.args.get('value', 'default_value')

        message_queue.put((key, value))  # Thêm tin nhắn vào hàng đợi
        return jsonify({'success': True, 'message': 'Message added to queue'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

