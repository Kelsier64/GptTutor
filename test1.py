from gtts import gTTS
import os

# 要轉換的文本
text = "你好，這是一個文本到語音的示例。"

# 創建 gTTS 對象
tts = gTTS(text=text, lang='zh', slow=False)

# 保存語音文件
tts.save("output.mp3")

# 播放語音文件
os.system("start output.mp3")  # Windows 使用 start，Linux 使用 xdg-open