import asyncio
import time

import websockets
import json


class Paddle:
    def __init__(self, loc, websocket):
        self.loc = loc
        self.y = 50
        self.moving = 0
        self.websocket = websocket

    async def move(self, delta_time, speed=50):
        # self.moving = float(self.moving)
        self.y += self.moving * speed * delta_time
        if self.y > 80:
            self.y = 80
        elif self.y < 0:
            self.y = 0
        print(self.moving)
        if self.moving != 0:
            try:
                print("send y = " + str(len(connected_clients.items())))
                for websocket, paddle in connected_clients.items():
                    await websocket.send(json.dumps({'y': self.y, 'loc': self.loc}))
            except websockets.exceptions.ConnectionClosed:
                pass


class Response:
    @staticmethod
    def handle_response(message, websocket):
        obj = json.loads(message)
        if obj['type'] == 'move':
            print("move " + str(obj['data']))
            paddle = connected_clients.get(websocket)
            if paddle:
                paddle.moving = int(obj['data'])


# Set of connected clients
connected_clients = {}

last_time = time.time()


# Function to handle each client connection
async def handle_client(websocket):
    loc = "left" if len(connected_clients) == 0 else "right"
    paddle = Paddle(loc, websocket)
    # Add the new client and its associated paddle to the set
    connected_clients[websocket] = paddle
    try:
        # Listen for messages from the client
        async for message in websocket:
            Response.handle_response(message, websocket)
            # Broadcast the message to all other connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Remove the client from the set of connected clients
        del connected_clients[websocket]


# Main function to start the WebSocket server
async def main():
    global last_time

    server = await websockets.serve(handle_client, 'localhost', 12345)

    while True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        for websocket, paddle in connected_clients.items():
            await paddle.move(delta_time)

        await asyncio.sleep(1 / 60)

    await server.wait_closed()


# Run the server
if __name__ == "__main__":
    asyncio.run(main())
