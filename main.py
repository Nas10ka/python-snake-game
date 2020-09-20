import pygame
import random
import pygame_menu

pygame.init()
bg = pygame.image.load("snake.png")
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
size = [(BLOCK_SIZE + MARGIN) * COLS + SIDES_MARGIN * 2,
        (BLOCK_SIZE + MARGIN) * COLS + SIDES_MARGIN * 2 + HEADER_MARGIN]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Nas10ka Snake')
courier = pygame.font.SysFont('courier', 32)
timer = pygame.time.Clock()


def start_the_game():
    timer_tick = float(1.0)
    paused = False

    class SnakeBlock:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def is_inside(self):
            return 0 <= self.x < COLS and 0 <= self.y < COLS

        def __eq__(self, other):
            return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


    def get_random_apple_block():
        random.randint(0, COLS)
        return SnakeBlock(
            random.randint(0, COLS-1),
            random.randint(0, COLS-1)
        )


    apple = get_random_apple_block()
    snake_blocks = [SnakeBlock(8, 9), SnakeBlock(8, 10), SnakeBlock(8, 11)]
    d_row = 1
    d_col = 0
    total = 0


    def draw_block(col, row, color):
        cols = (SIDES_MARGIN + MARGIN * col) + col * BLOCK_SIZE
        rows = (SIDES_MARGIN + MARGIN * row) + row * BLOCK_SIZE + HEADER_MARGIN
        pygame.draw.rect(screen, color, [cols, rows, BLOCK_SIZE, BLOCK_SIZE])


    while not paused:

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, (BLOCK_SIZE + MARGIN) * COLS + SIDES_MARGIN * 2, HEADER_MARGIN])

        text_total = courier.render(f"Total: {total * 10}", 0, SNAKE_COLOR)
        speed_text = courier.render(f"Speed: {total + 1}", 0, SNAKE_COLOR)
        screen.blit(text_total, (BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(speed_text, (BLOCK_SIZE + 220, BLOCK_SIZE))

        for row in range(COLS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = RECT_COLOR
                else:
                    color = LIGHT_RECT_COLOR
                draw_block(col, row, color)


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
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
                elif event.key == pygame.K_SPACE and paused:
                    paused = False
                elif event.key == pygame.K_SPACE and not paused:
                    paused = True
                    # paused = not paused

        head = snake_blocks[-1]  # take the latest element in array of snake blocks

        if head.x + d_col == apple.x and head.y + d_row== apple.y:
            new_head = SnakeBlock(head.x + d_col, head.y + d_row)
            if not head.is_inside() or new_head in snake_blocks:
                break
            snake_blocks.append(new_head)
            total += 1
            timer_tick += 0.25

            for block in snake_blocks:
                draw_block(block.x, block.y, SNAKE_COLOR)
            apple = get_random_apple_block()  # create new apple
        else:
            new_head = SnakeBlock(head.x + d_col, head.y + d_row)
            if not new_head.is_inside() or new_head in snake_blocks:
                break
            snake_blocks.append(new_head)
            snake_blocks.pop(0)

        for block in snake_blocks:
            draw_block(block.x, block.y, SNAKE_COLOR)

        draw_block(apple.x, apple.y, APPLE_COLOR)

        pygame.display.flip()

        timer.tick(timer_tick)

    pass

# def set_difficulty(value, difficulty):
#     # Do the job here !
#     pass

mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0), # transparent background
                title_background_color=(4, 47, 126, 0),
title_font=pygame_menu.font.FONT_OPEN_SANS,
                                   menubar_close_button=False)
menu = pygame_menu.Menu(250, 400, ' ', theme=mytheme)

menu.add_text_input('Nickname :', default='Player 1')
# menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)


def draw_background():
    screen.blit(bg, (0, 0))


while True:

    draw_background()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()