from kafka import KafkaProducer

# Khai báo địa chỉ của Kafka broker
bootstrap_servers = '192.168.200.130:32046'  # Thay thế địa chỉ IP và cổng NodePort của Kafka broker của bạn

# Tạo producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Gửi một tin nhắn tới topic 'test'
topic = 'test'
message = b'hello world!'
producer.send(topic, message)

# Đóng producer sau khi gửi tin nhắn
producer.close()
