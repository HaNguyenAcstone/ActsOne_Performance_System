import json
import requests
from concurrent.futures import ThreadPoolExecutor
import random
import string

# Hàm tạo chuỗi ngẫu nhiên
def generate_random_value(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def send_messages_to_api(num_requests):
    url = "http://192.168.2.39:30002/send-message"
    headers = {'Content-Type': 'application/json'}

    with ThreadPoolExecutor() as executor:
        futures = []

        # Gửi các yêu cầu POST đồng thời
        for i in range(num_requests):
            # Tạo một đối tượng data mới cho mỗi yêu cầu
            data = {'key': 'test_key', 'value': generate_random_value()}
            future = executor.submit(send_message_to_api, url, data, headers)
            futures.append(future)

        # Chờ tất cả các yêu cầu hoàn thành
        for future in futures:
            response = future.result()

def send_message_to_api(url, data, headers):
    response = requests.post(url, json=data, headers=headers)
    return response

if __name__ == "__main__":
    num_requests = 100000
    send_messages_to_api(num_requests)
