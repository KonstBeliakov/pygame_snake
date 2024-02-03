import pygame
from time import perf_counter

class Snake():
    def __init__(self):
        self.position = [(0, 0)]
        self.length = 1
        self.speed = 8
        self.time = perf_counter()

    def draw(self, screen):
        pass

    def update(self, direction, temp_map, map_size):
        event = None
        if perf_counter() - self.time > 1 / self.speed:
            self.time += 1 / self.speed

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
                    self.speed *= 2
                    event = 'SpeedAppleEaten'
                case 3|1:
                    return 'GameOver'

            self.position.append(head)
        return event