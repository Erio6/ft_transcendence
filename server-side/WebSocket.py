import asyncio
import time
from importlib.metadata import pass_none

import websockets
import json


class Paddle:
    def __init__(self, loc, websocket):
        self.loc = loc
        self.y = 50
        self.moving = 0
        self.websocket = websocket
        self.length = 25
        self.width = 3.5
        self.speed = 100
        self.x = 2

    async def send_data(self, websocket):
        await websocket.send(json.dumps({'type': 'paddle', 'y': self.y, 'size': self.length, 'loc': self.loc}))

    async def init_paddle(self, websocket):
        await websocket.send(
            json.dumps(
                {'type': 'init_paddle', 'loc': self.loc, 'size': self.length, 'width': self.width, 'x': self.x,
                 'y': self.y}))

    async def move(self, delta_time):
        # self.moving = float(self.moving)
        self.y += self.moving * self.speed * delta_time
        if self.y > 100 - self.length / 2:
            self.y = 100 - self.length / 2
        elif self.y < self.length / 2:
            self.y = self.length / 2
        if self.moving != 0:
            try:
                for websocket, paddle in connected_clients.items():
                    if self.websocket != websocket:
                        await self.send_data(websocket)
            except websockets.exceptions.ConnectionClosed:
                pass


class Response:
    @staticmethod
    async def handle_response(message, websocket):
        obj = json.loads(message)
        if obj['type'] == 'move':
            print("move " + str(obj['data']))
            paddle = connected_clients.get(websocket)
            if paddle:
                paddle.moving = int(obj['data'])
                if paddle.moving == 0:
                    for websocket, paddleO in connected_clients.items():
                        await paddle.send_data(websocket)


class Ball:
    def __init__(self):
        self.min_speed = 0.5
        self.current_speed = 10
        self.radius = 3
        self.x = 50
        self.y = 0
        self.v_x = 0.5
        self.v_y = 0.5

    async def init_ball(self, websocket):
        await websocket.send(
            json.dumps({'type': 'init_ball', 'y': self.y, 'x': self.x, 'v_x': self.v_x, 'v_y': self.v_y,
                        'speed': self.current_speed, 'radius': self.radius}))

    async def move(self, delta_time):
        self.x += self.v_x * delta_time * self.current_speed
        self.y += self.v_y * delta_time * self.current_speed
        if self.y < 0:
            self.y = 0
        if self.y > 100:
            self.y = 100

    async def wall_collide(self):
        if self.y <= 0 or self.y >= 100:
            print("collide")
            self.v_y *= -1
            for websocket in connected_clients:
                await self.send_data(websocket)

    async def send_data(self, websocket):
        await websocket.send(json.dumps(
            {'type': 'ball', 'y': self.y, 'x': self.x, 'v_x': self.v_x, 'v_y': self.v_y, 'speed': self.current_speed}))

    async def paddles_collide(self, paddle):
        offset_center = paddle.length / 2
        proportional_center = (paddle.y - 50) / 50
        real_center = paddle.y - (proportional_center * offset_center)
        # for websocket in connected_clients:
        #     await websocket.send(json.dumps({'type': 'line', 'data': real_center}))
        print("y check: " + str(paddle.y - paddle.length / 2 <= self.y <= paddle.y + paddle.length / 2))
        if paddle.loc == "left":
            if self.x <= paddle.x + paddle.width and real_center - paddle.length / 2 <= self.y <= real_center + paddle.length / 2:
                self.v_x *= -1
                self.v_y += (self.y - (paddle.y + paddle.length / 2)) * 0.1
                for websocket in connected_clients:
                    await self.send_data(websocket)
        elif paddle.loc == "right":
            if self.x >= 100 - (
                    paddle.width + paddle.x) and real_center - paddle.length / 2 <= self.y <= real_center + paddle.length / 2:
                self.v_x *= -1
                self.v_y += (self.y - (paddle.y + paddle.length / 2)) * 0.03
                for websocket in connected_clients:
                    await self.send_data(websocket)

        if self.x < 0:
            self.x = 50
            self.y = 50
            self.v_x = 1
            self.v_y = 0
            for websocket in connected_clients:
                await self.send_data(websocket)
        elif self.x > 100:
            self.x = 50
            self.y = 50
            self.v_x = 1
            self.v_y = 0
            for websocket in connected_clients:
                await self.send_data(websocket)


# Set of connected clients
connected_clients = {}

last_time = time.time()


# Function to handle each client connection
async def handle_client(websocket):
    loc = "left" if len(connected_clients) == 0 else "right"
    paddle = Paddle(loc, websocket)
    await websocket.send(json.dumps({'type': 'client', 'loc': loc, 'speed': paddle.speed}))
    await ball.init_ball(websocket)
    connected_clients[websocket] = paddle
    for websocketO, paddleO in connected_clients.items():
        if websocketO != websocket:
            await paddle.init_paddle(websocketO)
        await paddleO.init_paddle(websocket)
    # Add the new client and its associated paddle to the set
    try:
        # Listen for messages from the client
        async for message in websocket:
            await Response.handle_response(message, websocket)
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

        await ball.wall_collide()

        for websocket, paddle in connected_clients.items():
            await paddle.move(delta_time)
            await ball.paddles_collide(paddle)

        await ball.move(delta_time)
        await asyncio.sleep(1 / 60)

    await server.wait_closed()


# Run the server
if __name__ == "__main__":
    asyncio.run(main())
