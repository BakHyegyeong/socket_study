from socket import *
serverName = 'serverName'
serverPort = 12000
message = "happy"
clientSocket = socket(AF_INET, SOCK_STREAM)

# connection 생성
clientSocket.connect(serverName, serverPort)

# 통신과정
clientSocket.send(message.encode())
modifiedMessage = clientSocket.recv(2048)
clientSocket.close()