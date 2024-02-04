import pygame
import copy

import snake
import item

class Map():
    def __init__(self):
        self.sell_size = 20
        self.map_size = 20
        self.map = []
        self.updating_map = []
        self.block_colors = [(255, 255, 255), (0, 255, 0), (255, 0, 0), (50, 50, 50), (0, 255, 255), (0, 100, 0),
                             (150, 150, 0)]

    def loadMap(self, level):
        self.map = []
        with open(f'level{level}.txt', encoding='utf-8') as file:
            for line in file.readlines():
                self.map.append([int(i) for i in line.split()])

    def draw(self, screen, snake, items):
        self.updating_map = copy.deepcopy(self.map)

        for i in snake.position:
            self.updating_map[i[0]][i[1]] = 1

        for i in items:
            self.updating_map[i.position[0]][i.position[1]] = i.type


        for i in range(self.map_size):
            for j in range(self.map_size):
                pygame.draw.rect(screen, self.block_colors[self.updating_map[i][j]], pygame.Rect(10 + i * (self.sell_size + 2),
                                         10 + j * (self.sell_size + 2), self.sell_size, self.sell_size))
