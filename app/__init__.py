from flask import Flask, request, jsonify
import easyocr
from PIL import Image

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

reader = easyocr.Reader(['en']) 
@app.route('/scan-license-plate', methods=['POST'])
def ocr():
    if 'fileImage' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    # Lấy đường dẫn của tệp tin
    image_file = request.files['fileImage']
    
    # Lấy đường dẫn của tệp tin
    file_path = image_file.filename

    image_bytes = image_file.read()

    result = reader.readtext(image_bytes)
    text = " ".join([res[1] for res in result])

    if text == "": 
        return jsonify({"text": file_path})
    return jsonify({"text": text})
