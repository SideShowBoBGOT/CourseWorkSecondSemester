import pygame
import sys
from game_constants import FONT_SIZE, WIDTH, HEIGHT
from game_colors import GREY, LIGHT_GREY, WHITE
from game_objects import Button, TumblerButton
from other_functions import get_font


class Menu:
    def __init__(self, screen, text, buttons, funcs):
        self.screen = screen
        self.text = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
        self.rect = self.text.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        self.buttons = []
        for button, func in zip(enumerate(buttons), funcs):
            self.buttons.append(button[1][1](pos=(WIDTH // 2, HEIGHT // 3 + FONT_SIZE * button[0]),
                                             text_input=button[1][0],
                                             font=get_font(FONT_SIZE), base_color=WHITE,
                                             hovering_color=LIGHT_GREY, func=func))

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
                            if button.__class__.__name__ == Button.__name__:
                                button.func(**(kwargs[button.text_input]))
                            elif button.__class__.__name__ == TumblerButton.__name__:
                                button.switched = not button.switched
            pygame.display.update()


def options(screen):
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill(GREY)

        OPTIONS_TEXT = get_font(FONT_SIZE).render('OPTIONS', False, GREY, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(pos=(WIDTH // 2, HEIGHT // 1.5), text_input='BACK',
                              font=get_font(FONT_SIZE), base_color=WHITE,
                              hovering_color=LIGHT_GREY, func=None)

        OPTIONS_BACK.change_color(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

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
