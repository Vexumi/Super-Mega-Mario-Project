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


def Question():
    FPS = 20
    clock = pygame.time.Clock()
    text_color = (255, 150, 100)
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


Question()
pygame.quit()
