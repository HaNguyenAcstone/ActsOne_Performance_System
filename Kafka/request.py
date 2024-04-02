import requests
import json

# Dữ liệu JSON để gửi đi
data = {
    "topic": "ActsOnes_2",
    "message": {
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
}

# Gửi yêu cầu POST đến URL
url = 'http://192.168.2.39:5000/send_message'
response = requests.post(url, json=data)

# Kiểm tra kết quả
if response.status_code == 200:
    print("Yêu cầu đã được xử lý thành công!")
else:
    print("Đã xảy ra lỗi:", response.text)
