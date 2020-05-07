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