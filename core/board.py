from .cell import Cell
from random import choice


class Board:
    def __init__(self, rows: int, columns: int) -> None:
        self._rows = rows
        self._columns = columns
        self._grid = [
            [Cell() for _ in range(columns)]
            for _ in range(rows)
        ]

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns
    
    def __getitem__(self, idx: int) -> list[Cell]:
        '''
        Получение строки по индексу.

        :param idx: Индекс строки
        :return: Строка поля
        '''

        return self._grid[idx]

    @staticmethod
    def get_row_and_column_by_position(pos_mouse: tuple[int], cell_width: int, cell_height: int) -> tuple[int]:
        '''
        Получить строку и столбец по позиции мыши.

        :param pos_mouse: Позиция мыши. Формат: (x, y)
        :param cell_width: Ширина клетки
        :param cell_height: Высота клетки
        :return: tuple (строка, столбец)
        '''

        # Координаты мыши
        x, y = pos_mouse

        # Строка и столбец на основе координат и величин сторон
        row = y // cell_height
        col = x // cell_width

        return row, col

    def get_cell_by_position(self, pos_mouse: tuple[int], cell_width: int, cell_height: int) -> Cell:
        '''
        Получить клетку по позиции мыши.

        :param pos_mouse: Позиция мыши. Формат: (x, y)
        :param cell_width: Ширина клетки
        :param cell_height: Высота клетки
        :return: Cell
        '''

        row, col = self.get_row_and_column_by_position(pos_mouse, cell_width, cell_height)
        return self._grid[row][col]

    def add_pattern(self, pattern: list[list[int]], row: int, column: int) -> None:
        '''
        Добавить паттерн в таблицу.

        :param pattern: Паттерн. Формат: [[0, 1, ..., 0], ..., [0, 0, ..., 0]]
        :param row: Строка левого верхнего угла
        :param column: Столбец левого верхнего угла
        '''

        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                cur_row = (row + i) % self.rows
                cur_column = (column + j) % self.columns
                self._grid[cur_row][cur_column].is_alive = bool(pattern[i][j])

    @classmethod
    def from_matrix_of_numbers(cls, matrix: list[list[int]]) -> 'Board':
        '''
        Получаем поле из двумерной матрицы чисел, где:
            - 0 - мертвая клетка (is_alive=False)
            - 1 - живая клетка (is_alive=True)

        :param cls: Класс поля
        :param matrix: Двумерная матрица чисел
        :return: Board
        '''

        rows, columns = len(matrix), len(matrix[0])
        board = cls(rows, columns)

        for row in range(rows):
            for col in range(columns):
                board._grid[row][col].is_alive = bool(matrix[row][col])

        return board

    @classmethod
    def make_random_board(cls, rows: int, columns: int) -> 'Board':
        '''
        Создание рандомного поля по количеству строк и столбцов.
        
        :param cls: Класс поля
        :param rows: Количество строк
        :param columns: Количество столбцов
        :return: Board
        '''

        matrix = [
            [choice((0, 1)) for _ in range(columns)]
            for _ in range(rows)
        ]
        return cls.from_matrix_of_numbers(matrix)

    def to_matrix(self) -> list[list[int]]:
        '''
        Преобразование поля в двумерный массив числе, где:
            - 0 - "мертвая" клетка (is_alive=False)
            - 1 - "живая" клетка (is_alive=True)

        :return: Двумерный массив чисел
        '''
        matrix = [
            [int(cell.is_alive) for cell in row]
            for row in self._grid
        ]
        return matrix
        
