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