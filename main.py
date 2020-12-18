import pygame
from pygame import *
import os
import sys

file_dir = os.path.dirname(__file__)


def loadimage(name, directory, colorkey=None):
    fullname = os.path.join(directory, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "level_data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Platform(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, width, height = camera
    l, t = -l + screen_width / 2, -t + screen_height / 2

    l = min(0, l)
    l = max(-(camera.width - screen_width), l)
    t = max(-(camera.height - screen_height), t)
    t = min(0, t)

    return Rect(l, t, width, height)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.onGround = False
        self.jump_power = 10
        self.jump_extra_power = 15
        self.gravity = 0.35
        self.yvel = 0
        self.xvel = 0
        self.player_speed = 10

        self.image = player_image
        self.rect = self.image.get_rect().move(
            platform_width * pos_x + 15, platform_height * pos_y + 5)

    def update(self, up, left, right, running):
        if left:
            self.xvel = -self.player_speed
        if right:
            self.xvel = self.player_speed
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -self.jump_power
                if running and (right or left):  # если есть ускорение и мы движемся
                    self.yvel = -self.jump_extra_power  # то прыгаем выше
        if not self.onGround:
            self.yvel += self.gravity
        if not (left or right):
            self.xvel = 0
        self.onGround = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0)

    def collide(self, xvel, yvel):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if xvel > 0:
                    self.rect.x += self.xvel
                if xvel < 0:
                    self.rect.x -= self.xvel

                if yvel > 0:
                    self.rect.y -= self.yvel
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.y += self.yvel
                    self.yvel = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(platform_group, all_sprites)
        self.image = platform_image
        self.rect = self.image.get_rect().move(
            platform_width * pos_x, platform_height * pos_y)
        platforms.append(self)


def main():
    hero, x, y = generate_level(load_level('level_1.txt'))

    left = right = False  # по умолчанию - стоим
    up = False
    running = False

    Exit = True
    speed = 1
    fps = 60
    clock = pygame.time.Clock()

    while Exit:
        for event in pygame.event.get():
            if event.type == QUIT:
                Exit = False
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            if event.type == KEYDOWN and event.key == K_LSHIFT:
                running = True

            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LSHIFT:
                running = False
        screen.fill((0, 0, 0))
        hero.update(up, left, right, running)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


screen_width = 800
screen_height = 640
display = (screen_width, screen_height)
background_color = "#000000"
platforms = []
level = []

player_group = pygame.sprite.Group()
player_image = loadimage('0.png', 'mario')

platform_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
platform_image = loadimage('platform.png', 'image_data')
platform_width = 32
platform_height = 32

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Перемещение героя')
    size = width, height = screen_width, screen_height
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    main()
    pygame.quit()
