"""
Модуль, що описує додаткові функції
"""
import pygame
from game_constants import FONT_NAME



def get_font(font_size):
    """
    Функція, що видає шрифт потрібного розміру
    :param font_size: int
    :return: pygame.SysFont
    """
    return pygame.font.Font(FONT_NAME, font_size)
