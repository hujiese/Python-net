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