import json

from asgiref.sync import sync_to_async
from django.utils.timezone import now

from blockchain.utils import blockchain_score_storage
from game.models import Game
from game.paddle import Paddle
from game.room import Room


class OnlineRoom(Room):
    def __init__(self, room_id):
        super().__init__(room_id)

    async def update(self):
        if not await super().update():
            return

        await self.ball.wall_collide()

        await self.left_paddle.move(self.delta_time, self)
        await self.right_paddle.move(self.delta_time, self)

        await self.ball.paddles_collide_check(self.left_paddle)
        await self.ball.paddles_collide_check(self.right_paddle)

        await self.ball.send_data(self.left_paddle.consumer)
        await self.ball.send_score(self.left_paddle.consumer)

        if len(self.spectators) > 0:
            await self.ball.send_data(self.spectators[0])
            await self.ball.send_score(self.spectators[0])
            await self.left_paddle.send_data_chan(self.spectators[0])
            await self.right_paddle.send_data_chan(self.spectators[0])

        await self.ball.move(self.delta_time)

    async def end_game(self):
        self.running = False
        game = await sync_to_async(Game.objects.get)(pk=self.id)
        player_one = await sync_to_async(lambda: game.player_one)()
        winner = self.left_paddle if self.right_paddle.score >= 10 else self.right_paddle
        looser = self.right_paddle if winner == self.left_paddle else self.left_paddle
        player1 = self.left_paddle if self.left_paddle.consumer.user_profile == player_one else self.right_paddle
        player2 = self.left_paddle if player1 == self.right_paddle else self.right_paddle
        game.winner = winner.consumer.user_profile
        game.looser = looser.consumer.user_profile
        game.winner_score = looser.score
        game.looser_score = winner.score
        game.player_one_score = player1.score
        game.player_two_score = player2.score
        game.end_time = now()
        game.is_completed = True
        print("save the game")
        await sync_to_async(game.save)(force_update=True)
        print("game saved")
        # try:
        #     await blockchain_score_storage(game)
        # except Exception as e:
        #     print(f"Erreur lors de l'enregistrement sur la blockchain : {e}")

    async def handle_paddle_msg(self, consumer, message):
        if consumer == self.left_paddle.consumer:
            if message['data'] == 1:
                self.left_paddle.movingDown = 1 if message['value'] else 0
            else:
                self.left_paddle.movingUp = 1 if message['value'] else 0
            if self.left_paddle.movingDown == 0 and self.left_paddle.movingUp == 0:
                await self.left_paddle.send_data()
        elif consumer == self.right_paddle.consumer:
            if message['data'] == 1:
                self.right_paddle.movingDown = 1 if message['value'] else 0
            else:
                self.right_paddle.movingUp = 1 if message['value'] else 0
            if self.right_paddle.movingDown == 0 and self.right_paddle.movingUp == 0:
                await self.right_paddle.send_data()

    async def register_consumer(self, consumer):
        # if consumer == self.left_paddle.consumer or consumer == self.right_paddle.consumer or consumer in self.spectators:
        #     return False
        if not self.left_paddle:
            self.left_paddle = Paddle("left", consumer, consumer.user_profile.display_name)
            await consumer.send(json.dumps({'type': 'client', 'loc': 'left', 'speed': self.left_paddle.speed}))
            await self.left_paddle.init_paddle()
            # await self.ball.init_ball_chan(consumer)
        elif not self.right_paddle:
            self.right_paddle = Paddle("right", consumer, consumer.user_profile.display_name)
            await consumer.send(json.dumps({'type': 'client', 'loc': 'right', 'speed': self.right_paddle.speed}))
            print("send right paddle")
            await self.right_paddle.init_paddle_chan(consumer)
            await self.right_paddle.init_paddle_chan(self.left_paddle.consumer)
            await self.left_paddle.init_paddle_chan(consumer)
            await self.start_game()
            print("game started")
            # await self.ball.init_ball_chan(consumer)
        else:
            self.spectators.append(consumer)
            await consumer.send(json.dumps({'type': 'client', 'loc': 'spectator'}))
            await self.left_paddle.init_paddle_chan(consumer)
            await self.right_paddle.init_paddle_chan(consumer)
            if self.running:
                await self.ball.init_ball_chan(consumer)

    async def remove_consumer(self, consumer):
        if consumer == self.left_paddle.consumer or consumer == self.right_paddle.consumer:
            self.running = False
        if consumer in self.spectators:
            self.spectators.remove(consumer)
        elif consumer == self.left_paddle.consumer:
            del self.left_paddle
            self.left_paddle = None
            print("delete left", self.left_paddle)
        elif consumer == self.right_paddle.consumer:
            del self.right_paddle
            self.right_paddle = None
