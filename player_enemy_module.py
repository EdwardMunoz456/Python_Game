import pygame
import random
width = 1000
height = 1000
sprite1 = pygame.Surface((50, 50))
sprite2 = pygame.Surface((50, 50))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite1
        self.image.fill((225, 225, 225))
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.speedy = 0
        self.in_air = False
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.y += self.speedy
        if self.rect.top > 950:
            self.rect.top = 950
            self.speedy = 0
            self.in_air = False
        else:
            self.in_air = True
        if self.rect.bottom < 50:
            self.rect.bottom = 50

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite2
        self.image.fill((225, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(20, 950)
        self.rect.bottom = random.randint(100, 400)