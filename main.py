import pygame
import sys
import random

FRAME_COLOR = (0, 25, 51)
APPLE_COLOR = (204, 0, 102)
RECT_COLOR = (0, 51, 102)
LIGHT_RECT_COLOR = (31, 63, 118)
HEADER_COLOR = (0, 21, 44)
SNAKE_COLOR = (0, 128, 255)
COLS = 25
BLOCK_SIZE = 20
MARGIN = 1
SIDES_MARGIN = 20
HEADER_MARGIN = 70
size = [(BLOCK_SIZE + MARGIN) * COLS + SIDES_MARGIN * 2, (BLOCK_SIZE + MARGIN) * COLS + SIDES_MARGIN * 2 + HEADER_MARGIN]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Nas10ka Snake')

timer = pygame.time.Clock()


def exitGame(reason='exit'):
    print(reason)
    pygame.quit()
    sys.exit()


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COLS and 0 <= self.y < COLS


def get_random_apple_block():
    random.randint(0, COLS)
    return SnakeBlock(
        random.randint(0, COLS-1),
        random.randint(0, COLS-1)
    )


apple = get_random_apple_block()
snake_blocks = [SnakeBlock(8, 9), SnakeBlock(8, 10), SnakeBlock(8, 11)]


def draw_block(col, row, color):
    cols = (SIDES_MARGIN + MARGIN * col) + col * BLOCK_SIZE
    rows = (SIDES_MARGIN + MARGIN * row) + row * BLOCK_SIZE + HEADER_MARGIN
    pygame.draw.rect(screen, color, [cols, rows, BLOCK_SIZE, BLOCK_SIZE])


d_row = 1
d_col = 0

while True:

    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, (BLOCK_SIZE + MARGIN) * COLS + SIDES_MARGIN * 2, HEADER_MARGIN])

    for row in range(COLS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                color = RECT_COLOR
            else:
                color = LIGHT_RECT_COLOR
            draw_block(col, row, color)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and d_col != 0:
                d_row = -1
                d_col = 0
            elif event.key == pygame.K_DOWN and d_col != 0:
                d_row = 1
                d_col = 0
            elif event.key == pygame.K_LEFT and d_row != 0:
                d_row = 0
                d_col = -1
            elif event.key == pygame.K_RIGHT and d_row != 0:
                d_row = 0
                d_col = 1

    head = snake_blocks[-1]  # take the latest element in array of snake blocks

    if head.x + d_col == apple.x and head.y + d_row== apple.y:
        snake_blocks.append(SnakeBlock(head.x + d_col, head.y + d_row))
        for block in snake_blocks:
            draw_block(block.x, block.y, SNAKE_COLOR)
        apple = get_random_apple_block()  # create new apple
    else:
        new_head = SnakeBlock(head.x + d_col, head.y + d_row)
        snake_blocks.append(new_head)
        snake_blocks.pop(0)

    for block in snake_blocks:
        draw_block(block.x, block.y, SNAKE_COLOR)

    if not head.is_inside():
        exitGame('crash')

    draw_block(apple.x, apple.y, APPLE_COLOR)

    pygame.display.flip()

    timer.tick(2)
