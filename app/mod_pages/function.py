import json
# from openalpr import Alpr
import easyocr

reader = easyocr.Reader(['en'])

def recognize_license_plate(file_path):
    with open(file_path, 'rb') as f:
        image_bytes = f.read()
    result = reader.readtext(image_bytes)
    text = " ".join([res[1] for res in result])
    return text

    alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
    if not alpr.is_loaded():
        return "Error loading OpenALPR"

    results = alpr.recognize_file(file_path)
    alpr.unload()

    # Kiểm tra xem kết quả có dữ liệu không
    if results['results']:
        # Lấy biển số xe từ kết quả nhận dạng
        plate_number = results['results'][0]['plate']
        print("Plate number:", plate_number)
        return plate_number
    else:
        return "No plate number found"
