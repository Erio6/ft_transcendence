import asyncio
import os
import time
from math import trunc

import neat
from twisted.web.html import output

import game.consumers
from game.room import Room


class AIGame:

    def __init__(self, room):
        self.genome2 = None
        self.genome1 = None
        self.room = room
        self.left_paddle = self.room.left_paddle
        self.right_paddle = self.room.right_paddle
        self.ball = self.room.ball

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True

        self.genome1 = genome1
        self.genome2 = genome2

        start_time = time.time()
        last_time = start_time

        loop = asyncio.get_event_loop()

        while run:
            delta_time = time.time() - last_time
            last_time = time.time()
            loop.run_until_complete(self.room.update())
            self.ai_movement(net1, net2, delta_time)
            if self.room.left_paddle.score > 0 or self.room.right_paddle.score > 0:
                run = False
        self.compute_fitness(last_time - start_time)

    def ai_movement(self, net1, net2, delta_time):
        players = [(self.genome1, net1, self.left_paddle, True), (self.genome2, net2, self.right_paddle, False)]
        for genome, net, paddle, left in players:
            output = net.activate((paddle.y, abs(paddle.x - self.ball.x), self.ball.y, self.ball.v_x, self.ball.v_y))
            decision = output.index(max(output))
            value = paddle.speed * delta_time
            if decision == 0:
                genome.fitness -= 0.01
            elif decision == 1:
                self.move_paddle(-value, genome, left=left)
            else:
                self.move_paddle(value, genome, left=left)

    def move_paddle(self, value, genome, left=True):
        isValid = True
        if left:
            isValid = self.left_paddle.force_move(value)
        else:
            isValid = self.right_paddle.force_move(value)

        if not isValid:
            genome.fitness -= 1

    def compute_fitness(self, duration):
        self.genome1.fitness += duration + self.left_paddle.hit
        self.genome2.fitness += duration + self.right_paddle.hit


def eval_genomes(genomes, config):
    room = Room(True)
    game.consumers.group_rooms["69"] = room
    loop = asyncio.get_event_loop()
    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0

        for genome_id2, genome2 in genomes[min(len(genomes) - 1, i + 1):]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            ai_game = AIGame(room)
            loop.run_until_complete(room.reset())
            ai_game.train_ai(genome1, genome2, config)


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
