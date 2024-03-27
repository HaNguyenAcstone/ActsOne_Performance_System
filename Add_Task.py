from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
queue_name = 'task_queue'

def add_task(content_input):
    redis_client.rpush(queue_name, content_input)

# Tại
def insert_data(key, value):
    redis_client.set(key, value)

@app.route('/insert', methods=['POST'])
def insert():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if key and value:
        insert_data(key, value)
        return jsonify({'message': 'Data inserted successfully'}), 200
    else:
        return jsonify({'error': 'Key and value must be provided'}), 400

if __name__ == '__main__':
    # Adding tasks to the queue
    for i in range(1, 1000001):
        add_task("Message: " + str(i))
    
    app.run(debug=True)
