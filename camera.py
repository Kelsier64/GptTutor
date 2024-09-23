
import numpy as np
import cv2
import crop
from PIL import Image
# 開啟攝像頭
cap = cv2.VideoCapture(0)

while True:
    # 捕捉攝像頭中的幀
    ret, frame = cap.read()
    
    # 將圖片轉換為灰度

# 將圖片轉為灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 邊緣檢測 (可以調整參數)
    edges = cv2.Canny(gray, 50, 150)

    # 創建十字形的結構元素進行形態學操作
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

    # 使用形態學運算增強十字形的形狀
    cross_detected = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # 找到輪廓
    contours, _ = cv2.findContours(cross_detected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 繪製輪廓
    for cnt in contours:
        # 計算輪廓的幾何矩
        M = cv2.moments(cnt)

        # 確保計算結果不為零，避免除以零的錯誤
        if M['m00'] != 0:
            # 計算質心
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])

            # 在圖片上標記質心
            cv2.circle(frame, (cX, cY), 5, (255, 255, 0), -1)

            # 繪製偵測到的十字形
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
    # 顯示處理後的畫面
    cv2.imshow('Camera', frame)
    
    # 按下 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝像頭資源並關閉窗口
cap.release()
cv2.destroyAllWindows()
