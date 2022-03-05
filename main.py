import pygame
from constants import MAP_SIZE
from game_objects import Player, Battleship
pygame.init()
pygame.display.set_caption("Battleship")

# global variables

sq_size = 30
h_margin = sq_size * 4
v_margin = sq_size
width = sq_size * MAP_SIZE * 2 + h_margin
height = sq_size * MAP_SIZE * 2 + v_margin
screen = pygame.display.set_mode((width, height))

# colors
grey = (40, 50, 60)
white = (255, 250, 250)
green = (50, 200, 150)

# function to draw a grid
def draw_grid(left=0, top=0):
    for i in range(121):
        x = left + i % MAP_SIZE * sq_size
        y = top + i // MAP_SIZE * sq_size
        square = pygame.Rect(x, y, sq_size, sq_size)
        pygame.draw.rect(screen, white, square, width=3)

# function to draw ships onto the position grids
def draw_ships(player, left=0, top=0):
    for ship in player.ships:
        x = left + ship.col * sq_size
        y = top + ship.row * sq_size
        if ship.orientation == 'h':
            width = ship.size * sq_size
            height = sq_size
        elif ship.orientation == 'v':
            width = sq_size
            height = ship.size * sq_size
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, green, rectangle)

# pygame loop
player = Player()
run = True
pause = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                pause = not pause
    if not pause:
        # draw background
        screen.fill(grey)

        # draw search grids
        draw_grid()
        draw_grid(left=(width - h_margin) // 2 + h_margin)

        # draw position grids
        draw_grid(left=(width - h_margin) // 2 + h_margin, top=(height - v_margin) // 2 + v_margin)
        draw_grid(top=(height - v_margin) // 2 + v_margin)

        # draw ships onto position grids
        draw_ships(player)

        pygame.display.flip()
