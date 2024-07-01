import os
import cv2
import torch
import function.utils_rotate as utils_rotate
import function.helper as helper
import os
import pytesseract
from PIL import Image
from dotenv import load_dotenv

# Detection license plate
def detection_license_plate(filename):
    # Your image detection code here
    yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector.pt', force_reload=True, source='local')
    yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr.pt', force_reload=True, source='local')
    yolo_license_plate.conf = 0.60

    img = cv2.imread(filename)  # Read the image file
    plates = yolo_LP_detect(img, size=640)
    list_plates = plates.pandas().xyxy[0].values.tolist()
    list_read_plates = set()

    try:
        if len(list_plates) == 0:
            lp = helper.read_plate(yolo_license_plate, img)
            if lp != "unknown":
                list_read_plates.add(lp)
        else:
            for plate in list_plates:
                flag = 0
                x = int(plate[0])  # xmin
                y = int(plate[1])  # ymin
                w = int(plate[2] - plate[0])  # xmax - xmin
                h = int(plate[3] - plate[1])  # ymax - ymin
                crop_img = img[y:y+h, x:x+w]
                cv2.rectangle(img, (int(plate[0]), int(plate[1])), (int(plate[2]), int(plate[3])), color=(0, 0, 225), thickness=2)
                # cv2.imwrite("crop.jpg", crop_img)
                lp = ""

                for cc in range(0, 2):
                    for ct in range(0, 2):
                        lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                        if lp != "unknown":
                            list_read_plates.add(lp)
                            flag = 1
                            break
                    if flag == 1:
                        break
    finally:
        # Delete the image file after processing
        os.remove(filename)

    # Return the result as text
    return list_read_plates

# Load environment variables from .env file
load_dotenv()
# Set the TESSDATA_PREFIX environment variable from .env
tessdata_prefix = os.getenv('TESSDATA_PREFIX')
if tessdata_prefix:
    os.environ['TESSDATA_PREFIX'] = tessdata_prefix

def detect_text_tesseract(image_files):
    textReturn = ""
    for file in image_files:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)  # Thay 'vie' bằng mã ngôn ngữ của bạn nếu cần
        textReturn += text
    # Xoá hết các khoảng trắng chứa 2 space trở lên
    textReturn = " ".join(textReturn.split()) 
    return textReturn

def count_service_codes_check_multi(text, service_codes, checked):
    counts = {}
    for code in service_codes:
        counts[code] = text.count(code)
    for code in checked:
        counts[code] = text.count(code)
    return counts

def count_service_code(text, service_code, checked):
    if checked in text:
        if service_code in text:
            count = 1 # If 'SERVICE CODE' is exist and service_code is exist => set count to 1
        else :
            count = 0
    else:
        # If 'SERVICE CODE' is not found, set counts for all service_codes to 0        
        count = 0
    return count