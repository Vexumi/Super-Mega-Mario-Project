import pygame
from Variables import *
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
        self.last_hp = player_group.sprites()[0].hp

    def update(self, event):
        hp = player_group.sprites()[0].hp
        if hp == 3 and self.last_hp != hp:
            self.image = loadimage('full_hp.png', 'Sprites')
            self.rect = self.image.get_rect()
        elif hp == 2 and self.last_hp != hp:
            self.image = loadimage('half_hp.png', 'Sprites')
            self.rect = self.image.get_rect()
        elif hp == 1 and self.last_hp != hp:
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
            start_menu()


class Interface(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__(menu_interface_group)
        self.type = type
        if self.type == 'Start':
            self.image = pygame.transform.scale(loadimage('play.png', 'image_data'), (150, 75))
            self.rect = self.image.get_rect().move(325, 260)
        elif self.type == 'Exit':
            self.image = pygame.transform.scale(loadimage('exit.png', 'image_data'), (150, 75))
            self.rect = self.image.get_rect().move(325, 360)
        menu_interface.append(self)

    def update(self, event):
        if self.rect.collidepoint(event.pos) and self.type == 'Start':
            return 'Start'
        elif self.rect.collidepoint(event.pos) and self.type == 'Exit':
            return 'Exit'


def start_menu():
    size = screen_width, screen_height
    screen_menu = pygame.display.set_mode(size)
    screen_menu.fill((0, 100, 100))
    fon = pygame.transform.scale(screen_menu, (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    a = Interface('Start')
    b = Interface('Exit')
    FPS = 60
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    command = None
                    for i in menu_interface:
                        command = i.update(event)
                        if command == 'Start':
                            return
                        elif command == 'Exit':
                            pygame.quit()
                            sys.exit()
        menu_interface_group.draw(screen_menu)
        pygame.display.flip()
        clock.tick(FPS)
