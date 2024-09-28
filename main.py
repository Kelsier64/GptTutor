import point
import img2text
import answer
import cv2
image = cv2.imread("img/ex7.jpg")
img = point.blue(image)
reply = img2text.gpt4o(img)
print(reply)
ans = answer.gpt4o(reply)
print(ans)