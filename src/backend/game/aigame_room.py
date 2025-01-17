import json

from game.paddle import Paddle
from game.room import Room


class AIGameRoom(Room):
    def __init__(self, room_id):
        super().__init__(room_id)
        self.old_pos = [0, 0]
        self.send_left = False
        self.send_right = False

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
