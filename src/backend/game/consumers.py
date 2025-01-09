import asyncio
import json
import time

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from game.ball import Ball
from game.models import Game
from game.online_room import OnlineRoom
from game.paddle import Paddle
from game.room import Room
from user.models import UserProfile

connected_clients = {}
group_rooms = {}
default_consumer = None
ball = None


async def game_loop():
    global group_rooms

    while True:
        for room in group_rooms.values():
            await room.update()
        await asyncio.sleep(1 / 60)


class GameConsumer(AsyncWebsocketConsumer):
    room_name = ""

    async def connect(self):
        global group_rooms

        user = self.scope["user"]
        print(user)
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        print(user.is_authenticated)

        if user.is_authenticated:
            # Convert the lazy User object into a real User instance
            user = await sync_to_async(lambda: User.objects.get(pk=user.pk))()

            # Fetch the UserProfile asynchronously
            self.user_profile = await sync_to_async(UserProfile.objects.get)(user=user)
            await sync_to_async(print)(self.user_profile)
            try:
                self.game = await sync_to_async(Game.objects.get)(id=self.room_name)
                if self.room_name in group_rooms:
                    for consumer in group_rooms[self.room_name].get_consumers():
                        if consumer.user_profile == self.user_profile:
                            print("already in the game")
                            return

                print("valid id")
            except Game.DoesNotExist:
                print("invalid id")
                return
        else:
            return

        start_loop = False

        await self.channel_layer.group_add(self.room_name, self.channel_name)

        if len(group_rooms) == 0:
            start_loop = True

        await self.accept()

        if self.room_name not in group_rooms:
            print("create Room, room name", type(self.room_name))
            group_rooms[self.room_name] = OnlineRoom(self.room_name)
        await group_rooms[self.room_name].register_consumer(self)

        if start_loop:
            asyncio.create_task(game_loop())

        # print(self.room_name)
        # print(group_rooms[self.room_name])

        # loc = "left" if len(connected_clients) == 0 else "right"
        # paddle = Paddle(loc, self)
        # self.paddle = paddle
        # if loc == "left":
        #   ball = Ball()
        #   asyncio.create_task(game_loop())

        # await self.send(json.dumps({'type': 'client', 'loc': loc, 'speed': paddle.speed}))

        # await paddle.init_paddle()

        # if ball is not None:
        #     await ball.init_ball(self)

        # for client, pad in connected_clients.items():
        #     if client != self:
        #         await paddle.init_paddle()
        #     await pad.init_paddle()
        # if loc == "left":

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print("disconnect")
        if self.room_name in group_rooms and self in group_rooms[self.room_name].get_consumers():
            await group_rooms[self.room_name].remove_consumer(self)
            print("is room empty :", group_rooms[self.room_name].is_empty())
            if group_rooms[self.room_name].is_empty():
                del group_rooms[self.room_name]
                print("delete room")

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        print(message)
        if message['type'] == 'move':
            room = group_rooms[self.room_name]
            if room:
                await room.handle_paddle_msg(self, message)
            # paddle = connected_clients.get(self)
            # if paddle:
            #     paddle.moving = int(message['data'])
            #     if paddle.moving == 0:
            #         for consumer, other_paddle in connected_clients.items():
            #             await paddle.send_data()

    # Broadcast methods called from group_send

    async def init_ball(self, event):
        await self.send(text_data=json.dumps(
            {'type': 'init_ball', 'y': event['y'], 'x': event['x'], 'v_x': event['v_x'], 'v_y': event['v_y'],
             'speed': event['speed'], 'radius': event['radius']}))

    async def ball_update(self, event):
        await self.send(text_data=json.dumps(
            {'type': 'ball', 'x': event['x'], 'y': event['y'], 'v_x': event['v_x'], 'v_y': event['v_y'],
             'speed': event['speed']}))

    async def score_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'score', 'value': event['value'], 'loc': event['loc'], 'y': event['y'], 'x': event['x'],
            'v_x': event['v_x'], 'v_y': event['v_y'], 'speed': event['speed']
        }))

    async def paddle_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'paddle', 'y': event['y'], 'size': event['size'], 'loc': event['loc']
        }))

    async def init_paddle(self, event):
        await self.send(text_data=json.dumps({
            'type': 'init_paddle', 'loc': event['loc'], 'size': event['size'], 'width': event['width'], 'y': event['y'],
            'x': event['x'], 'speed': event['speed'], 'name': event['name']
        }))

    async def start_game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'start_game',
        }))
