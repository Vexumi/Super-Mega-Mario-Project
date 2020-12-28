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


class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(interface_group)
        self.image = pygame.transform.scale(pause_image, (50, 50))
        self.rect = self.image.get_rect()
        interface.append(self)

    def update(self, event):
        if self.rect.collidepoint(event.pos):
            global game_started, in_game
            in_game = True
            game_started = True
            command = start_menu(True)
            if command == 'New Game':
                print('New Game Started from Pause')

                global now_level
                now_level = 'level_1'
                game_started = True
                file = open('gamer.txt', mode='w', encoding='utf-8')
                file.write("game_started = False\nnow_level = 'level_1'\nplayer_money = None\nplayer_hp = None")
                file.close()

                for i in test():
                    exec(i)
                in_game = True


class Interface(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__(menu_interface_group)
        self.type = type
        if self.type == 'Start':
            self.image = pygame.transform.scale(loadimage('play.png', 'image_data'), (150, 75))
            self.rect = self.image.get_rect().move(int(screen_width / 2) - 75, int(screen_height / 2))
        elif self.type == 'Exit':
            self.image = pygame.transform.scale(loadimage('exit.png', 'image_data'), (150, 75))
            self.rect = self.image.get_rect().move(int(screen_width / 2) - 75, int(screen_height / 2) + 140)
        elif self.type == 'New_game':
            self.image = pygame.transform.scale(loadimage('new game.png', 'image_data'), (150, 75))
            self.rect = self.image.get_rect().move(int(screen_width / 2) - 75, int(screen_height / 2) + 75)
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


def start_menu(game_started):
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
    Settings = Interface("Settings")
    Question = Interface('Question')
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
                            return
                        elif command == 'New Game':
                            return 'New Game'
                        elif command == 'Exit':
                            QUIT = True
        menu_interface_group.draw(screen_menu)
        pygame.display.flip()
        clock.tick(FPS)
