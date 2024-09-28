import cv2
import numpy as np
import point
import img2text
import answer
import time
# 開啟相機
cap = cv2.VideoCapture(0)  # 0 通常是預設的相機
count = 0
while True:
    # 捕獲幀
    ret, frame = cap.read()
    if not ret:
        print("無法讀取影像")
        break
    img,check = point.camera(frame)



    if check:
        count += 1
    else:
        count = 0
    if count == 20:
        reply = img2text.gpt4o(img)
        print(reply)
        ans = answer.gpt4o(reply)
        print(ans)
        count = 0
        time.sleep(10)

    cv2.imshow("blue", img)
    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放相機資源
cap.release()
cv2.destroyAllWindows()
