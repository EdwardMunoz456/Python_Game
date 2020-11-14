import pygame
import random

width = 500
height = 500
sprite1 = pygame.Surface((16, 16))
sprite2 = pygame.Surface((16, 16))
sprite3 = pygame.Surface((16, 16))
left = False
right = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("character.png")
        self.image = pygame.transform.scale(self.image, (16, 32))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.left = 272
        self.rect.top = 320
        self.speedx = 0
        self.speedy = 0
        self.movement = [0,0]


    def update(self):
        self.movement[0] += self.speedx
        self.movement[1] += self.speedy
        self.speedx = 0
        self.speedy = 0

        if self.rect.right >= width:
            self.rect.right = width
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height
        if self.rect.top <= 0:
            self.rect.top = 0



class red_her(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite2
        self.image.fill((225, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.left = 352
        self.rect.bottom = 272



class goal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite3
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.left = 0 * 16
        self.rect.bottom = 4 * 16
