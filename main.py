from redis import Redis
from rq import Queue

redis_conn = Redis(host='192.168.2.39', port=6379, db=0)
queue = Queue(connection=redis_conn)

stream_name = 'task_stream_new'

# Xác định tên nhóm bạn muốn consumer tham gia
group_name = 'group1'

# Đọc message từ nhóm cụ thể trong Redis Stream
while True:
    # Đọc message từ nhóm cụ thể
    messages = redis_conn.xreadgroup(group_name, consumer_name='consumer1', streams={stream_name: '>'}, count=1)

    for stream, message_list in messages:
        for message_id, message in message_list:
            # Xử lý message ở đây, ví dụ:
            content = message['content']
            print(f"Consumer received: {content}")

            # Sau khi xử lý xong, đánh dấu message đã được xử lý
            redis_conn.xack(stream_name, group_name, message_id)
