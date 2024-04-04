from flask import Flask, request, jsonify
from confluent_kafka import Consumer, KafkaError
import socket

app = Flask(__name__)

# Topic to subscribe
topic_to_subscribe = 'my-topic'

# Connect with Kafka Consumer
conf_consumer = {
    'bootstrap.servers': 'kafka-service:9092',
    'group.id': socket.gethostname(),
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf_consumer)
consumer.subscribe([topic_to_subscribe])

# API route for consuming messages
@app.route('/consume-messages', methods=['GET'])
def consume_messages():
    messages = []
    try:
        while True:
            msg = consumer.poll(1.0)  # Poll messages with timeout of 1 second
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition, continue polling
                    continue
                else:
                    # Other error, log it
                    print("Consumer error: {}".format(msg.error()))
                    break
            messages.append(msg.value().decode('utf-8'))  # Decode message and append to list
    except KeyboardInterrupt:
        consumer.close()
    
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
