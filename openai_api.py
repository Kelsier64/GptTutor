import streamlit as st
import openai
import os
import json
import time
import openai
import re
import requests
import base64
from num2words import num2words
import pandas as pd
import numpy as np
import cv2
from dotenv import load_dotenv
from openai import AzureOpenAI
import azure_o1
load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-09-01-preview",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)
def encode_image(img):
    # 將圖像編碼為 JPEG 格式，返回 (retval, buffer)
    retval, buffer = cv2.imencode(".jpg", img)
    # 將編碼後的圖像轉換為 Base64 字符串
    return base64.b64encode(buffer).decode('utf-8')

def api_request(messages, max_tokens):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except:
        return "error"
    
init_img2text = {
    "role": "user",
    "content":  
    """
    我們要輔助沒有視覺的學生寫題目
    所以幫我把題目圖片轉成文字
    題目分成文字敘述跟圖兩個部分或是只有文字
    假如有圖片 處理完文字後 要分析圖片 寫下對題目有用的內容 且盡量詳細
    分析完成題目後 把你的計算過程填入下面的json格式範例 

    Response Format:
    Use JSON with keys:
    "type":(values: 'mono'(單題) or 'multi'(多題-題與題沒關係) or 'assemble'(題組-題與題有關係)),
    "assemble_context":"題組的文本 只有assemble有 其他都"no",
    "questions":[{question1},{question2}],
    "complex":(是否複雜 是否需要推理)(values: 'yes' or 'no')

    question JSON keys:
    "number" (題號), 
    "text" (題目內容 請跟原文一模一樣), 
    "image_description" (如果有圖片，請輸入圖片描述，否則為"no"，這部分是輔助盲人學生判斷題目的重點，所以假如有，要盡可能詳盡),
    "options" (如果有選項，請輸入圖片描述，否則為"no"), 
    "idea" (你的思考過程，請把剛剛所有分析填入這裡), 
    "answer" (最後的答案),
    
    
    Example of a valid JSON response(mono):
    ```json
    {
    "type":"mono",
    "assemble_context":"no",
    "questions":[{"number":"1","text":"1+1=?","image_description":"no","options":"1,2,3,4","idea":"1+1=2","answer":"2"}],
    "complex":"yes"
    }```

    Example of a valid JSON response(multi):
    ```json
    {
    "type":"multi",
    "assemble_context":"no",
    "questions":[{"number":"1","text":"1+1=?","image_description":"no","options":"1,2,3,4","idea":"1+1=2","answer":"2"},{"number":"1","text":"1+1=?","image_description":"no","options":"1,2,3,4","idea":"1+1=2","answer":"2"}],
    "complex":"yes"
    }```

    Example of a valid JSON response(assemble):
    ```json
    {
    "type":"assemble",
    "assemble_context":"題組的文本",
    "questions":[{"number":"1","text":"1+1=?","image_description":"no","options":"1,2,3,4","idea":"1+1=2","answer":"2"},{"number":"1","text":"1+1=?","image_description":"no","options":"1,2,3,4","idea":"1+1=2","answer":"2"}],
    "complex":"yes"
    }```


    全部內容要能讓學生判斷並完成題目
    一定要用"questions":list
    """
}
def img_pattern(img):
    base64_image = encode_image(img)
    messages = [{"role": "user","content": [{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]},
                init_img2text
                ]
    reply = api_request(messages,2000)
    if reply["complex"] == "yes":
        if reply["type"] == "mono":
            text = reply["questions"][0]["text"]
            image_description = reply["questions"][0]["image_description"]
            options = reply["questions"][0]["options"]
            msg = "question:"+text+";image_description:"+image_description+";options:"+options
            print(msg)
            ans = azure_o1.o1_function(msg)
    return ans




def main():
    img = cv2.imread("img/ex0.jpg")
    reply = img_pattern(img)
    print(reply)


if __name__ == "__main__":
    main()