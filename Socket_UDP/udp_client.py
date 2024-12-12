from socket import *
serverName = 'hostName'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

# 메시지 전송
message = "test socket"
clientSocket.sendto(message.encode(), (serverName,serverPort))

# 서버에서 온 메시지를 읽고 socket 닫음
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
modifiedMessage.decode()
clientSocket.close()