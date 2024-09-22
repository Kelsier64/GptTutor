import crop
import img2text
import answer
crop.cropping("ex0.jpg")
reply = img2text.gpt4o()
print(reply)
ans = answer.gpt4o(reply)
print(ans)