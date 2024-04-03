from confluent_kafka import Producer, Consumer
import time

# Kafka broker address
bootstrap_servers = '192.168.200.131:32142'

# Kafka topic
topic = 'test-topic-2'

# Producer function
def produce_message():
    producer = Producer({'bootstrap.servers': bootstrap_servers})

    try:
        # Produce message to Kafka topic
        for i in range(10):
            message = f"Message {i}"
            producer.produce(topic, value=message.encode('utf-8'))
            producer.flush()
            print(f"Produced message: {message}")
            time.sleep(1)
    except Exception as e:
        print(f"Failed to produce message: {str(e)}")
    finally:
        producer.flush()

# Consumer function
def consume_message():
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'my-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    try:
        # Consume messages from Kafka topic
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            print(f"Consumed message: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    # Start producer and consumer
    produce_message()
    # Wait for a while before starting consumer
    time.sleep(5)
    consume_message()
