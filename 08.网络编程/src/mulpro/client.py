#!/usr/bin/python3

from socket import *

# 服务器的ip地址
address='127.0.0.1'   
# 服务器的端口号
port=9999           
# 接收数据的缓存大小
buffsize=1024   

def main():     
	s = socket(AF_INET, SOCK_STREAM)
	s.connect((address,port))
	while True:
		senddata = input('想要发送的数据：')
		if senddata == 'exit':
			break
		else:
			s.send(senddata.encode())
			recvdata=s.recv(buffsize).decode('utf-8')
			print(recvdata)
		
	s.close()

if __name__ == "__main__":
    main()