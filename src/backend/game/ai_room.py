import asyncio
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
        self.old_pos = [0, 0]
        self.send_left = False
        self.send_right = False

    async def update(self):
        if not await super().update():
            return

        # print(self.send_left, self.send_right)
        new_pos = [self.left_paddle.y, self.right_paddle.y]
        # print(self.old_pos, new_pos)

        await self.ball.wall_collide()
        self.ball.paddles_collide_check(self.left_paddle)
        self.ball.paddles_collide_check(self.right_paddle)
        # if self.ball.x > 97.5:
        #     self.ball.last_touch = "right"
        #     if 0.05 > self.ball.v_y >= 0:
        #         self.ball.v_y = 0.2
        #     if -0.05 < self.ball.v_y < 0:
        #         self.ball.v_y = -0.2
        #     self.ball.v_x *= -1
        #     self.ball.normalize()
        #     self.ball.x = 97.5
        #     if len(self.spectators) > 0:
        #         self.ball.sending_data = True
        #         await self.ball.send_data(self.spectators[0])

        if len(self.spectators) > 0:
            # print("send to spec : ", self.spectators)
            await self.ball.send_data(self.spectators[0])
            await self.ball.send_score(self.spectators[0])
            if self.send_left:
                # print("left difference")
                await self.left_paddle.send_data_chan(self.spectators[0])
                self.send_left = False
            if self.send_right:
                # print("right difference")
                await self.right_paddle.send_data_chan(self.spectators[0])
                self.send_right = False

        self.old_pos = [new_pos[0], new_pos[1]]
        await self.ball.move(self.delta_time)
        await asyncio.sleep(1 / 60)

    async def reset(self):
        await super().reset()
        self.left_paddle = Paddle("left", None, "p1")
        self.right_paddle = Paddle("right", None, "p2")

    async def start_game(self):
        self.old_pos = [self.left_paddle.y, self.right_paddle.y]
        await super().start_game()

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
