from flask import Flask
from redis import Redis
from rq import Queue

app = Flask(__name__)

redis_conn = Redis(host='192.168.2.39', port=6379, db=0)

# Tên của Redis Stream
stream_name = 'task_stream_new'

# Tên nhóm mà consumer sẽ tham gia
group_name = 'group1'

# API consumer
@app.route('/consume')
def consume_messages():
    try:
        # Đọc message từ nhóm cụ thể trong Redis Stream
        messages = redis_conn.xreadgroup(group_name, 'consumer1', {stream_name: '>'}, count=10)
        
        for _, message_list in messages:
            for message_id, message in message_list:
                # Xử lý message
                content = message['content']
                print(f"Consumer received: {content}")

                # Đánh dấu message đã được xử lý
                redis_conn.xack(stream_name, group_name, message_id)
        
        return 'Messages consumed successfully'
    
    except Exception as e:
        return f"Error while consuming messages: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
