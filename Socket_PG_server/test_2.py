import asyncio

async def tcp_echo_client(nickname, loop):
    reader, writer = await asyncio.open_connection('localhost', 8000)

    print(f'Send: {nickname!r}')
    writer.write(nickname.encode())

    while True:
        message = input("Enter your message: ")
        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        print(f'Received: {data.decode()!r}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    nickname = input("Enter your nickname: ")
    loop.run_until_complete(tcp_echo_client(nickname, loop))
