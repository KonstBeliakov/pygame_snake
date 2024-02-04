import pygame

def in_rect(click_pos, position, size):
    return position[0] <= click_pos[0] <= position[0] + size[0] and position[1] <= click_pos[1] <= position[1] + size[1]


class Button():
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.pressed = False
        self.color = (150, 150, 150)
        self.pressed_color = (100, 100, 100)

    def draw(self, screen):
        pygame.draw.rect(screen, self.pressed_color if self.pressed else self.color,
                         pygame.Rect(*self.position, *self.size))

    def update(self, event):
        if event == 'pressed':
            if in_rect(pygame.mouse.get_pos(), self.position, self.size):
                self.pressed = True
        if event == 'released':
            t = self.pressed
            self.pressed = False
            return t



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    gameOver = False

    b = Button((10, 10), (200, 30))
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                b.update('pressed')
            elif event.type == pygame.MOUSEBUTTONUP:
                b.update('released')

        b.draw(screen)

        pygame.display.flip()