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
        super().__init__(platform_group)
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
                if not (game_started):
                    print('new player')
                    new_player = Player(loadimage("idle_right.png", 'Sprites', (255, 255, 255)), 10,
                                        1, x * platform_width, y * platform_height, money=0, hp=3)
                else:
                    print('old player')
                    new_player = Player(loadimage("idle_right.png", 'Sprites', (255, 255, 255)), 10,
                                        1, x * platform_width, y * platform_height, money=player_money,
                                        hp=player_hp)
            elif level[y][x] == '-':
                Platform('grass', x, y)
            elif level[y][x] == '+':
                Platform('underground', x, y)
            elif level[y][x] == 'S':
                Enemy('360_spike', x, y)
            elif level[y][x] == 'M':
                Chest(x, y)
            elif level[y][x] == 'L':
                Trigger(x, y, platform_width, platform_height, 'New_level_triggered') # триггер для смены уровня

    return new_player, x, y


class Trigger(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, returned_trigger='Triggered'):
        super().__init__(all_sprites, trigger_group)
        self.image = pygame.transform.scale(loadimage('void.png', 'image_data'), (width, height))
        self.rect = self.image.get_rect().move(
            width * x, height * y)
        self.returned_trigger = returned_trigger

    def update(self, obj_group):
        if player_group.sprites()[0] in pygame.sprite.spritecollide(self, obj_group, False):
            return self.returned_trigger
        else:
            return False