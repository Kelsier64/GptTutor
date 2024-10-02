import re
import json
res = '''
klewjqrljlkqwjrklqwejS
```json
[
    {
        "number": "1",
        "answer": "需要進一步計算和驗證，暫時無法確定答案。"
    }
]
```
'''

def str_code(response):
    string = re.search(r'```(.*?)```', response, re.DOTALL)
    if string:
        code = string.group(0)
        code = code.replace('\n', '')  
    else:
        print("未找到內容")
    return code

def json_code(response):
    string = re.search(r'\[(.*)\]', response, re.DOTALL)
    if string:
        code = string.group(0)  
    else:
        print("未找到內容")
    return code

ans_json = json_code(str_code(res))
print(ans_json)
deta = json.loads(ans_json)
text = "第"+ deta[0]["number"] + "題" + deta[0]["answer"]
print(text)