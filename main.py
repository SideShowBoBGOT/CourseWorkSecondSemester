import sys

import pygame
from game_colors import GREY, WHITE, GREEN, LIGHT_GREY, COLORS
from game_constants import MAP_SIZE, FONT_NAME, FONT_SIZE, TITLE, \
    SQ_SIZE, INDENT, H_MARGIN, V_MARGIN, WIDTH, HEIGHT
from game_objects import Game, Button

pygame.init()
pygame.font.init()
pygame.display.set_caption(TITLE)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


# function to get font of certain size
def get_font(font_size):
    return pygame.font.SysFont(FONT_NAME, font_size)


# function to draw a grid
def draw_grid(player, left=0, top=0, search=False):
    for i in range(MAP_SIZE**2):
        x = left + i % MAP_SIZE * SQ_SIZE
        y = top + i // MAP_SIZE * SQ_SIZE
        square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width=3)
        if search:
            x += SQ_SIZE // 2
            y += SQ_SIZE // 2
            pygame.draw.circle(SCREEN, COLORS[player.search[i]], (x, y), radius=SQ_SIZE // 4)


# function to draw ships onto the position grids
def draw_ships(player, left=0, top=0):
    for ship in player.ships:
        x = left + ship.col * SQ_SIZE + INDENT
        y = top + ship.row * SQ_SIZE + INDENT
        if ship.orientation == 'h':
            width = ship.size * SQ_SIZE - INDENT * 2
            height = SQ_SIZE - INDENT * 2
        elif ship.orientation == 'v':
            width = SQ_SIZE - INDENT * 2
            height = ship.size * SQ_SIZE - INDENT * 2
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, GREEN, rectangle, border_radius=15)


# function to start main_menu
def main_menu():
    is_human1 = False
    is_human2 = False
    while True:
        SCREEN.fill(GREY)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(FONT_SIZE).render('MAIN MENU', False, GREY, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 5))

        PLAY_BUTTON = Button(pos=(WIDTH // 2, HEIGHT // 3), text_input='PLAY',
                             font=get_font(FONT_SIZE), base_color=WHITE,
                             hovering_color=LIGHT_GREY)
        OPTIONS_BUTTON = Button(pos=(WIDTH // 2, HEIGHT // 2), text_input='OPTIONS',
                                font=get_font(FONT_SIZE), base_color=WHITE,
                                hovering_color=LIGHT_GREY)
        QUIT_BUTTON = Button(pos=(WIDTH // 2, HEIGHT // 1.5), text_input='QUIT',
                             font=get_font(FONT_SIZE), base_color=WHITE,
                             hovering_color=LIGHT_GREY)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pre_play(is_human1, is_human2)
                if OPTIONS_BUTTON.check_for_input(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


# function to get options
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill(GREY)

        OPTIONS_TEXT = get_font(FONT_SIZE).render('OPTIONS', False, GREY, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(pos=(WIDTH // 2, HEIGHT // 1.5), text_input='BACK',
                              font=get_font(FONT_SIZE), base_color=WHITE,
                              hovering_color=LIGHT_GREY)

        OPTIONS_BACK.change_color(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.check_for_input(OPTIONS_MOUSE_POS):
                    return
            if event.type == pygame.K_ESCAPE:
                return

        pygame.display.update()


def pre_play(is_human1, is_human2):
    game = Game(is_human1, is_human2)
    play(game)


# function to play game
def play(game):
    pause = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # user mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                x, y = pygame.mouse.get_pos()
                if not game.over:
                    if game.player1_turn and x < SQ_SIZE * MAP_SIZE and y < SQ_SIZE * MAP_SIZE:
                        row = y // SQ_SIZE
                        col = x // SQ_SIZE
                        index = row * MAP_SIZE + col
                        game.make_move(index)
                    elif not game.player1_turn and x > WIDTH - SQ_SIZE * MAP_SIZE and y > SQ_SIZE * MAP_SIZE + V_MARGIN:
                        row = (y - SQ_SIZE * MAP_SIZE - V_MARGIN) // SQ_SIZE
                        col = (x - SQ_SIZE * MAP_SIZE - H_MARGIN) // SQ_SIZE
                        index = row * MAP_SIZE + col
                        game.make_move(index)
            if event.type == pygame.KEYDOWN:

                # escape key to close the animation
                if event.key == pygame.K_ESCAPE:
                    return
                # space bar to pause and unpause the animation
                if event.key == pygame.K_SPACE and not game.over:
                    pause = not pause

                # return key to restart the game
                if event.key == pygame.K_RETURN:
                    game = Game(game.is_human1, game.is_human2)

        if not pause:
            # draw background
            SCREEN.fill(GREY)

            # draw search grids
            draw_grid(game.player1, search=True)
            draw_grid(game.player2, search=True, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN,
                      top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)

            # draw position grids
            draw_grid(game.player1, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
            draw_grid(game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)

            # draw ships onto position grids
            draw_ships(game.player1, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
            draw_ships(game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)

            # computer moves
            if not game.over and game.computer_turn:
                game.basic_ai()

            # game over message
            if game.over:
                text = "Player " + str(game.result) + " wins!"
                textbox = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
                SCREEN.blit(textbox, (WIDTH // 5, HEIGHT // 2.22))
        elif pause and not game.over:
            text = "Pause"
            textbox = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
            SCREEN.blit(textbox, (WIDTH // 2.7, HEIGHT // 2.22))
        pygame.time.delay(0)
        pygame.display.flip()


main_menu()
