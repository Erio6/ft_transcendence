import json


class Paddle:
    def __init__(self, loc, consumer):
        self.loc = loc
        self.y = 50
        self.moving = 0
        self.consumer = consumer
        self.length = 25
        self.width = 3.5
        self.speed = 100
        self.x = 2
        self.score = 0

    async def send_data(self, consumer):
        await consumer.send(json.dumps({'type': 'paddle', 'y': self.y, 'size': self.length, 'loc': self.loc}))

    async def init_paddle(self, consumer):
        await consumer.send(
            json.dumps(
                {'type': 'init_paddle', 'loc': self.loc, 'size': self.length, 'width': self.width, 'x': self.x,
                 'y': self.y}))

    async def move(self, delta_time, connected_clients):
        # self.moving = float(self.moving)
        self.y += self.moving * self.speed * delta_time

        if self.y > 100 - self.length / 2:
            self.y = 100 - self.length / 2
        elif self.y < self.length / 2:
            self.y = self.length / 2

        if self.moving != 0:
            for consumer, paddle in connected_clients.items():
                if self.consumer != consumer:
                    await self.send_data(consumer)
