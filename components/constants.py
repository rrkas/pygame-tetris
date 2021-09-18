# 10 x 20 square grid
import pygame


class Constants:
    def __init__(self):
        # strings
        self.app_name = "Tetris"
        self.best_score_filename = "best_score.txt"

        # dimensions
        self.block_size = 30

        self.rows = 15
        self.cols = 10

        self.play_width = self.block_size * self.cols
        self.play_height = self.block_size * self.rows

        self.s_width = self.play_width + 500
        self.s_height = self.play_height + 100

        self.top_left_x = (self.s_width - self.play_width) // 2
        self.top_left_y = self.s_height - self.play_height

        self.padding_bottom = 50

        self.gap_score = 10

        # colors
        self.grid_line_color = (0, 0, 0, 128)
        self.label_color = (255, 255, 255)
        self.initial_bgcolor = (128, 128, 128)
        self.game_border_color = (255, 0, 0)

        # fonts
        self.font_global = "comicsans"
        self.font_appname_size = 60
        self.font_sidetext_size = 30

        # time
        self.exit_delay_secs = 1.5

        # keys
        self.continue_keys = [pygame.K_KP_ENTER, pygame.K_RETURN]
        self.exit_pause_keys = [pygame.K_ESCAPE]


constants = Constants()
