# 10 x 20 square grid


class Constants:
    def __init__(self):
        self.block_size = 30

        self.rows = 15
        self.cols = 10

        self.play_width = self.block_size * self.cols
        self.play_height = self.block_size * self.rows

        self.s_width = self.play_width + 100
        self.s_height = self.play_height + 100

        self.top_left_x = (self.s_width - self.play_width) // 2
        self.top_left_y = self.s_height - self.play_height
        self.app_name = 'Tetris'

        self.grid_line_color = (128, 128, 128, 128)
        self.label_color = (255, 255, 255)
        self.initial_bgcolor = (0, 0, 0)
        self.game_border_color = (255, 0, 0)


constants = Constants()
