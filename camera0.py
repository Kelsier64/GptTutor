import cv2
import numpy as np

# 開啟攝像頭
cap = cv2.VideoCapture(0)

def detect_crosses(frame):
    # 將影像轉為灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 對影像進行模糊處理來去除噪點
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 使用邊緣檢測來找出可能的形狀
    edges = cv2.Canny(blurred, 50, 150)
    
    # 尋找輪廓
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    crosses = []
    
    for contour in contours:
        # 將輪廓逼近為多邊形
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        if len(approx) == 12:  # 假設十字軸的形狀接近有12個角
            # 找到中心點
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                crosses.append((cX, cY))
    
    return crosses

def draw_square(frame, points):
    if len(points) == 2:
        # 根據兩個十字軸的座標繪製正方形
        (x1, y1), (x2, y2) = points
        
        # 計算正方形的邊長
        side_length = int(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        
        # 根據中心點和邊長繪製正方形
        cv2.rectangle(frame, (x1, y1), (x1 + side_length, y1 + side_length), (0, 255, 0), 2)

while True:
    # 讀取攝像頭影像
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # 檢測影像中的十字軸
    crosses = detect_crosses(frame)
    
    # 如果找到兩個十字軸，則繪製正方形
    if len(crosses) == 2:
        draw_square(frame, crosses)
    
    # 顯示影像
    cv2.imshow("Frame", frame)
    
    # 按下 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝像頭並關閉視窗
cap.release()
cv2.destroyAllWindows()
