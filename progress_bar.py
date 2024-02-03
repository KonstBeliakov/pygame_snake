import pygame

class ProgressBar():
    def __init__(self, volume, max_volume, sector_size=1):
        self.volume = volume
        self.size = (100, 30)
        self.max_volume = max_volume
        self.color = (0, 255, 0)
        self.bg_color = (25, 25, 25)
        self.border_color = (50, 50, 50)
        self.position = (10, 10)
        self.sector_volume = sector_size
        self.border_width = 2

    def set_position(self, x, y):
        self.position = (x, y)

    def set_color(self, color):
        self.color = color

    def set_volume(self, volume):
        self.volume = volume

    def set_size(self, size):
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, self.border_color,
                         pygame.Rect(self.position[0] - self.border_width, self.position[1] - self.border_width,
                                     self.size[0] + self.border_width * 2, self.size[1] + self.border_width * 2))
        pygame.draw.rect(screen, self.bg_color, pygame.Rect(*self.position, *self.size))

        sector_size = self.size[0] * self.sector_volume // self.max_volume - self.border_width
        for i in range(self.volume // self.sector_volume):
            pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0] + i * (sector_size + self.border_width),
                                                             self.position[1], sector_size, self.size[1]))