import pygame
from Defs import loadimage, load_music

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
in_game = False

# инициализация игры
pygame.init()
pygame.display.set_caption('Mega Mario Boooooooooy')
size = width, height = screen_width, screen_height
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))
now_level = None
go_next_lvl = False
is_hero_live = True

# Music and Sounds
pygame.mixer.init()
music = pygame.mixer.music.load(load_music('Race to Mars.mp3', 'D:\Git_projects\SMMP\sound_data'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()

Dead_sound = pygame.mixer.Sound(load_music('dead_sound.mp3', 'sound_data'))
Jump_sound = pygame.mixer.Sound(load_music('jump_sound.mp3', 'sound_data'))
Exit_sound = pygame.mixer.Sound(load_music('Exit_sound_2.mp3', 'sound_data'))
Hit_sound = pygame.mixer.Sound(load_music('hit_sound.mp3', 'sound_data'))
Pause_sound = pygame.mixer.Sound(load_music('pause_btn_sound.mp3', 'sound_data'))
Play_sound = pygame.mixer.Sound(load_music('play btn sound.mp3', 'sound_data'))
Checkpoint_sound = pygame.mixer.Sound(load_music('checkpoint_loaded_sound.mp3', 'sound_data'))
Chest_sound = pygame.mixer.Sound(load_music('get_money_sound.mp3', 'sound_data'))
Batman_sound = pygame.mixer.Sound(load_music('batman.mp3', 'sound_data'))
Win_sound = pygame.mixer.Sound(load_music('win_sound.mp3', 'sound_data'))

is_music_on = True

# enemies
enemies = []
enemies_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# queen group
queen_group = pygame.sprite.Group()

secret_group = pygame.sprite.Group()

# переменные связанные с платформой и спрайтами
platform_group = pygame.sprite.Group()

# платформы
platform_width = 32
platform_height = 32
global_offset = [0, 0]
trigger_group = pygame.sprite.Group()

# winner
winner = False

# сундук
chest_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()


def init_vars_def():
    a = []
    file = open('init_var.txt', mode='r', encoding='utf-8')
    data = file.readlines()
    data = [i.rstrip('\n') for i in data]
    for i in data:
        a.append(i)
    file.close()
    return a
