import asyncio
import os
import pickle
import time

import neat

import game.consumers
from game.ai_room import AIRoom


class AIGame:

    def __init__(self, room):
        self.genome2 = None
        self.genome1 = None
        self.room = room
        self.ball = self.room.ball

    # def train_ai(self, genome1, genome2, config):
    #     net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    #     net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
    #
    #     run = True
    #
    #     self.genome1 = genome1
    #     self.genome2 = genome2
    #
    #     start_time = time.time()
    #     last_time = start_time
    #
    #     loop = asyncio.get_event_loop()
    #
    #     while run:
    #         delta_time = time.time() - last_time
    #         last_time = time.time()
    #         loop.run_until_complete(self.room.update())
    #         old_pos = [self.room.left_paddle.y, self.room.right_paddle.y]
    #         self.ai_movement(net1, net2, delta_time)
    #         new_pos = [self.room.left_paddle.y, self.room.right_paddle.y]
    #         if new_pos[0] != old_pos[0]:
    #             self.room.send_left = True
    #         if new_pos[1] != old_pos[1]:
    #             self.room.send_right = True
    #         # print(old_pos, new_pos)
    #         # print(old_pos == new_pos)
    #         if self.room.left_paddle.score > 0 or self.room.right_paddle.score > 0:
    #             # print("score > 0")
    #             if self.room.left_paddle.score > 0 and self.room.left_paddle.hit > 0:
    #                 self.genome1.fitness += 1
    #             elif self.room.right_paddle.score > 0 and self.room.right_paddle.hit > 0:
    #                 self.genome2.fitness += 1
    #             run = False
    #     self.compute_fitness(last_time - start_time)
    #
    # def ai_movement(self, net1, net2, delta_time):
    #     players = [(self.genome1, net1, self.room.left_paddle, True),
    #                (self.genome2, net2, self.room.right_paddle, False)]
    #     i = 1
    #     for genome, net, paddle, left in players:
    #         if i == 1:
    #             # print((paddle.y / 100, abs(0.02 - self.room.ball.x / 100), self.room.ball.y / 100, self.room.ball.v_x,
    #             #        self.room.ball.v_y))
    #             output = net.activate(
    #                 (paddle.y / 100, abs(0.02 - self.room.ball.x / 100), self.room.ball.y / 100, self.room.ball.v_x,
    #                  self.room.ball.v_y))
    #         else:
    #             output = net.activate(
    #                 (paddle.y / 100, abs(0.98 - self.room.ball.x / 100), self.room.ball.y / 100, self.room.ball.v_x,
    #                  self.room.ball.v_y))
    #
    #         decision = output.index(max(output))
    #         # print(i, decision)
    #         value = paddle.speed * delta_time
    #         if decision == 1:
    #             self.move_paddle(-value, genome, left=left)
    #         elif decision == 0:
    #             genome.fitness -= 0.02
    #         else:
    #             self.move_paddle(value, genome, left=left)
    #         i += 1

    def train_ai(self, genome1, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)

        run = True

        self.genome1 = genome1

        start_time = time.time()
        last_time = start_time

        loop = asyncio.get_event_loop()

        while run:
            # if self.room.left_paddle.score > 0:
            #     self.genome1.fitness -= abs(self.room.left_paddle.y - self.room.ball.y) / 75
            delta_time = time.time() - last_time
            last_time = time.time()
            loop.run_until_complete(self.room.update())
            old_pos = self.room.left_paddle.y
            # print("ball x =", self.room.ball.x)
            self.ai_movement(net1, delta_time)
            new_pos = self.room.left_paddle.y
            if new_pos != old_pos:
                self.room.send_left = True
            if self.room.left_paddle.score > 0:
                # print("score > 0")
                run = False
        self.compute_fitness(last_time - start_time)

    def ai_movement(self, net1, delta_time):
        i = 1
        # print("y:", self.room.left_paddle.y / 100, " | x:", abs(0.02 - self.room.ball.x / 100), " | ball.y:",
        #       self.room.ball.y / 100)
        # print(self.room.left_paddle.y / 100, abs(0.02 - self.room.ball.x / 100), self.room.ball.y / 100)
        output = net1.activate(
            (self.room.left_paddle.y / 100, abs(0.02 - self.room.ball.x / 100), self.room.ball.y / 100,
             self.room.ball.v_x,
             self.room.ball.v_y))
        decision = output.index(max(output))
        # print(decision)
        # print(i, decision)
        value = self.room.left_paddle.speed * delta_time
        if decision == 1:
            self.move_paddle(-value, self.genome1, left=True)
        elif decision == 0:
            self.genome1.fitness -= 0.005
        else:
            self.move_paddle(value, self.genome1, left=True)
        i += 1

    def move_paddle(self, value, genome, left=True):
        # print("ai should move", value)
        if left:
            is_valid = self.room.left_paddle.force_move(value)
        else:
            is_valid = self.room.right_paddle.force_move(value)

        if not is_valid:
            genome.fitness -= 0.005

    def compute_fitness(self, duration):
        self.genome1.fitness += self.room.left_paddle.hit * 8
        self.genome1.fitness -= self.room.left_paddle.dist / 100
        # self.genome2.fitness += self.room.left_paddle.hit * 3 + duration
        # self.genome2.fitness -= self.room.left_paddle.dist / 100


def eval_genomes(genomes, config):
    room = AIRoom(69)
    game.consumers.group_rooms["69"] = room
    loop = asyncio.get_event_loop()

    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
        for j in range(1):
            # print(genome_id1, "vs wall")
            ai_game = AIGame(room)
            loop.run_until_complete(room.reset())
            ai_game.train_ai(genome1, config)
            print(ai_game.genome1.fitness)

        # for genome_id2, genome2 in genomes[min(len(genomes) - 1, i + 1):]:
        #     print(genome_id1, "vs", genome_id2)
        # genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
        # ai_game = AIGame(room)
        # loop.run_until_complete(room.reset())
        # ai_game.train_ai(genome1, genome2, config)


def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4-5inputs')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.Checkpointer(1))

    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 100)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
