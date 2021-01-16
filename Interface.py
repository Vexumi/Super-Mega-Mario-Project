import pygame
from Variables import *
from Defs import *
from Player import player_group
from Platforms import *
import sys


class View_hp_hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(interface_group)
        self.image = loadimage('full_hp.png', 'Sprites')
        self.rect = self.image.get_rect()
        self.rect.x = screen_width - 20
        self.rect.y = screen_height - 20
        interface.append(self)
        self.type = 'Hp_hero'

    def update(self, event):
        hp = player_group.sprites()[0].hp
        if hp == 3:
            self.image = loadimage('full_hp.png', 'Sprites')
            self.rect = self.image.get_rect()
        elif hp == 2:
            self.image = loadimage('half_hp.png', 'Sprites')
            self.rect = self.image.get_rect()
        elif hp == 1:
            self.image = loadimage('low_hp.png', 'Sprites')
            self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = screen_height - 60


# класс паузы в игре
class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(interface_group)
        self.image = pygame.transform.scale(pause_image, (50, 50))
        self.rect = self.image.get_rect()
        interface.append(self)
        self.type = 'Pause'

    def update(self, event):
        global winner
        if self.rect.collidepoint(event.pos):
            Pause_sound.play()
            global game_started, in_game, is_music_on
            in_game = True
            game_started = True
            command = start_menu(True)
            if command[0] == 'New Game':
                player_group.sprites()[0].money = 0
                player_group.sprites()[0].go_die()
                player_group.sprites()[0].hp = 3

            if command[1]:
                if not is_music_on:
                    pygame.mixer.music.unpause()
                    is_music_on = True
            else:
                if is_music_on:
                    pygame.mixer.music.pause()
                    is_music_on = False


# класс создания кнопок в интерфейсе
class Interface(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__(menu_interface_group)
        self.type = type
        if self.type == 'Start':
            self.image = pygame.transform.scale(loadimage('play.png', 'image_data'), (150, 75))
            self.rect = self.image.get_rect().move(int(screen_width / 2) - 75,
                                                   int(screen_height / 2))
        elif self.type == 'Exit':
            self.image = pygame.transform.scale(loadimage('exit.png', 'image_data'), (150, 75))
            self.rect = self.image.get_rect().move(int(screen_width / 2) - 75,
                                                   int(screen_height / 2) + 140)
        elif self.type == 'New_game':
            self.image = pygame.transform.scale(loadimage('new game.png', 'image_data'), (150, 75))
            self.rect = self.image.get_rect().move(int(screen_width / 2) - 75,
                                                   int(screen_height / 2) + 75)
        elif self.type == 'Settings':
            self.image = pygame.transform.scale(loadimage('settings.png', 'image_data'), (70, 70))
            self.rect = self.image.get_rect().move(screen_width - 75, screen_height - 75)
        elif self.type == 'Question':
            self.image = pygame.transform.scale(loadimage('question.png', 'image_data'), (70, 70))
            self.rect = self.image.get_rect().move(screen_width - 75, screen_height - 75)
        elif self.type == 'Label':
            self.image = pygame.transform.scale(loadimage('label.png', 'image_data'), (500, 220))
            self.rect = self.image.get_rect().move(int(screen_width / 2) - 250, 75)
        elif self.type == 'Music':
            self.image = pygame.transform.scale(loadimage('music_on.png', 'image_data'),
                                                (70, 70))
            self.rect = self.image.get_rect().move(5, screen_height - 75)
        menu_interface.append(self)

    def update(self, event):
        if self.rect.collidepoint(event.pos) and self.type == 'Start':
            return 'Start'
        elif self.rect.collidepoint(event.pos) and self.type == 'Exit':
            return 'Exit'
        elif self.rect.collidepoint(event.pos) and self.type == 'New_game':
            return 'New Game'
        elif self.rect.collidepoint(event.pos) and self.type == 'Music':
            return 'Music'
        elif self.rect.collidepoint(event.pos) and self.type == 'Question':
            Question()
            return

    def change_image(self, new_image, size):
        self.image = pygame.transform.scale(loadimage(new_image, 'image_data'), size)


# загрузочный экран
def start_menu(game_started):
    global interface_group, is_music_on, menu_interface, now_level, trigger_to_close
    for sprite in menu_interface_group.sprites():
        sprite.kill()
    for sprite in menu_interface:
        sprite.kill()
    menu_interface = []
    size = screen_width, screen_height
    screen_menu = pygame.display.set_mode(size)
    screen_menu.fill((0, 100, 100))
    fon = pygame.transform.scale(screen_menu, (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    Label = Interface('Label')
    if game_started:
        Start = Interface('Start')
    New_game = Interface('New_game')
    Music = Interface('Music')
    Question = Interface('Question')
    Exit = Interface('Exit')
    if not is_music_on:
        Music.change_image('music_off.png', (70, 70))
    is_music = is_music_on
    FPS = 30
    clock = pygame.time.Clock()
    QUIT = False
    while True:
        screen.fill((0, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or QUIT:
                if game_started and in_game:
                    file = open('gamer.txt', mode='w', encoding='utf-8')
                    if player_group.sprites()[0].hp > 0:
                        file.write('game_started = True\n'
                                   'now_level = "{}"\n'
                                   'player_money = {}\n'
                                   'player_hp = {}'.format(player_group.sprites()[0].now_lvl,
                                                           player_group.sprites()[0].money,
                                                           player_group.sprites()[0].hp))
                    else:
                        file.write('game_started = False\n'
                                   'now_level = None\n'
                                   'player_money = 0\n'
                                   'player_hp = 3')
                    file.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    command = None
                    for i in menu_interface:
                        command = i.update(event)
                        if command == 'Start':
                            Play_sound.play()
                            return '', is_music
                        elif command == 'New Game':
                            for chest in chest_group.sprites():
                                chest.close_chest()
                            for queen in queen_group:
                                queen.founded = False
                            return 'New Game', is_music
                        elif command == 'Exit':
                            pygame.mixer.music.stop()
                            Exit_sound.play()
                            pygame.time.wait(80)
                            QUIT = True

                        elif command == 'Music':
                            if is_music:
                                Music.change_image('music_off.png', (70, 70))
                                is_music = False
                            else:
                                Music.change_image('music_on.png', (70, 70))
                                is_music = True
                            break
        menu_interface_group.draw(screen_menu)
        pygame.display.flip()
        clock.tick(FPS)


# экран смерти
def died_screen():
    global chest_group
    for sprite in chest_group.sprites():
        sprite.close_chest()
    Dead_sound.play()
    size = screen_width, screen_height
    screen_menu = pygame.display.set_mode(size)
    screen_menu.fill((80, 75, 75))
    fon = pygame.transform.scale(screen_menu, (screen_width, screen_height))
    screen.blit(fon, (0, 0))

    FPS = 30
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return
        displayText('You Died', color=pygame.Color('red'), size=80,
                    pos=(int(screen_width / 2) - 130, int(screen_height / 2) - 100))
        displayText('|Press any key|', color=pygame.Color('red'), size=20,
                    pos=(int(screen_width / 2) - 60, int(screen_height / 2) + 100))
        pygame.display.flip()
        clock.tick(FPS)


def winner_screen():
    Win_sound.play()
    if is_music_on:
        pygame.mixer.music.pause()
    size = screen_width, screen_height
    screen_menu = pygame.display.set_mode(size)
    screen_menu.fill((50, 150, 130))
    fon = pygame.transform.scale(screen_menu, (screen_width, screen_height))
    screen.blit(fon, (0, 0))

    FPS = 30
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if is_music_on:
                    pygame.mixer.music.unpause()
                Win_sound.stop()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if is_music_on:
                    pygame.mixer.music.unpause()
                Win_sound.stop()
                return
        displayText('You Win!', color=pygame.Color('blue'), size=80,
                    pos=(int(screen_width / 2) - 130, int(screen_height / 2) - 100))
        displayText('Your score: {}'.format(player_group.sprites()[0].money),
                    color=pygame.Color("green"), size=40,
                    pos=(int(screen_width / 2) - 110, int(screen_height / 2) + 50))
        displayText('|Press any key|', color=pygame.Color('blue'), size=20, pos=(335, 450))
        pygame.display.flip()
        clock.tick(FPS)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, text, size, size_text, text_pos, box_color, text_color,
                 fill_color=(0, 0, 0)):
        super().__init__(buttons_group)
        self.image = pygame.Surface(size)
        self.image.fill(fill_color)
        self.rect = self.image.get_rect().move(pos[0], pos[1])
        displayText(text, text_color, size_text, text_pos, None, self.image)
        pygame.draw.rect(self.image, box_color, (0, 0, self.rect.width, self.rect.height), 1)
        self.text = text

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            return self.text
        return None


def level_choose():
    global buttons_group
    buttons_group = pygame.sprite.Group()
    levels_list = ['level_1', 'level_2', 'sandbox']
    now_pos = [200, 200]
    size = (100, 40)
    size_text = 30
    text_pos = (5, 0)
    box_color = (100, 200, 100)
    text_color = (255, 255, 0)
    fill_color = (0, 100, 100)
    step = 150
    for level in levels_list:
        Button(now_pos, level, size, size_text, text_pos, box_color, text_color, fill_color)
        now_pos[0] += step

    FPS = 20
    clock = pygame.time.Clock()
    screen.fill((0, 100, 100))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Error'
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in buttons_group.sprites():
                    btn = sprite.update(event)
                    if btn:
                        return btn
        displayText('Choose level', (50, 255, 255), 80, (220, 30), None, screen)
        displayText('Выбор уровня в игре будет недоступен!', (150, 0, 0), 22, (240, 560), None,
                    screen)
        displayText('Потребуется перезапуск игры.', (150, 0, 0), 22, (280, 600), None, screen)
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def Question():
    FPS = 20
    clock = pygame.time.Clock()
    text_color = (255, 150, 100)
    screen.fill((0, 100, 100))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                return
        displayText('Управление:', text_color, 50, (100, 10))
        displayText('W - Arrow Up - прыжок', text_color, 25, (110, 70))
        displayText('A - Arrow Left - влево', text_color, 25, (110, 95))
        displayText('D - Arrow Right - вправо', text_color, 25, (110, 120))

        displayText('Цель:', text_color, 50, (100, 200))
        displayText('* Вам нужно добраться до принцессы', text_color, 25, (110, 260))
        displayText('собрав максимальное количество монет.', text_color, 25, (130, 285))
        displayText('* У вас есть 3 жизни, после смерти уровень начнется', text_color, 25, (110, 310))
        displayText('заново и вы потеряете 15 монет.', text_color, 25, (130, 335))

        displayText('|Press any key|', color=text_color, size=20, pos=(335, 450))
        pygame.display.flip()
        clock.tick(FPS)


# отображение текста
def displayText(text, color, size=50, pos=(100, 100), flag=None, sc=screen):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', size)
    textsurface = font.render(str(text), False, color)
    sc.blit(textsurface, pos)
    # отображение счетчика монет есть есть флаг "+coin"
    if flag == '+coin':
        coin = loadimage('coin.png', 'image_data')
        sc.blit(coin, (screen_width - 35, 13))
