import os
import cv2
import torch
import function.utils_rotate as utils_rotate
import function.helper as helper
import base64
from flask import request

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


API_URL = "https://imagetext.io/api/extract-text"

def extract_serial_text(image_files):
    combined_text = ""
    headers = {
        "Content-Type": "application/json"
    }

    for file in image_files:
        file_content = file.read()
        base64_content = base64.b64encode(file_content).decode('utf-8')
        payload = {
            "locale": "eng",
            "imageBase64": base64_content
        }

        response = request.post(API_URL, json=payload, headers=headers)
        error = data.get("ocrResult", {}).get("ErrorDetails", "")
        if error != "":
            return {"errorMessage": error}
        
        data = response.json()
        text = data.get("text", {}).get("ParsedText", "")
        combined_text += text

    return {"errorMessage":"", "data":combined_text}
