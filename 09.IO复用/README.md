<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [IO 复用](#io-%E5%A4%8D%E7%94%A8)
    - [1、select](#1select)
    - [2、epoll](#2epoll)
    - [3、selectors](#3selectors)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# IO 复用

参考 [python之IO多路复用](https://www.cnblogs.com/clschao/articles/9713797.html) [python--selectors模块](https://www.cnblogs.com/clschao/articles/9718463.html)

### 1、select

python中也提供了select接口，直接上代码src/select_server.py：

```python
#!/usr/bin/env python3

from socket import *
import select

ADDR = '127.0.0.1'
PORT = 8096

def main():
	# 创建监听套接字
	server = socket(AF_INET, SOCK_STREAM)
	# 设置监听套接字为非阻塞
	server.setblocking(False)
	# 设置地址复用
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	# 绑定地址和端口
	server.bind((ADDR, PORT))
	# 监听
	server.listen(5)

	# read_fds 存放所有read事件发生的文件描述符，初始化将服务端socket对象加入监听列表
	read_fds=[server,]

	print('启动服务...')

	while True:
		# 启用select，如果监听套接字集合中有事件发生则返回，超时时间为1s，返回发生读、写和错误的文件描述符集合
		rfds, wfds, efds = select.select(read_fds, [], [], 1)
		# 遍历rfds，处理集合中套接字的“读事件”
		for sock in rfds:
			# socket 监听套接字上发生了读事件, 说明有客户端连接
			if sock == server:
				# accept 客户端的连接, 获取客户端套接字和地址
				conn, addr = sock.accept()
				print('client ', addr, ' connected ...')
				# 把新的客户端连接加入到“读事件”监听列表中，监听该客户端套接字上的“读事件”
				read_fds.append(conn)
			else:
				# 客户端套接字上有“读事件”发生，处理该客户端事件
				try:
					data = sock.recv(1024).decode('utf-8') # 读取客户端发来的数据
					peer = sock.getpeername()
					# read返回0，说明客户端关闭连接，将该客户端从监听列表中移除
					if not data:
						print('client ', peer, ' off line ...')
						sock.close()  # 关闭该套接字，释放资源
						read_fds.remove(sock)
						continue # 继续处理下一个套接字事件
					print('receive from ', peer, ' ,data is ', data)
					# 将消息回射给客户端
					sock.send(data.encode('utf-8'))
				#如果这个连接出错了，客户端暴力断开了（注意，我还没有接收他的消息，或者接收他的消息的过程中出错了）
				except Exception:
					print('Exception.......')
					# 关闭该连接
					sock.close()
					# 直接移除
					read_fds.remove(sock)
					
if __name__ == "__main__":
    main()
```

为了方便，这里的客户端使用了nc工具，测试结果如下：

![](./img/select.jpg)

### 2、epoll

同样地，直接上代码src/epoll_server.py：

```python
#!/usr/bin/env python3

import select  
import socket    

ADDR = '127.0.0.1'
PORT = 8096

def main():
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	# socket默认是阻塞的，需要开启非阻塞模式。  
	serversocket.setblocking(False)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind((ADDR, PORT))  
	serversocket.listen(5)

	# 创建一个epoll对象  
	epoll = select.epoll()  
	# 在监听套接字上面注册对“读事件”的关注，监听套接字发生读事件说明有客户端连接到来 
	epoll.register(serversocket.fileno(), select.EPOLLIN)  

	try:  
		# 字典conns映射文件描述符（整数）到其相应的网络连接对象  
		conns = {}  
		while True:  
			# 调用poll，超时时间为1s  
			events = epoll.poll(1)  
			# event作为一个序列（fileno，event）的元组返回  
			for fileno, event in events:  
				# 监听套接字上有连接到来 
				if fileno == serversocket.fileno():  
					conn, addr = serversocket.accept()  
					print('client ', addr, ' connected ...')
					# 设置新的socket为非阻塞模式  
					conn.setblocking(False)  
					# 为新的socket注册对读（EPOLLIN）event的关注  
					epoll.register(conn.fileno(), select.EPOLLIN)  
					conns[conn.fileno()] = conn  
				# 如果客户端连接套接字发生一个读event，直接读取数据并回射回去 
				elif event & select.EPOLLIN:  
					# 接收客户端发送过来的数据  
					data = conns[fileno].recv(1024).decode('utf-8') 
					peer = conns[fileno].getpeername()
					# 如果客户端退出,关闭客户端连接，取消所有的读和写监听  
					if not data:  
						print('client ', peer, ' off line ...')
						conns[fileno].close()  
						# 删除conns字典中的监听对象  
						del conns[fileno]  
						epoll.unregister(fileno)  
					else:  
						print('receive from ', peer, ' ,data is ', data)
				# HUP（挂起）event表明客户端socket已经断开（即关闭），所以服务端也需要关闭。  
				# 没有必要注册对HUP event的关注。在socket上面，它们总是会被epoll对象注册  
				elif event & select.EPOLLHUP:  
					# 注销对此socket连接的关注  
					epoll.unregister(fileno)  
					# 关闭socket连接  
					conns[fileno].close()  
					del conns[fileno]  
					peer = conns[fileno].getpeername()
					print('client ', peer, ' off line ...')
	finally:  
		# 打开的socket连接不需要关闭，因为Python会在程序结束的时候关闭。
		epoll.unregister(serversocket.fileno())  
		epoll.close()  
		serversocket.close()  
		
if __name__ == "__main__":
    main()
```

测试结果如下：

![](./img/epoll.jpg)

### 3、selectors

函数参数介绍来源 [python--selectors模块](https://www.cnblogs.com/clschao/articles/9718463.html)

前面介绍的IO多路复用模型在不同的平台有着不同的支持，而epoll在windows下就不支持，selectors解决了这个问题，程序员只需要填写监听对象，然后处理消息事件，但具体如何监听的，选择的是select还是epoll，全部交给selector。更多内容查看 python文档：https://docs.python.org/3/library/selectors.html

该模块定义了一个 BaseSelector的抽象基类， 以及它的子类，包括：SelectSelector， PollSelector,，EpollSelector，DevpollSelector，KqueueSelector.。除此之外外还有一个DefaultSelector类，它其实是以上其中一个子类的别名而已，它自动选择为当前环境中最有效的Selector，所以通常使用 DefaultSelector类就可以了，其它类用不到。

 **该模块定义了两个常量，用于描述 event Mask**

> EVENT_READ ：   表示可读的，值为1；
>
> EVENT_WRITE：   表示可写的，值为2；

 **模块定义了一个 SelectorKey类， 一般用这个类的实例 来描述一个已经注册的文件对象的状态， 这个类的几个属性常用到：**

> fileobj：  表示已经注册的文件对象；
>
> fd:     表示文件对象的描述符，是一个整数，它是文件对象的 fileno()方法的返回值；
>
> events:  表示注册一个文件对象时，关注的事件类型,  即上面的event Mask
>
> data:    表示注册一个文件对象是邦定的data；

 **最后说说抽象基类中的方法：**

> register(fileobj, events, data=None)   
>
> 　　作用：注册一个文件对象。
>
> 　　参数： fileobj——即可以是fd 也可以是一个拥有fileno()方法的对象； 
>
> 　　events——上面的event Mask 常量； data
>
> 　　返回值： 一个SelectorKey类的实例；
>
> 
>
> unregister(fileobj)             
>
> 　　作用： 注销一个已经注册过的文件对象；   
>
> 　　返回值：一个SelectorKey类的实例；
>
>  
>
> modify(fileobj, events, data=None)  
>
> 　　作用：用于修改一个注册过的文件对象，比如从监听可读变为监听可写；它其实就是register() 后再跟unregister(),    但是使用modify( ) 更高效；
>
> 　　返回值：一个SelectorKey类的实例；
>
>  
>
> select(timeout=None)          
>
> 　　作用： 用于选择满足我们监听的event的文件对象；
>
> 　　返回值： 是一个(key, events)的元组， 其中key是一个SelectorKey类的实例， 而events 就是 event Mask（EVENT_READ或EVENT_WRITE,或者二者的组合)
>
>  
>
> close()                  
>
> 　　 作用：关闭 selector。 最后一定要记得调用它， 要确保所有的资源被释放；
>
>  
>
> get_key(fileobj)             
>
> 　　作用： 返回注册文件对象的 key；
>
> 　　返回值 ：一个SelectorKey类的实例；

有了前面的基础后，直接上代码src/selector.py：

```python
#!/usr/bin/env python3

from socket import *
import selectors

ADDR = '127.0.0.1'
PORT = 8096

def read(conn, sel):
	try:
		data = conn.recv(1024).decode('utf-8') 
		peer = conn.getpeername()
		if not data:
			print('client ', peer, ' off line ...')
			sel.unregister(conn)
			conn.close()
			return
		print('receive from ', peer, ' ,data is ', data)
		conn.send(data.encode('utf-8'))
	except Exception:
		print('Exception...')
		sel.unregister(conn)
		conn.close()
		
def accept(server, sel):
	conn, addr=server.accept()
	sel.register(conn, selectors.EVENT_READ, read)
	print('client ', addr, ' connected ...')

def main():
	server = socket(AF_INET, SOCK_STREAM)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	server.setblocking(False)
	server.bind((ADDR, PORT))
	server.listen(5)

	sel=selectors.DefaultSelector()
	# 关注监听套接字的“读事件”，处理函数为accept
	sel.register(server, selectors.EVENT_READ, accept) 

	while True:
		events = sel.select() #检测所有的fileobj，是否有完成wait data的
		'''
		fileobj：    表示已经注册的文件对象；
		fd:          表示文件对象的描述符，是一个整数，它是文件对象的 fileno()方法的返回值；
		events:      表示注册一个文件对象时，关注事件的类型, event mask :
																EVENT_READ ：表示可读的，值其实是1
																EVENT_WRITE：表示可写的，值其实是2
		data:        表示注册一个文件对象是邦定的data；
		'''
		for sel_obj, mask in events:
			# 获取事件处理函数，例如，server监听套接字为accept
			callback = sel_obj.data 
			# 调用事件处理函数
			callback(sel_obj.fileobj, sel)

if __name__ == "__main__":
    main()
```

运行结果如下：

![](./img/selector.jpg)