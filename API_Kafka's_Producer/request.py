import requests

def send_message_to_api(data):
    url = "http://192.168.2.39:30002/send-message"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response

# Chuẩn bị dữ liệu JSON để gửi
data = {'key': 'test_key', 'value': 'test_value'}

# Gửi yêu cầu POST đến API
response = send_message_to_api(data)

# In phản hồi từ API
print(response.text)
