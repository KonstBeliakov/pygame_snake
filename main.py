import pygame
import copy
from time import perf_counter
import random

import progress_bar
import item
import snake
import map

snake_map = map.Map()

snake_map.loadMap(1)

pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False

SELL_SIZE = 20

n = 20

snake = snake.Snake()

direction = 'RIGHT'

t = perf_counter()

items = []
apple_position = None

gameOver = False

cyclic_map = False

level_progress_bar = progress_bar.ProgressBar(1, 6)
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

    snake_map.draw(screen, snake, items, apple_position)

    snake_event = snake.update(direction, snake_map.updating_map, n)

    match snake_event:
        case 'GameOver':
            gameOver = True
        case 'AppleEaten':
            apple_position = None
            if snake.length == level_progress_bar.max_volume:
                level_bar.add_volume(1)
                level_progress_bar.set_volume(1)
                snake.position = [(1, 1)]
                snake.length = 1
                direction = 'RIGHT'
                snake_map.loadMap(2)
                apple_position = None
            else:
                level_progress_bar.set_volume(snake.length)
            if not items:
                t = random.randrange(5)
                pos = random.choice([(i, j) for i in range(n) for j in range(n) if not snake_map.updating_map[i][j]])
                match t:
                    case 0:
                        items.append(item.Item(pos, 4, 'speed'))
                    case 1:
                        items.append(item.Item(pos, 5, 'slowness'))
        case 'SpeedAppleEaten':
            for i in range(len(items)):
                if items[i].effect == 'speed':
                    del items[i]
        case 'SlownessAppleEaten':
            for i in range(len(items)):
                if items[i].effect == 'slowness':
                    del items[i]

    if not apple_position:
        apple_position = random.choice([(i, j) for i in range(n) for j in range(n) if not snake_map.updating_map[i][j]])

    level_progress_bar.draw(screen)
    level_bar.draw(screen)

    snake.draw(screen)

    pygame.display.flip()
