import requests
import time

def make_request(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    
    print("Thời gian hoàn thành yêu cầu:", end_time - start_time, "giây")
    
    if response.ok:
        print("Kết quả trả về:", response.text)
    else:
        print("Yêu cầu không thành công. Mã trạng thái:", response.status_code)

def request_lv_1(qty):
    
    for i in range(qty):

        url = "http://192.168.2.39:30000/just_send_request"
        make_request(url)

def request_lv_2(qty):
    
    for i in range(qty):

        url = "http://192.168.2.39:30000/not_save_message"
        make_request(url)

def request_lv_3(qty):

    for i in range(qty):

        url = "http://192.168.2.39:30000/save_message?get=2&text=Client" + str(i)
        make_request(url)

# Run test request
request_lv_3(10)


