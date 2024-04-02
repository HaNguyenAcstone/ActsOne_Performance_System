from flask import Flask, request, jsonify
from confluent_kafka import Producer
import json
from configparser import ConfigParser

app = Flask(__name__)

def get_kafka_producer(bootstrap_servers, group_id):
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id
    }
    producer = Producer(producer_config)
    return producer

# Truyền vào thông số bootstrap_servers và group_id
producer = get_kafka_producer("localhost:9092", "python_example_group_1")

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
    get_param = request.args.get('get')
    topic = 'ActsOnes_2'

    if get_param == '1':
        try:
            producer.produce(topic, json.dumps(fixed_json_message))
            producer.flush()
            return jsonify({'success': True}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid GET parameter'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
