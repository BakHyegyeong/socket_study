import asyncio

clients = {} #dictionary 형태로 선언, 나중에 nickname : writer 객체 형태가 될 것.
server = None

async def handle_client(reader,writer): # 인자로 자동으로 reader,wirter이 생성

    data = await reader.read(1024)
    nickname = data.decode().strip()    # 처음에 온 데이터는 nickname
    clients[nickname] = writer  # nickname : writer 형태로 dictionary안에 저장
    await broadcast_message("{} joined the chat!".format(nickname))

    while True:
        try :
            #print("여기 들어오긴 하니?")
            #data = await asyncio.wait_for(reader.read(1024),timeout=10)
            data = await reader.read(1024)
            # print("메시지를 수신했습니다.")
            message = data.decode().strip()   #strip은 공백문자를 제거하는 메서드
            # print("메시지 변환")
            if message:
                # print("메시지를 client에게 전송하고자 합니다.")
                await broadcast_message("{}:{} ".format(nickname,message))
            else :
                raise EOFError

        except EOFError :
            del clients[nickname]
            await broadcast_message(f"{nickname} left the chat.")
            break

        except ConnectionResetError:
            del clients[nickname]
            await broadcast_message(f"{nickname} left the chat.")
            break

        except Exception as e:
            print(f"Error broadcasting message: {e}")


async def broadcast_message(message):
    print(message)

    for client in clients.values() :
        try :
            client.write((message + '\n').encode())  # 각 client들에게 message를 보내는 과정
            # 개행문자는 메시지들이 전송되는 과정에서 각 메시지를 새로운 줄에서 시작하게 하는 역할.
            await client.drain()
            print("client들에게 메시지 전송 완료!")

        except Exception as e:
            print(f"error : {e}")

async def start_server(host,port):
    server = await asyncio.start_server(handle_client,host,port)
    # client의 연결을 수락할 때마다 새로운 핸들러(코루틴)이 생성됨.
    # 이 핸들러는 스레드, 프로세스도 될 수 있음.
    # 각 핸들러는 client와의 통신을 독립적으로 관리, 요청과 응답을 처리

if __name__ == "__main__" :
    loop = asyncio.get_event_loop()
    print("server start")

    try :
        loop.run_until_complete(start_server('0.0.0.0',8000))
        loop.run_forever()  # 이벤트 루프를 시작하고 계속 실행하는 역할.

    except KeyboardInterrupt:
        print("Shutting down server")