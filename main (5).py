import pygame
from pygame.locals import *
import random

pygame.init()

CLOCK = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 752
SCREEN_HEIGHT = 652

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     
pygame.display.set_caption('Flappy Bird')


FONT = pygame.font.SysFont('Bauhaus 93', 60)

WHITE = (255, 255, 255)

GROUND_SCROLL = 0
SCROLL_SPEDD = 4
FLYING = False
GAME_OVER = False
PIPE_GAP = 150
PIPE_FREQUENCY = 1500 
LAST_PIPE = pygame.time.get_ticks() - PIPE_FREQUENCY
SCORE = 0
PASS_PIPE = False


BG = pygame.image.load('bg.png')
GROUND_IMG = pygame.image.load('ground.png')
BUTTON_IMG = pygame.image.load('restart.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    score = 0
    return score



class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if FLYING == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if GAME_OVER == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(PIPE_GAP / 2)]

    def update(self):
        self.rect.x -= SCROLL_SPEDD
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(SCREEN_HEIGHT / 2))

bird_group.add(flappy)

button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, BUTTON_IMG)

run = True
while run:

    CLOCK.tick(FPS)

    screen.blit(BG, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(GROUND_IMG, (GROUND_SCROLL, 768))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and PASS_PIPE == False:
            PASS_PIPE = True
        if PASS_PIPE == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                SCORE += 1
                PASS_PIPE = False


    draw_text(str(SCORE), FONT, WHITE, int(SCREEN_WIDTH / 2), 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        GAME_OVER = True

    if flappy.rect.bottom >= 768:
        GAME_OVER = True
        FLYING = False


    if GAME_OVER == False and FLYING == True:

        time_now = pygame.time.get_ticks()
        if time_now - LAST_PIPE > PIPE_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            LAST_PIPE = time_now


        GROUND_SCROLL -= SCROLL_SPEDD
        if abs(GROUND_SCROLL) > 35:
            GROUND_SCROLL = 0

        pipe_group.update()


    if GAME_OVER == True:
        if button.draw() == True:
            GAME_OVER = False
            SCORE = reset_game()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and FLYING == False and GAME_OVER == False:
            FLYING = True

    pygame.display.update()

pygame.quit()