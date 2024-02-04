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

    def loadMap(self, level):
        self.map = []
        with open(f'level{level}.txt', encoding='utf-8') as file:
            for line in file.readlines():
                self.map.append([int(i) for i in line.split()])

    def draw(self, screen, snake, items, apple_position):
        self.updating_map = copy.deepcopy(self.map)

        for i in snake.position:
            self.updating_map[i[0]][i[1]] = 1
        if apple_position:
            self.updating_map[apple_position[0]][apple_position[1]] = 2
        for i in items:
            self.updating_map[i.position[0]][i.position[1]] = i.type


        for i in range(self.map_size):
            for j in range(self.map_size):
                match self.updating_map[i][j]:
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
                    case 5:
                        color = (0, 100, 0)

                pygame.draw.rect(screen, color, pygame.Rect(10 + i * (self.sell_size + 2),
                                                            10 + j * (self.sell_size + 2), self.sell_size, self.sell_size))
