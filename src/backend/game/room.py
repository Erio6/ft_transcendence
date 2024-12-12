import json
import time

from asgiref.sync import async_to_sync

from game.ball import Ball
from game.paddle import Paddle


class Room:
    def __init__(self):
        self.left_paddle = None
        self.right_paddle = None
        self.spectators = []
        self.ball = Ball()
        self.last_time = time.time()
        self.running = True

    async def update(self):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        if not self.left_paddle or not self.right_paddle:
            return

        await self.ball.wall_collide()
        await self.left_paddle.move(delta_time, self)
        await self.right_paddle.move(delta_time, self)
        await self.ball.paddles_collide_check(self.left_paddle)
        await self.ball.paddles_collide_check(self.right_paddle)

        await self.ball.send_data(self.left_paddle.consumer)
        await self.ball.send_score(self.left_paddle.consumer)
        await self.ball.move(delta_time)

    async def handle_paddle_msg(self, consumer, message):
        if consumer == self.left_paddle.consumer:
            if message['data'] == 1:
                self.left_paddle.movingDown = 1 if message['value'] else 0
            else:
                self.left_paddle.movingUp = 1 if message['value'] else 0

            # self.left_paddle.moving = int(message['data'])
            # if self.left_paddle.moving == 0:
            #     self.left_paddle.send_data_chan(self.left_paddle.consumer)
            # await self.left_paddle.send_data()
        elif consumer == self.right_paddle.consumer:
            if message['data'] == 1:
                self.right_paddle.movingDown = 1 if message['value'] else 0
            else:
                self.right_paddle.movingUp = 1 if message['value'] else 0
            # self.right_paddle.moving = int(message['data'])
            # await self.right_paddle.send_data()

    async def register_consumer(self, consumer):
        if not self.left_paddle:
            self.left_paddle = Paddle("left", consumer)
            await consumer.send(json.dumps({'type': 'client', 'loc': 'left', 'speed': self.left_paddle.speed}))
            await self.left_paddle.init_paddle()
            await self.ball.init_ball_chan(consumer)
        elif not self.right_paddle:
            self.right_paddle = Paddle("right", consumer)
            await consumer.send(json.dumps({'type': 'client', 'loc': 'right', 'speed': self.right_paddle.speed}))
            await self.right_paddle.init_paddle()
            await self.left_paddle.init_paddle_chan(consumer)
            await self.ball.init_ball_chan(consumer)
        else:
            self.spectators.append(consumer)
            await consumer.send(json.dumps({'type': 'client', 'loc': 'spectator'}))
            await self.ball.init_ball_chan(consumer)
            await self.left_paddle.init_paddle_chan(consumer)
            await self.right_paddle.init_paddle_chan(consumer)

    async def remove_consumer(self, consumer):
        if consumer in self.spectators:
            self.spectators.remove(consumer)
        # elif consumer == self.left_paddle.consumer:
        #     self.left_paddle.consumer = None
        # elif consumer == self.right_paddle.consumer:
        #     self.right_paddle.consumer = None
        elif consumer == self.left_paddle.consumer or consumer == self.right_paddle.consumer:
            self.running = False

    def get_consumers(self):
        consumers = [self.left_paddle, self.right_paddle]
        for consumer in self.spectators:
            consumers.append(consumer)

        return consumers
