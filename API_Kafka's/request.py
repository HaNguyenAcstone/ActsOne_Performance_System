import requests
import json

def send_message_to_kafka_api_from_json(url,json_file_path):
    
    # Đọc dữ liệu từ tệp JSON
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    headers = {'Content-Type': 'application/json'}

    # Gửi yêu cầu POST đến API
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Kiểm tra phản hồi từ API và in ra kết quả
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message:", response.text)


# Sử dụng hàm để gửi yêu cầu POST đến API từ tệp JSON
send_message_to_kafka_api_from_json('http://localhost:5000/send-message' ,'message.json')
