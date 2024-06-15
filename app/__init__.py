from flask import Flask, request, jsonify
# from PIL import Image
from app.mod_pages.function import detection_license_plate
from app.mod_pages.function import extract_serial_text
from werkzeug.utils import secure_filename
import base64
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/image-to-serial-check', methods=['POST'])
def image_to_serial_check():
    if 'fileImage' not in request.files:
        return jsonify({"errorMessage": "No image provided"}), 400

    # Lấy các tệp ảnh từ yêu cầu
    image_files = request.files.getlist('fileImage')
    # Lấy danh sách tên file từ image_files
    base64_files = []
    for file in image_files:
        file_name = file.filename
        file_content = file.read()
        base64_content = base64.b64encode(file_content).decode('utf-8')
        base64_files.append({
            "fileName": file_name,
            "base64Content": base64_content
        })

    return jsonify({"base64Files": base64_files}), 200

    if not image_files:
        return jsonify({"errorMessage": "No images provided"}), 400
    
    image_bytes_list = [image.read() for image in image_files]
    result = extract_serial_text(image_bytes_list)

    if "errorMessage" in result:
        return jsonify({"errorMessage":result.get("errorMessage")}), 400
    else:
        return jsonify({"data": result}), 200

@app.route('/scan-license-plate', methods=['POST'])
def scan_license_plate():
    if 'fileImage' not in request.files:
        return jsonify({"errorMessage": "No image provided"}), 400
    file = request.files['fileImage']
    filename = secure_filename(file.filename)
    file.save(filename)

    result = detection_license_plate(filename)
    if not result: 
        return jsonify({"errorMessage": "Không nhận dạng được ảnh!"}), 400
    return jsonify({"errorMessage":"", "data": list(result)}), 200
