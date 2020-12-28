import pygame
import random
from Variables import *
from Defs import *

player_group = pygame.sprite.Group()

# враг
enemies_image = {'360_spike': loadimage('360_spike.png', 'image_data')}
enemy_width = 32
enemy_height = 32


# класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos_x, pos_y, money, hp):
        super().__init__(player_group, all_sprites)
        self.money = money
        self.hp = hp

        self.init_physics(pos_x, pos_y)

        self.init_animation(sheet, columns, rows, pos_x, pos_y)

    def init_physics(self, pos_x, pos_y):
        # физика персонажа
        self.last_move = None
        self.stay = True
        self.startx = pos_x
        self.starty = pos_y
        self.onGround = False
        self.jump_power = 10
        self.jump_extra_power = 1
        self.gravity = 0.35
        self.yvel = 0
        self.xvel = 0
        self.player_speed = 6
        self.player_speed_extra = 12
        self.last_yvel = 0

    def init_animation(self, sheet, columns, rows, x, y):
        # анимация
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

        self.iter = 0
        self.anim_idle_changed = True
        self.anim_run_changed = False
        self.anim_jump_changed = True
        self.now_animation = 'Idle_right'

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, up, left, right, running):
        if self.iter == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.iter = 0
        else:
            self.iter += 1
        if up:
            if self.onGround:
                self.yvel = -self.jump_power
                if running and (right or left):
                    self.yvel = -self.jump_extra_power
            self.anim_jump_changed = False
        if left:
            if running:
                self.xvel = -self.player_speed_extra
            else:
                self.xvel = -self.player_speed

            if self.last_move == 'Right':
                self.anim_run_changed = False
                self.anim_idle_changed = False
            self.last_move = 'Left'
        if right:
            if running:
                self.xvel = self.player_speed_extra
            else:
                self.xvel = self.player_speed

            if self.last_move == 'Left':
                self.anim_run_changed = False
                self.anim_idle_changed = False
            self.last_move = 'Right'

        if not self.onGround:
            self.yvel += self.gravity

        if not (left or right) or right and left:
            self.xvel = 0
            if not (self.anim_idle_changed):
                self.anim_idle_changed = False
                self.anim_jump_changed = True
                self.anim_run_changed = True

        self.onGround = False

        # смена анимации
        self.change_animation()

        # проверка коллизии
        self.rect.y += self.yvel
        self.collide(0, self.yvel)

        # проверка коллизии
        self.rect.x += self.xvel
        self.collide(self.xvel, 0)

        self.last_yvel = self.yvel

    def change_animation(self):
        # смена анимации
        if not (self.anim_run_changed) and self.xvel != 0:
            if self.xvel < 0 and -2 < self.yvel < 2:
                self.init_animation(loadimage("run_left.png", 'Sprites'), 8, 1,
                                    self.rect.x, self.rect.y)
                self.now_animation = 'Run_left'
            elif self.xvel > 0 and -2 < self.yvel < 2:
                self.init_animation(loadimage("run_right.png", 'Sprites'), 8, 1,
                                    self.rect.x, self.rect.y)
                self.now_animation = 'Run_right'
            self.anim_run_changed = True

        elif self.xvel == 0 and -2 < self.yvel < 2 and not (self.anim_idle_changed):
            if self.last_move == 'Left':
                self.init_animation(loadimage("idle_left.png", 'Sprites', ), 10, 1,
                                    self.rect.x, self.rect.y)
                self.now_animation = 'Idle_left'
            else:
                self.init_animation(loadimage("idle_right.png", 'Sprites'), 10, 1,
                                    self.rect.x, self.rect.y)
                self.now_animation = 'Idle_right'
            self.anim_idle_changed = True
        elif self.yvel < -1 and not (self.anim_jump_changed):
            if self.last_move == 'Left':
                self.init_animation(loadimage("jump_left.png", 'Sprites', ), 3, 1,
                                    self.rect.x, self.rect.y)
                self.now_animation = 'Jump_left'
            elif self.last_move == 'Right':
                self.init_animation(loadimage("jump_right.png", 'Sprites', ), 3, 1,
                                    self.rect.x, self.rect.y)
                self.now_animation = 'Jump_right'
        elif self.yvel > 2 and not (self.anim_jump_changed):
            if self.last_move == 'Left':
                self.init_animation(loadimage("down_left.png", 'Sprites', ), 3, 1,
                                    self.rect.x, self.rect.y)
                self.now_animation = 'Down_left'
            elif self.last_move == 'Right':
                self.init_animation(loadimage("down_right.png", 'Sprites', ), 3, 1,
                                    self.rect.x, self.rect.y)
                self.now_animation = 'Down_right'

        # проверка правильности направления анимации
        if self.xvel != 0 and self.now_animation[0:4] == 'Idle' and -2 < self.yvel < 2:
            self.anim_run_changed = False
        elif self.xvel == 0 and self.now_animation[0:4] != 'Idle' and -2 < self.yvel < 2:
            self.anim_idle_changed = False
        if self.yvel < 2 and self.now_animation[0:4] != 'Jump':
            self.anim_jump_changed = False
        elif self.yvel > -2 and self.now_animation[0:4] != 'Down':
            self.anim_jump_changed = False
        if 0 < self.xvel and self.now_animation == 'Run_left' and -2 < self.yvel < 2:
            self.anim_run_changed = False
        elif 0 > self.xvel and self.now_animation == 'Run_right' and -2 < self.yvel < 2:
            self.anim_run_changed = False

    # коллизия со стенками
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

    # телепорт персонажа
    def teleport(self, x, y):
        self.rect.x = x * platform_width + global_offset[0]
        self.rect.y = y * platform_height + global_offset[1]

        self.xvel = 0
        self.yvel = 0

    # смерть персонажа
    def go_die(self):
        self.hp -= 1

        if self.money >= 15:
            self.money -= 15
        else:
            self.money = 0

        self.teleport(int(self.startx / platform_width), int(self.starty / platform_height))
        pygame.time.wait(500)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = enemies_image[type]
        self.rect = self.image.get_rect().move(
            enemy_width * pos_x, enemy_height * pos_y)
        enemies.append(self)

    def update(self, *args):
        if player_group.sprites()[0] in pygame.sprite.spritecollide(self, all_sprites, False):
            for i in player_group:
                i.go_die()


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(chest_group, all_sprites)
        self.chest_power = random.randint(0, 100)
        self.closed = True

        self.image = loadimage('chest_close.png', 'image_data')
        self.rect = self.image.get_rect().move(
            x * platform_width, y * platform_height)

    def update(self, *args):
        if self.closed and (
                player_group.sprites()[0] in pygame.sprite.spritecollide(self, all_sprites, False)):
            self.image = loadimage('chest_open.png', 'image_data')
            self.closed = False
            player_group.sprites()[0].money += self.chest_power
            self.create_particles((self.rect.x, self.rect.y))

    def create_particles(self, position):
        # количество создаваемых частиц
        particle_count = 20
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))


class Particle(pygame.sprite.Sprite):
    screen_rect = (0, 0, screen_width, screen_height)
    # сгенерируем частицы разного размера
    fire = [loadimage("star.png", 'image_data')]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(star_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos[0], pos[1] - 30

        # гравитация будет одинаковой (значение константы)
        self.gravity = -0.35

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(self.screen_rect):
            self.kill()
