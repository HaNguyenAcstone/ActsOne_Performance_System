### Thông tin mẫu của 1 Server chạy các service

```bash

root@serverlocal:~# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' f73c725cced0
172.22.0.2
root@serverlocal:~# curl 172.22.0.2:8125/metrics
# HELP cpu_usage_guest Telegraf collected metric
# TYPE cpu_usage_guest gauge
cpu_usage_guest{cpu="cpu-total",host="f73c725cced0"} 0
cpu_usage_guest{cpu="cpu0",host="f73c725cced0"} 0
cpu_usage_guest{cpu="cpu1",host="f73c725cced0"} 0
# HELP cpu_usage_guest_nice Telegraf collected metric
# TYPE cpu_usage_guest_nice gauge
cpu_usage_guest_nice{cpu="cpu-total",host="f73c725cced0"} 0
cpu_usage_guest_nice{cpu="cpu0",host="f73c725cced0"} 0
cpu_usage_guest_nice{cpu="cpu1",host="f73c725cced0"} 0
# HELP cpu_usage_idle Telegraf collected metric
# TYPE cpu_usage_idle gauge
cpu_usage_idle{cpu="cpu-total",host="f73c725cced0"} 99.3930197268549
cpu_usage_idle{cpu="cpu0",host="f73c725cced0"} 99.39393939393538
cpu_usage_idle{cpu="cpu1",host="f73c725cced0"} 99.3914807302191
# HELP cpu_usage_iowait Telegraf collected metric
# TYPE cpu_usage_iowait gauge
cpu_usage_iowait{cpu="cpu-total",host="f73c725cced0"} 0
cpu_usage_iowait{cpu="cpu0",host="f73c725cced0"} 0
cpu_usage_iowait{cpu="cpu1",host="f73c725cced0"} 0
# HELP cpu_usage_irq Telegraf collected metric
# TYPE cpu_usage_irq gauge
cpu_usage_irq{cpu="cpu-total",host="f73c725cced0"} 0
cpu_usage_irq{cpu="cpu0",host="f73c725cced0"} 0
cpu_usage_irq{cpu="cpu1",host="f73c725cced0"} 0
# HELP cpu_usage_nice Telegraf collected metric
# TYPE cpu_usage_nice gauge
cpu_usage_nice{cpu="cpu-total",host="f73c725cced0"} 0
cpu_usage_nice{cpu="cpu0",host="f73c725cced0"} 0
cpu_usage_nice{cpu="cpu1",host="f73c725cced0"} 0
# HELP cpu_usage_softirq Telegraf collected metric
# TYPE cpu_usage_softirq gauge
cpu_usage_softirq{cpu="cpu-total",host="f73c725cced0"} 0
cpu_usage_softirq{cpu="cpu0",host="f73c725cced0"} 0
cpu_usage_softirq{cpu="cpu1",host="f73c725cced0"} 0
# HELP cpu_usage_steal Telegraf collected metric
# TYPE cpu_usage_steal gauge
cpu_usage_steal{cpu="cpu-total",host="f73c725cced0"} 0
cpu_usage_steal{cpu="cpu0",host="f73c725cced0"} 0
cpu_usage_steal{cpu="cpu1",host="f73c725cced0"} 0
# HELP cpu_usage_system Telegraf collected metric
# TYPE cpu_usage_system gauge
cpu_usage_system{cpu="cpu-total",host="f73c725cced0"} 0.20232675771378805
cpu_usage_system{cpu="cpu0",host="f73c725cced0"} 0.3030303030302978
cpu_usage_system{cpu="cpu1",host="f73c725cced0"} 0.20283975659223977
# HELP cpu_usage_user Telegraf collected metric
# TYPE cpu_usage_user gauge
cpu_usage_user{cpu="cpu-total",host="f73c725cced0"} 0.4046535154272886
cpu_usage_user{cpu="cpu0",host="f73c725cced0"} 0.3030303030302978
cpu_usage_user{cpu="cpu1",host="f73c725cced0"} 0.40567951318447953

# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 7.03
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 9
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 1.2392448e+08
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.71161221321e+09
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 5.7863168e+09
# HELP process_virtual_memory_max_bytes Maximum amount of virtual memory available in bytes.
# TYPE process_virtual_memory_max_bytes gauge
process_virtual_memory_max_bytes 1.8446744073709552e+19

```

----

#### Giải nghĩa
Thông tin này là các metric được thu thập bởi Telegraf, một agent thu thập dữ liệu và chuyển đổi nó thành định dạng tương thích với Prometheus để giám sát hệ thống của bạn. Dưới đây là mô tả về mỗi metric:

1. **cpu_usage_guest**: Tỉ lệ thời gian CPU dành cho các tiến trình khách (guest) trên CPU cụ thể hoặc tổng thể.

2. **cpu_usage_guest_nice**: Tỉ lệ thời gian CPU dành cho các tiến trình khách với độ ưu tiên thấp (nice) trên CPU cụ thể hoặc tổng thể.

3. **cpu_usage_idle**: Tỉ lệ thời gian CPU không hoạt động trên CPU cụ thể hoặc tổng thể.

4. **cpu_usage_iowait**: Tỉ lệ thời gian CPU đang chờ đợi I/O trên CPU cụ thể hoặc tổng thể.

5. **cpu_usage_irq**: Tỉ lệ thời gian CPU dành cho xử lý interrupt trên CPU cụ thể hoặc tổng thể.

6. **cpu_usage_nice**: Tỉ lệ thời gian CPU dành cho các tiến trình với độ ưu tiên thấp (nice) trên CPU cụ thể hoặc tổng thể.

7. **cpu_usage_softirq**: Tỉ lệ thời gian CPU dành cho xử lý soft interrupt trên CPU cụ thể hoặc tổng thể.

8. **cpu_usage_steal**: Tỉ lệ thời gian CPU bị "stolen" bởi máy ảo hoặc các tiến trình khác trên CPU cụ thể hoặc tổng thể.

9. **cpu_usage_system**: Tỉ lệ thời gian CPU được sử dụng cho các tiến trình hệ thống trên CPU cụ thể hoặc tổng thể.

10. **cpu_usage_user**: Tỉ lệ thời gian CPU được sử dụng bởi các tiến trình người dùng trên CPU cụ thể hoặc tổng thể.

----

Dưới đây là giải thích cho các metric khác:

1. **process_cpu_seconds_total**: Đây là tổng số lượng thời gian CPU (tính bằng giây) mà quá trình đã sử dụng tính từ lúc bắt đầu quá trình đó. Metric này cung cấp một cái nhìn tổng quan về việc sử dụng CPU của quá trình.

2. **process_max_fds**: Đây là số lượng tối đa của file descriptor (mô tả file) mà quá trình có thể mở đồng thời. Mỗi file descriptor đại diện cho một file, socket, hoặc đối tượng hệ thống tập tin khác mà quá trình đang sử dụng.

3. **process_open_fds**: Đây là số lượng file descriptor (mô tả file) mà quá trình hiện đang mở. Metric này cung cấp thông tin về số lượng tài nguyên hệ thống đang được sử dụng bởi quá trình.

4. **process_start_time_seconds**: Đây là thời gian kể từ khi quá trình được bắt đầu tính bằng giây, tính từ thời điểm Epoch (thường là 1 tháng 1 năm 1970). Metric này cho biết thời gian khởi đầu của quá trình đó.

5. **process_virtual_memory_bytes**: Đây là kích thước của bộ nhớ ảo mà quá trình đang sử dụng. Nó bao gồm tất cả các phần của bộ nhớ mà quá trình có thể truy cập, bao gồm cả bộ nhớ vật lý và ổ đĩa.

6. **process_virtual_memory_max_bytes**: Đây là giới hạn tối đa của bộ nhớ ảo mà quá trình có thể sử dụng. Metric này cung cấp một cái nhìn về giới hạn cao nhất của bộ nhớ mà quá trình có thể sử dụng.