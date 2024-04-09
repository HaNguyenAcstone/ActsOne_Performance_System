# from flask import Flask, request, jsonify
# from confluent_kafka import Producer
# import socket

# app = Flask(__name__)

# # Topic Use 
# topic_Use = 'my-topic'
# # Connect with Kafka Producer
# conf = {"bootstrap.servers": "kafka-service:9092", "client.id": socket.gethostname()}
# producer = Producer(conf)

# # API GET
# @app.route('/send-big-message', methods=['GET'])
# def send_big_message():
#     key = request.args.get('key', 'message')

#     try:
#         num_orders = int(request.args.get('value', ''))
#         for order_number in range(1, num_orders + 1):
#             value = "New Order: " + str(order_number)
#             producer.produce(topic_Use, key=key, value=value)
#         producer.flush()
#         return jsonify({'success': True, 'message': f'{num_orders} messages sent successfully'}), 200
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

# # Run ---------------------------
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# -----------------------------------------------------

from flask import Flask, request, jsonify
from confluent_kafka import Producer
import socket
import threading
import queue

app = Flask(__name__)

# Topic Use 
topic_Use = 'my-topic'
# Connect with Kafka Producer
conf = {"bootstrap.servers": "kafka-service:9092", "client.id": socket.gethostname()}
producer = Producer(conf)

# Global message queue
message_queue = queue.Queue()

# Function to send messages to Kafka
def send_messages():
    while True:
        try:
            key, value = message_queue.get()
            producer.produce(topic_Use, key=key, value=value)
            producer.poll(0)  # Poll the producer to trigger delivery reports
            message_queue.task_done()
        except Exception as e:
            print(f'Failed to send message: {e}')

# Start a thread to continuously send messages
message_sender_thread = threading.Thread(target=send_messages)
message_sender_thread.daemon = True
message_sender_thread.start()

# API GET
@app.route('/send-big-message', methods=['GET'])
def send_big_message():
    key = request.args.get('key', 'message')

    try:
        num_orders = int(request.args.get('value', ''))
        for order_number in range(1, num_orders + 1):
            value = "New Order: " + str(order_number)
            message_queue.put((key, value))
        return jsonify({'success': True, 'message': f'{num_orders} messages added to queue'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Run ---------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
