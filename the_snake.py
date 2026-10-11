import sys
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь для обработки нажатий клавиш:
TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}

# Базовые цвета:
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (93, 216, 228)
WHITE = (255, 255, 255)

# Цвета объектов:
BOARD_BACKGROUND_COLOR = BLACK
BORDER_COLOR = LIGHT_BLUE
APPLE_COLOR = RED
SNAKE_COLOR = GREEN
DEFAULT_COLOR = WHITE
ROCK_COLOR = GRAY

# Позиция по умолчанию для объектов:
DEFAULT_POSITION = (0, 0)

# Позиция змейки:
START_POSITION = (GRID_SIZE * 5, GRID_SIZE * 5)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов, яблоко, камень и змейка."""

    def __init__(self, position=DEFAULT_POSITION, body_color=DEFAULT_COLOR):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color=None, border_color=BORDER_COLOR):
        """Метод отрисовки одного объекта на игровом поле."""
        if color is None:
            color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Метод для отрисовки объекта на игровом поле."""
        raise NotImplementedError(
            'Метод draw() должен быть реализован в подклассе.'
        )


class Apple(GameObject):
    """Класс для яблока и камня, наследуется от GameObject."""

    def __init__(self, position=DEFAULT_POSITION, body_color=APPLE_COLOR):
        super().__init__(position, body_color)

    def randomize_position(self, occupied_positions):
        """Метод вызова случайной позиции объекта на игровом поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для змейки, наследуется от GameObject."""

    def __init__(self, position=START_POSITION, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()

    def reset(self):
        """Метод для сброса змейки в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод для получения позиции головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод для перемещения змейки на игровом поле."""
        head_x, head_y = self.get_head_position()
        new_head = ((head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)
        # last: удалённый хвост или None, если змейка растёт
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Затирает хвост и отрисовывает голову змейки."""
        if self.last:
            self.draw_cell(
                self.last,
                color=BOARD_BACKGROUND_COLOR,
                border_color=BOARD_BACKGROUND_COLOR
            )
        self.draw_cell(self.get_head_position())


def handle_keys(game_object):
    """Функция для обработки нажатий клавиш пользователем."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key in TURNS:
                new_direction, opposite_direction = TURNS[event.key]
                if game_object.direction != opposite_direction:
                    game_object.next_direction = new_direction


def main():
    """Главная функция для запуска игры."""
    pg.init()

    snake = Snake()
    rock = Apple(body_color=ROCK_COLOR)
    rock.randomize_position(snake.positions)
    apple = Apple()
    apple.randomize_position(snake.positions + [rock.position])
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head = snake.get_head_position()

        if head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions + [rock.position])
        elif head in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions + [rock.position])
        elif head == rock.position:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            rock.randomize_position(snake.positions)
            apple.randomize_position(snake.positions + [rock.position])

        apple.draw()
        rock.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
