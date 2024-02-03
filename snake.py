import pygame

class Snake():
    def __init__(self):
        self.position = [(0, 0)]
        self.length = 1

    def draw(self, screen):
        pass

    def update(self, direction, temp_map, map_size):
        event = None

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
            print('AppleEaten')
            self.length += 1
            event = 'AppleEaten'

        if head in self.position or temp_map[head[0]][head[1]] == 3:
            return 'GameOver'
        else:
            self.position.append(head)
        return event