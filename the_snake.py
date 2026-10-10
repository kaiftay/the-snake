from random import choice, randint

import pygame

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color
    # Метод вызова случайной позиции объекта на игровом поле

    def randomize_position(self):
        x_cell = randint(0, GRID_WIDTH - 1)
        y_cell = randint(0, GRID_HEIGHT - 1)

        new_x = x_cell * GRID_SIZE
        new_y = y_cell * GRID_SIZE

        self.position = (new_x, new_y)

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self, position=(0, 0), body_color=APPLE_COLOR):
        super().__init__(position, body_color)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Rock(GameObject):
    def __init__(self, position=None, body_color=(128, 128, 128)):
        super().__init__(position, body_color)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=SNAKE_COLOR, length=1, direction=RIGHT,
                 next_direction=None):
        self.position = position
        self.positions = [position]
        self.body_color = body_color
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.last = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        # Логика движения змейки
        head = self.get_head_position()
        new_head = (head[0] + self.direction[0] * GRID_SIZE,
                    head[1] + self.direction[1] * GRID_SIZE)

        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        self.positions.insert(0, new_head)
        # Удаление последнего сегмента змейки, если длина больше текущей длины
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
    # Метод сброса змейки в начальное состояние

    def reset(self, position):
        self.positions = [position]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


# Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    print("Игра 'Змейка' запущена. Управление: стрелки на клавиатуре.")

    apple = Apple((0, 0))
    apple.randomize_position()
    rock = Rock((0, 0))
    rock.randomize_position()
    while rock.position == apple.position:
        rock.randomize_position()
    snake = Snake((GRID_SIZE * 5, GRID_SIZE * 5))

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset((GRID_SIZE * 5, GRID_SIZE * 5))
            apple.randomize_position()
        if snake.get_head_position() == rock.position:
            snake.reset((GRID_SIZE * 5, GRID_SIZE * 5))
            apple.randomize_position()
            rock.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        rock.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
