import cv2
import numpy as np
def merge_close_points(points, threshold=100):
    merged_points = []
    while points:
        ref_point = points.pop(0)
        close_points = [ref_point]
        points_to_remove = []
        for point in points:
            distance = np.sqrt((ref_point[0] - point[0])**2 + (ref_point[1] - point[1])**2)
            if distance < threshold:
                close_points.append(point)
                points_to_remove.append(point)
        
        for point in points_to_remove:
            points.remove(point)

        # 計算所有近距離點的平均值
        avg_x = int(np.mean([p[0] for p in close_points]))
        avg_y = int(np.mean([p[1] for p in close_points]))
        merged_points.append((avg_x, avg_y))

    return merged_points
def blue(img):
    image = img

# 將圖片從 BGR 轉換到 HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 定義藍色的HSV範圍
    lower_blue = np.array([70, 50, 0])  # 藍色的下界
    upper_blue = np.array([140, 255, 255])  # 藍色的上界

# 創建遮罩，過濾掉非藍色部分
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 尋找輪廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 儲存點的座標
    blue_points = []

# 遍歷每個輪廓，計算中心點
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            blue_points.append((cx, cy))

    points = merge_close_points(blue_points)
    if len(points) == 4:
        p = np.int64(points)
        x = min(p[:,0])
        y = min(p[:,1])
        w = max(p[:, 0]) - min(p[:, 0])
        h = max(p[:, 1]) - min(p[:, 1])
        img = image[y:y+h, x:x+w]

    for point in points:
        cv2.circle(img, point, 5, (0, 255, 0), -1)

    print(f"合併後的藍色點座標: {points}")
    cv2.imwrite("blue.jpg", img)
    return img

def camera(img):
    image = img

# 將圖片從 BGR 轉換到 HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 定義藍色的HSV範圍
    lower_blue = np.array([70, 50, 0])  # 藍色的下界
    upper_blue = np.array([140, 255, 255])  # 藍色的上界

# 創建遮罩，過濾掉非藍色部分
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 尋找輪廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 儲存點的座標
    blue_points = []

# 遍歷每個輪廓，計算中心點
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            blue_points.append((cx, cy))

    points = merge_close_points(blue_points)
    if len(points) == 4:
        p = np.int64(points)
        x = min(p[:,0])
        y = min(p[:,1])
        w = max(p[:, 0]) - min(p[:, 0])
        h = max(p[:, 1]) - min(p[:, 1])
        image = image[y:y+h, x:x+w]
        return image,True

    for point in points:
        cv2.circle(image, point, 5, (0, 255, 0), -1)

    cv2.imwrite("blue.jpg", image)
    return image,False
