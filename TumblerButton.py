from Button import Button


class TumblerButton(Button):
    """
    Клас, що представляє кнопку-тумблер

    ...

    Батьки класу
    ------------
    Button

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
    switched        :   bool
        Значення, чи є кнопка-тумблер увімкненою

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

        Повертає: None
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
        Button.__init__(self, pos, font, text_input, base_color, hovering_color, func)
        self.__switched = False

    @property
    def switched(self):
        return self.__switched

    @switched.setter
    def switched(self, value):
        self.__switched = value

    def update(self, screen):
        self.change_color()
        screen.blit(self.text, self.text_rect)

    def change_color(self, position=(0, 0)):
        if self.switched:
            self.text = self.font.render(self.text_input, False, self.hovering_color, self.base_color)
        else:
            self.text = self.font.render(self.text_input, False, self.base_color, self.hovering_color)
