import websockets, asyncio

client_list = {}


async def broadcast(message):
    for client in client_list:
        await client.send(message)


async def handler(websocket):
    username = await websocket.recv()

    client_list[websocket] = username

    print(f"{username} joined the chat")

    try:
        async for message in websocket:
            print(f"{username}: {message}")

            await broadcast(f"{username}: {message}")

    finally:
        del client_list[websocket]
        print(f"{username} left the chat")


async def main():
    async with websockets.serve(handler, "localhost", 8000):
        print("Server started...")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
