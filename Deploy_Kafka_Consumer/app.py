from confluent_kafka import Consumer, KafkaError
import socket

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

# Start consuming messages
try:
    while True:
        msg = consumer.poll(1.0)  # Poll for new messages
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition (reached end of topic)
                continue
            else:
                # Other error
                print(msg.error())
                break
        else:
            # Message received successfully
            print('Received message: {}'.format(msg.value().decode('utf-8')))  # Print the message value
finally:
    # Clean up the consumer
    consumer.close()
