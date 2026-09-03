import pygame
import json
import pathlib

from core import *
from rendering import *


# Путь к директории с main.py
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent

# Импорт настроек, цветов и пресетов
with open(PROJECT_ROOT / "configs" / "config.json") as file:
    config = json.load(file)


# Константы
TITLE = config["settings"]["title"]
DISPLAY_WIDTH = config["settings"]["display_width"]
DISPLAY_HEIGHT = config["settings"]["display_height"]
FPS = config["settings"]["fps"]
ROWS = config["settings"]["board_rows"]
COLUMNS = config["settings"]["board_columns"]
CELL_WIDTH = DISPLAY_WIDTH // COLUMNS
CELL_HEIGHT = DISPLAY_HEIGHT // ROWS
HAVE_BOUNDARIES = bool(config["settings"]["have_boundaries"])

DISPLAY_COLOR = config["colors"]["background"]
CELL_DEAD_COLOR = config["colors"]["cell_dead_color"]
CELL_LIVING_COLOR = config["colors"]["cell_living_color"]

PRESET = config["presets"]["conway"]


# Основная логика игры
with PygameContext([pygame.display]):
    pygame.display.set_caption(TITLE)

    # Основные переменные
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pygame.time.Clock()

    board = Board(ROWS, COLUMNS)
    rules = Rules.from_string(PRESET)
    rules.have_boundaries = HAVE_BOUNDARIES

    running = True
    playing = False

    # Игровой цикл
    while running:
        
        # Отрисовка экрана
        screen.fill(DISPLAY_COLOR)

        # Отрисовка поля
        renderer.draw_board(screen, board, CELL_WIDTH, CELL_HEIGHT, CELL_LIVING_COLOR, CELL_DEAD_COLOR)

        # Логика нажатий на клавиши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = board.get_cell_by_position(event.pos, CELL_WIDTH, CELL_HEIGHT)
                cell.is_alive = not cell.is_alive

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_r:
                    board = Board(ROWS, COLUMNS)
                    
                if event.key == pygame.K_t:
                    board = Board.make_random_board(ROWS, COLUMNS)

                if event.key == pygame.K_1:
                    row, column = board.get_row_and_column_by_position(pygame.mouse.get_pos(), CELL_WIDTH, CELL_HEIGHT)
                    board.add_pattern(GLIDER, row, column)
                if event.key == pygame.K_2:
                    row, column = board.get_row_and_column_by_position(pygame.mouse.get_pos(), CELL_WIDTH, CELL_HEIGHT)
                    board.add_pattern(LIGHTWEIGHT_SPACESHIP, row, column)
                if event.key == pygame.K_3:
                    row, column = board.get_row_and_column_by_position(pygame.mouse.get_pos(), CELL_WIDTH, CELL_HEIGHT)
                    board.add_pattern(MIDDLEWEIGHT_SPACESHIP, row, column)

        # Обновление поля в соответствие с правилами
        if playing:
            new_board = Board(ROWS, COLUMNS)

            for row in range(board.rows):
                for col in range(board.columns):
                    new_board[row][col].is_alive = rules.get_next_state(board, row, col)

            board = new_board

        # Обновление поля
        pygame.display.flip()

        # Частота кадров
        clock.tick(FPS)
