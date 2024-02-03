import pygame

class ProgressBar():
    def __init__(self, volume, max_volume, ):
        self.volume = volume
        self.size = (100, 30)
        self.max_volume = max_volume
        self.color = (0, 255, 0)
        self.position = (10, 10)

    def set_position(self, x, y):
        self.position = (x, y)

    def set_color(self, color):
        self.color = color

    def set_volume(self, volume):
        self.volume = volume

    def set_size(self, size):
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1]))