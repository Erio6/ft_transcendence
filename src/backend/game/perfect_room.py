import json

from asgiref.sync import sync_to_async
from django.utils.timezone import now

from game.models import Game
from game.paddle import Paddle
from game.perfect_paddle import PerfectPaddle
from game.room import Room


class AIPerfectRoom(Room):
    def __init__(self, room_id):
        super().__init__(room_id)
        self.old_pos = [0, 0]
        self.send_left = False
        self.send_right = False
        self.net = None

    async def update(self):
        if not await super().update():
            return

        await self.ball.wall_collide()
        await self.left_paddle.move(self.delta_time, self)
        await self.right_paddle.move(self.delta_time, self)

        hit1 = self.ball.paddles_collide_check(self.left_paddle)
        hit2 = self.ball.paddles_collide_check(self.right_paddle)

        hit3 = self.ball.sending_score

        await self.ball.send_data(self.left_paddle.consumer)
        await self.ball.send_score(self.left_paddle.consumer)

        if len(self.spectators) > 0:
            await self.ball.send_data(self.spectators[0])
            await self.ball.send_score(self.spectators[0])
            await self.left_paddle.send_data_chan(self.spectators[0])
            await self.right_paddle.send_data_chan(self.spectators[0])

        await self.ball.move(self.delta_time)
        if hit1 or hit2 or hit3:
            self.right_paddle.compute_pos(self.ball)

    async def end_game(self):
        self.running = False
        game = await sync_to_async(Game.objects.get)(pk=self.id)
        player_one = await sync_to_async(lambda: game.player_one)()
        game.player_one_score = self.left_paddle.score
        game.player_two_score = self.right_paddle.score
        game.end_time = now()
        game.is_completed = True
        await sync_to_async(game.save)(force_update=True)
        if self.left_paddle:
            await self.left_paddle.consumer.send(json.dumps({'type': 'redirect', 'url': '/game/'}))
            await self.left_paddle.consumer.close()

    async def start_game(self):
        await super().start_game()
        self.right_paddle.compute_pos(self.ball)

    async def handle_paddle_msg(self, consumer, message):
        if consumer == self.left_paddle.consumer:
            if message['data'] == 1:
                self.left_paddle.movingDown = 1 if message['value'] else 0
            else:
                self.left_paddle.movingUp = 1 if message['value'] else 0
            if self.left_paddle.movingDown == 0 and self.left_paddle.movingUp == 0:
                await self.left_paddle.send_data()

    async def register_consumer(self, consumer):
        if not self.left_paddle:
            self.left_paddle = Paddle("left", consumer, consumer.user_profile.display_name)
            self.right_paddle = PerfectPaddle("right", None, "IA Hard")
            await consumer.send(json.dumps({'type': 'client', 'loc': 'left', 'speed': self.left_paddle.speed}))
            await self.left_paddle.init_paddle_chan(self.left_paddle.consumer)
            await self.right_paddle.init_paddle_chan(self.left_paddle.consumer)
            await self.start_game()
        else:
            self.spectators.append(consumer)
            await consumer.send(json.dumps({'type': 'client', 'loc': 'spectator'}))
            await self.left_paddle.init_paddle_chan(consumer)
            await self.right_paddle.init_paddle_chan(consumer)
            if self.running:
                await self.ball.init_ball_chan(consumer)
