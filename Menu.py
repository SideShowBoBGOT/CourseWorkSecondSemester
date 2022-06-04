import inspect
import sys
import pygame
from game_colors import WHITE, GREY, LIGHT_GREY
from game_constants import FONT_SIZE, WIDTH, HEIGHT
from other_functions import get_font
from Button import Button
from TumblerButton import TumblerButton


class Menu:
    """
    Клас, що представляє меню

    ...

    Атрибути
    --------

    screen : pygame.display.Surface
        Екран, на якому малюється меню
    text : pygame.SysFont
        Текст меню
    rect    : pygame.Rect
        Прямокутник тексту
    buttons : list
        Список кнопок меню

    Методи
    ------

    ********************************************************
    ********************************************************
    def __init__(self, screen, text, buttons, funcs)
        Конструктор класу

        Аргументи:

        1) self -об'єкт класу
        2) screen - екран
        3) text - основний текст
        4) buttons - об'єкти класу Buttons
        5) funcs - функції до кнопок

        Повертає: None
    ********************************************************
    ********************************************************
    def draw(self, **kwargs)
        Відображає об'єкт класу на екрані

        Аргументи:

        1) self - об'єкт класу
        2) **kwargs - словник назв кнопок та їх функцій

        Повертає: None
    ********************************************************
    ********************************************************
    """

    def __init__(self, screen, text, buttons, funcs):
        self.__screen = screen
        self.__text = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
        self.__rect = self.text.get_rect(center=(WIDTH // 2, HEIGHT // 5.5))
        self.__buttons = []
        indent = 0
        for button, func in zip(enumerate(buttons), funcs):
            self.__buttons.append(button[1][1](pos=(WIDTH // 2, HEIGHT // 3 + FONT_SIZE * button[0] + indent),
                                               text_input=button[1][0],
                                               font=get_font(FONT_SIZE), base_color=WHITE,
                                               hovering_color=LIGHT_GREY, func=func))
            indent += 30
        self.__buttons.append(Button(pos=(WIDTH // 2, HEIGHT // 3 + FONT_SIZE * (button[0] + 1) + indent),
                                     text_input='QUIT',
                                     font=get_font(FONT_SIZE), base_color=WHITE,
                                     hovering_color=LIGHT_GREY, func=None))

    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, value):
        self.__screen = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def buttons(self):
        return self.__buttons

    @buttons.setter
    def buttons(self, value):
        self.__buttons = value

    def draw(self, **kwargs):
        while True:
            self.screen.fill(GREY)
            self.screen.blit(self.text, self.rect)
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.change_color(mouse_pos)
                button.update(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.check_for_input(mouse_pos):
                            if button.text_input == 'QUIT':
                                return
                            elif button.__class__.__name__ == Button.__name__:
                                if inspect.signature(button.func).parameters:
                                    button.func(**(kwargs[button.text_input]))
                                else:
                                    button.func()
                            elif button.__class__.__name__ == TumblerButton.__name__:
                                button.switched = not button.switched
            pygame.display.update()
