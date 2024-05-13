from flask import Flask, jsonify, request

from app.mod_pages.function import recognize_license_plate

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/scan-license-plate', methods=['POST'])
def scan_api():
    # return "Xin chào Quang"
    # Xử lý yêu cầu POST
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']

    # Kiểm tra xem có phải là tệp tin hợp lệ hay không
    if file.filename == '':
        return 'No file selected', 400

    # Lấy đường dẫn của tệp tin
    file_path = file.filename
    # return 'Đã lấy được file ' + file_path

    result = recognize_license_plate(file_path)

    # Trả về kết quả
    if result:
        return jsonify({"plate_number": result})
    else:
        return 'Could not recognize license plate'
