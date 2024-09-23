import cv2
import numpy as np

# 開啟攝像頭
cap = cv2.VideoCapture(0)

while True:
    # 捕捉攝像頭中的幀
    ret, frame = cap.read()
    
    # 將圖片轉換為灰度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 使用 Canny 邊緣檢測
    edges = cv2.Canny(gray, 50, 150)
    
    # 尋找邊緣的輪廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # 尋找近似的多邊形來檢測矩形框
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # 如果有四個頂點，則認為是矩形
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            
            # 繪製矩形框（你可以先確認框的檢測是否正確）
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
            
            # 裁剪矩形框內的區域
            cropped = frame[y:y+h, x:x+w]
            
            # 儲存裁切的圖片
            cv2.imwrite("cropped_image.png", cropped)
    
    # 顯示處理後的畫面
    cv2.imshow('Camera', frame)
    
    # 按下 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝像頭資源並關閉窗口
cap.release()
cv2.destroyAllWindows()
