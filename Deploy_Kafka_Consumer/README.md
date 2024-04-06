**Imports:**

- `confluent_kafka`: Provides classes and functions for interacting with Kafka as a consumer.
- `socket`: Used to retrieve the hostname for consumer group ID.

**Configuration:**

- `topic_to_subscribe`: The Kafka topic you want this consumer to subscribe to.
- `conf_consumer`: A dictionary containing the Kafka consumer configuration:
    - `bootstrap.servers`: The address of your Kafka broker (replace with your actual server).
    - `group.id`: A unique identifier for this consumer group. Defaults to the hostname (using `socket.gethostname()`).
    - `auto.offset.reset`: Specifies what to do when there are no previously committed offsets for the consumer group.  Here, it's set to `'earliest'`, instructing the consumer to start reading from the beginning of the topic partitions.

**Consumer Creation and Subscription:**

- `consumer`: An instance of the `Consumer` class is created with the configuration dictionary.
- `consumer.subscribe([topic_to_subscribe])`: Subscribes the consumer to the specified topic.

**Message Consumption Loop:**

- `try...finally` block ensures proper consumer cleanup even if an exception occurs.
- `while True`: An infinite loop to continuously poll for messages.
    - `msg = consumer.poll(1.0)`: Polls for new messages with a 1-second timeout.
        - If `msg` is `None`, no new messages were available within the timeout.
        - Otherwise, `msg` contains information about the received message.
    - `if msg.error()`: Checks for any errors during message retrieval.
        - `if msg.error().code() == KafkaError._PARTITION_EOF`: Handles end-of-partition scenario.
            - In this case, we simply continue the loop (optional: you could implement logic to handle reaching the end of the topic).
        - `else`: Handles other errors (prints the error message and breaks out of the loop).
    - `else`: If no errors occurred:
        - `print('Received message: {}'.format(msg.value().decode('utf-8')))`: Decodes the message value (assumed to be UTF-8 encoded) and prints it.

**Consumer Cleanup:**

- `finally`: Ensures that the consumer is properly closed, even if an exception occurs in the loop.
    - `consumer.close()`: Closes the consumer connection.

**Enhancements:**

- **Error Handling:** Consider adding more specific error handling beyond the provided `KafkaError._PARTITION_EOF` check.
- **Custom Logic:** Modify the message processing logic within the `else` block to handle received messages according to your needs (e.g., storing, processing, or forwarding messages).
- **Offsets Management:** Investigate Kafka consumer offset management strategies to control where the consumer starts reading from the topic (e.g., commit offsets periodically).
- **Threading:** For high-throughput scenarios, explore using threads or asynchronous programming patterns to handle message processing concurrently with message polling.

**Additional Notes:**

- Replace `'kafka-service:9092'` with the actual address of your Kafka broker(s).
- This code demonstrates a basic Kafka consumer setup. Adapt it to your specific use case and requirements.