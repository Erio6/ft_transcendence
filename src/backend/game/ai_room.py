import json
import time

from asgiref.sync import sync_to_async
from django.utils.timezone import now

from blockchain.utils import blockchain_score_storage
from game.ball import Ball
from game.models import Game
from game.paddle import Paddle
from game.room import Room


class AIRoom(Room):
    def __init__(self, room_id):
        super().__init__(room_id)
        self.right_paddle = Paddle("right", None, "p1")
        self.left_paddle = Paddle("left", None, "p2")

    async def update(self):
        if not await super().update():
            return

        await self.ball.wall_collide()
        self.ball.paddles_collide_check(self.left_paddle)
        self.ball.paddles_collide_check(self.right_paddle)
        if len(self.spectators) > 0:
            await self.ball.send_data(self.spectators[0])
            await self.ball.send_score(self.spectators[0])
            await self.left_paddle.send_data_chan(self.spectators[0])
            await self.right_paddle.send_data_chan(self.spectators[0])

        await self.ball.move(self.delta_time)

    async def reset(self):
        await super().reset()
        self.left_paddle = Paddle("left", None, "p1")
        self.right_paddle = Paddle("right", None, "p2")

    async def end_game(self):
        self.running = False

    async def handle_paddle_msg(self, consumer, message):
        pass

    async def register_consumer(self, consumer):
        self.spectators.append(consumer)
        print("send hello to spec")
        await consumer.send(json.dumps({'type': 'client', 'loc': 'spectator'}))
        await self.left_paddle.init_paddle_chan(consumer)
        await self.right_paddle.init_paddle_chan(consumer)
        if self.running:
            await self.ball.init_ball_chan(consumer)

    async def remove_consumer(self, consumer):
        if consumer in self.spectators:
            self.spectators.remove(consumer)
