
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2

def cropping(image_path):
    image = cv2.imread(image_path)
    # 轉換為灰度圖像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 使用邊緣檢測找到鉛筆框的邊界
    edges = cv2.Canny(gray, 50, 150)
    # 尋找輪廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 過濾掉過小或過大的輪廓
    filtered_contours = [cnt for cnt in contours if 1000 < cv2.contourArea(cnt) < 50000]
    # 繪製最大輪廓的矩形框
    max = 0
    for counter in filtered_contours:
        x, y, w, h = cv2.boundingRect(counter)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        m2 = w*h
        if m2 > max:
            max = m2
            cropped_image = image[y:y+h, x:x+w]
    # 將裁切後的圖片保存
    cropped_image_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    cropped_image_pil.save('cropped_image.jpg')

    # plt.subplot(121), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.title('Original Image with Bounding Box'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(edges, cmap='gray')
    # plt.title('Edge Detection'), plt.xticks([]), plt.yticks([])
    # plt.show()