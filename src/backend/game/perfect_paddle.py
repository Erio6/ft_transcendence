from game.paddle import Paddle


class PerfectPaddle(Paddle):
    def __init__(self, loc, consumer, name):
        super().__init__(loc, consumer, name)
        self.new_pos = 50
        self.direction = 0

    def compute_pos(self, ball):
        if ball.last_touch == self.loc:
            self.new_pos = 50
            self.direction = 1 if self.y < 50 else -1
        else:
            velocity_x = ball.v_x * ball.current_speed
            velocity_y = ball.v_y * ball.current_speed
            target_x = 2 if self.loc == "left" else 98

            time = (target_x - ball.x) / velocity_x
            naive_y = ball.y + time * velocity_y
            bounce_range = 2 * (100 - ball.radius / 2)
            remainder = naive_y % bounce_range
            if remainder > 100 - ball.radius / 2:
                self.new_pos = 2 * (100 - ball.radius / 2) - remainder
            else:
                self.new_pos = remainder
            if self.new_pos > self.y:
                self.direction = 1
            elif self.new_pos < self.y:
                self.direction = -1
            else:
                self.direction = 0
        print(self.new_pos, self.direction)

    async def move(self, delta_time, room):
        if self.direction != 0:
            value = self.speed * delta_time * self.direction
            self.y += value

            if self.y > 100 - self.length / 2:
                self.y = 100 - self.length / 2
                self.direction = 0
            elif self.y < self.length / 2:
                self.y = self.length / 2
                self.direction = 0
            elif self.direction == -1 and self.y <= self.new_pos:
                self.direction = 0
            elif self.direction == 1 and self.y >= self.new_pos:
                self.direction = 0

            for consumer in room.get_consumers(self.loc != "left", self.loc != "right"):
                await self.send_data_chan(consumer)
