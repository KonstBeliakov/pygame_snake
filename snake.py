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

            if temp_map[head[0]][head[1]] == 2:
                self.length += 1
                event = 'AppleEaten'
            elif temp_map[head[0]][head[1]] == 4:
                self.speed *= 2
                event = 'SpeedAppleEaten'

            if head in self.position or temp_map[head[0]][head[1]] == 3:
                return 'GameOver'
            else:
                self.position.append(head)
        return event