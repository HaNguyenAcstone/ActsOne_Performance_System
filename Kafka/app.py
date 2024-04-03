from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json
from configparser import ConfigParser

app = Flask(__name__)

# Function to read configuration from getting_started.ini
def read_config():
    config = ConfigParser()
    config.read('getting_started.ini')
    return config

# Get Kafka producer with bootstrap.servers and group.id from config
def get_kafka_producer(config):
    bootstrap_servers = config.get('default', 'bootstrap.servers')
    group_id = config.get('consumer', 'group.id')
    
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id
    }
    producer = Producer(producer_config)
    return producer

# Read configuration file
config = read_config()

# Get Kafka producer
producer = get_kafka_producer(config)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        topic = data.get('topic')
        if not topic:
            return jsonify({'error': 'Topic not provided in JSON data'}), 400

        message = data.get('message')
        if not message:
            return jsonify({'error': 'Message not provided in JSON data'}), 400

        producer.produce(topic, json.dumps(message))
        producer.flush()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
