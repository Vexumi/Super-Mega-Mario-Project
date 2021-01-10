import pygame
from Defs import loadimage, load_level
from Variables import *
from Player import *

# спрайты платформ
platform_image = {
    'wall': loadimage('platform.png', 'image_data'),
    'grass': loadimage('grass.png', 'image_data'),
    'underground': loadimage('underground.png', 'image_data')
}


# создание платформы для уровня
class Platform(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(platform_group)
        self.image = platform_image[type]
        self.rect = self.image.get_rect().move(
            platform_width * pos_x, platform_height * pos_y)
        platforms.append(self)


# генерация мира
def generate_level(level, lvl, money, hp):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':  # создание кирпичного блока
                Platform('wall', x, y)
            elif level[y][x] == '@':  # создание персонажа
                if not (game_started):
                    new_player = Player(loadimage("idle_right.png", 'Sprites', (255, 255, 255)), 10,
                                        1, x * platform_width, y * platform_height, money=0, hp=3,
                                        lvl=lvl)
                else:
                    new_player = Player(loadimage("idle_right.png", 'Sprites', (255, 255, 255)), 10,
                                        1, x * platform_width, y * platform_height,
                                        money=money,
                                        hp=hp, lvl=lvl)
            elif level[y][x] == '-':  # создание блока травы
                Platform('grass', x, y)
            elif level[y][x] == '+':  # создание блока земли
                Platform('underground', x, y)
            elif level[y][x] == 'O':  # создание шипов направленных во все стороны
                Enemy('360_spike', x, y)
            elif level[y][x] == 'L':  # создание стреляющего монстра влево
                Enemy('Shoot_monster_left', x, y, 'Left')
            elif level[y][x] == 'R':  # создание стреляющего монстра вправо
                Enemy('Shoot_monster_right', x, y, 'Right')
            elif level[y][x] == 'U':  # создание стреляющего монстра вверх
                Enemy('Shoot_monster_up', x, y, 'Up')
            elif level[y][x] == 'D':  # создание стреляющего монстра вниз
                Enemy('Shoot_monster_down', x, y, 'Down')
            elif level[y][x] == 'C':  # создание сундука
                Chest(x, y)
            elif level[y][x] == 'T':
                Trigger(x, y, platform_width, platform_height,
                        'New_level_triggered')  # триггер для смены уровня
            elif level[y][x] == 'Q':  # создание принцессы
                Queen(x, y)
            elif level[y][x] == 'B':
                Secret(x, y)

    return new_player, x, y


# класс триггера
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
