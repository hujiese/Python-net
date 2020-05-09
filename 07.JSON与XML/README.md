<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [JSON 与 XML](#json-%E4%B8%8E-xml)
    - [1、JSON](#1json)
    - [2、XML](#2xml)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# JSON 与 XML

参考：[Python3 JSON 数据解析](https://www.runoob.com/python3/python3-json.html)  [Python3 XML 解析](https://www.runoob.com/python3/python3-xml-processing.html)

### 1、JSON

JSON (JavaScript Object Notation) 是一种轻量级的数据交换格式。它基于ECMAScript的一个子集。

Python3 中可以使用 json 模块来对 JSON 数据进行编解码，它包含了两个函数：

- **json.dumps():** 对数据进行编码
- **json.loads():** 对数据进行解码

使用起来非常简单，代码见src/js.py：

```python
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
```

输出结果如下：

```
Python 原始数据： {'name': 'jack', 'no': 1, 'age': 30}
JSON 对象： {"name": "jack", "no": 1, "age": 30}
data2['name']:  jack
data2['age']:  30
```

### 2、XML

文件对象模型（Document Object Model，简称DOM），是W3C组织推荐的处理可扩展置标语言的标准编程接口。一个 DOM 的解析器在解析一个 XML 文档时，一次性读取整个文档，把文档中所有元素保存在内存中的一个树结构里，之后你可以利用DOM 提供的不同的函数来读取或修改文档的内容和结构，也可以把修改过的内容写入xml文件。

python中用xml.dom.minidom来解析xml文件，现有xml如下 src/xml/movies.xml：

```xml
<collection shelf="New Arrivals">
	<movie title="Enemy Behind">
	   <type>War, Thriller</type>
	   <format>DVD</format>
	   <year>2003</year>
	   <rating>PG</rating>
	   <stars>10</stars>
	   <description>Talk about a US-Japan war</description>
	</movie>
	<movie title="Transformers">
	   <type>Anime, Science Fiction</type>
	   <format>DVD</format>
	   <year>1989</year>
	   <rating>R</rating>
	   <stars>8</stars>
	   <description>A schientific fiction</description>
	</movie>
	   <movie title="Trigun">
	   <type>Anime, Action</type>
	   <format>DVD</format>
	   <episodes>4</episodes>
	   <rating>PG</rating>
	   <stars>10</stars>
	   <description>Vash the Stampede!</description>
	</movie>
</collection>
```

采用dom解析该xml源码如下src/xml/xl.py：

```python
#!/usr/bin/python3

from xml.dom.minidom import parse
import xml.dom.minidom

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("movies.xml")
# 获取根元素
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
   print ("Root element : %s" % collection.getAttribute("shelf"))

# 在集合中获取所有电影
movies = collection.getElementsByTagName("movie")

# 打印每部电影的详细信息
for movie in movies:
   print ("*****Movie*****")
   if movie.hasAttribute("title"):
      print ("Title: %s" % movie.getAttribute("title"))

   type = movie.getElementsByTagName('type')[0]
   print ("Type: %s" % type.childNodes[0].data)
   format = movie.getElementsByTagName('format')[0]
   print ("Format: %s" % format.childNodes[0].data)
   rating = movie.getElementsByTagName('rating')[0]
   print ("Rating: %s" % rating.childNodes[0].data)
   description = movie.getElementsByTagName('description')[0]
   print ("Description: %s" % description.childNodes[0].data)
```

输出如下：

```
Root element : New Arrivals
*****Movie*****
Title: Enemy Behind
Type: War, Thriller
Format: DVD
Rating: PG
Description: Talk about a US-Japan war
*****Movie*****
Title: Transformers
Type: Anime, Science Fiction
Format: DVD
Rating: R
Description: A schientific fiction
*****Movie*****
Title: Trigun
Type: Anime, Action
Format: DVD
Rating: PG
Description: Vash the Stampede!
```

