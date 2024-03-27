### Setup Grafana

version: '3'
services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - /var/lib/grafana:/var/lib/grafana
    restart: always

### Deploy test images to Docker in Server 
root@serverlocal:~# docker images
REPOSITORY                      TAG       IMAGE ID       CREATED              SIZE
linhtran2023/performance_test   v01       7889d8f14bf7   About a minute ago   137MB

docker run -d -p 5000:5000 linhtran2023/performance_test:v01

###
2. Cấu hình Prometheus để thu thập dữ liệu:
Cài đặt Prometheus và cấu hình nó để thu thập dữ liệu từ container của bạn. Bạn cần chỉ định các endpoint hoặc các thước đo mà Prometheus sẽ scrape từ container của bạn.
Đảm bảo rằng Prometheus được cấu hình để lưu trữ dữ liệu đã scrape.

```bash
docker run -d -p 9090:9090 --name prometheus prom/prometheus
```

### Setup để lấy Logs từ ứng dụng, sau đó biểu diễn trên Grafana 

1. Thêm Metrics vào Ứng Dụng của Bạn:
Sử dụng Prometheus Client Library cho Python để tạo và xuất metrics từ ứng dụng của bạn. Bạn có thể sử dụng gói Prometheus Client Python, được cung cấp bởi Prometheus.
Đảm bảo rằng ứng dụng của bạn xuất metrics thông qua HTTP endpoint để Prometheus có thể scrape dữ liệu. Các endpoints này thường được gọi là /metrics.

##### Ví dụ trên python 

```bash 
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

```


#####
Để thống kê hiệu suất của ứng dụng test của bạn với Prometheus, bạn cần cấu hình Prometheus để thu thập các metrics từ ứng dụng của bạn thông qua các endpoint hoặc các thước đo được hiệu quả. Dưới đây là các bước bạn có thể thực hiện:

1. **Thêm Metrics vào Ứng Dụng của Bạn**: Trước tiên, bạn cần phải thêm các endpoints hoặc các thước đo metrics vào ứng dụng Python của bạn. Các metrics này thường là các số liệu liên quan đến hiệu suất của ứng dụng như thời gian xử lý, số lượng requests, số lượng lỗi, v.v. Một thư viện phổ biến để thực hiện điều này trong Python là Prometheus client library. Bạn có thể sử dụng Prometheus client library để tạo và xuất các metrics từ ứng dụng của mình.

2. **Cấu Hình Prometheus để Thu Thập Metrics**: Tiếp theo, bạn cần cấu hình Prometheus để scrape (lấy dữ liệu) từ các endpoint hoặc các thước đo metrics mà ứng dụng của bạn cung cấp. Bạn cần chỉ định các job trong file cấu hình Prometheus (`prometheus.yml`) để nó biết nơi scrape dữ liệu.

3. **Khởi Chạy và Kiểm Tra Cấu Hình Prometheus**: Khởi chạy lại Prometheus và kiểm tra xem nó đã scrape dữ liệu từ ứng dụng của bạn chưa. Bạn có thể kiểm tra bằng cách truy cập vào giao diện web của Prometheus và chuyển đến mục "Targets" hoặc "Status" để xem trạng thái scrape và xác định liệu có lỗi nào xuất hiện không.

4. **Trực Quan Hóa Dữ Liệu với Grafana**: Sau khi bạn đã thu thập dữ liệu từ ứng dụng của mình bằng Prometheus, bạn có thể sử dụng Grafana để trực quan hóa dữ liệu và tạo các biểu đồ và bảng điều khiển để theo dõi hiệu suất của ứng dụng. Grafana có thể được tích hợp với Prometheus một cách dễ dàng và hỗ trợ nhiều loại biểu đồ và dashboard để hiển thị dữ liệu một cách dễ hiểu và thú vị.

Với các bước trên, bạn sẽ có thể bắt đầu thu thập và trực quan hóa dữ liệu hiệu suất của ứng dụng test của mình một cách hiệu quả với Prometheus và Grafana.  


----

### Điều chỉnh config cho Prometheus.yaml
```bash
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090", "ip:9100"]


```

#### Sau khi sửa xong cp file vào docker và cho chạy lại nè 
```bash
root@serverlocal:~# docker cp prometheus.yml prometheus:/etc/prometheus/prometheus.yml
root@serverlocal:~# docker restart prometheus
prometheus
root@serverlocal:~#

# Sau đó vào lại check prometheus đã có lấy được metric chưa bằng cách sau
# Nhập lệnh này: up{instance="192.168.200.128:9100", job="prometheus"}

# Nhập vào Expression

```
#### Định nghĩa của Metrics  

metrics là những con số hoặc chỉ số mà hệ thống hoặc ứng dụng của bạn thu thập và xuất ra để cung cấp thông tin về hiệu suất và trạng thái của chúng.

Đây là một ví dụ đơn giản: Hãy tưởng tượng bạn đang chạy một cửa hàng trực tuyến. Bạn có thể thu thập các metrics sau:

Số lượng người truy cập trang web: Đây là số lượng người truy cập trang web của bạn trong một khoảng thời gian nhất định.
Tỉ lệ chuyển đổi: Số lượng người dùng đã thực hiện mua hàng so với số lượng người dùng đã truy cập trang web.
Thời gian phản hồi của máy chủ: Thời gian mà máy chủ phản hồi lại yêu cầu từ người dùng.
Các metrics này giúp bạn đo lường và theo dõi hiệu suất của cửa hàng trực tuyến của bạn. Khi sử dụng Prometheus, bạn có thể thu thập và lưu trữ các metrics như thế này từ ứng dụng của mình. Sau đó, bạn có thể sử dụng Prometheus để giám sát và phân tích các metrics này để theo dõi hoạt động của cửa hàng trực tuyến của bạn và xác định bất kỳ vấn đề nào mà bạn cần giải quyết.

#### Bước tiếp theo:

Để biểu diễn các metrics thu thập được từ Prometheus trên Grafana thành các biểu đồ giao diện người dùng đẹp, bạn có thể tuân theo các bước sau:

Kết nối Grafana với Prometheus: Trước tiên, bạn cần kết nối Grafana với Prometheus. Điều này cho phép Grafana truy vấn dữ liệu từ Prometheus để tạo các biểu đồ.

Tạo Dashboard mới: Sau khi kết nối, bạn sẽ tạo một Dashboard mới trên Grafana. Dashboard sẽ chứa các biểu đồ và đồ thị của các metrics mà bạn muốn hiển thị.

Thêm Panels (Biểu Đồ): Trong Dashboard, bạn sẽ thêm các Panels (biểu đồ) để hiển thị các metrics. Grafana cung cấp một loạt các tùy chọn biểu đồ, bao gồm biểu đồ đường, biểu đồ cột, biểu đồ vòng tròn, và nhiều loại biểu đồ khác.

Cấu hình Truy vấn (Query): Đối với mỗi Panel, bạn sẽ cấu hình truy vấn để lấy dữ liệu từ Prometheus. Trong truy vấn, bạn chỉ định metrics mà bạn muốn hiển thị và áp dụng các phép lọc, biến đổi hoặc tính toán khác nếu cần.

Tùy chỉnh và Điều chỉnh: Bạn có thể tùy chỉnh các biểu đồ và đồ thị để phản ánh các metrics một cách trực quan và dễ hiểu nhất. Điều chỉnh các màu sắc, nhãn, tiêu đề và định dạng khác để tạo ra một giao diện người dùng đẹp và dễ đọc.

Lưu và Chia sẻ Dashboard: Sau khi tạo và tinh chỉnh Dashboard của bạn, bạn có thể lưu nó và chia sẻ với đồng nghiệp hoặc các thành viên khác của nhóm để họ có thể theo dõi hiệu suất của hệ thống hoặc ứng dụng.

Qua các bước này, bạn có thể biểu diễn các metrics từ Prometheus trên Grafana thành các biểu đồ và đồ thị giao diện người dùng đẹp và dễ đọc.

### Setup Redis


http://192.168.200.128:9090/targets?search=

docker run -d -p 5000:5000 --name admiring_goldwasser linhtran2023/performance_test:v06
