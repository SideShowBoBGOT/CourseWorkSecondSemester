import sys
import pygame
from game_colors import GREY, WHITE
from game_constants import MAP_SIZE, FONT_SIZE, \
    SQ_SIZE, H_MARGIN, V_MARGIN, WIDTH, HEIGHT, SHIPS_SIZES
from game_classes import Game, Grid, Button, Battleship, Player, TumblerButton
from other_functions import get_font


def pre_play(screen, options_menu):
    game = Game(options_menu.buttons[0].switched, options_menu.buttons[1].switched)

    for player in (game.player1, game.player2):
        if player.is_human:
            buttons = []
            used_buttons = []
            # create buttons
            for i, size in enumerate(SHIPS_SIZES):
                x = i % 4
                y = i // 4
                button = TumblerButton((SQ_SIZE * MAP_SIZE + x * SQ_SIZE + SQ_SIZE * 0.5,
                                        y * SQ_SIZE + SQ_SIZE), get_font(SQ_SIZE),
                                       str(size), GREY, WHITE, None)
                buttons.append(button)

            while True:
                GAME_MOUSE_POSITION = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # click on buttons and chose size of a ship
                        for i1, button in enumerate(buttons):
                            if button.check_for_input(GAME_MOUSE_POSITION):
                                button.switched = not button.switched
                                button.change_color(GAME_MOUSE_POSITION)
                                for i2, other_button in enumerate(buttons):
                                    if i2 != i1:
                                        other_button.switched = False
                                        other_button.change_color(GAME_MOUSE_POSITION)
                                break
                        # chose square to put ship onto
                        for i1, button in enumerate(buttons):
                            if button.switched:
                                x, y = GAME_MOUSE_POSITION
                                if x < SQ_SIZE * MAP_SIZE and y > SQ_SIZE * MAP_SIZE + V_MARGIN:
                                    orientation = 'h' if pygame.mouse.get_pressed()[0] else 'v'
                                    row = (y - SQ_SIZE * MAP_SIZE - V_MARGIN) // SQ_SIZE
                                    col = x // SQ_SIZE
                                    ship = Battleship(size=int(button.text_input), row=row,
                                                      col=col, orientation=orientation)
                                    if player.check_ship(ship):
                                        player.ships.append(ship)
                                        used_buttons.append(buttons.pop(i1))
                                        for i2, other_button in enumerate(buttons):
                                            x = i2 % 4
                                            y = i2 // 4
                                            other_button.text_rect = other_button.text.get_rect(center=
                                            (
                                                SQ_SIZE * MAP_SIZE + x * SQ_SIZE + SQ_SIZE * 0.5,
                                                y * SQ_SIZE + SQ_SIZE))
                                break
                            # chose ship to be replaced
                            for i1, ship in enumerate(player.ships):
                                x, y = GAME_MOUSE_POSITION
                                if x < SQ_SIZE * MAP_SIZE and y > SQ_SIZE * MAP_SIZE + V_MARGIN:
                                    row = (y - SQ_SIZE * MAP_SIZE - V_MARGIN) // SQ_SIZE
                                    col = x // SQ_SIZE
                                    index = row * MAP_SIZE + col
                                    if index in ship.ship_indexes:
                                        for i2, used_button in enumerate(used_buttons):
                                            if ship.size == int(used_button.text_input):
                                                used_button.switched = False
                                                used_button.change_color(GAME_MOUSE_POSITION)
                                                buttons.append(used_buttons.pop(i2))
                                                break
                                        buttons.sort(key=lambda x: int(x.text_input), reverse=True)
                                        for i3, button in enumerate(buttons):
                                            x = i3 % 4
                                            y = i3 // 4
                                            button.text_rect = button.text.get_rect(center=
                                            (
                                                SQ_SIZE * MAP_SIZE + x * SQ_SIZE + SQ_SIZE * 0.5,
                                                y * SQ_SIZE + SQ_SIZE))
                                        player.ships.pop(i1)

                screen.fill(GREY)
                # draw_grid search grids
                search_grid1 = Grid(screen=screen, player=None)
                search_grid2 = Grid(screen=screen, player=None,
                                    left=(WIDTH - H_MARGIN) // 2 + H_MARGIN,
                                    top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
                search_grid1.draw_grid()
                search_grid2.draw_grid()
                # draw_grid buttons
                for button in buttons:
                    button.update(screen)
                # draw_grid position grids
                position_grid1 = Grid(screen=screen, player=game.player1,
                                      top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
                position_grid2 = Grid(screen=screen, player=game.player2,
                                      left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)
                position_grid1.draw_grid()
                position_grid2.draw_grid()

                # draw_grid ships onto position grids
                position_grid1.draw_ships()
                pygame.display.update()

    play(screen, game)


# function to play game
def play(screen, game):
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
            screen.fill(GREY)
            # draw_grid search grids
            search_grid1 = Grid(screen=screen, player=game.player1)
            search_grid2 = Grid(screen=screen, player=game.player2,
                                left=(WIDTH - H_MARGIN) // 2 + H_MARGIN,
                                top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
            search_grid1.draw_grid(search=True)
            search_grid2.draw_grid(search=True)
            # draw_grid position grids
            position_grid1 = Grid(screen=screen, player=game.player1,
                                  top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
            position_grid2 = Grid(screen=screen, player=game.player2,
                                  left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)
            position_grid1.draw_grid()
            position_grid2.draw_grid()

            # draw_grid ships onto position grids
            position_grid1.draw_ships()
            position_grid2.draw_ships()

            # computer moves
            if not game.over and game.computer_turn:
                game.basic_ai()

            # game over message
            if game.over:
                text = "Player " + str(game.result) + " wins!"
                textbox = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
                screen.blit(textbox, (WIDTH // 5, HEIGHT // 2.22))
        elif pause and not game.over:
            text = "Pause"
            textbox = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
            screen.blit(textbox, (WIDTH // 2.7, HEIGHT // 2.22))
        pygame.time.delay(0)
        pygame.display.flip()
