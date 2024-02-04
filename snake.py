import pygame
from time import perf_counter
import progress_bar

class Snake():
    def __init__(self):
        self.position = [(0, 0)]
        self.length = 1
        self.speed = 8
        self.time = perf_counter()
        self.effects = []
        self.effect_time_bars = []
        self.effect_color = {'speed': (0, 255, 255), 'slowness': (0, 100, 0)}

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
        self.effects.append([effect_type, 10])
        self.effect_time_bars.append(progress_bar.ProgressBar(20, 20))
        self.effect_time_bars[-1].set_color(self.effect_color[effect_type])

    def update(self, direction, temp_map, map_size):
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
                    del self.effects[i]
                    del self.effect_time_bars[i]
                else:
                    self.effect_time_bars[i].set_volume(int(self.effects[i][1] // 0.5))

            match direction:
                case 'LEFT':
                    head = (self.position[-1][0] - 1, self.position[-1][1])
                case 'RIGHT':
                    head = (self.position[-1][0] + 1, self.position[-1][1])
                case 'UP':
                    head = (self.position[-1][0], self.position[-1][1] - 1)
                case 'DOWN':
                    head = (self.position[-1][0], self.position[-1][1] + 1)

            if head[0] < 0 or head[1] < 0 or head[0] > map_size - 1 or head[1] > map_size - 1:
                return 'GameOver'

            if self.length <= len(self.position):
                del self.position[0]

            match(temp_map[head[0]][head[1]]):
                case 2:
                    self.length += 1
                    event = 'AppleEaten'
                case 4:
                    event = 'SpeedAppleEaten'
                    self.add_effect('speed')
                case 5:
                    event = 'SlownessAppleEaten'
                    self.add_effect('slowness')
                case 3|1:
                    return 'GameOver'

            self.position.append(head)
        return event