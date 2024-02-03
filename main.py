import pygame
import copy
from time import perf_counter
from random import choice

import progress_bar

pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False

SELL_SIZE = 20

n = 20

map = [[0 for _ in range(n)] for _ in range(n)]

for i in range(6, 15):
    for j in range(6, 15):
        map[i][j] = 3

snake = [(0, 0)]
snake_length = 1

direction = 'RIGHT'

t = perf_counter()

apple_position = None

gameOver = False

cyclic_map = False

level_progress_bar = progress_bar.ProgressBar(1, 10)
level_progress_bar.set_position(n * (SELL_SIZE + 2) + 50, 10)
level_progress_bar.set_size(200, 30)

level_bar = progress_bar.ProgressBar(1, 10)
level_bar.set_position(n * (SELL_SIZE + 2) + 50, 50)
level_bar.set_size(200, 30)

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    screen.fill((0, 0, 0))  #
    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT]:
        direction = 'LEFT'
    if keys[pygame.K_RIGHT]:
        direction = 'RIGHT'
    if keys[pygame.K_UP]:
        direction = 'UP'
    if keys[pygame.K_DOWN]:
        direction = 'DOWN'

    if perf_counter() - t > 0.2:
        t += 0.2
        match direction:
            case 'LEFT':
                head = (snake[-1][0] - 1, snake[-1][1])
            case 'RIGHT':
                head = (snake[-1][0] + 1, snake[-1][1])
            case 'UP':
                head = (snake[-1][0], snake[-1][1] - 1)
            case 'DOWN':
                head = (snake[-1][0], snake[-1][1] + 1)

        if snake_length <= len(snake):
            del snake[0]
        if head == apple_position:
            snake_length += 1
            apple_position = None
        if head[0] < 0 or head[1] < 0 or head[0] > n - 1 or head[1] > n - 1:
            gameOver = True

        if head in snake or map[head[0]][head[1]]:
            gameOver = True
        else:
            snake.append(head)

    temp_map = copy.deepcopy(map)

    for i in snake:
        temp_map[i[0]][i[1]] = 1
    if apple_position:
        temp_map[apple_position[0]][apple_position[1]] = 2

    if not apple_position:
        apple_position = choice([(i, j) for i in range(n) for j in range(n) if not temp_map[i][j]])

    for i in range(len(temp_map)):
        for j in range(len(temp_map[i])):
            match temp_map[i][j]:
                case 0:
                    color = (255, 255, 255)
                case 1:
                    color = (0, 255, 0)
                case 2:
                    color = (255, 0, 0)
                case 3:
                     color = (50, 50, 50)

            pygame.draw.rect(screen, color, pygame.Rect(10 + i * (SELL_SIZE + 2), 10 + j * (SELL_SIZE + 2),
                                                        SELL_SIZE, SELL_SIZE))

            if snake_length == level_progress_bar.max_volume:
                level_bar.add_volume(1)
                level_progress_bar.set_volume(1)
                snake = [(0, 0)]
                snake_length = 1
            else:
                level_progress_bar.set_volume(snake_length)

            level_progress_bar.draw(screen)
            level_bar.draw(screen)
    pygame.display.flip()
