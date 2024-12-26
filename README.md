# Image-Detection-Software for Gara: A Real-Time Vietnamese License Plate Recognition System

This project showcases a real-time image detection software designed for use in parking garages (gara), focusing on the accurate detection and recognition of Vietnamese license plates. Leveraging a combination of deep learning techniques with a Flask-based web application, the system provides a robust and efficient solution for automated vehicle entry and tracking.

## Key Features:

*   **Real-Time Detection:** The system is capable of processing video feeds and still images, detecting license plates within a fraction of a second.
*   **High Accuracy:** Achieves high recognition accuracy for Vietnamese license plates, accounting for various fonts, sizes, and lighting conditions.
*   **Flask-Based Web Application:** The user interface is built using Flask, providing a simple and intuitive platform to interact with the system.
*   **Deep Learning Powered:** Employs state-of-the-art deep learning models trained on a large dataset of Vietnamese license plate images, optimized for performance and accuracy.
*   **Scalable:** Designed to handle multiple concurrent users and processing requests.

## Technical Details:

The core of the application consists of a convolutional neural network (CNN) for license plate detection, and an optical character recognition (OCR) model for text recognition. The Flask application handles image uploads or video streaming, passing the image frames to the detection pipeline, extracting license plate information, and presenting the results to the user.

## Images:

<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/architecture.jpg?raw=true" width="600" alt="Example architecture diagram of the system"/>
    <br/>*Example architecture diagram of the system*
</div>
<br/>
<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/input.jpg?raw=true" width="600" alt="A sample input image with a license plate"/>
    <br/>*A sample input image with a license plate*
</div>
<br/>
<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/flow.png?raw=true" width="600" alt="The detected license plate and recognized text output"/>
    <br/>*The detected license plate and recognized text output*
</div>

I'm excited to present this project at the Computer Vision Projects Expo 2024!



# Vietnamese:

# Phần mềm Nhận diện Hình ảnh cho Gara: Hệ thống Nhận dạng Biển số Xe Việt Nam Theo Thời Gian Thực

Dự án này giới thiệu một phần mềm nhận diện hình ảnh thời gian thực được thiết kế để sử dụng trong các gara đậu xe, tập trung vào việc phát hiện và nhận dạng chính xác biển số xe Việt Nam. Sử dụng kết hợp các kỹ thuật học sâu với một ứng dụng web dựa trên Flask, hệ thống cung cấp một giải pháp mạnh mẽ và hiệu quả để tự động hóa việc vào và theo dõi xe.

## Các Tính năng Chính:

*   **Phát hiện Thời gian Thực:** Hệ thống có khả năng xử lý các luồng video và ảnh tĩnh, phát hiện biển số xe trong một phần nhỏ của giây.
*   **Độ chính xác Cao:** Đạt được độ chính xác nhận dạng cao cho biển số xe Việt Nam, tính đến các phông chữ, kích thước và điều kiện ánh sáng khác nhau.
*   **Ứng dụng Web Dựa trên Flask:** Giao diện người dùng được xây dựng bằng Flask, cung cấp một nền tảng đơn giản và trực quan để tương tác với hệ thống.
*   **Ứng dụng Học Sâu:** Sử dụng các mô hình học sâu tiên tiến được đào tạo trên một tập dữ liệu lớn các hình ảnh biển số xe Việt Nam, được tối ưu hóa cho hiệu suất và độ chính xác.
*   **Khả năng Mở rộng:** Được thiết kế để xử lý nhiều người dùng đồng thời và các yêu cầu xử lý.

## Chi tiết Kỹ thuật:

Cốt lõi của ứng dụng bao gồm một mạng nơ-ron tích chập (CNN) để phát hiện biển số xe và một mô hình nhận dạng ký tự quang học (OCR) để nhận dạng văn bản. Ứng dụng Flask xử lý việc tải lên hình ảnh hoặc phát trực tiếp video, chuyển các khung hình đến pipeline phát hiện, trích xuất thông tin biển số xe và hiển thị kết quả cho người dùng.

## Hình ảnh:

<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/architecture.jpg?raw=true" width="600" alt="Ví dụ về sơ đồ kiến trúc của hệ thống"/>
    <br/>*Ví dụ về sơ đồ kiến trúc của hệ thống*
</div>
<br/>
<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/input.jpg?raw=true" width="600" alt="Một ảnh đầu vào mẫu có biển số xe"/>
    <br/>*Một ảnh đầu vào mẫu có biển số xe*
</div>
<br/>
<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/flow.png?raw=true" width="600" alt="Biển số xe được phát hiện và văn bản nhận dạng được xuất ra"/>
    <br/>*Biển số xe được phát hiện và văn bản nhận dạng được xuất ra*
</div>



# Chinese:

# 停车场图像检测软件：实时越南车牌识别系统

本项目展示了一个专为停车场（gara）设计的实时图像检测软件，专注于准确检测和识别越南车牌。通过结合深度学习技术与基于 Flask 的 Web 应用程序，该系统为自动化车辆进入和跟踪提供了一个强大而高效的解决方案。

## 主要特点：

*   **实时检测：** 系统能够处理视频流和静态图像，在几分之一秒内检测到车牌。
*   **高精度：** 对越南车牌实现高识别准确率，考虑了各种字体、大小和光照条件。
*   **基于 Flask 的 Web 应用程序：** 用户界面使用 Flask 构建，提供了一个简单直观的平台与系统进行交互。
*   **深度学习驱动：** 采用最先进的深度学习模型，这些模型在大量越南车牌图像数据集上训练，并针对性能和准确性进行了优化。
*   **可扩展性：** 设计用于处理多个并发用户和处理请求。

## 技术细节：

该应用程序的核心包括用于车牌检测的卷积神经网络 (CNN) 和用于文本识别的光学字符识别 (OCR) 模型。 Flask 应用程序处理图像上传或视频流，将图像帧传递到检测管道，提取车牌信息，并将结果呈现给用户。

## 图片：

<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/architecture.jpg?raw=true" width="600" alt="系统架构图示例"/>
    <br/>*系统架构图示例*
</div>
<br/>
<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/input.jpg?raw=true" width="600" alt="带有车牌的示例输入图像"/>
    <br/>*带有车牌的示例输入图像*
</div>
<br/>
<div align="center">
    <img src="https://github.com/coronatusvi/Image-detection-software/blob/main/images/flow.png?raw=true" width="600" alt="检测到的车牌和识别的文本输出"/>
    <br/>*检测到的车牌和识别的文本输出*
</div>


# Vietnamese License Plate

This repository provides you with a detailed guide on how to training and build a Vietnamese License Plate detection and recognition system. This system can work on 2 types of license plate in Vietnam, 1 line plates and 2 lines plates.

## Installation

```bash
  # install dependencies using pip 
  pip install -r ./requirement.txt
```
  
## Run License Plate

```bash
  # run inference on webcam (15-20fps if there is 1 license plate in scene)
  python webcam.py 

  # run inference on image
  python lp_image.py -i test_image/3.jpg

  # run LP_recognition.ipynb if you want to know how model work in each step
```

## Result

## Vietnamese Plate Dataset

## Training

**Training code for Yolov5:**

Use code in ./training folder
```bash
  training/Plate_detection.ipynb     #for LP_Detection
  training/Letter_detection.ipynb    #for Letter_detection
```
```
  pip install pytesseract
  !sudo apt-get install tesseract-ocr
  !tesseract --version
```
