import json
import uuid
from django.urls import reverse
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import Match
from game.models import Game
from user.models import UserProfile
from channels.db import database_sync_to_async


class MatchMakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.connection_id = str(uuid.uuid4())  # this will create a unique identifier for this connection
        self.match_id = self.scope["url_route"]["kwargs"].get("match_id")
        # print("**********" + self.match_id + "*************")
        self.user = self.scope["user"]
        # print("***********" + str(self.user) + "****************")

        if not self.user.is_authenticated:
            await self.close()
            return

        self.match = await self.get_or_create_match(self.match_id)

        self.match_group_name = f"match_{self.match.id}"
        await self.channel_layer.group_add(
            self.match_group_name,
            self.channel_name
        )

        await self.accept()

        await self.add_connection_to_match()

        if self.match.status == "matched" and len(self.match.connected_players) == 2:
            await self.notify_players(self.match)

    async def disconnect(self, close_code):
        if hasattr(self, "match_group_name"):
            await self.channel_layer.group_discard(
                self.match_group_name,
                self.channel_name
            )
        if hasattr(self, "match"):
            await self.remove_connection_from_match()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "cancel_matchmaking":
            await self.cancel_matchmaking()

    async def cancel_matchmaking(self):
        if hasattr(self, "match"):
            await self.remove_connection_from_match()

            if self.match.status == "waiting":
                await self.delete_match()

        await self.close()

    @sync_to_async
    def delete_match(self):
        if self.match.status == "waiting":
            print("Deleting match" + str(self.match.id))
            self.match.delete()

    @sync_to_async
    def add_connection_to_match(self):
        if self.connection_id not in self.match.connected_players:
            self.match.connected_players.append(self.connection_id)
            self.match.save()

    @sync_to_async
    def remove_connection_from_match(self):
        if self.connection_id in self.match.connected_players:
            self.match.connected_players.remove(self.connection_id)
            self.match.save()

    @sync_to_async
    def get_or_create_match(self, match_id):
        user_profile = UserProfile.objects.get(user=self.user)

        if match_id:
            match = Match.objects.filter(id=match_id).first()
            if not match:
                raise ValueError(f"No match found with ID {match_id}")

            # if match.player_two is None and match.status == "waiting":
            #     if match.player_one != user_profile:
            #         match.player_two = user_profile
            #         match.status = "matched"
            #         match.save()
        # else:
        #     match = Match.objects.filter(player_two__isnull=True, status="waiting").exclude(player_one=user_profile).first()
        #     if match:
        #         match.player_two = user_profile
        #         match.status = "matched"
        #         match.save()
        #     else:
        #         match = Match.objects.create(player_one=user_profile, status="waiting")

        return match

    @sync_to_async
    def notify_players(self, match):
        # Create the Game instance
        game = Game.objects.create(player_one=match.player_one, player_two=match.player_two)

        # Send the game URL to both players
        game_url = reverse('game:real_game', kwargs={'game_id': game.id})  # f"/game/game/{game.id}/"
        async_to_sync(self.channel_layer.group_send)(
            f"match_{match.id}",
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
