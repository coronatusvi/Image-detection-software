from flask import Flask, request, jsonify
# from PIL import Image
from app.mod_pages.function import detection_license_plate
from app.mod_pages.function import detect_text_tesseract
from app.mod_pages.function import count_service_codes
from werkzeug.utils import secure_filename
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/image-to-serial-check', methods=['POST'])
def image_to_serial_check():
    if 'fileImage' not in request.files:
        return jsonify({"errorMessage": "No image provided", "data": None}), 400

    image_files = request.files.getlist('fileImage')

    if not image_files:
        return jsonify({"errorMessage": "No images provided", "data": None}), 400

    if 'serviceCodes' not in request.form:
        return jsonify({"errorMessage": "No service codes provided", "data": None}), 400

    service_codes = request.form.getlist('serviceCodes')
    checked = ["SERVICE CODE"]

    try:
        text = detect_text_tesseract(image_files)
        counts = count_service_codes(text, service_codes, checked)
        return jsonify({"errorMessage": "", "data": counts}), 200
    except Exception as e:
        return jsonify({"errorMessage": str(e), "data": None}), 400

@app.route('/scan-license-plate', methods=['POST'])
def scan_license_plate():
    if 'fileImage' not in request.files:
        return jsonify({"errorMessage": "No image provided"}), 400
    file = request.files['fileImage']
    filename = secure_filename(file.filename)
    file.save(filename)

    result = detection_license_plate(filename)
    if not result: 
        return jsonify(
            {
                "errorMessage": "Không nhận dạng được ảnh!",
                "data": list("")
                }
            ), 400
    return jsonify(
        {"errorMessage":"",
          "data": list(result)
          }
        ), 200
