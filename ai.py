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
init_img2text = {
    "role": "user",
    "content":  """
                請把圖片中的題目轉化成文字
                題目分成文字敘述跟圖兩個部分或是只有文字
                假如有圖片 請分析圖片 告訴我對題目有用的內容 且盡量詳細

                然後輸出給我題目敘述 跟你分析過後的圖片 
                最後再統整所有資訊 分析題目 寫出答案
                Json格式範例:
                {
                "number": “題號”,
                "text": "題目內容",
                "image_description": "如果有圖片，請輸入圖片描述，否則為 null",
                "options": “如果有選項，請輸入圖片描述，否則為 null”,
                "idea":"統整以上並分析題目 寫下你的思考過程",
                "answer":"答案"
                }
                """
}

def encode_image(img):
    # 將圖像編碼為 JPEG 格式，返回 (retval, buffer)
    retval, buffer = cv2.imencode(".jpg", img)
    # 將編碼後的圖像轉換為 Base64 字符串
    return base64.b64encode(buffer).decode('utf-8')

def img2text(img):
    base64_image = encode_image(img)
    messages = []
    
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
    messages.append(init_img2text)
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

init_answer = {
    "role": "user",
    "content":  """            
                根據以下内容 分析題目跟想法 判斷是否正確 輸出新答案或維持一樣
                最後輸出json格式答案
                json格式範例： 
                {
                "number": “題號”,
                "answer": "答案 如果有選項 只要選項字母即可"
                }
                """
}
def answer(question):
    messages = []
    
        # 添加用戶輸入到 messages 中
    messages.append({"role": "user", 
                    "content": question
                    })  
    messages.append(init_answer)
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