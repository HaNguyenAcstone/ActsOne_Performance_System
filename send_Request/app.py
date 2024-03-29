from flask import Flask, request, jsonify
import redis
import time

app = Flask(__name__)


@app.route('/send_request', methods=['GET'])
def send_request():
    # Lấy dữ liệu từ URL parameters
    key = request.args.get('key')
    value = request.args.get('value')
    
    return ''

if __name__ == '__main__':
    app.run(debug=True)
