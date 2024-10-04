import base64
import requests
import json
import cv2
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"
api_version = "2024-09-01-preview"
headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
}
endpoint_url = RESOURCE_ENDPOINT+"/openai/deployments/"+deployment_name+"/chat/completions?api-version="+api_version

init_img2text = {
    "role": "user",
    "content":  
    """
    我們要輔助沒有視覺的學生寫題目
    所以幫我把題目圖片轉成文字
    題目分成文字敘述跟圖兩個部分或是只有文字
    假如有圖片 處理完文字後 要分析圖片 寫下對題目有用的內容 且盡量詳細
    分析完成題目後 把你的計算過程填入下面的json格式範例 
    
    Json格式:
    {
    "number": “題號”,
    "text": "題目內容 請跟原文一模一樣",
    "image_description": "如果有圖片，請輸入圖片描述，否則為 null，這部分是輔助盲人學生判斷題目的重點，所以假如有，要盡可能詳盡",
    "options": “如果有選項，請輸入圖片描述，否則為 null”,
    "idea":"你的思考過程，請把剛剛所有分析填入這裡",
    "answer":"最後的答案"
    }
    全部內容要能讓學生判斷並完成題目 並在最後輸出內含json的list比如[{question1},{question2}] 注意，就算只有一個json也要用list格式
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
        "temperature": 0.4,  
        "top_p": 0.95,  
        "max_tokens": 2000  
    }
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))  
    if response.status_code == 200:  
        response_data = response.json()  
        reply = response_data['choices'][0]['message']['content']
        return reply
    return "error"

init_answer = {
    "role": "user",
    "content":  """            
                以下是一個學生寫的題目 以及他的計算過程 請判斷是否正確 答案可以是維持一樣或是新的

                並在最後輸出內含json的list比如[{question1},{question2}]
                Json格式範例： 
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
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))  
    if response.status_code == 200:  
        response_data = response.json()  
        reply = response_data['choices'][0]['message']['content']
        return reply
    return "error"
