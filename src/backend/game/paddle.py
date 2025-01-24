import json


class Paddle:
    def __init__(self, loc, consumer, name):
        self.loc = loc
        self.y = 50
        self.movingUp = 0
        self.movingDown = 0
        self.moving = 0
        self.consumer = consumer
        self.length = 25
        self.width = 3.5
        self.speed = 100
        self.x = 2
        self.score = 0
        self.hit = 0
        self.name = name
        self.dist = 0

    async def send_data(self):
        print("send to all")
        await self.consumer.channel_layer.group_send(
            self.consumer.room_name,
            {
                'type': 'paddle_update',
                'y': self.y,
                'x': self.x,
                'size': self.length,
                'loc': self.loc,
            }
        )

    async def send_data_chan(self, consumer):
        if not consumer:
            return
        await consumer.send(json.dumps({
            'type': 'paddle', 'loc': self.loc, 'size': self.length, 'y': self.y,
        }))

    async def init_paddle(self):
        await self.consumer.channel_layer.group_send(
            self.consumer.room_name,
            {
                'type': 'init_paddle',
                'loc': self.loc,
                'size': self.length,
                'width': self.width,
                'speed': self.speed,
                'x': self.x,
                'y': self.y,
                'name': self.name,
            }
        )

    async def init_paddle_chan(self, consumer):
        await consumer.send(json.dumps({
            'type': 'init_paddle', 'loc': self.loc, 'size': self.length, 'speed': self.speed, 'width': self.width,
            'x': self.x, 'y': self.y, 'name': self.name,
        }))

    async def move(self, delta_time, room):
        self.moving = self.movingDown - self.movingUp
        self.y += self.moving * self.speed * delta_time

        if self.y > 100 - self.length / 2:
            self.y = 100 - self.length / 2
        elif self.y < self.length / 2:
            self.y = self.length / 2

        if self.moving != 0:
            # print(self.movingDown, self.movingUp)
            for consumer in room.get_consumers(self.loc != "left", self.loc != "right"):
                await self.send_data_chan(consumer)

    def force_move(self, value):
        if self.y >= 100 - self.length / 2 and value > 0:
            return False
        elif self.y <= self.length / 2 and value < 0:
            return False

        self.y += value
        # print("y after changes", self.y)

        if self.y > 100 - self.length / 2:
            self.y = 100 - self.length / 2
        elif self.y < self.length / 2:
            self.y = self.length / 2

        return True
