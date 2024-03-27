from flask import Flask, Response
from prometheus_client import Counter, generate_latest, REGISTRY

app = Flask(__name__)

# Định nghĩa một counter metric với tên là 'requests_total' và mô tả 'Số lượng requests đã được gửi'
requests_total = Counter('requests_total', 'Số lượng requests đã được gửi')

@app.route('/')
def hello():
    requests_total.inc()  # Tăng giá trị của metric 'requests_total' mỗi khi endpoint này được gọi
    return "Hello, World!"

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
