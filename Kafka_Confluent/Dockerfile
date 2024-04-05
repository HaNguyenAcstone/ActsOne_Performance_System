# Sử dụng một image cơ sở với Python
FROM python:3.9-slim

# Set thư mục làm việc là /app
WORKDIR /app

# Sao chép mã nguồn vào thư mục /app trong container
COPY . .

# Cài đặt dependencies từ file requirements.txt nếu có
# Nếu không có, bạn cũng có thể cài đặt trực tiếp các dependencies cần thiết ở đây
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt confluent_kafka package
RUN pip install confluent_kafka

# Chạy script khi container được khởi động
CMD [ "python", "app.py", "getting_started.ini" ]
