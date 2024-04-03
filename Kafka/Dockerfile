# # Sử dụng image Python làm base
# FROM python:3.9-slim

# # Thiết lập thư mục làm việc
# WORKDIR /app

# # Copy file requirements.txt vào thư mục /app
# COPY requirements.txt .

# # Cài đặt các dependencies từ requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy mã nguồn ứng dụng vào thư mục /app trong container
# COPY . .

# # Cấp quyền thực thi cho file app.py
# RUN chmod u+x app.py

# # Khởi chạy ứng dụng khi container được khởi động
# CMD ["python", "app.py"]

# Sử dụng một base image có sẵn, ví dụ: Python 3.9 slim
FROM python:3.9-slim

# Copy các tệp cần thiết vào container
COPY producer.py getting_started.ini /app/

# Đặt thư mục làm việc
WORKDIR /app

# Copy file requirements.txt vào thư mục /app
COPY requirements.txt .

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Thay đổi quyền cho producer.py và chạy script khi container được khởi động
RUN chmod u+x producer.py

# Định nghĩa entry point script để chạy khi container được khởi động
ENTRYPOINT ["./producer.py", "getting_started.ini"]
