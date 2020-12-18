import pygame
from pygame import *
import os
import sys


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
    return new_player, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, level_width, level_height):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.onGround = False
        self.jump_power = 10
        self.jump_extra_power = 1
        self.gravity = 0.35
        self.yvel = 0
        self.xvel = 0
        self.player_speed = 6
        self.player_speed_extra = 12
        self.money = 0

        self.image = player_image
        self.rect = self.image.get_rect().move(
            platform_width * pos_x + 15, platform_height * pos_y + 5)

    def update(self, up, left, right, running):
        if up:
            if self.onGround:
                self.yvel = -self.jump_power
                if running and (right or left):
                    self.yvel = -self.jump_extra_power
        if left:
            if running:
                self.xvel = -self.player_speed_extra
            else:
                self.xvel = -self.player_speed
        if right:
            if running:
                self.xvel = self.player_speed_extra
            else:
                self.xvel = self.player_speed
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
                    self.rect.right = platform.rect.left

                if xvel < 0:
                    self.rect.left = platform.rect.right

                if yvel > 0:
                    self.rect.bottom = platform.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = platform.rect.bottom
                    self.yvel = 0

    def teleport(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def go_die(self):
        if self.money >= 15:
            self.money -= 15
        else:
            self.money = 0

        self.teleport(startx, starty)


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(platform_group, all_sprites)
        self.image = platform_image
        self.rect = self.image.get_rect().move(
            platform_width * pos_x, platform_height * pos_y)
        platforms.append(self)


def main():
    left = right = False
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
        camera.update(hero)
        hero.update(up, left, right, running)
        all_sprites.draw(screen)
        for sprite in all_sprites:
            camera.apply(sprite)
        clock.tick(fps)
        pygame.display.update()


screen_width = 800
screen_height = 640
display = (screen_width, screen_height)
background_color = "#000000"
platforms = []

player_group = pygame.sprite.Group()
player_image = loadimage('0.png', 'mario')

platform_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
platform_image = loadimage('platform.png', 'image_data')
platform_width = 32
platform_height = 32

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Mega Mario Boooooooooy')
    size = width, height = screen_width, screen_height
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    level = load_level('level_1.txt')
    hero, startx, starty = generate_level(level)

    level_width = platform_width * len(level[0])
    level_height = platform_height * len(level)
    camera = Camera(level_width, level_height)

    main()
    pygame.quit()
