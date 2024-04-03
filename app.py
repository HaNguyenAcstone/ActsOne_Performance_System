from kafka import KafkaConsumer

# Thiết lập Kafka Consumer
consumer = KafkaConsumer(
    'test-topic',  # Tên của Kafka topic bạn muốn subscribe
    bootstrap_servers='192.168.200.131:32142',  # Địa chỉ IP của node Kubernetes và cổng NodePort của dịch vụ Kafka
    auto_offset_reset='earliest',  # Đặt lại offset để đọc tất cả các tin nhắn từ đầu
    group_id='my-group'  # ID của consumer group
)

# Đọc và in các tin nhắn từ Kafka topic
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")

# Đóng Kafka Consumer
consumer.close()
