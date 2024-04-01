import requests
import time

def make_request(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    
    print("Thời gian hoàn thành yêu cầu:", end_time - start_time, "giây")
    
    if response.ok:
        content_size_kb = len(response.content) / 1024  # Chuyển từ byte sang KB
        print("Dung lượng của yêu cầu:", content_size_kb, "KB")
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

        #url = "http://192.168.2.39:30000/save_message?get=2&text=Client" + str(i)
        url = "http://192.168.2.39:5000/save_message?get=2&text=Client" + str(i)
        make_request(url)

# Run test request
request_lv_3(1)


