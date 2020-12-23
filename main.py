# импорт библиотек
import pygame
from pygame import *
import os
import sys
from Player import *
from Variables import *
from Defs import *
from Platforms import *
from Interface import *


# отображение текста
def displayText(text, color, size=50, pos=(100, 100), flag=None):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', size)
    textsurface = font.render(str(text), False, color)
    screen.blit(textsurface, pos)

    if flag == '+coin':
        coin = loadimage('coin.png', 'image_data')
        screen.blit(coin, (screen_width - 35, 13))


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
    camera.update(hero)
    hero.update(up, left, right, running)
    for i in enemies:
        i.update()
    screen.blit(background, (0, 0))
    chest_group.update()
    star_group.update()
    for sprite in all_sprites:
        camera.apply(sprite)


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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    interface_group.update(event)
        # screen.fill(pygame.Color('#086FA1'))
        update_sprites(up, left, right, running, background)
        hp_hero.update(None)
        star_group.draw(screen)
        all_sprites.draw(screen)
        interface_group.draw(screen)
        displayText(hero.money, (0, 255, 255), 30, (screen_width - 70, 10), '+coin')
        clock.tick(fps)
        pygame.display.update()

        if hero.hp == 0:
            Exit = False
            global reset_game
            reset_game = True


if __name__ == "__main__":
    command = start_menu(game_started)
    if command == 'New Game':
        game_started = True
        now_level = 'level_1'


    init = True
    while init:
        init_variables()
        init = False
        # переменная для переигрывания уровня
        reset_game = False
        # переменные для уровня
        hero, x, y = generate_level(load_level(now_level + '.txt'))

        # переменные для камеры
        camera = Camera(level_width, level_height)

        main()

        # переигрывание если True
        if reset_game: # TODO: перезапуск игры после смерти
            init = True

    pygame.quit()

    file = open('gamer.txt', mode='w', encoding='utf-8')
    file.write('game_started = {}\n'
               'now_level = "{}"\n'
               'save_pos = {}\n'
               'player_money = {}\n'
               'player_hp = {}'.format(game_started, now_level, (hero.rect.x, hero.rect.y), hero.money, hero.hp))
    file.close()


#game_started = False
#now_level = 'level_1'
#save_pos = [None, None]
#player_money = None
#player_hp = None