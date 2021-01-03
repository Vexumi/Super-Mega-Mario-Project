import pygame
from Variables import *
from Defs import *
from Player import player_group
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
            global game_started, in_game
            in_game = True
            game_started = True
            command = start_menu(True)
            if command == 'New Game':
                player_group.sprites()[0].money = 0
                player_group.sprites()[0].go_die()
                player_group.sprites()[0].hp = 3


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
            self.rect = self.image.get_rect().move(5, screen_height - 75)
        elif self.type == 'Label':
            self.image = pygame.transform.scale(loadimage('label.png', 'image_data'), (500, 220))
            self.rect = self.image.get_rect().move(int(screen_width / 2) - 250, 75)
        menu_interface.append(self)

    def update(self, event):
        if self.rect.collidepoint(event.pos) and self.type == 'Start':
            return 'Start'
        elif self.rect.collidepoint(event.pos) and self.type == 'Exit':
            return 'Exit'
        elif self.rect.collidepoint(event.pos) and self.type == 'New_game':
            return 'New Game'


# загрузочный экран
def start_menu(game_started):
    global interface_group
    for sprite in menu_interface_group.sprites():
        sprite.kill()
    size = screen_width, screen_height
    screen_menu = pygame.display.set_mode(size)
    screen_menu.fill((0, 100, 100))
    fon = pygame.transform.scale(screen_menu, (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    Label = Interface('Label')
    if game_started:
        Start = Interface('Start')
    New_game = Interface('New_game')
    Exit = Interface('Exit')
    # Settings = Interface("Settings")
    # Question = Interface('Question')
    FPS = 30
    clock = pygame.time.Clock()
    QUIT = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or QUIT:
                if game_started and in_game:
                    file = open('gamer.txt', mode='w', encoding='utf-8')
                    file.write('game_started = {}\n'
                               'now_level = "{}"\n'
                               'player_money = {}\n'
                               'player_hp = {}'.format(game_started, now_level,
                                                       player_group.sprites()[0].money,
                                                       player_group.sprites()[0].hp))
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
                            return
                        elif command == 'New Game':
                            for chest in chest_group.sprites():
                                chest.close_chest()
                            for queen in queen_group:
                                queen.founded = False
                            return 'New Game'
                        elif command == 'Exit':
                            pygame.mixer.music.stop()
                            Exit_sound.play()
                            pygame.time.wait(80)
                            QUIT = True
        menu_interface_group.draw(screen_menu)
        pygame.display.flip()
        clock.tick(FPS)


# экран смерти
def died_screen():
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
                pygame.mixer.music.unpause()
                Win_sound.stop()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
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


# отображение текста
def displayText(text, color, size=50, pos=(100, 100), flag=None):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', size)
    textsurface = font.render(str(text), False, color)
    screen.blit(textsurface, pos)
    # отображение счетчика монет есть есть флаг "+coin"
    if flag == '+coin':
        coin = loadimage('coin.png', 'image_data')
        screen.blit(coin, (screen_width - 35, 13))
