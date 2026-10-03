import websockets, asyncio


async def receive_message(websocket):
    async for message in websocket:
        print(f"\nServer: {message}")


async def send_message(websocket):
    while True:
        message = await asyncio.to_thread(
            input, "Enter message: "
        )

        if message == "exit":
            break

        await websocket.send(message)


async def main():
    async with websockets.connect("ws://localhost:8000") as websocket:

        username = await asyncio.to_thread(
            input, "Enter username: "
        )

        await websocket.send(username)

        receive_task = asyncio.create_task(
            receive_message(websocket)
        )

        await send_message(websocket)

        receive_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())