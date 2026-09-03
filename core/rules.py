from .board import Board
from .cell import Cell


class Rules:
    def __init__(self, birth: list[int], survival: list[int], have_boundaries: bool=False) -> None:
        self._rules = {
            'birth': birth,
            'survival': survival
        }
        self._have_boundaries = have_boundaries

    @property
    def have_boundaries(self):
        return self._have_boundaries

    @have_boundaries.setter
    def have_boundaries(self, new_value):
        if not isinstance(new_value, bool):
            raise TypeError('have_boundaries должно быть типа bool')
        self._have_boundaries = new_value

    def get_next_state(self, board: Board, row: int, column: int) -> bool:
        '''
        Функция определяет следующее состояние (is_alive) клетки True/False.

        :param board: Игровое поле
        :param row: Индекс строки
        :param column: Индекс столбца
        :return: True/False - следующее состояние (is_alive) для Cell
        '''

        cell = board[row][column]
        neighbours = self._get_neighbours(board, row, column)
        count = sum(cell.is_alive for cell in neighbours) - cell.is_alive

        return count in self._rules.get(['birth', 'survival'][cell.is_alive])


    def _get_neighbours(self, board: Board, row: int, column: int) -> list[Cell]:
        '''
        Вспомогательная функция для получения соседей клетки (включая саму клетку).

        :param board: Игровое поле
        :param row: Индекс строки
        :param column: Индекс столбца
        :return: Список клеток-соседей
        '''

        max_rows, max_columns = board.rows, board.columns
        neighbours = []
        unique_pos = set()

        for i in range(-1, 2):
            for j in range(-1, 2):
                # Логика нахожения индексов соседа, если ЕСТЬ границы
                if self.have_boundaries:
                    neighbour_row = row + i
                    neighbour_column = column + j
                    if not (-1 < neighbour_row < max_rows) or not (-1 < neighbour_column < max_columns):
                        continue
                # Логика, если границ НЕТ
                else:
                    neighbour_row = (max_rows + row + i) % max_rows
                    neighbour_column = (max_columns + column + j) % max_columns

                # Проверка уникальности клеток
                pos = (neighbour_row, neighbour_column)
                if pos in unique_pos:
                    continue

                neighbours.append(board[neighbour_row][neighbour_column])
                unique_pos.add(pos)

        return neighbours


    @classmethod
    def from_string(cls, rule: str) -> 'Rules':
        '''
        Создание класса Rules из строки.

        Формат строки: "B{цифры}/S{цифры}", где
            - B (Birth) - цифры, при которых "мертвая" клетка "рождается"
            - S (Survival) - цифры, при которых "живая" клетка продолжает "существовать"

        Пример (Conway's Life): B3/S23

        :param rule: Строка в формате "B{цифры}/S{цифры}", определяющая правило игры
        :return: Rules
        '''

        birth_string, survival_string = rule.split('/')

        birth = list(map(int, birth_string[1:]))
        survival = list(map(int, survival_string[1:]))

        return cls(birth, survival)
