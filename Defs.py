import pygame
import os
import sys


# загрузка изображения спрайта
def loadimage(name, directory, colorkey=None):
    fullname = os.path.join(directory, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# загрузка мира
def load_level(filename):
    global now_level
    now_level = filename[:-4]
    filename = "level_data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_music(name, directory):
    fullname = os.path.join(directory, name)
    return fullname

def import_gamer():
    global game_started, now_level, player_money, player_hp
    file = open('gamer.txt', mode='r', encoding='utf-8')
    data = file.readlines()
    data = [i.rstrip('\n') for i in data]
    for i in data:
        exec(i)
    file.close()
