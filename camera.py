import cv2
import numpy as np
import point
import ai
import time
import re
import json
# 開啟相機
cap = cv2.VideoCapture(0)  # 0 通常是預設的相機
count = 0

def str_code(response):
    string = re.search(r'```(.*?)```', response, re.DOTALL)
    if string:
        code = string.group(0)
        code = code.replace('\n', '')  
    else:
        print("未找到內容")
    return code

def json_code(response):
    string = re.search(r'\[(.*)\]', response, re.DOTALL)
    if string:
        code = string.group(0)  
    else:
        print("未找到內容")
    return code

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

        reply = ai.img2text(img)
        print(reply)
        print("======================================================")
        reply_json = json_code(str_code(reply))
        print(reply_json)
        print("======================================================")
        ans = ai.answer(reply_json)
        print(ans)
        print("======================================================")
        ans_json = json_code(str_code(ans))
        data = json.loads(ans_json)
        print(data)
        print(data[0]["number"])
        count = 0
        time.sleep(10)
        

    cv2.imshow("blue", img)
    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放相機資源
cap.release()
cv2.destroyAllWindows()
