class Button:
    """
    Клас, що представляє кнопку

    ...

    Атрибути
    --------
    x               :   int
        Позиція кнопки по горизонталі
    y               :   int
        Позиція кнопки по вертикалі
    font            :   pygame.Font
        Шрифт тексту
    base_color      :   tuple
        Базовий колір кнопки
    hovering_color  :   tuple
        Другорядний колір кнопки
    text_input      :   str
        Текст кнопки
    text            :   pygame.SysFont
        Власне рендерений текст кнопки
    text_rect       :   pygame.Rect
        Прямокутник тексту
    func            :   FunctionType
        Функція, прив'язана до кнопки

    Методи
    ------

    ********************************************************
    ********************************************************
    def __init__(self, pos, font, text_input, base_color, hovering_color, func)
        Конструктор класу

        Аргументи:

        1) self - об'єкт класу
        2) pos - позиція миші
        3) font - шрифт тексту
        4) text_input - текст кнопки
        5) base_color - основний колір
        6) hovering_color - другорядний колір
        7) func - функція

        Повертає: None
    ********************************************************
    ********************************************************
    def update(self, screen)
        Відображає об'єкт класу на екрані

        Аргументи:

        1) self - об'єкт класу
        2) screen - екран

        Повертає: None
    ********************************************************
    ********************************************************
    def check_for_input(self, position)
        Відображає об'єкт класу на екрані

        Аргументи:

        1) self - об'єкт класу
        2) position - позиція миші

        Повертає: bool
    ********************************************************
    ********************************************************
    def change_color(self, position)
        Змінює колір при наведенні

        Аргументи:

        1) self - об'єкт класу
        2) position - позиція миші

        Повертає: None
    ********************************************************
    ********************************************************
    """

    def __init__(self, pos, font, text_input, base_color, hovering_color, func):
        self.__x = pos[0]
        self.__y = pos[1]
        self.__font = font
        self.__base_color = base_color
        self.__hovering_color = hovering_color
        self.__text_input = text_input
        self.__text = self.__font.render(self.__text_input, False,
                                         self.__base_color, self.__hovering_color)
        self.__text_rect = self.text.get_rect(center=(self.__x, self.__y))
        self.__func = func

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, value):
        self.__font = value

    @property
    def base_color(self):
        return self.__base_color

    @base_color.setter
    def base_color(self, value):
        self.__base_color = value

    @property
    def hovering_color(self):
        return self.__hovering_color

    @hovering_color.setter
    def hovering_color(self, value):
        self.__hovering_color = value

    @property
    def text_input(self):
        return self.__text_input

    @text_input.setter
    def text_input(self, value):
        self.__text_input = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def text_rect(self):
        return self.__text_rect

    @text_rect.setter
    def text_rect(self, value):
        self.__text_rect = value

    @property
    def func(self):
        return self.__func

    @func.setter
    def func(self, value):
        self.__func = value

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) \
                and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) \
                and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, False, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, False, self.base_color)
