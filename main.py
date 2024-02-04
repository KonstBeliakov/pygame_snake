import pygame
import copy
from time import perf_counter
import random

import progress_bar
import item
import snake
import map
import button

snake_map = map.Map()

snake_map.loadMap(1)

pygame.init()
screen = pygame.display.set_mode((800, 600))

SELL_SIZE = 20

n = 20

snake = snake.Snake()

t = perf_counter()

items = [item.Item((5, 5), 2)]

gameOver = False

cyclic_map = False

level_progress_bar = progress_bar.ProgressBar(1, 10)
level_progress_bar.set_position(n * (SELL_SIZE + 2) + 50, 10)
level_progress_bar.set_size(200, 30)

level_bar = progress_bar.ProgressBar(1, 10)
level_bar.set_position(n * (SELL_SIZE + 2) + 50, 50)
level_bar.set_size(200, 30)

button_continue = button.Button((10, 10), (200, 30))

pause = False

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_continue.update('pressed')
        elif event.type == pygame.MOUSEBUTTONUP:
            if button_continue.update('released'):
                pause = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pause = True

    screen.fill((0, 0, 0))

    if not pause:
        snake_map.draw(screen, snake, items)
        snake_event = snake.update(snake_map.updating_map, n)

        match snake_event:
            case 'GameOver':
                gameOver = True
            case 'AppleEaten', position:
                for i in range(len(items)):
                    if items[i].position == position:
                        del items[i]
                        break
                if snake.length == level_progress_bar.max_volume:
                    level_bar.add_volume(1)
                    level_progress_bar.set_volume(1)
                    snake.position = [(1, 1)]
                    snake.length = 1
                    snake.direction = 'RIGHT'
                    snake_map.loadMap(2)
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
                        case 2:
                            items.append(item.Item(pos, 6, 'disorientation'))
                        case 3:
                            items.append(item.Item(pos, 7, 'darkness'))
                        case _:
                            items.append(item.Item(pos, 2))

        level_progress_bar.draw(screen)
        level_bar.draw(screen)

        snake.draw(screen)
    else:
        button_continue.draw(screen)

    pygame.display.flip()
