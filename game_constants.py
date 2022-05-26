"""
Модуль для зберігання ігрових констант
"""
#Назва
TITLE = 'Battleship'
#Розмір пами
MAP_SIZE = 11
#Кораблі
SHIPS_SIZES = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5]
#Шрифт
FONT_NAME = 'fresansttf'
#Розмір шрифта
FONT_SIZE = 100
#Розмір клітинки
SQ_SIZE = 30
#Ширина градки
INDENT = 8
#Відступ між градками по горизонталі
H_MARGIN = SQ_SIZE * 4
#Відступ між градками по вертикалі
V_MARGIN = SQ_SIZE
#Ширина екрана
WIDTH = SQ_SIZE * MAP_SIZE * 2 + H_MARGIN
#Висота екрана
HEIGHT = SQ_SIZE * MAP_SIZE * 2 + V_MARGIN
