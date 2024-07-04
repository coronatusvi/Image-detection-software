FROM python:3.10-slim-buster

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && \
    apt-get install -y \
    python3-dev \
    gcc \
    g++ \
    libtesseract-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép các tệp của ứng dụng vào Docker image
COPY . .

# Cài đặt các thư viện Python từ requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Chạy ứng dụng
CMD ["python3", "app.py"]
