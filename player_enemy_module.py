import pygame
# screen width and height
width = 500
height = 500
# were place holders for characters
sprite1 = pygame.Surface((16, 16))
sprite2 = pygame.Surface((16, 16))
sprite3 = pygame.Surface((16, 16))
# facing left or right
left = False
right = False
# the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/character.png")
        self.image = pygame.transform.scale(self.image, (16, 32))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.left = 272
        self.rect.top = 320
        # used for movement and collision calculation
        self.speedx = 0
        self.speedy = 0
        self.movement = [0,0]

#boundaries and the rect and image move at the same rate
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


# Red herring or the one you want to avoid
class red_her(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/time_waste.png")
        self.image = pygame.transform.scale(self.image, (16, 32))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 352
        self.rect.bottom = 272


# Goal or the one you want to help
class goal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/need_help.png")
        self.image = pygame.transform.scale(self.image, (32, 16))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.rect.left = 0
        self.rect.bottom = 48
