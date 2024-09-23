import base64
import key
import requests
import json
API_KEY = key.API_KEY
headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
} 
ENDPOINT = "https://hsh2024.openai.azure.com/openai/deployments/gpt4o/chat/completions?api-version=2024-02-15-preview"  
init = {
    "role": "system",
    "content":  """
                根據題目敘述回答答案 答案格式 ： 第number題answer /n number是題號 answer是答案 ABCD即可 不用括弧 
                """
}
def gpt4o(question):
    messages = []
    messages.append(init)
        # 添加用戶輸入到 messages 中
    messages.append({"role": "user", 
                    "content": question
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