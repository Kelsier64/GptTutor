import openai
import os
import re
import requests
import sys
from num2words import num2words
import pandas as pd
import numpy as np
import tiktoken
from dotenv import load_dotenv
import os
from openai import AzureOpenAI
load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-09-01-preview",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

# 定義系統消息和用戶輸入
system_message = "我是一個熱愛徒步旅行的助手，幫助人們發現附近的徒步路線。"
user_input = "hello"

# 發送請求到 Azure OpenAI 模型
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ],
    temperature=0.7,
    max_tokens=400
)

# 獲取並打印生成的文本
generated_text = response.choices[0].message.content
print("回應: " + generated_text)