# импорт библиотек
import pygame
import importlib
from pygame import *
import os
import sys
from Player import *
from Variables import *
from Defs import *
from Platforms import *
from Interface import *


# класс камеры
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, level_width, level_height):
        self.dx = 0
        self.dy = 0
        self.world_offset = [0, 0]

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, offset=False):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

        global global_offset
        global_offset[0] += -(target.rect.x + target.rect.w // 2 - width // 2)
        global_offset[1] += -(target.rect.y + target.rect.h // 2 - height // 2)


# обновление всех спрайтов
def update_sprites(up, left, right, running, background):
    global hero, now_level, all_sprites, player_group, platforms, platform_group, x, y
    if hero.winner:
        winner_screen()
        command = start_menu(False)
        if command == 'New Game':
            hero.money = 0
            hero.go_die()
            hero.hp = 3
        hero.winner = False
    camera.update(hero)
    hero.update(up, left, right, running)
    for i in enemies:
        i.update()
    screen.blit(background, (0, 0))
    chest_group.update()
    star_group.update()
    for sprite in all_sprites:
        camera.apply(sprite)
    for sprite in platform_group:
        camera.apply(sprite)
    for sprite in queen_group:
        camera.apply(sprite)
        sprite.update()
    for sprite in secret_group:
        camera.apply(sprite)
        sprite.update()
    platform_group.draw(screen)
    for event in trigger_group.sprites():  # TODO: смена уровня
        if event.update(all_sprites) == 'New_level_triggered' and now_level != 'level_2':
            all_sprites = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            platform_group = pygame.sprite.Group()
            platforms = []
            now_level = 'level_2'
            hero, x, y = generate_level(load_level(now_level + '.txt'))
    bullet_group.update()
    for sprite in bullet_group:
        camera.apply(sprite)
    bullet_group.draw(screen)


# основная функция
def main():
    # переменные для определения передвижения персонажа
    left = right = False
    up = False
    running = False

    # переменные для управления игрой
    Exit = True
    speed = 1
    fps = 60
    clock = pygame.time.Clock()
    pause = Pause()
    hp_hero = View_hp_hero()
    hp_hero.last_hp = True
    hp_hero.update(None)
    background = pygame.transform.scale(loadimage('bg_underground.png', 'image_data'),
                                        (screen_width, screen_height))

    # основной цикл
    while Exit:
        for event in pygame.event.get():
            if event.type == QUIT:
                Exit = False
            if event.type == KEYDOWN and (event.key == K_UP or event.key == K_w):
                up = True
            if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_a):
                left = True
            if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_d):
                right = True
            if event.type == KEYDOWN and event.key == K_LSHIFT:
                running = True

            if event.type == KEYUP and (event.key == K_UP or event.key == K_w):
                up = False
            if event.type == KEYUP and (event.key == K_LEFT or event.key == K_a):
                left = False
            if event.type == KEYUP and (event.key == K_RIGHT or event.key == K_d):
                right = False
            if event.type == KEYUP and event.key == K_LSHIFT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    interface_group.update(event)
        update_sprites(up, left, right, running, background)
        hp_hero.update(None)
        star_group.draw(screen)
        all_sprites.draw(screen)
        queen_group.draw(screen)
        secret_group.draw(screen)
        player_group.draw(screen)
        interface_group.draw(screen)
        displayText(hero.money, (0, 255, 255), 30, (screen_width - 70, 10), '+coin')
        clock.tick(fps)
        pygame.display.update()
        if hero.hp == 0 or not is_hero_live:
            died_screen()
            hero.go_die()
            hero.hp = 3
            hero.money = 0

    file = open('gamer.txt', mode='w', encoding='utf-8')
    if hero.hp > 0:
        file.write('game_started = True\n'
                   'now_level = "{}"\n'
                   'player_money = {}\n'
                   'player_hp = {}'.format(now_level, hero.money, hero.hp))
    else:
        file.write('game_started = False\n'
                   'now_level = "level_1"\n'
                   'player_money = 0\n'
                   'player_hp = 3')
    file.close()

    return Exit


# старт игры
if __name__ == "__main__":
    in_game = False
    command = start_menu(game_started)

    if command == 'New Game':
        print('New Game Started')
        game_started = False
        now_level = "level_1"
        player_money = 0
        player_hp = 3
        in_game = False

    # переменные для уровня
    hero, x, y = generate_level(load_level(now_level + '.txt'))

    if command == 'New Game':
        hero.go_die()
        hero.hp = 3
        hero.money = 0

    # переменные для камеры
    camera = Camera(level_width, level_height)

    main()

    pygame.quit()
    sys.exit()
game_started = False
now_level = "level_1"
player_money = 0
player_hp = 3
