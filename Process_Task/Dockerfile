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

# Expose cổng 5001 để ứng dụng Flask lắng nghe request
EXPOSE 5001

# Khởi chạy ứng dụng
CMD ["python", "Add_Task.py"]
