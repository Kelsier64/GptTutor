import base64
import key
import requests
import json
import cv2
API_KEY = key.API_KEY
headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
} 
ENDPOINT = "https://hsh2024.openai.azure.com/openai/deployments/gpt4o/chat/completions?api-version=2024-02-15-preview"  
init = {
    "role": "system",
    "content":  """
                把圖片中的題目敘述 圖片説明 （如果有圖片就輸出對題目有用的敘述 盡量詳細） 選項 變成文字
                格式：題號和題目敘述\n圖片説明 （如果有）\n選項
                """
}
def encode_image(img):
    # 將圖像編碼為 JPEG 格式，返回 (retval, buffer)
    retval, buffer = cv2.imencode(".jpg", img)
    # 將編碼後的圖像轉換為 Base64 字符串
    return base64.b64encode(buffer).decode('utf-8')

def gpt4o(img):
    base64_image = encode_image(img)
    messages = []
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
        return reply
    return "error"