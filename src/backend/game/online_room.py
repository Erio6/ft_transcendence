import asyncio
import json
import threading
import time
import threading

from asgiref.sync import sync_to_async
from django.shortcuts import redirect
from django.utils.timezone import now

from tournaments.models import Tournament, TournamentGame
from user.models import UserProfile

from blockchain.utils import blockchain_score_storage
from game.models import Game
from game.paddle import Paddle
from game.room import Room


class OnlineRoom(Room):
    def __init__(self, room_id, is_tournament):
        super().__init__(room_id)
        self.is_tournament = is_tournament

    async def update(self):
        if not await super().update():
            return

        await self.ball.wall_collide()
        # await self.ball.send_data(self.left_paddle.consumer)

        await self.left_paddle.move(self.delta_time, self)
        await self.right_paddle.move(self.delta_time, self)

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

    async def end_game(self):
        self.running = False
        game = await sync_to_async(Game.objects.get)(pk=self.id)
        player_one = await sync_to_async(lambda: game.player_one)()
        winner = self.left_paddle if self.right_paddle.score >= 10 else self.right_paddle
        looser = self.right_paddle if winner == self.left_paddle else self.left_paddle
        # await sync_to_async(print)(self.left_paddle.consumer.user_profile, player_one)
        player1 = self.left_paddle if self.left_paddle.consumer.user_profile == player_one else self.right_paddle
        player2 = self.left_paddle if player1 == self.right_paddle else self.right_paddle
        game.winner = winner.consumer.user_profile
        game.looser = looser.consumer.user_profile
        game.winner_score = looser.score
        game.looser_score = winner.score
        game.player_one_score = player2.score
        game.player_two_score = player1.score
        game.end_time = now()
        game.is_completed = True
        print("save the game")
        await sync_to_async(game.save)(force_update=True)
        print("game saved")
        # await asyncio.sleep(0.5)
        if self.is_tournament:
            tournament_game = await sync_to_async(TournamentGame.objects.get)(game=self.id)
            tournament_id = await sync_to_async(lambda: tournament_game.tournament.id)()
            print("tournament", tournament_id)
            new_url = "/tournament/tree/" + str(tournament_id) + "/"
        else:
            new_url = "/game/end/" + self.id + "/"
        print(new_url)
        if self.left_paddle:
            await self.left_paddle.consumer.send(json.dumps({'type': 'redirect', 'url': new_url}))
            await self.left_paddle.consumer.close()
        if self.right_paddle:
            await self.right_paddle.consumer.send(json.dumps({'type': 'redirect', 'url': new_url}))
            await self.right_paddle.consumer.close()
        for consumer in self.spectators:
            await consumer.send(json.dumps({'type': 'redirect', 'url': "/"}))
            await consumer.close()

    #     if not self.is_tournament:
    #         threading.Thread(target=self.run_async_blockchain_task,daemon=True, args=(game.id,)).start()
    #         print("blockchain task started")
    #
    # def run_async_blockchain_task(self, game_id):
    #     asyncio.run(self.blockchain_recording_task(game_id))
    #
    # async def blockchain_recording_task(self, game_id):
    #     print("recording game on blockchain")
    #     tx_hash = await blockchain_score_storage(game_id)
    #     game =  await sync_to_async(Game.objects.get)(pk=game_id)
    #     if tx_hash:
    #         print(f"Game recorded on blockchain with tx_hash: {tx_hash}")
    #         game.tx_hash = tx_hash
    #         game.is_recorded_on_blockchain = True
    #     else:
    #         print("Failed to record game on blockchain.")
    #
    #     await sync_to_async(game.save)(force_update=True)

    async def force_end(self, looser_left=True):
        winner = self.right_paddle if looser_left else self.left_paddle
        print("someone has disconnected so the winner is :", winner.consumer.user_profile)
        looser = self.right_paddle if winner == self.left_paddle else self.left_paddle
        looser.score = 10
        game = await sync_to_async(Game.objects.get)(pk=self.id)
        player_one = await sync_to_async(lambda: game.player_one)()
        player1 = self.left_paddle if self.left_paddle.consumer.user_profile == player_one else self.right_paddle
        player2 = self.left_paddle if player1 == self.right_paddle else self.right_paddle
        game.winner = winner.consumer.user_profile
        game.looser = looser.consumer.user_profile
        game.winner_score = 10
        game.looser_score = winner.score
        game.player_one_score = player2.score
        game.player_two_score = player1.score
        game.end_time = now()
        game.is_completed = True
        await sync_to_async(game.save)(force_update=True)
        # await asyncio.sleep(0.5)
        if self.is_tournament:
            tournament_game = await sync_to_async(TournamentGame.objects.get)(game=self.id)
            tournament_id = await sync_to_async(lambda: tournament_game.tournament.id)()
            new_url = "/tournament/tree/" + str(tournament_id) + "/"
        else:
            new_url = "/game/end/" + self.id + "/"
        if self.left_paddle:
            await self.left_paddle.consumer.send(json.dumps({'type': 'redirect', 'url': new_url}))
            await self.left_paddle.consumer.close()
        if self.right_paddle:
            await self.right_paddle.consumer.send(json.dumps({'type': 'redirect', 'url': new_url}))
            await self.right_paddle.consumer.close()
        for consumer in self.spectators:
            await consumer.send(json.dumps({'type': 'redirect', 'url': "/"}))
            await consumer.close()

    async def check_alone_async(self):
        time.sleep(4)
        if self.left_paddle and self.right_paddle:
            print("Game Full")
        elif self.left_paddle or self.right_paddle:
            winner = self.left_paddle if self.left_paddle else self.right_paddle
            game = await sync_to_async(Game.objects.get)(pk=self.id)
            player_one = await sync_to_async(lambda: game.player_one)()
            player_two = await sync_to_async(lambda: game.player_two)()
            game.winner = winner.consumer.user_profile
            game.winner_score = 10
            game.looser_score = 0
            game.player_one_score = 10 if winner == player_one else 0
            game.player_two_score = 10 if winner == player_two else 0
            game.end_time = now()
            game.is_completed = True
            await sync_to_async(game.save)(force_update=True)
            tournament_game = await sync_to_async(TournamentGame.objects.get)(game=self.id)
            tournament_id = await sync_to_async(lambda: tournament_game.tournament.id)()
            new_url = "/tournament/tree/" + str(tournament_id) + "/"
            if self.left_paddle:
                await self.left_paddle.consumer.send(json.dumps({'type': 'redirect', 'url': new_url}))
                await self.left_paddle.consumer.close()
            if self.right_paddle:
                await self.right_paddle.consumer.send(json.dumps({'type': 'redirect', 'url': new_url}))
                await self.right_paddle.consumer.close()

    def check_alone(self):
        asyncio.run(self.check_alone_async())

    async def handle_paddle_msg(self, consumer, message):
        if self.left_paddle and consumer == self.left_paddle.consumer:
            if message['data'] == 1:
                self.left_paddle.movingDown = 1 if message['value'] else 0
            else:
                self.left_paddle.movingUp = 1 if message['value'] else 0
            if self.left_paddle.movingDown == 0 and self.left_paddle.movingUp == 0:
                await self.left_paddle.send_data()
        elif self.right_paddle and consumer == self.right_paddle.consumer:
            if message['data'] == 1:
                self.right_paddle.movingDown = 1 if message['value'] else 0
            else:
                self.right_paddle.movingUp = 1 if message['value'] else 0
            if self.right_paddle.movingDown == 0 and self.right_paddle.movingUp == 0:
                await self.right_paddle.send_data()

    async def register_consumer(self, consumer):
        # if consumer == self.left_paddle.consumer or consumer == self.right_paddle.consumer or consumer in self.spectators:
        #     return False
        print("register")
        if self.is_tournament and not self.left_paddle and not self.right_paddle:
            threading.Thread(target=self.check_alone, daemon=True).start()
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
            print("should add spec")
            self.spectators.append(consumer)
            await consumer.send(json.dumps({'type': 'client', 'loc': 'spectator'}))
            await self.left_paddle.init_paddle_chan(consumer)
            await self.right_paddle.init_paddle_chan(consumer)
            if self.running:
                await self.ball.init_ball_chan(consumer)

    async def remove_consumer(self, consumer):
        wasRunning = self.running
        if (self.left_paddle and consumer == self.left_paddle.consumer) or (
                self.right_paddle and consumer == self.right_paddle.consumer):
            self.running = False
        if consumer in self.spectators:
            self.spectators.remove(consumer)
        elif self.left_paddle and consumer == self.left_paddle.consumer:
            if wasRunning:
                print("someone left then force end")
                await self.force_end(True)
            del self.left_paddle
            self.left_paddle = None
        elif self.right_paddle and consumer == self.right_paddle.consumer:
            if wasRunning:
                print("someone right then force end")
                await self.force_end(False)
            del self.right_paddle
            self.right_paddle = None
