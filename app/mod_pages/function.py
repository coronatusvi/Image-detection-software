import easyocr
import re
import io
from PIL import Image
import numpy as np

reader = easyocr.Reader(['en'])

def is_license_plate(text):
    pattern = r'\b\d{2}-?[A-Z][A-Z\d](\d{3}\.\d{2}|\d{4})\b'
    return bool(re.search(pattern, text))

def process_text(text):
    # Loại bỏ khoảng trắng và ký tự xuống dòng thừa
    cleaned_text = re.sub(r'[\s\n\r]+', '', text)

    for i in range(len(cleaned_text) - 1):
        substring = cleaned_text[i:i+12]
        if is_license_plate(substring):
            return substring
        return ""

def detection_license_plate(image_file):
    try:
        # Đọc tệp ảnh từ request
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image_np = np.array(image)
        
        # Sử dụng EasyOCR để đọc văn bản từ ảnh
        result = reader.readtext(image_np)
        text = " ".join([res[1] for res in result])
        response = process_text(text)
        
        return response
    except Exception as e:
        return ""
    