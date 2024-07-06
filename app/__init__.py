from flask import Flask, request, jsonify
# from PIL import Image
from app.mod_pages.function import detection_license_plate
from app.mod_pages.function import extract_serial_text
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from PIL import Image
import pytesseract
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/curl-image-to-serial-check', methods=['POST'])
def image_to_serial_check():
    try:
        file_path = "/home/dev/flask/Flask-Scan-License-Plate/images/370301498CE.jpg"

        if not os.path.exists(file_path):
            return jsonify({"errorMessage": "File not found", "data": None}), 404

        # Detect text in the image
        image = Image.open(file_path)
        result_text = pytesseract.image_to_string(image)

        return jsonify({
            "errorMessage": "",
            "data": {
                "textInImage": result_text
            }
        }), 200

    except Exception as e:
        return jsonify({"errorMessage": str(e), "data": None}), 500
    
@app.route('/image-to-serial-check', methods=['POST'])
def image_to_serial_check():
    if 'fileImage' not in request.files:
        return jsonify({"errorMessage": "No image provided"}), 400

    # Lấy các tệp ảnh từ yêu cầu
    image_files = request.files.getlist('fileImage')
    # Lấy danh sách tên file từ image_files
    file_names = [file.filename for file in image_files]

    return jsonify({"fileNames": file_names}), 200
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
