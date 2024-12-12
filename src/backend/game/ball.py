import json
import math

from asgiref.sync import async_to_sync


class Ball:
    def __init__(self):
        self.min_speed = 10
        self.current_speed = 10
        self.radius = 3
        self.x = 50
        self.y = 0
        self.v_x = 0.5
        self.v_y = 0.5
        self.sending_data = False
        self.sending_score = None
        self.last_touch = "left"

    async def init_ball(self, consumer):
        await consumer.channel_layer.group_send(
            consumer.room_name,
            {
                'type': 'init_ball',
                'x': self.x,
                'y': self.y,
                'v_x': self.v_x,
                'v_y': self.v_y,
                'speed': self.current_speed,
                'radius': self.radius,
            }
        )

    async def init_ball_chan(self, consumer):
        await consumer.send(json.dumps({'type': 'init_ball', 'y': self.y, 'x': self.x, 'v_x': self.v_x, 'v_y': self.v_y,
                                        'speed': self.current_speed, 'radius': self.radius}))

    async def move(self, delta_time):
        self.x += self.v_x * delta_time * self.current_speed
        self.y += self.v_y * delta_time * self.current_speed
        # if self.y < 0:
        #     self.y = 0
        # if self.y > 100:
        #     self.y = 100

    async def wall_collide(self):
        if self.y < self.radius / 2:
            self.y = self.radius / 2
        if self.y > 100 - self.radius / 2:
            self.y = 100 - self.radius / 2
        if self.y <= self.radius / 2 or self.y >= 100 - self.radius / 2:
            self.v_y *= -1
            self.sending_data = True

    async def send_data(self, consumer):
        if self.sending_data:
            await consumer.channel_layer.group_send(
                consumer.room_name,
                {
                    'type': 'ball_update',
                    'x': self.x,
                    'y': self.y,
                    'v_x': self.v_x,
                    'v_y': self.v_y,
                    'speed': self.current_speed,
                }
            )
            self.sending_data = False

    async def send_score(self, consumer):
        if self.sending_score is None:
            return

        self.x = 50
        self.y = 50
        self.v_x = 1
        self.v_y = 0
        self.current_speed = self.min_speed

        await consumer.channel_layer.group_send(
            consumer.room_name,
            {
                'type': 'score_update',
                'value': self.sending_score.score,
                'loc': self.sending_score.loc,
                'x': self.x,
                'y': self.y,
                'v_x': self.v_x,
                'v_y': self.v_y,
                'speed': self.current_speed,
            }
        )
        self.sending_score = None

    async def paddles_collide_check(self, paddle):
        if paddle.loc == "left":
            # print(str(self.x <= paddle.x + paddle.width) + " | " + str(
            #     paddle.y - self.radius - paddle.length / 2 <= self.y <= paddle.y + self.radius + paddle.length / 2))
            # await paddle.consumer.send(json.dumps(
            #     {'type': 'debug', 'line1': paddle.y - self.radius - paddle.length / 2,
            #      'line2': paddle.y + self.radius + paddle.length / 2}))
            if self.x < 0:
                paddle.score += 1
                self.last_touch = "left"
                self.sending_score = paddle
            elif self.last_touch == "right" and self.x - self.radius / 2 <= paddle.x + paddle.width and paddle.y - self.radius - paddle.length / 2 <= self.y <= paddle.y + self.radius + paddle.length / 2:
                await self.paddle_collide(paddle, self.x - (paddle.x + paddle.width))

        elif paddle.loc == "right":
            if self.x > 100:
                paddle.score += 1
                self.last_touch = "left"
                self.sending_score = paddle
            elif self.last_touch == "left" and self.x + self.radius / 2 >= 100 - (
                    paddle.width + paddle.x) and paddle.y - self.radius - paddle.length / 2 <= self.y <= paddle.y + self.radius + paddle.length / 2:
                await self.paddle_collide(paddle, 100 - (paddle.width + paddle.x) - self.x)

    async def paddle_collide(self, paddle, diff_x):
        diff_y = min(abs((paddle.y - self.radius - paddle.length / 2) - self.y),
                     abs(self.y - (paddle.y + self.radius + paddle.length / 2)))
        diff_x = abs(diff_x)
        # print("diff_x = " + str(diff_x) + " | diff_y = " + str(diff_y))
        # print("1 = " + str((paddle.y - self.radius - paddle.length / 2) - self.y) + " | 2 = " + str(
        #     self.y - (paddle.y + self.radius + paddle.length / 2)))
        if diff_x > diff_y:
            self.current_speed += 10
            if self.y < paddle.y:
                # self.y += 2 * diff_y
                self.v_y = -1
            else:
                # self.y -= 2 * diff_y
                self.v_y = 1
                self.current_speed += 10
        else:
            self.v_y += (self.y - (paddle.y + paddle.length / 2)) * 0.03
            self.v_y += paddle.moving * 0.5
        self.normalize()
        self.v_x *= -1
        self.current_speed += 10
        self.last_touch = paddle.loc
        self.sending_data = True

    def normalize(self):
        m = math.sqrt(self.v_x ** 2 + self.v_y ** 2)
        self.v_x /= m
        self.v_y /= m
