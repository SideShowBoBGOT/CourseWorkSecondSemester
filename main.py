import pygame

pygame.init()
pygame.display.set_caption("Battleship")

# global variables
sq_size = 30
h_margin = sq_size * 4
v_margin = sq_size
width = sq_size * 11 * 2 + h_margin
height = sq_size * 11 * 2 + v_margin
screen = pygame.display.set_mode((width, height))

# colors
grey = (40, 50, 60)
white = (255, 250, 250)


# function to draw a grid
def draw_grid(left=0, top=0):
    for i in range(121):
        x = left + i % 11 * sq_size
        y = top + i // 11 * sq_size
        square = pygame.Rect(x, y, sq_size, sq_size)
        pygame.draw.rect(screen, white, square, width=3)



# pygame loop
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
        screen.fill(grey)
        draw_grid()
        draw_grid(left=(width-h_margin)//2 + h_margin)

        draw_grid(left=(width-h_margin)//2 + h_margin, top=(height-v_margin)//2 + v_margin)
        draw_grid(top=(height-v_margin)//2 + v_margin)
        pygame.display.flip()
