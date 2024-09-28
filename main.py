import point
import ai
import cv2
image = cv2.imread("img/ex7.jpg")
reply = ai.img2text(image)
print(reply)
ans = ai.answer(reply)
print(ans)