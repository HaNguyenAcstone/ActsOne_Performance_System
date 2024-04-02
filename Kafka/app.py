from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json
from configparser import ConfigParser

app = Flask(__name__)

def get_kafka_producer(config_file):
    config_parser = ConfigParser()
    config_parser.read(config_file)
    config = dict(config_parser['default'])
    producer = Producer(config)
    return producer

producer = get_kafka_producer('getting_started.ini')

fixed_json_message = {
    "data": {
        "items": [],
        "ordersn": "220810QSK8S7BX",
        "status": "PROCESSED",
        "completed_scenario": "",
        "update_time": 1660123127
    },
    "shop_id": 727720655,
    "code": 3,
    "timestamp": 1660123127
}

@app.route('/send_message')
def send_message():
    topic = 'Actsone_ms'

    try:
        producer.produce(topic, json.dumps(fixed_json_message))
        producer.flush()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
