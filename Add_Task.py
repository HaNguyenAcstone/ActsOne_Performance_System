from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='192.168.200.128', port=6379, db=0)
queue_name = 'task_queue'

# Add Task theo cơ chế Messege queue theo redis 
def add_task(content_Input):
    redis_client.rpush(queue_name, content_Input)

# Hàm lưu vào Redis Data
def insert_data(key, value):
    redis_client.set(key, value)
        
@app.route('/message')
def index():
    get_value = request.args.get('get', default=1, type=int)

    if get_value > 0 and get_value != "":
        # Insert tự động dữ liệu vào queue
        for i in range(1, get_value):

            # Add Task theo cơ chế Messege queue theo redis 
            add_task("Message: " + str(i))
            
            # Lưu vào DB
            insert_data("Message: ",   str(i))

    return format(get_value)

if __name__ == '__main__':
    app.run(debug=True)
