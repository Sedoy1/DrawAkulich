import time
import galois
import pygame
import sys
import itertools
import numpy as np

try:
    with open("settings.txt", "r") as file:
        line = file.readline()
        N = int(line)
    file.close()
except:
    N = 4

pygame.init()

size_block = 500 // N
margin = 15
width = height = size_block * N + margin * (N + 1)

size_window = (width, height + 100)
screen = pygame.display.set_mode(size_window)
pygame.display.set_caption("Задача Леонардо")
button = pygame.Rect(0.1 * width, height + 50, width * 0.8, 40)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

font_button = pygame.font.SysFont("stxingkai", width // 12)
text_button = font_button.render("Показать все раскраски", True, red)
text_rect = text_button.get_rect()
button_text_x = screen.get_width() / 2 - text_rect.width / 2
button_text_y = screen.get_height() - 45
solutions = []
arr = [[0] * N for i in range(N)]
clock = pygame.time.Clock()


def solve():
    n = N ** 2
    arr = []
    for i in range(n):
        arr.append([0] * n)
        arr[i][i] = 1
        if i % N > 0:
            arr[i][i - 1] = 1
        if i % N < N - 1:
            arr[i][i + 1] = 1
        if i // N < N - 1:
            arr[i][i + N] = 1
        if i // N > 0:
            arr[i][i - N] = 1

    b_res = [1] * len(arr)
    a2 = galois.GF2(arr)
    b2 = galois.GF2(b_res)
    solutions = []
    if N > 4:
        solutions.append(np.linalg.solve(a2, b2))
        return solutions

    for numbers in itertools.product([0, 1], repeat=len(b_res)):
        tmp = galois.GF2(numbers)
        tmp2 = a2 @ tmp
        if tmp2.all() == b2.all():
            solutions.append(list(numbers))
    return solutions


def check_win(array):
    return array == [[1 for i in range(len(array))] for j in range(len(array))]


def output_example_array(array):
    new_array = [[0] * N for i in range(N)]
    for i in range(N ** 2):
        if array[i] == 1:
            new_array[i // N][i % N] = 1
    for row in range(N):
        for col in range(N):
            if new_array[col][row] == 1:
                color = red
            else:
                color = white
            x = col * size_block + (col + 1) * margin
            y = row * size_block + (row + 1) * margin
            pygame.draw.rect(screen, color, (x, y, size_block, size_block))
    time.sleep(2)


def slider(solutions):
    for i in range(len(solutions)):
        screen.fill(black)
        output_example_array(solutions[i])

        text_surface = font_button.render(f"Решение #{i + 1} из {len(solutions)}", True, white)
        text_rect_surface = text_surface.get_rect()
        surface_text_x = screen.get_width() / 2 - text_rect_surface.width / 2
        surface_text_y = screen.get_height() - 45
        screen.blit(text_surface, [surface_text_x, surface_text_y])
        pygame.display.update()


game_over = False
while True:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            if button.collidepoint((x_mouse, y_mouse)):
                arr = [[0] * N for i in range(N)]
                screen.fill(black)
                game_over = True
                if len(solutions) == 0:
                    solutions = solve()
                    print(f"{len(solutions)} found")
                slider(solutions)
            elif y_mouse < (size_block + margin) * N and x_mouse < (size_block + margin) * N:
                col = x_mouse // (size_block + margin)
                row = y_mouse // (size_block + margin)
                arr[col][row] ^= 1
                if row > 0:
                    arr[col][row - 1] ^= 1
                if col > 0:
                    arr[col - 1][row] ^= 1
                if col < N - 1:
                    arr[col + 1][row] ^= 1
                if row < N - 1:
                    arr[col][row + 1] ^= 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_over = False
            arr = [[0] * N for i in range(N)]
            screen.fill(black)

    if not game_over:
        for row in range(N):
            for col in range(N):
                if arr[col][row] == 1:
                    color = red
                else:
                    color = white
                x = col * size_block + (col + 1) * margin
                y = row * size_block + (row + 1) * margin
                pygame.draw.rect(screen, color, (x, y, size_block, size_block))

    if check_win(arr):
        screen.fill(white)
        font = pygame.font.SysFont("stxingkai", 80)
        text = font.render("Победа", True, red)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2

        screen.blit(text, [text_x, text_y])
        game_over = True
    else:
        pygame.draw.rect(screen, white, button)
        screen.blit(text_button, [button_text_x, button_text_y])

    pygame.display.update()
