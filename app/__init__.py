from flask import Flask, request, jsonify
# from PIL import Image
from app.mod_pages.function import detection_license_plate
from app.mod_pages.function import detect_text_tesseract
from app.mod_pages.function import count_service_code
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
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
    serial_list = request.form.getlist('serialList')

    if not image_files: 
        # Check if the images are provided
        return jsonify({"errorMessage": "No images provided", "data": None}), 400
    if not serial_list: 
        # Check if the serial list is provided
        return jsonify({"errorMessage": "No serial list provided", "data": None}), 400
    if len(image_files) != len(serial_list): 
        # Check if the number of images and serials match
        return jsonify({"errorMessage": "Number of images and serials do not match", "data": None}), 400

    file_paths = []
    data = []
    checked = "SERVICE CODE"
    resultTextFinal = ""

    try:
        # Ensure the directory exists
        input_dir = './images/inputs'
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)

        index = 0
        for file in image_files:
            # Save the file to the input directory
            file_path = os.path.join(input_dir, file.filename)
            file.save(file_path)

            # Detect text in the image
            resultText = detect_text_tesseract([file_path])
            file_paths.append({"id": index, "serialNo":serial_list[index], "path": f"{file_path}", "textInImage": resultText})
            # Count the number of service codes in image
            count = count_service_code(resultText, serial_list[index], checked)
            data.append({"count": count, "serial": serial_list[index], "id": index})
            
            index = index + 1
        return jsonify({"errorMessage": "", "data":data, "filePaths": file_paths, "serialList": serial_list}), 200
    
    except Exception as e:
        return jsonify({"errorMessage": str(e), "data": None}), 500

    finally:
        # Cleanup: Delete all files in the input directory
        for file in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        # Optional: Remove the directory itself if you want
        # shutil.rmtree(input_dir)

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
