from confluent_kafka import Consumer, KafkaError
import socket
import threading

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

# Global variable to control consumer status
running = True

# Function to start the consumer
def start_consumer():
    global running
    try:
        while running:
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
            print("Received message:", msg.value().decode('utf-8'))  # Decode message and print it
    except KeyboardInterrupt:
        consumer.close()

# Start the consumer
threading.Thread(target=start_consumer).start()
