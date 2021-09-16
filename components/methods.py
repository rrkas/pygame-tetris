import random

import pygame

from .models import Piece
from .constants import constants
from .shapes import shapes


def create_grid(locked_positions):
    locked_positions = locked_positions or {}
    grid = [[constants.initial_bgcolor for _ in range(10)] for __ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid


def get_piece():
    return Piece(5, 0, random.choice(shapes))


def draw_grid(surface, grid):
    sx = constants.top_left_x
    sy = constants.top_left_y

    for i in range(len(grid)):
        pygame.draw.line(
            surface,
            constants.grid_line_color,
            (sx, sy + i * constants.block_size),
            (sx + constants.play_width, sy + i * constants.block_size)
        )
        for j in range(len(grid[0])):
            pygame.draw.line(
                surface,
                constants.grid_line_color,
                (sx + j * constants.block_size, sy),
                (sx + j * constants.block_size, sy + i * constants.play_height)
            )


def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render(constants.app_name, 1, constants.label_color)
    surface.blit(
        label,
        (constants.top_left_x + (constants.play_width / 2) - (label.get_width() / 2), constants.block_size)
    )

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (
                    constants.top_left_x + j * constants.block_size,
                    constants.top_left_y + i * constants.block_size,
                    constants.block_size,
                    constants.block_size,
                ),
                0,
            )
    pygame.draw.rect(
        surface,
        constants.game_border_color,
        (
            constants.top_left_x,
            constants.top_left_y,
            constants.play_width,
            constants.play_height,
        ),
        4,
    )

    draw_grid(surface, grid)
    pygame.display.update()


def clear_rows(grid, locked):
    pass


def convert_shape_format(shape):
    pass


def valid_space(shape, grid):
    pass


def check_lost(positions):
    pass


def draw_text_middle(text, size, color, surface):
    pass


def draw_next_shape(shape, surface):
    pass
