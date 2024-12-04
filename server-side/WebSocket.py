import asyncio
import math
import time

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
        self.score = 0

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
        self.min_speed = 10
        self.current_speed = 10
        self.radius = 3
        self.x = 50
        self.y = 0
        self.v_x = 0.5
        self.v_y = 0.5
        self.last_touch = "left"

    async def init_ball(self, websocket):
        await websocket.send(
            json.dumps({'type': 'init_ball', 'y': self.y, 'x': self.x, 'v_x': self.v_x, 'v_y': self.v_y,
                        'speed': self.current_speed, 'radius': self.radius}))

    async def move(self, delta_time):
        self.x += self.v_x * delta_time * self.current_speed
        self.y += self.v_y * delta_time * self.current_speed
        # if self.y < 0:
        #     self.y = 0
        # if self.y > 100:
        #     self.y = 100

    async def wall_collide(self):
        if self.y < 0:
            self.y = 0
        if self.y > 100:
            self.y = 100
        if self.y <= 0 or self.y >= 100:
            self.v_y *= -1
            for websocket in connected_clients:
                await self.send_data(websocket)

    async def send_data(self, websocket):
        await websocket.send(json.dumps(
            {'type': 'ball', 'y': self.y, 'x': self.x, 'v_x': self.v_x, 'v_y': self.v_y,
             'speed': self.current_speed}))

    async def send_score(self, paddle):
        self.x = 50
        self.y = 50
        self.v_x = 1
        self.v_y = 0
        self.current_speed = self.min_speed
        for websocket in connected_clients:
            await websocket.send(
                json.dumps({'type': 'score', 'value': paddle.score, 'loc': paddle.loc, 'y': self.y, 'x': self.x,
                            'v_x': self.v_x, 'v_y': self.v_y, 'speed': self.current_speed}))

    async def paddles_collide_check(self, paddle):
        if paddle.loc == "left":
            # print(str(self.x <= paddle.x + paddle.width) + " | " + str(
            #     paddle.y - self.radius - paddle.length / 2 <= self.y <= paddle.y + self.radius + paddle.length / 2))
            await paddle.websocket.send(json.dumps(
                {'type': 'debug', 'line1': paddle.y - self.radius - paddle.length / 2,
                 'line2': paddle.y + self.radius + paddle.length / 2}))
            if self.x < 0:
                paddle.score += 1
                self.last_touch = "left"
                await self.send_score(paddle)
            elif self.last_touch == "right" and self.x <= paddle.x + paddle.width and paddle.y - self.radius - paddle.length / 2 <= self.y <= paddle.y + self.radius + paddle.length / 2:
                await self.paddle_collide(paddle, self.x - (paddle.x + paddle.width))

        elif paddle.loc == "right":
            if self.x > 100:
                paddle.score += 1
                self.last_touch = "left"
                await self.send_score(paddle)
            elif self.last_touch == "left" and self.x >= 100 - (
                    paddle.width + paddle.x) and paddle.y - self.radius - paddle.length / 2 <= self.y <= paddle.y + self.radius + paddle.length / 2:
                await self.paddle_collide(paddle, 100 - (paddle.width + paddle.x) - self.x)

    async def paddle_collide(self, paddle, diff_x):
        diff_y = min(abs((paddle.y - self.radius - paddle.length / 2) - self.y),
                     abs(self.y - (paddle.y + self.radius + paddle.length / 2)))
        diff_x = abs(diff_x)
        print("diff_x = " + str(diff_x) + " | diff_y = " + str(diff_y))
        print("1 = " + str((paddle.y - self.radius - paddle.length / 2) - self.y) + " | 2 = " + str(
            self.y - (paddle.y + self.radius + paddle.length / 2)))
        if diff_x > diff_y:
            self.current_speed += 10
            if self.y < paddle.y:
                # self.y += 2 * diff_y
                self.v_y = -1
            else:
                # self.y -= 2 * diff_y
                self.v_y = 1
                self.current_speed += 10
        else:
            self.v_y += (self.y - (paddle.y + paddle.length / 2)) * 0.03
            self.v_y += paddle.moving * 0.5
        self.normalize()
        self.v_x *= -1
        self.current_speed += 10
        self.last_touch = paddle.loc
        for websocket in connected_clients:
            await self.send_data(websocket)

    def normalize(self):
        m = math.sqrt(self.v_x ** 2 + self.v_y ** 2)
        self.v_x /= m
        self.v_y /= m


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
            await ball.paddles_collide_check(paddle)

        await ball.move(delta_time)
        await asyncio.sleep(1 / 60)

    await server.wait_closed()


# Run the server
if __name__ == "__main__":
    asyncio.run(main())
