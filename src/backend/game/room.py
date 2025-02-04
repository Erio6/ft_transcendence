import asyncio
import json
import time

from game.ball import Ball


class Room:
    def __init__(self, room_id):
        self.left_paddle = None
        self.right_paddle = None
        self.spectators = []
        self.id = room_id
        self.ball = Ball()
        self.last_time = time.time()
        self.running = False
        self.delta_time = 0
        self.completed = False

    async def update(self):
        if not self.running:
            return False
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time

        if not self.left_paddle or not self.right_paddle:
            return False

        if self.left_paddle.score >= 10 or self.right_paddle.score >= 10:
            print("score >= 10")
            await self.end_game()
            return False
        return True

    async def end_game(self):
        pass

    async def start_game(self):
        if not self.left_paddle or not self.right_paddle:
            self.running = False
            return
        await asyncio.sleep(3)
        if self.left_paddle:
            await self.left_paddle.consumer.channel_layer.group_send(
                self.left_paddle.consumer.room_name,
                {
                    'type': 'start_game',
                }
            )
        self.last_time = time.time()
        await self.ball.init_ball(self.left_paddle.consumer)
        self.running = True

    async def handle_paddle_msg(self, consumer, message):
        pass

    async def register_consumer(self, consumer):
        pass

    async def remove_consumer(self, consumer):
        pass

    def get_consumers(self, left=True, right=True):
        consumers = []
        if left and self.left_paddle:
            consumers.append(self.left_paddle.consumer)
        if right and self.right_paddle:
            consumers.append(self.right_paddle.consumer)
        for consumer in self.spectators:
            consumers.append(consumer)

        return consumers

    async def reset(self):
        self.running = True
        self.last_time = time.time()
        self.ball = Ball()
        for consumer in self.spectators:
            await consumer.send(json.dumps({'type': 'client', 'loc': 'spectator'}))
            await self.ball.init_ball_chan(consumer)
            await self.left_paddle.init_paddle_chan(consumer)
            await self.right_paddle.init_paddle_chan(consumer)

    def is_empty(self):
        if len(self.spectators) != 0:
            return False
        if self.left_paddle or self.right_paddle:
            return False
        return True
