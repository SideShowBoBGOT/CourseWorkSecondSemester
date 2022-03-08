import pygame
from game_constants import FONT_NAME


# function to get font of certain size
def get_font(font_size):
    return pygame.font.SysFont(FONT_NAME, font_size)
