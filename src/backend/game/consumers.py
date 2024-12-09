import asyncio
import json
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from game.ball import Ball
from game.paddle import Paddle

connected_clients = {}
default_consumer = None
ball = None


async def game_loop():
    global ball
    global connected_clients
    global default_consumer
    last_time = time.time()

    while True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        await ball.wall_collide()

        for consumer, paddle in connected_clients.items():
            await paddle.move(delta_time, connected_clients)
            await ball.paddles_collide_check(paddle)

        await ball.send_data(default_consumer)
        await ball.send_score(default_consumer)
        await ball.move(delta_time)

        await asyncio.sleep(1 / 60)


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global connected_clients
        global ball
        global default_consumer

        self.room_name = self.scope['url_route']['kwargs']['room_id']
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        loc = "left" if len(connected_clients) == 0 else "right"
        if (loc == "left"):
            ball = Ball()
            asyncio.create_task(game_loop())

        paddle = Paddle(loc, self)
        default_consumer = self

        await self.accept()

        await self.send(json.dumps({'type': 'client', 'loc': loc, 'speed': paddle.speed}))
        connected_clients[self] = paddle

        await paddle.init_paddle(self)

        if ball is not None:
            await ball.init_ball(self)

        for client, pad in connected_clients.items():
            if client != self:
                await paddle.init_paddle(client)
            await pad.init_paddle(self)
        # if loc == "left":

    async def disconnect(self, code):
        global connected_clients
        if self in connected_clients:
            del connected_clients[self]

    async def receive(self, text_data=None, bytes_data=None):
        global connected_clients
        message = json.loads(text_data)
        if message['type'] == 'move':
            paddle = connected_clients.get(self)
            if paddle:
                paddle.moving = int(message['data'])
                if paddle.moving == 0:
                    for consumer, other_paddle in connected_clients.items():
                        await paddle.send_data(consumer)

    # Broadcast methods called from group_send

    async def init_ball(self, event):
        await self.send(text_data=json.dumps(
            {'type': 'init_ball', 'y': event['y'], 'x': event['x'], 'v_x': event['v_x'], 'v_y': event['v_y'],
             'speed': event['speed'], 'radius': event['radius']}))

    async def ball_update(self, event):
        await self.send(text_data=json.dumps(
            {'type': 'ball', 'x': event['x'], 'y': event['y'], 'v_x': event['v_x'], 'v_y': event['v_y'],
             'speed': event['speed']}))

    async def score_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'score', 'value': event['score'], 'loc': event['loc'], 'y': event['y'], 'x': event['x'],
            'v_x': event['v_x'], 'v_y': event['v_y'], 'speed': event['speed']
        }))
