from confluent_kafka import Producer
import socket

# Khởi tạo cấu hình cho producer
conf = {
    "bootstrap.servers": "kafka-service:9092",  # Kafka broker mà producer sẽ kết nối tới
    "client.id": socket.gethostname()  # Đặt client.id của producer thành hostname của máy chủ
}

# Tạo một instance của producer với cấu hình đã chỉ định
producer = Producer(conf)

# Kafka topic mà chúng ta muốn gửi tin nhắn tới
topic = "minikube-topic"

# Gửi một tin nhắn tới Kafka topic
def delivery_report(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message delivered to topic {msg.topic()}")

# Gửi tin nhắn với nội dung và khóa được chỉ định
producer.produce(topic, key="message", value="message_from_python_producer", callback=delivery_report)

# Đảm bảo rằng tất cả các tin nhắn đã được gửi
producer.flush()
