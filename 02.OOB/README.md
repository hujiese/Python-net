[TOC]

# 面向对象

有过C++或者java编程经验的程序员都知道面向对象，面向的对象就是class，python也支持class。一个class一般由构造函数、成员变量和成员函数构成，而成员变量和函数又有共有和私有之分。

### 1、定义一个类

在src/demo1中有一个people.py，里面定义了一个person类，该文件内容如下：

```python
#!/usr/bin/python3

#类定义
class person:
	#定义基本属性
	weight = 0
	#定义私有属性,私有属性在类外部无法直接进行访问
	__name = ''
	__age = 0
	#定义构造函数
	def __init__(self,n,a,w):
		self.weight = w
		self.__name = n
		self.__age = a
		
	def setName(self, name):
		self.__name = name
		
	def getName(self):
		return self.__name
		
	def setAge(self, age):
		self.__age = age;
		
	def getAge(self):
		return self.__age
		
	def __private(self):
		print("私有方法，外部不可访问")
		
	def call_private_func(self):
		print("间接调用私有方法")
		self.__private()
		
	# 定义普通成员函数，可以被外部调用
	def speak(self):
		print("%s 说: 我 %d 岁。" %(self.__name,self.__age))

```

在分析该类之前需要知道，Python并没有真正的私有化支持，但可用下划线得到伪私有，尽量避免定义以下划线开头的变量：
  （1）_xxx    "**单下划线** " 开始的成员变量叫做保护**变量**，意思是只有类对象（即类实例）和子类对象自己能访问到这些变量，需通过类提供的接口进行访问；不能用'from module import *'导入，这个有点像C++里的**protected**关键字。
  （2）\_\_xxx  类中的**私有变量/方法名** （Python的函数也是对象，所以成员方法称为成员变量也行得通。）," **双下划线** " 开始的是私有成员，意思是只有类对象自己能访问，连子类对象也不能访问到这个数据，有点像**private**关键字。
  （3）\_\_xxx__ 系统定义名字，**前后均有一个“双下划线”** 代表python里特殊方法专用的标识，如 __init__() 代表类的构造函数。

**该类是非常“制式”的模板，定义一个class时需要注意下面几点：**

* **class 通过__(双下划线)**来区分成员变量和函数是否可以被外界调用，例如，\_\_private()函数前加了双下划线，表示该函数只能在class的内部调用，类似于C++或者java里被private修饰。
* 对于变量，可以使用单下划线来修饰，表示protected；双下划线表示private。
* **成员函数如果要修饰为private属性，一定要使用双下划线，使用单下划线修饰成员函数是没有任何作用的。**
* 所有的函数，不管是构造函数还是成员函数，**函数的第一个参数一定要是self**。当然 ，**self** 的名字并不是规定死的，也可以使用 **this**，但是最好还是按照约定是用 **self**。
* 在class内部对成员变量操作时，需要通过**self.**来引用，例如 **self.__age。**

 下面看看测试代码，测试代码在src/demo1/test.py里，代码内容如下：

```python
#!/usr/bin/python3

from people import person

# 测试构造函数
p = person('jack', 25, 115)
p.speak() # jack 说: 我 25 岁。

# 测试私有方法
# p.__private() # error !
p.call_private_func() # 间接调用私有方法 \n 私有方法，外部不可访问

# 测试成员函数
p.setName('Mary')
p.setAge(23)

# 测试修改成员变量
p.weight = 100

print(p.getName()) # Mary
print(p.getAge()) # 23
print(p.weight) # 100
```

测试结果如下：

```
jack 说: 我 25 岁。
间接调用私有方法
私有方法，外部不可访问
Mary
23
100
```

### 2、继承

为了方便演示，这里构建一个base类，该类在src/demo2/base.py中，代码如下所示：

```python
#!/usr/bin/python3

class father:
	def __init__(self, name, age, id, info):
		self._name = name
		self._age = age
		self.__id = id
		self.info = info
		
	def __private(self):
		print("私有方法，外部不可访问")
		
	def print(self):
		print("father %s 说: 我 %d 岁了。" %(self._name,self._age))
		
	def foobar(self):
		print("foo bar ... ")
```

接下来具体分析下，这个类为什么要这样设计。

首先是构造函数，init函数中的\_name和\_age设置为protected，\_\_id设置为private，info设置为public，这几个变量在后面子类中会测试用于验证访问权限。

\_\_private函数设置为private，子类无法访问。

print函数在后面的子类中会被子类重写。

foobar的出现是为了验证继承，子类可以调用该方法。

下面开始分析子类，该子类于src/demo2/extends.py中：

```python
from base import father

class son(father):
	def __init__(self, name, age, id, info, grade):
	    # 调用父类构造函数
		father.__init__(self, name, age, id, info)
		self.grade = grade
		
	def test_private(self):
		print(self._name)
		print(self._age)
		# print(self.__id) # 父类私有变量不可调用
		print(self.info)
		print(self.grade)
		# self.__private() # 父类私有方法不可调用
		
	# 重写父类方法
	def print(self):
		print("son %s 说: 我 %d 岁了。" %(self._name,self._age))	
```

python通过该方法来继承一个父类：

```python
class son(father):
```

该子类的构造函数中调用了父类的构造函数，test_private函数测试父类变量的访问权限，其中**双下划线修饰的private变量子类也无法访问**。print函数重写了父类方法。

下面就是测试案例了，测试案例位于src/demo2/test.py中，代码如下：

```python
#!/usr/bin/python3
from extends import son

if __name__ == '__main__':
	s = son('jack', 20, 10010, 'student', 96)
	s.test_private() # jack \n 20 \n student \n 96
	s.print() # son jack 说: 我 20 岁了。
	# 测试父类方法
	s.foobar() # foo bar ...
```

测试结果如下：

```
jack
20
student
96
son jack 说: 我 20 岁了。
foo bar ... 
```

### 3、多态

多态这种特性，有过C++或者JAVA编程经验的程序员都知道，Python也支持多态。测试代码可见src/demo2/test2.py，代码如下：

```python
#!/usr/bin/python3
from extends import son
from base import father

def print(father):
	father.print()
	
if __name__ == '__main__':
	f = father('jack', 50, 50050, 'boss')
	s = son('jackson', 20, 10010, 'student', 96)
	
	print(f) # father jack 说: 我 50 岁了。
	print(s) # son jackson 说: 我 20 岁了。
	
	f = s
	f.print() # son jackson 说: 我 20 岁了。
```

测试结果如下：

```
father jack 说: 我 50 岁了。
son jackson 说: 我 20 岁了。
son jackson 说: 我 20 岁了。
```

### 4、类型信息

要了解一个对象是什么类型、继承于哪个类、有哪些属性和方法，可以通过下面这一组函数来完成：

```python
type() # 判断对象类型
isinstance() # 判断class的继承类型
dir() # 获得一个对象的所有属性和方法
```

测试案例于src/demo2/test3.py中，测试代码如下所示：

```python
#!/usr/bin/python3
from extends import son
from base import father
	
if __name__ == '__main__':
	f = father('jack', 50, 50050, 'boss')
	s = son('jackson', 20, 10010, 'student', 96)
	
	print(type(f)) # <class 'base.father'>
	print(type(s)) # <class 'extends.son'>
	
	print(isinstance(s, father)) # True
	
	print(dir(f))
	'''['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_age', '_father__id', '_father__private', '_name', 'foobar', 'info', 'print']
	'''
	print(dir(s))
	'''
	['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_age', '_father__id', '_father__private', '_name', 'foobar', 'grade', 'info', 'print', 'test_private']
	'''
```

打印结果如下：

```
<class 'base.father'>
<class 'extends.son'>
True
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_age', '_father__id', '_father__private', '_name', 'foobar', 'info', 'print']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_age', '_father__id', '_father__private', '_name', 'foobar', 'grade', 'info', 'print', 'test_private']
```

