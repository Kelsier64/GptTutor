import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import json
import requests
import base64
import crop
import key
crop.cropping("ex0")

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image("cropped_image.jpg")
API_KEY = key.API_KEY
headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
} 
ENDPOINT = "https://hsh2024.openai.azure.com/openai/deployments/gpt4o/chat/completions?api-version=2024-02-15-preview"  


messages = []
init = {
    "role": "system",
    "content":  """
                把圖片中的題目敘述 圖片説明 （如果有圖片就輸出對題目有用的資訊 盡量詳細） 選項 變成文字
                格式：題號和題目敘述\n圖片説明 （如果有）\n選項
                """
}
messages.append(init)
        
        # 添加用戶輸入到 messages 中
messages.append({"role": "user", 
                 "content": [
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                })  

payload = {  
    "messages": messages,
    "temperature": 0.7,  
    "top_p": 0.95,  
    "max_tokens": 800  
}
response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))  
if response.status_code == 200:  
    response_data = response.json()  
    reply = response_data['choices'][0]['message']['content']

print(reply)