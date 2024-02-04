import pygame
import copy
from time import perf_counter
import random

import progress_bar
import snake

def loadMap(level):
    global map
    map = []
    with open(f'level{level}.txt', encoding='utf-8') as file:
        for line in file.readlines():
            map.append([int(i) for i in  line.split()])

loadMap(1)

pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False

SELL_SIZE = 20

n = 20

snake = snake.Snake()

direction = 'RIGHT'

t = perf_counter()

apple_position = None
speed_apple_position = None

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

    temp_map = copy.deepcopy(map)

    for i in snake.position:
        temp_map[i[0]][i[1]] = 1
    if apple_position:
        temp_map[apple_position[0]][apple_position[1]] = 2
    if speed_apple_position:
        temp_map[speed_apple_position[0]][speed_apple_position[1]] = 4

    snake_event = snake.update(direction, temp_map, n)

    match snake_event:
        case 'GameOver':
            gameOver = True
        case 'AppleEaten':
            apple_position = None
            if snake.length == level_progress_bar.max_volume:
                level_bar.add_volume(1)
                level_progress_bar.set_volume(1)
                snake.position = [(0, 0)]
                snake.length = 1
                loadMap(2)
            else:
                level_progress_bar.set_volume(snake.length)
            if not random.randrange(2) and not speed_apple_position:
                speed_apple_position = random.choice([(i, j) for i in range(n) for j in range(n) if not temp_map[i][j]])
        case 'SpeedAppleEaten':
            speed_apple_position = None

    if not apple_position:
        apple_position = random.choice([(i, j) for i in range(n) for j in range(n) if not temp_map[i][j]])

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
                case 4:
                    color = (0, 255, 255)

            pygame.draw.rect(screen, color, pygame.Rect(10 + i * (SELL_SIZE + 2), 10 + j * (SELL_SIZE + 2),
                                                        SELL_SIZE, SELL_SIZE))


            level_progress_bar.draw(screen)
            level_bar.draw(screen)

            snake.draw(screen)
    pygame.display.flip()
