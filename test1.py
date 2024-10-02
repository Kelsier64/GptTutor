import json

# 字串
s = "[2,3,4]"

# 將字串轉換為列表
lst = json.loads(s)

# 輸出結果
print(lst)  # [2, 3, 4]
