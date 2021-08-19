from utils.settings import WHITE, BLACK, RED, BLUE, GREEN, FPS, ROWS, COLS
from utils.settings import WIDTH, HEIGHT, PIXEL_SIZE, DRAW_GRID_LINES
from utils.settings import TOOLBAR_HEIGHT, BG_COLOR
from utils.button import Button

import pygame

# This creates the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Pad")


def init_grid(rows, cols, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i *
                             PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE),
                             (WIDTH, i * PIXEL_SIZE))
            for i in range(COLS + 1):
                pygame.draw.line(win, BLACK, (i * PIXEL_SIZE, 0),
                                 (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for btn in buttons:
        btn.draw(win)

    pygame.display.update()


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    # if row >= ROWS:
    #     raise IndexError

    return row, col


run = True
clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK
ERASER_SIZE = PIXEL_SIZE * 2

button_y = HEIGHT - TOOLBAR_HEIGHT/2 - 25
buttons = [
    Button(10, button_y, 50, 50, BLACK),
    Button(70, button_y, 50, 50, RED),
    Button(130, button_y, 50, 50, GREEN),
    Button(190, button_y, 50, 50, BLUE),
    Button(250, button_y, 50, 50, WHITE, "Erase", BLACK),
    Button(310, button_y, 50, 50, WHITE, "Clear", BLACK)
]

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        # This event happens with the user presses the exit button
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            row, col = get_row_col_from_pos(pos)

            if row >= ROWS:
                for button in buttons:
                    if not button.clicked(pos):
                        continue

                    drawing_color = button.color

                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
            else:
                grid[row][col] = drawing_color

            # try:
            #     row, col = get_row_col_from_pos(pos)
            #     grid[row][col] = drawing_color
            # except IndexError:
            #     for button in buttons:
            #         if not button.clicked(pos):
            #             continue

            #         drawing_color = button.color
            #         if button.text == "Erase":
            #             for i in range(PIXEL_SIZE + 5):
            #                 grid[row + i][col + i] = drawing_color

    draw(WIN, grid, buttons)

pygame.quit()
