import re
import json
res = '''
klewjqrljlkqwjrklqwejS
```json
[
    {
        "number": "8",
        "text": "已知在ABC中，若△ABC之內切圓分別切三邊BC、CA、AB於A1、B1、C1三點，其中∠B1A1C1=0，如圖(一)中，內切圓O之內切圓 分別切三邊BC、CA、AB於A2、B2、C2三點，其中∠B2A2C2=θ，如圖(二)中，依此規則推演下去，可得一數列，其中n為正整數，則下列選項 何者正θ1+2θ2=180° 為一個等差數列數列的遞迴公式為θn=θn-1 - θn-2，其中n≥2\n(4)所有的頂點A1、B1、C1、A2、B2"

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
data = json.loads(ans_json)
print(data)
print(data[0]["number"])