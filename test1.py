import base64
import requests
import json
from dotenv import load_dotenv
import os
import re
load_dotenv()
def str_code(response):
    string = re.search(r'```(.*?)```', response, re.DOTALL)
    if string:
        code = string.group(0)
        code = code.replace('\n','')  
    else:
        print("未找到內容")
    return code

API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"
api_version = "2024-09-01-preview"
headers = {  
    "Content-Type": "application/json",  
    "api-key": API_KEY,  
} 

url = RESOURCE_ENDPOINT+"/openai/deployments/"+deployment_name+"/chat/completions?api-version="+api_version
messages = []

messages.append({"role": "user","content": "hello"})
payload = {  
    "messages": messages,
    "temperature": 0.7,  
    "top_p": 0.95,  
    "max_tokens": 800
}
response = requests.post(url, headers=headers, data=json.dumps(payload))  

if response.status_code == 200:  
    response_data = response.json()  
    reply = response_data['choices'][0]['message']['content']
    print(reply)
else:
    print(response)