"""
Основний файл, у якому створюються усі об'єкти
та ініціалізуються налаштування гри
"""
import pygame
from game_constants import TITLE, WIDTH, HEIGHT
from game_classes import Button, TumblerButton, Menu, Game

pygame.init()
pygame.font.init()
pygame.display.set_caption(TITLE)

is_human1 = True
is_human2 = True

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

OPTIONS_MENU_TEXT = 'OPTIONS'
OPTIONS_MENU_BUTTONS = [['PLAYER1', TumblerButton],
                        ['PLAYER2', TumblerButton]]
OPTIONS_MENU_FUNCS = [None, None]
options_menu = Menu(screen=SCREEN, text=OPTIONS_MENU_TEXT,
                    buttons=OPTIONS_MENU_BUTTONS,
                    funcs=OPTIONS_MENU_FUNCS)
options_menu.buttons[0].switched = False
options_menu.buttons[1].switched = False

game = Game(screen=SCREEN, options_menu=options_menu)

MAIN_MENU_TEXT = 'MAIN MENU'
MAIN_MENU_BUTTONS = [['PLAY', Button],
                     ['OPTIONS', Button]]
MAIN_MENU_FUNCS = [game.prepare_to_play, options_menu.draw]

main_menu = Menu(screen=SCREEN, text=MAIN_MENU_TEXT,
                 buttons=MAIN_MENU_BUTTONS,
                 funcs=MAIN_MENU_FUNCS)

main_menu.draw(PLAY={'None': None}, OPTIONS={'None': None})

