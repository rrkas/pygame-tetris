from components.methods import *

pygame.font.init()


def main(surface):
    locked_positions = {}

    sx = constants.top_left_x + constants.play_width + 50
    sy = constants.top_left_y + constants.play_height / 2 - 100

    change_piece = False
    run = True
    current_piece = get_piece()
    next_piece = get_piece()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.4
    level_time = 0
    level = 1
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.22:
                fall_speed -= 0.005
                level += 1

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(
                        current_piece.shape.shape_lists
                    )
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(
                            current_piece.shape.shape_lists
                        )

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.shape.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.shape.color
            current_piece = next_piece
            next_piece = get_piece()
            change_piece = False

            # update score
            score += clear_rows(grid, locked_positions) * 10
            pygame.display.update()

        draw_window(surface, grid)
        draw_next_shape(next_piece, surface)

        font = pygame.font.SysFont(constants.font_global, constants.font_sidetext_size)
        label = font.render(f"Score: {score or 0}", 1, constants.label_color)
        surface.blit(label, (sx + 30, sy + 160))

        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(
                surface,
                "Game Over!",
                constants.font_appname_size,
                constants.label_color,
            )
            pygame.display.update()
            pygame.time.delay(int(constants.exit_delay_secs * 1000))
            run = False

    return score


def main_menu(surface):
    run = True
    score = None
    best_score = get_best_score()
    while run:
        surface.fill(constants.initial_bgcolor)
        draw_text_middle(
            surface,
            "Press any key to Play!",
            constants.font_appname_size,
            constants.label_color,
        )
        if score is not None:
            if best_score is None:
                best_score = score
            else:
                best_score = max(best_score, score)
                save_best_score(best_score)
            draw_text_middle(
                surface,
                f"Score: {score}",
                constants.font_sidetext_size,
                constants.label_color,
                vertical_center=False,
                margin_top=(constants.s_height + constants.padding_bottom) / 2
                + constants.font_appname_size
                + constants.gap_score,
            )
        if best_score is not None:
            draw_text_middle(
                surface,
                f"Best Score: {best_score}",
                constants.font_sidetext_size,
                constants.label_color,
                vertical_center=False,
                margin_top=(constants.s_height + constants.padding_bottom) / 2
                + constants.font_appname_size
                + constants.font_sidetext_size
                + 2 * constants.gap_score,
            )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                else:
                    score = main(surface)

    pygame.display.quit()


if __name__ == "__main__":
    surface = pygame.display.set_mode(
        (constants.s_width, constants.s_height + constants.padding_bottom)
    )
    pygame.display.set_caption(constants.app_name)
    main_menu(surface)
