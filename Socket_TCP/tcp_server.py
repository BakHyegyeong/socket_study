from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind("",serverPort)

# 대기상태
serverSocket.listen(1)

while True:
	# 요청수락
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024).decode()
    connectionSocket.send(message.encode())
    connectionSocket.close()