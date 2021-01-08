import pygame

screen_width = 800
screen_height = 640
display = (screen_width, screen_height)
background_color = "#000000"
pygame.init()
pygame.display.set_caption('msrio ttest')
size = width, height = screen_width, screen_height
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

buttons_group = pygame.sprite.Group()


# отображение текста
def displayText(text, color, size=50, pos=(100, 100), flag=None, sc=screen):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', size)
    textsurface = font.render(str(text), False, color)
    sc.blit(textsurface, pos)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, text, size, size_text, text_pos, box_color, text_color):
        super().__init__(buttons_group)
        self.image = pygame.Surface(size)
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
    step = 150
    for level in levels_list:
        Button(now_pos, level, size, size_text, text_pos, box_color, text_color)
        now_pos[0] += step

    FPS = 20
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in buttons_group.sprites():
                    btn = sprite.update(event)
                    if btn:
                        return btn + '.txt'
        displayText('Choose level', (50, 255, 255), 80, (200, 30), None, screen)
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


print(level_choose())
pygame.quit()
