# from flask import Flask, request, jsonify
# from confluent_kafka import Producer
# import json
# from configparser import ConfigParser

# app = Flask(__name__)

# def get_kafka_producer(bootstrap_servers, group_id):
#     producer_config = {
#         'bootstrap.servers': bootstrap_servers,
#         'group.id': group_id
#     }
#     producer = Producer(producer_config)
#     return producer

# # Truyền vào thông số bootstrap_servers và group_id
# producer = get_kafka_producer("0.0.0.0:9092", "python_example_group_1")

# @app.route('/send_message', methods=['POST'])
# def send_message():
#     try:
#         data = request.json
#         if not data:
#             return jsonify({'error': 'No JSON data provided'}), 400

#         topic = data.get('topic')
#         if not topic:
#             return jsonify({'error': 'Topic not provided in JSON data'}), 400

#         message = data.get('message')
#         if not message:
#             return jsonify({'error': 'Message not provided in JSON data'}), 400

#         producer.produce(topic, json.dumps(message))
#         producer.flush()
#         return jsonify({'success': True}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')


#!/usr/bin/env python

import sys
from random import choice
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    # Create Producer instance
    producer = Producer(config)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

    # Produce data by selecting random values from these lists.
    topic = "purchases"
    user_ids = ['eabara', 'jsmith', 'sgarcia', 'jbernard', 'htanaka', 'awalther']
    products = ['book', 'alarm clock', 't-shirts', 'gift card', 'batteries']

    count = 0
    for _ in range(10):

        user_id = choice(user_ids)
        product = choice(products)
        producer.produce(topic, product, user_id, callback=delivery_callback)
        count += 1

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()