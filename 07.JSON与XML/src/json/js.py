#!/usr/bin/python3
 
import json
 
data = {
    'no' : 1,
    'name' : 'jack',
    'age' : 30
}

# Python 字典类型转换为 JSON 对象
json_str = json.dumps(data)
print ("Python 原始数据：", repr(data)) # Python 原始数据： {'name': 'jack', 'no': 1, 'age': 30}
print ("JSON 对象：", json_str) # JSON 对象： {"name": "jack", "no": 1, "age": 30}
 
# 将 JSON 对象转换为 Python 字典
data2 = json.loads(json_str)
print ("data2['name']: ", data2['name']) # data2['name']:  jack
print ("data2['age']: ", data2['age']) # data2['age']:  30