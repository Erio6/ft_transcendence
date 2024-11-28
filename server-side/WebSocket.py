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
        if loc == "left":
            self.x = 5
        elif loc == "right":
            self.x = 95

    async def move(self, delta_time, speed=50):
        # self.moving = float(self.moving)
        self.y += self.moving * speed * delta_time
        if self.y > 80:
            self.y = 80
        elif self.y < 0:
            self.y = 0
        if self.moving != 0:
            try:
                print("send y = " + str(len(connected_clients.items())))
                for websocket, paddle in connected_clients.items():
                    await websocket.send(json.dumps({'type': 'paddle', 'y': self.y, 'loc': self.loc}))
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


class Ball:
    def __init__(self):
        self.min_speed = 0.5
        self.current_speed = 50
        self.radius = 0.1
        self.x = 50
        self.y = 0
        self.v_x = 0
        self.v_y = 1

    async def init_ball(self):
        for websocket, paddle in connected_clients.items():
            await websocket.send(json.dumps({'type': 'init_ball', 'y': self.y, 'loc': self.loc}))

    async def move(self, delta_time):
        self.x += self.v_x * delta_time * self.current_speed
        self.y += self.v_y * delta_time * self.current_speed
        for websocket, paddle in connected_clients.items():
            await websocket.send(json.dumps({'type': 'ball', 'x': self.x, 'y': self.y}))

    def wall_collide(self):
        print(self.y)
        if self.y < 0 or self.y + self.radius > 100:
            self.v_y *= -1

    def paddles_collide(self, paddle_left, paddle_right):
        if self.x - self.radius <= paddle_left.x and paddle_left.y <= self.y <= paddle_left.y + 10:
            self.v_x *= -1

        if self.x + self.radius >= paddle_right.x and paddle_right.y <= self.y <= paddle_right.y + 10:
            self.v_x *= -1


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

ball = Ball()


async def main():
    global last_time

    server = await websockets.serve(handle_client, 'localhost', 12345)

    while True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        for websocket, paddle in connected_clients.items():
            await paddle.move(delta_time)
        ball.wall_collide()
        await ball.move(delta_time)
        await asyncio.sleep(1 / 60)

    await server.wait_closed()


# Run the server
if __name__ == "__main__":
    asyncio.run(main())
