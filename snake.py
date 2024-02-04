import pygame
from time import perf_counter
import progress_bar

class Snake():
    def __init__(self):
        self.position = [(1, 1)]
        self.length = 1
        self.speed = 5
        self.normal_speed = 5
        self.time = perf_counter()
        self.effects = []
        self.effect_time_bars = []
        self.effect_color = {'speed': (0, 255, 255), 'slowness': (0, 150, 0), 'disorientation': (150, 150, 0),
                             'darkness': (100, 0, 100)}
        self.disorientation = False
        self.darkness = 0
        self.direction = 'RIGHT'

    def draw(self, screen):
        for i in range(len(self.effect_time_bars)):
            self.effect_time_bars[i].set_position(25 * 20, 200 + 50 * i)
            self.effect_time_bars[i].set_size(200, 30)
            self.effect_time_bars[i].draw(screen)

    def add_effect(self, effect_type):
        match effect_type:
            case 'speed':
                self.speed *= 2
            case 'slowness':
                self.speed /= 2
            case 'disorientation':
                self.disorientation = True
            case 'darkness':
                self.darkness += 1
        self.effects.append([effect_type, 10])
        self.effect_time_bars.append(progress_bar.ProgressBar(20, 20))
        self.effect_time_bars[-1].set_color(self.effect_color[effect_type])

    def effect_clear(self):
        self.speed = self.normal_speed
        self.disorientation = False
        self.darkness = 0

        self.effects = []
        self.effect_time_bars = []

    def update(self, temp_map, map_size):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction = 'RIGHT' if self.disorientation else 'LEFT'
        if keys[pygame.K_RIGHT]:
            self.direction = 'LEFT' if self.disorientation else 'RIGHT'
        if keys[pygame.K_UP]:
            self.direction = 'DOWN' if self.disorientation else 'UP'
        if keys[pygame.K_DOWN]:
            self.direction = 'UP' if self.disorientation else 'DOWN'

        event = None
        if perf_counter() - self.time > 1 / self.speed:
            self.time += 1 / self.speed

            for i in range(len(self.effects) - 1, -1, -1):
                self.effects[i][1] -= 1 / self.speed
                if self.effects[i][1] < 0:
                    if self.effects[i][0] == 'speed':
                        self.speed /= 2
                    elif self.effects[i][0] == 'slowness':
                        self.speed *= 2
                    elif self.effects[i][0] == 'disorientation':
                        self.disorientation = False
                    elif self.effects[i][0] == 'darkness':
                        self.darkness -= 1
                    del self.effects[i]
                    del self.effect_time_bars[i]
                else:
                    self.effect_time_bars[i].set_volume(int(self.effects[i][1] // 0.5))

            match self.direction:
                case 'LEFT':
                    head = (self.position[-1][0] - 1, self.position[-1][1])
                case 'RIGHT':
                    head = (self.position[-1][0] + 1, self.position[-1][1])
                case 'UP':
                    head = (self.position[-1][0], self.position[-1][1] - 1)
                case 'DOWN':
                    head = (self.position[-1][0], self.position[-1][1] + 1)

            head = (head[0] % map_size, head[1] % map_size)
            #if head[0] < 0 or head[1] < 0 or head[0] > map_size - 1 or head[1] > map_size - 1:
            #    return 'GameOver'

            if self.length <= len(self.position):
                del self.position[0]

            if temp_map[head[0]][head[1]] in [2, 4, 5, 6, 7]:
                self.length += 1
                event = ('AppleEaten', head)

            match(temp_map[head[0]][head[1]]):
                case 4:
                    self.add_effect('speed')
                case 5:
                    self.add_effect('slowness')
                case 6:
                    self.add_effect('disorientation')
                case 7:
                    self.add_effect('darkness')
                case 3|1:
                    return 'GameOver'

            self.position.append(head)
        return event