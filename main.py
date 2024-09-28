import point
import img2text
import answer
img = point.blue("img/ex7.jpg")
reply = img2text.gpt4o(img)
print(reply)
ans = answer.gpt4o(reply)
print(ans)