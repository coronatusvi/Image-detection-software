from flask import Flask, request, jsonify
import easyocr
# from PIL import Image
from app.mod_pages.function import detection_license_plate
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        return 'No file part in the request.'
    file = request.files['fileImage']
    filename = secure_filename(file.filename)
    file.save(filename)

    result = detection_license_plate(filename)
    if not result: 
        return jsonify({"data": "Không nhận dạng được ảnh " + filename})
    return jsonify({"data": list(result)}) 
