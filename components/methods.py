import os
import random

import pygame

from .constants import constants
from .models import Piece
from .shapes import shapes


# grid: colors in each cell

# initialize color grid
def create_grid(locked_positions):
    locked_positions = locked_positions or {}
    grid = [
        [constants.initial_bgcolor for _ in range(constants.cols)]
        for __ in range(constants.rows)
    ]

    for i in range(constants.rows):
        for j in range(constants.cols):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid


# randomly choose piece
def get_piece():
    return Piece(5, 0, random.choice(shapes))


# draw grid lines on screen
def draw_grid(surface):
    sx = constants.top_left_x
    sy = constants.top_left_y

    for i in range(constants.rows):
        pygame.draw.line(
            surface,
            constants.grid_line_color,
            (sx, sy + i * constants.block_size),
            (sx + constants.play_width, sy + i * constants.block_size),
        )
    for j in range(constants.cols):
        pygame.draw.line(
            surface,
            constants.grid_line_color,
            (sx + j * constants.block_size, sy),
            (sx + j * constants.block_size, sy + constants.play_height),
        )


# rotate shape
def convert_shape_format(shape: Piece):
    positions = []
    formatted = shape.shape.shape_lists[shape.rotation % len(shape.shape.shape_lists)]
    for i, line in enumerate(formatted):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((shape.x + j - 2, shape.y + i - 4))

    return positions


# render title, bg, grid
def draw_window(surface, grid):
    surface.fill(constants.initial_bgcolor)
    pygame.font.init()
    font = pygame.font.SysFont(constants.font_global, constants.font_appname_size)
    label = font.render(constants.app_name, 1, constants.label_color)
    surface.blit(
        label,
        (
            constants.top_left_x + (constants.play_width / 2) - (label.get_width() / 2),
            constants.block_size,
        ),
    )

    for i in range(constants.rows):
        for j in range(constants.cols):
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

    draw_grid(surface)

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


# check space validity
def valid_space(shape, grid):
    accepted_pos = [
        [
            (j, i)
            for j in range(constants.cols)
            if grid[i][j] == constants.initial_bgcolor
        ]
        for i in range(constants.rows)
    ]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


# check if game is lost
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# draw next shape on side
def draw_next_shape(shape: Piece, surface):
    font = pygame.font.SysFont(constants.font_global, constants.font_sidetext_size)
    label = font.render("Next Shape", 1, constants.label_color)

    sx = constants.top_left_x + constants.play_width + 50
    sy = constants.top_left_y + constants.play_height / 2 - 100
    surface.blit(label, (sx + 10, sy - 30))

    formatted = shape.shape.shape_lists[shape.rotation % len(shape.shape.shape_lists)]

    for i, line in enumerate(formatted):
        row = list(line)
        for j, col in enumerate(row):
            if col == "0":
                pygame.draw.rect(
                    surface,
                    shape.shape.color,
                    (
                        sx + j * constants.block_size,
                        sy + i * constants.block_size,
                        constants.block_size,
                        constants.block_size,
                    ),
                    0,
                )
                pygame.draw.line(
                    surface,
                    constants.grid_line_color,
                    (sx + j * constants.block_size, sy + i * constants.block_size),
                    (
                        sx + (j + 1) * constants.block_size,
                        sy + i * constants.block_size,
                    ),
                )
                pygame.draw.line(
                    surface,
                    constants.grid_line_color,
                    (sx + j * constants.block_size, sy + i * constants.block_size),
                    (
                        sx + j * constants.block_size,
                        sy + (i + 1) * constants.block_size,
                    ),
                )


# clear the filled rows and shift blocks
def clear_rows(grid, locked):
    inc, ind = 0, 0
    for i in range(constants.rows - 1, -1, -1):
        row = grid[i]
        if constants.initial_bgcolor not in row:
            inc += 1
            ind = i
            for j in range(constants.cols):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


# for game over and start game
def draw_text_middle(surface, text, size, color, vertical_center=True, margin_top=0):
    font = pygame.font.SysFont(constants.font_global, size, bold=True)
    label = font.render(text, 1, color)

    if vertical_center:
        surface.blit(
            label,
            (
                constants.top_left_x
                + constants.play_width / 2
                - (label.get_width() / 2),
                constants.play_height / 2
                - (label.get_height() / 2)
                + constants.padding_bottom,
            ),
        )
    else:
        surface.blit(
            label,
            (
                constants.top_left_x
                + constants.play_width / 2
                - (label.get_width() / 2),
                margin_top,
            ),
        )


# save best score
def save_best_score(score):
    with open(constants.best_score_filename, "w") as f:
        f.write(str(score))


# get best score
def get_best_score():
    if not os.path.exists(constants.best_score_filename):
        return None
    with open(constants.best_score_filename, "r") as f:
        score = f.readline()
        return int(score if len(score) > 0 else 0)
