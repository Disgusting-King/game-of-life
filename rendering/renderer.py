import pygame
from core.board import *


def draw_board(screen: pygame.Surface, board: Board, cell_width: int, cell_height: int, 
               cell_living_color: tuple[int] | str, cell_dead_color: tuple[int] | str) -> None:
    '''
    Функция для отрисовки поля.
    
    :paran screen: Поверхность, на которой отрисовываем игровое поле
    :paran board: Игровое поле
    :paran cell_width: Ширина клетки
    :paran cell_height: Высота клетки
    :paran cell_living_color: Цвет "живой" клетки
    :paran cell_dead_color: Цвет "мертвой" клетки
    '''

    for row in range(board.rows):
        for col in range(board.columns):
            # Координаты левого верхнего угла
            x = col * cell_width
            y = row * cell_height

            # Выбор цвета для клетки
            cell = board[row][col]
            color = cell_living_color if cell.is_alive else cell_dead_color

            # Отрисовка клетки
            pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))