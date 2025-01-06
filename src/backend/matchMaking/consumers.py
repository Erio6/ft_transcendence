import json
from channels.generic.websocket import AsyncWebsocketConsumer
import aioredis
from asgiref.sync import sync_to_async
from .models import Match
from game.models import Game
from user.models import UserProfile

class MatchMakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.accept()

        # Add the player to the match
        await self.add_player_to_match()

    async def disconnect(self, close_code):
        # Handle disconnection if needed
        pass

    @sync_to_async
    def add_player_to_match(self):
        # Fetch the match
        match = Match.objects.get(id=self.match_id)
        user_profile = UserProfile.objects.get(user=self.user)

        # Check if this user is already part of the match
        if match.player_one == user_profile or match.player_two == user_profile:
            return

        # Add this player as player_two if the slot is empty
        if match.player_two is None:
            match.player_two = user_profile
            match.status = 'matched'
            match.save()

            # Notify both players that the match is ready
            self.notify_players(match)

    @sync_to_async
    def notify_players(self, match):
        # Create the Game instance
        game = Game.objects.create(player_one=match.player_one, player_two=match.player_two)

        # Send the game URL to both players
        game_url = f"/game/{game.id}/"
        self.channel_layer.group_send(
            f"match_{self.match_id}",
            {
                "type": "game_ready",
                "game_url": game_url,
            },
        )

    async def game_ready(self, event):
        # Send the game URL to the frontend
        await self.send(text_data=json.dumps({
            "action": "game_ready",
            "game_url": event["game_url"],
        }))
    # async def connect(self):
    #     # here is store the data of a match in redis so i can find it quickly when doing the matchmaking
    #     self.user = self.scope['user']
    #     self.match_id = self.scope['url_route']['kwargs']['match_id']
    #     self.redis = await aioredis.from_url('redis://localhost')
    #
    #     if self.user.is_authenticated:
    #         await self.accept()
    #         await self.add_player_to_game()
    #     else:
    #         await self.close()
    #
    # async def disconnect(self, close_code):
    #     # here i clean the redis data of the match when there is a disconnection
    #     await self.redis.delete(f'match:{self.match_id}')
    #
    # async def add_player_to_game(self):
    #     # here i collect the data from redis that i store in the connect function. The goal is to create a match class and store inside all the information about the match
    #     match_data_raw = await self.redis.get(f"match_{self.match_id}")
    #     match_data = json.loads(match_data_raw) if match_data_raw else {}
    #
    #     if not match_data:
    #         await self.send(text_data=json.dumps({"error": "Invalid Match ID"}))
    #         await self.close()
    #         return
    #
    #     user_profile = await sync_to_async(UserProfile.objects.get)(user=self.user)
    #
    #     if not match_data.get("player_one"):
    #         match_data["player_one"] = user_profile.id
    #         match_data["player_one_channel"] = self.channel_name
    #     elif not match_data.get("player_two"):
    #         match_data["player_two"] = user_profile.id
    #         match_data["player_two_channel"] = self.channel_name
    #     else:
    #         await self.send(text_data=json.dumps({"error": "Match is full"}))
    #         await self.close()
    #         return
    #
    #     await self.redis.set(f"match_{self.match_id}", json.dumps(match_data))
    #
    #     if match_data.get("player_one_channel") and match_data.get("player_two_channel"):
    #         await self.start_game(match_data)
    #
    # async def start_game(self, match_data):
    #     player_one = await sync_to_async(UserProfile.objects.get)(id=match_data["player_one"])
    #     player_two = await sync_to_async(UserProfile.objects.get)(id=match_data["player_two"])
    #
    #     game = await sync_to_async(Game.objects.create)(player_one=player_one, player_two=player_two)
    #
    #     game_url = f"/game/{game.id}"
    #
    #     await self.channel_layer.group_send(
    #         f"match_{self.match_id}",
    #         {
    #             "type": "game_ready",
    #             "game_url": game_url,
    #         },
    #     )
    #
    # async def game_ready(self, event):
    #     await self.send(text_data=json.dumps({
    #         "action": "game_ready",
    #         "game_url": event["game_url"],
    #     }))