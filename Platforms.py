import pygame
from Defs import loadimage, load_level
from Variables import *
from Player import *
# платформа
platform_image = {
    'wall': loadimage('platform.png', 'image_data'),
    'grass': loadimage('grass.png', 'image_data'),
    'underground': loadimage('underground.png', 'image_data')
}

level = load_level('level_1.txt')
level_width = platform_width * len(level[0])
level_height = platform_height * len(level)

# переменные связанные с платформой и спрайтами
platform_group = pygame.sprite.Group()


# создание платформы для уровня
class Platform(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(platform_group, all_sprites)
        self.image = platform_image[type]
        self.rect = self.image.get_rect().move(
            platform_width * pos_x, platform_height * pos_y)
        platforms.append(self)


# генерация мира
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Platform('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(loadimage("idle_right.png", 'Sprites', (255, 255, 255)), 10, 1, x * platform_width, y * platform_height, money=100, hp=3)
            elif level[y][x] == '-':
                Platform('grass', x, y)
            elif level[y][x] == '+':
                Platform('underground', x, y)
            elif level[y][x] == 'S':
                Enemy('360_spike', x, y)
    return new_player, x, y