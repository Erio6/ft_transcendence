import json
import os
import pickle

import neat
from asgiref.sync import sync_to_async
from django.utils.timezone import now

from game.models import Game
from game.paddle import Paddle
from game.room import Room


class AIGameRoom(Room):
    def __init__(self, room_id, mode):
        super().__init__(room_id)
        self.mode = mode
        self.old_pos = [0, 0]
        self.send_left = False
        self.send_right = False
        self.net = None

    async def update(self):
        if not await super().update():
            return

        await self.ball.wall_collide()
        await self.left_paddle.move(self.delta_time, self)
        await self.move_ai()

        self.ball.paddles_collide_check(self.left_paddle)
        self.ball.paddles_collide_check(self.right_paddle)

        await self.ball.send_data(self.left_paddle.consumer)
        await self.ball.send_score(self.left_paddle.consumer)

        if len(self.spectators) > 0:
            await self.ball.send_data(self.spectators[0])
            await self.ball.send_score(self.spectators[0])
            await self.left_paddle.send_data_chan(self.spectators[0])
            await self.right_paddle.send_data_chan(self.spectators[0])

        await self.ball.move(self.delta_time)

    async def move_ai(self):
        if self.mode == "solo_IA_easy":
            output = self.net.activate((self.right_paddle.y / 100, self.ball.y / 100))
        elif self.mode == "solo_IA_medium":
            output = self.net.activate(
                (self.right_paddle.y / 100, abs(0.02 - self.ball.x / 100), self.ball.y / 100, self.ball.v_x,
                 self.ball.v_y))
        else:
            return

        decision = output.index(max(output))
        value = self.right_paddle.speed * self.delta_time
        if decision == 1:
            self.right_paddle.force_move(-value)
            self.send_right = True
        elif decision == 2:
            self.right_paddle.force_move(value)
            self.send_right = True

        if self.send_right:
            await self.right_paddle.send_data_chan(self.left_paddle.consumer)
            self.send_right = False

    async def end_game(self):
        self.running = False
        game = await sync_to_async(Game.objects.get)(pk=self.id)
        player_one = await sync_to_async(lambda: game.player_one)()
        game.player_one_score = self.left_paddle.score
        game.player_two_score = self.right_paddle.score
        game.end_time = now()
        game.is_completed = True
        await sync_to_async(game.save)(force_update=True)

    async def handle_paddle_msg(self, consumer, message):
        if consumer == self.left_paddle.consumer:
            if message['data'] == 1:
                self.left_paddle.movingDown = 1 if message['value'] else 0
            else:
                self.left_paddle.movingUp = 1 if message['value'] else 0
            if self.left_paddle.movingDown == 0 and self.left_paddle.movingUp == 0:
                await self.left_paddle.send_data()

    def register_ai(self):
        if self.mode == "solo_IA_easy":
            config_name = "easy.txt"
            with open("./AI/best.pickle", "rb") as f:
                winner = pickle.load(f)
        elif self.mode == "solo_IA_medium":
            config_name = "medium.txt"
            with open("./AI/medium.pickle", "rb") as f:
                winner = pickle.load(f)
        else:
            return

        local_dir = os.path.dirname(__file__)
        print(local_dir)
        config_path = os.path.join(local_dir + "/AIs/", config_name)
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)

        self.net = neat.nn.FeedForwardNetwork.create(winner, config)

    async def register_consumer(self, consumer):
        if not self.left_paddle:
            self.left_paddle = Paddle("left", consumer, consumer.user_profile.display_name)
            self.right_paddle = Paddle("right", None, "IA Easy" if self.mode == "solo_IA_easy" else "IA Medium")
            self.register_ai()
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

    async def remove_consumer(self, consumer):
        if consumer == self.left_paddle.consumer:
            self.running = False
            del self.left_paddle
            del self.right_paddle
            self.left_paddle = None
            self.right_paddle = None
            print("delete left", self.left_paddle)
        if consumer in self.spectators:
            self.spectators.remove(consumer)
