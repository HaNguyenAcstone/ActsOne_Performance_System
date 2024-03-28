# Sử dụng image Python làm base
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements.txt vào thư mục /app
COPY requirements.txt .

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn ứng dụng vào thư mục /app trong container
COPY . .

# Khởi chạy ứng dụng
CMD ["python", "app.py"]

# docker run -d -p 5000:5000 --name add_task_redis linhtran2023/add_task_redis:v08