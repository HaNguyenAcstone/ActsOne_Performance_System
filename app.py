from flask import Flask, send_file
import time

app = Flask(__name__)

@app.route('/endpoint1')
def endpoint1():
    time.sleep(1)
    # Đường dẫn của hình ảnh bạn muốn trả về
    image_path = 'images/2.png'  # Thay đổi đường dẫn tới hình ảnh thực tế của bạn

    # Trả về hình ảnh như là phản hồi
    return send_file(image_path, mimetype='image/png')

@app.route('/endpoint2')
def endpoint2():
    time.sleep(1)
    # Đường dẫn của hình ảnh bạn muốn trả về
    image_path = 'images/1.png'  # Thay đổi đường dẫn tới hình ảnh thực tế của bạn

    # Trả về hình ảnh như là phản hồi
    return send_file(image_path, mimetype='image/png')

@app.route('/endpoint3')
def endpoint3():
    time.sleep(1)
    # Đường dẫn của hình ảnh bạn muốn trả về
    image_path = 'images/2.png'  # Thay đổi đường dẫn tới hình ảnh thực tế của bạn

    # Trả về hình ảnh như là phản hồi
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
