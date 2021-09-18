class TetrisShape:
    def __init__(self, shape_lists: list, color: tuple):
        self.shape_lists = shape_lists
        self.color = color


class Piece:
    def __init__(self, x, y, shape: TetrisShape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0
