import datetime
import random

random.seed(datetime.datetime.now())


class TetrisShape:
    def __init__(self, shape_lists: list, color: tuple):
        self.shape_lists = shape_lists
        self.color = color


class Piece:
    def __init__(self, x: float, y: float, shape: TetrisShape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = int(random.random() * len(shape.shape_lists))


class GameState:
    running = 0
    paused = 1
    over = 2
