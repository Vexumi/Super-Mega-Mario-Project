import pygame
from Defs import loadimage

all_sprites = pygame.sprite.Group()
platforms = []

# переменные связанные с разрешением и pygame.screen
screen_width = 800
screen_height = 640
display = (screen_width, screen_height)
background_color = "#000000"

# интерфейс в игре
pause_image = loadimage('pause.png', 'image_data')
menu_interface = []
menu_interface_group = pygame.sprite.Group()
interface_group = pygame.sprite.Group()
interface = []

# инициализация игры
pygame.init()
pygame.display.set_caption('Mega Mario Boooooooooy')
size = width, height = screen_width, screen_height
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

# enemies
enemies = []
enemies_group = pygame.sprite.Group()

# платформы
platform_width = 32
platform_height = 32
global_offset = [0, 0]