import logging
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

# Configure logging
logging.basicConfig(filename='kafka_consumer.log', level=logging.INFO, format='%(message)s')

# Global variable to control consumer status
running = True

# Function to start the consumer
def start_consumer():
    global running
    try:
        while running:
            msg = consumer.poll(1.0)  # Poll messages with timeout of 1 second
            if msg is None:
                print("Waiting for messages ...")  # Display "Waiting ..." message when no new message
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition, continue polling
                    continue
                else:
                    # Other error, log it
                    logging.error("Consumer error: %s", msg.error())
                    break
            message = msg.value().decode('utf-8')  # Decode message
            print("Received message:", message)  # Print message
            logging.info(message)  # Log message
    except KeyboardInterrupt:
        consumer.close()

# Start the consumer
threading.Thread(target=start_consumer).start()