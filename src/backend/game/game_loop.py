import asyncio
import time

from .consumers import connected_clients, ball


async def game_loop():
    last_time = time.time()

    while True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        await ball.wall_collide()

        for consumer, paddle in connected_clients.items():
            await paddle.move(delta_time)
            await ball.paddles_collide_check(paddle)

        await ball.send_data(connected_clients)
        await ball.send_score(connected_clients)
        await ball.move(delta_time)

        await asyncio.sleep(1 / 60)
