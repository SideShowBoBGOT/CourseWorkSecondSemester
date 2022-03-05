import pygame
from constants import MAP_SIZE
from game_objects import Player, Battleship, Game

pygame.init()
pygame.display.set_caption("Battleship")

# global variables

SQ_SIZE = 30
H_MARGIN = SQ_SIZE * 4
V_MARGIN = SQ_SIZE
WIDTH = SQ_SIZE * MAP_SIZE * 2 + H_MARGIN
HEIGHT = SQ_SIZE * MAP_SIZE * 2 + V_MARGIN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INDENT = 8

# COLORS
GREY = (40, 50, 60)
WHITE = (255, 250, 250)
GREEN = (50, 200, 150)
BLUE = (50, 150, 200)
RED = (250, 50, 100)
ORANGE = (250, 140, 20)
COLORS = {"U": GREY, "M": BLUE, 'H': ORANGE, "S": RED}


# function to draw a grid
def draw_grid(player, left=0, top=0, search=False):
    for i in range(121):
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
            WIDTH = ship.size * SQ_SIZE - INDENT * 2
            HEIGHT = SQ_SIZE - INDENT * 2
        elif ship.orientation == 'v':
            WIDTH = SQ_SIZE - INDENT * 2
            HEIGHT = ship.size * SQ_SIZE - INDENT * 2
        rectangle = pygame.Rect(x, y, WIDTH, HEIGHT)
        pygame.draw.rect(SCREEN, GREEN, rectangle, border_radius=15)


# pygame loop
game = Game()

run = True
pause = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            exit()

        # user mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if game.player1_turn and x < SQ_SIZE*MAP_SIZE and y < SQ_SIZE*MAP_SIZE:
                row = y // SQ_SIZE
                col = x // SQ_SIZE
                index = row * MAP_SIZE + col
                game.make_move(index)
            elif not game.player1_turn and x > WIDTH - SQ_SIZE*MAP_SIZE and y > SQ_SIZE*MAP_SIZE + V_MARGIN:
                row = (y - SQ_SIZE*MAP_SIZE - V_MARGIN) // SQ_SIZE
                col = (x - SQ_SIZE * MAP_SIZE - H_MARGIN) // SQ_SIZE
                index = row * MAP_SIZE + col
                game.make_move(index)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                pause = not pause
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

        pygame.display.flip()
