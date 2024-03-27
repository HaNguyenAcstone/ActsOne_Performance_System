from flask import Flask, send_file
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
metrics = PrometheusMetrics(app)

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

# Sử dụng prometheus_client để xuất các metric
@app.route('/metrics')
def export_metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
