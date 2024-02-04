import pygame
import copy
from time import perf_counter
import random

import progress_bar
import item
import snake
import map
import button

snake = snake.Snake()

snake_map = map.Map()

snake_map.loadMap(1, snake)

pygame.init()
screen = pygame.display.set_mode((800, 600))

SELL_SIZE = 20

n = 20

t = perf_counter()

items = [item.Item((5, 5), 2)]

gameOver = False

cyclic_map = False

font = pygame.font.SysFont(None, 40)

text_color = (100, 150, 100)

text1 = font.render('Progress on level:', True, text_color)

level_progress_bar = progress_bar.ProgressBar(1, 6)
level_progress_bar.set_position(n * (SELL_SIZE + 2) + 50, 50)
level_progress_bar.set_size(200, 30)

text2 = font.render('Level:', True, text_color)

level_bar = progress_bar.ProgressBar(1, 10)
level_bar.set_position(n * (SELL_SIZE + 2) + 50, 130)
level_bar.set_size(200, 30)

button_continue = button.Button((10, 10), (200, 30), 'Continue')
level_buttons = [button.Button((10 + i * 45, 60), (30, 30), str(i + 1)) for i in range(5)]

pause = False

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_continue.update('pressed')
            for i in range(len(level_buttons)):
                level_buttons[i].update('pressed')
        elif event.type == pygame.MOUSEBUTTONUP:
            if button_continue.update('released'):
                pause = False
            for i in range(len(level_buttons)):
                if level_buttons[i].update('released'):
                    pause = False
                    snake_map.loadMap(i + 1, snake)
                    level_bar.set_volume(i + 1)

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
                    snake_map.loadMap(level_bar.volume, snake)
                else:
                    level_progress_bar.set_volume(snake.length)
                if not items:
                    t = random.randrange(5)
                    pos = random.choice([(i, j) for i in range(n) for j in range(n) if not snake_map.updating_map[i][j]])

                    effects = {2: None, 4: 'speed', 5: 'slowness', 6: 'disorientation', 7: 'darkness'}

                effect = random.choices([2, 4, 5, 6, 7], weights=[snake_map.drop_probability.get(i, 0) for i in [2, 4, 5, 6, 7]])[0] #
                items.append(item.Item(pos, effect, effects[effect]))

        level_progress_bar.draw(screen)
        level_bar.draw(screen)

        snake.draw(screen)

        screen.blit(text1, ((SELL_SIZE + 2) * n + 50, 10))
        screen.blit(text2, ((SELL_SIZE + 2) * n + 50, 90))
    else:
        button_continue.draw(screen, font)

        for i in range(len(level_buttons)):
            level_buttons[i].draw(screen, font)

    pygame.display.flip()
