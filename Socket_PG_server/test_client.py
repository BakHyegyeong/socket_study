import asyncio

async def send_message(writer, nickname,close_event):
    while True:
        message = input(f"{nickname}> ")

        if(message == 'exit'):
            close_event.set()

            writer.close()
            break

        writer.write((message + "\n").encode())
        await writer.drain()
        print("서버에게 메시지 전송 완료")


async def receive_message(reader,close_event):
    while not close_event.is_set():
        data = await reader.read(1024)
        print(data.decode().strip())



async def start_client(nickname, loop):
    reader, writer = await asyncio.open_connection('localhost', 8000)

    # Send the nickname to the server
    writer.write((nickname + " ").encode())
    await writer.drain()

    close_event = asyncio.Event()

    # 비동기 작업을 생성
    send_task = asyncio.create_task(send_message(writer, nickname,close_event))
    receive_task = asyncio.create_task(receive_message(reader,close_event))


    # 비동기 작업을 동시에 실행
    await asyncio.gather(send_task, receive_task)

    while True:
        if close_event.is_set():
            print("Closing the connection...")
            send_task.cancel()
            receive_task.cancel()

            try:
                # 비동기 작업이 종료될 때까지 기다림
                await send_task
                await receive_task

            except asyncio.CancelledError:
                pass  # tasks can raise this error when cancelled, which is expected here

            break

        else:
            await asyncio.sleep(1)

            # writer.close()
        # 이게 호출되면 reader도 같이 close됨.
        # asyncio.open_connection() 함수는 읽기와 쓰기를 위한 두 개의 분리된 객체를 반환하지만
        # 이들은 동일한 TCP 연결을 공유합니다. 따라서 한 쪽을 닫으면 다른 쪽도 자동으로 닫힙니다.


if __name__ == "__main__" :
    nickname = input("Enter your nickname: ")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_client(nickname, loop))
