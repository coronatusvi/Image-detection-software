# Sử dụng hình ảnh chính thức của Python làm hình ảnh cơ sở
FROM python:3.10.12

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép các tệp requirements.txt vào container
COPY requirements.txt requirements.txt

# Cài đặt các thư viện Python từ requirements.txt
RUN pip install -r requirements.txt

# Sao chép toàn bộ dự án vào container
COPY . .

# Chạy ứng dụng Flask bằng Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]