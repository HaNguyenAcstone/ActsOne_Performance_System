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

# Cấp quyền thực thi cho file app.py
RUN chmod u+x app.py

# Khởi chạy ứng dụng khi container được khởi động
CMD ["python", "app.py"]

# Lệnh để chạy container
# docker run -d -p 5000:5000 --name <tên-container> <tên-image>
