# #!/usr/bin/env python

# import sys
# from random import choice
# from argparse import ArgumentParser, FileType
# from configparser import ConfigParser
# from confluent_kafka import Producer

# if __name__ == '__main__':
#     # Parse the command line.
#     parser = ArgumentParser()
#     parser.add_argument('config_file', type=FileType('r'))
#     args = parser.parse_args()

#     # Parse the configuration.
#     # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
#     config_parser = ConfigParser()
#     config_parser.read_file(args.config_file)
#     config = dict(config_parser['default'])

#     # Create Producer instance
#     producer = Producer(config)

#     # Optional per-message delivery callback (triggered by poll() or flush())
#     # when a message has been successfully delivered or permanently
#     # failed delivery (after retries).
#     def delivery_callback(err, msg):
#         if err:
#             print('ERROR: Message failed delivery: {}'.format(err))
#         else:
#             print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
#                 topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

#     # Produce data by selecting random values from these lists.
#     topic = "purchases"
#     user_ids = ['eabara', 'jsmith', 'sgarcia', 'jbernard', 'htanaka', 'awalther']
#     products = ['book', 'alarm clock', 't-shirts', 'gift card', 'batteries']

#     count = 0
#     for _ in range(10):

#         user_id = choice(user_ids)
#         product = choice(products)
#         producer.produce(topic, product, user_id, callback=delivery_callback)
#         count += 1

#     # Block until the messages are sent.
#     producer.poll(10000)
#     producer.flush()

# --------------------------------------------------------------------

from confluent_kafka import Producer


def send_message_to_kafka(topic, message):
    # Khởi tạo producer
    producer = Producer({'bootstrap.servers': 'localhost:38695'})  # Thay đổi cổng tùy theo plaintext port bạn đã nhận được

    # Chờ cho producer sẵn sàng
    producer.poll(0)

    try:
        # Gửi tin nhắn tới chủ đề Kafka
        producer.produce(topic, value=message.encode('utf-8'))
        producer.flush()

        print(f"Tin nhắn đã được gửi tới chủ đề '{topic}': {message}")
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn tới chủ đề '{topic}': {str(e)}")
    finally:
        # Đóng producer
        producer.close()


# Sử dụng hàm để gửi tin nhắn tới chủ đề 'my-topic-2'
topic_name = "my-topic-2"
message_content = "Đây là một tin nhắn mẫu từ Python!"
send_message_to_kafka(topic_name, message_content)
