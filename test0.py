import re
import json
res = '''
```json
{
    "title": "Initial Problem Analysis",
    "content": "To approach this problem effectively, I'll first break down the given information into key components. This involves identifying...[detailed explanation]... By structuring the problem this way, we can systematically address each aspect.",
    "next_action": "continue"
}```
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
    string = re.search(r'\{(.*)\}', response, re.DOTALL)
    if string:
        code = string.group(0)  
    else:
        print("未找到內容")
    return code

ans_json = res
print(ans_json)
deta = json.loads(ans_json)
print(deta)