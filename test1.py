import base64
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
} 
ENDPOINT = "https://hsh2024.openai.azure.com/openai/deployments/gpt4o/chat/completions?api-version=2024-02-15-preview"  
messages = []
    
        # 添加用戶輸入到 messages 中
messages.append({"role": "user", 
                "content": "hello"
                })  
payload = {  
    "messages": messages,
    "temperature": 0.7,  
    "top_p": 0.95,  
    "max_tokens": 800  
}
response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))  
print(API_KEY)
print(response)
if response.status_code == 200:  
    response_data = response.json()  
    reply = response_data['choices'][0]['message']['content']
    print(reply)