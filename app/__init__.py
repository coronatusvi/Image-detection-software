from flask import Flask, request, jsonify
import easyocr
# from PIL import Image
from app.mod_pages.function import detection_license_plate

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/ocr', methods=['POST'])
def ocr():
    reader = easyocr.Reader(['en'])     
    if 'fileImage' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    # Lấy đường dẫn của tệp tin
    image_file = request.files['fileImage']

    image_bytes = image_file.read()

    result = reader.readtext(image_bytes)
    text = " ".join([res[1] for res in result])
    return jsonify({"text": text})


@app.route('/scan-license-plate', methods=['POST'])
def scan_license_plate():
    if 'fileImage' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    # Lấy đường dẫn của tệp tin
    image_file = request.files['fileImage']
    
    # Lấy đường dẫn của tệp tin
    file_path = image_file.filename

    result = detection_license_plate(image_file)
    if result == "": 
        return jsonify({"text": file_path})
    return jsonify({"text": result})
