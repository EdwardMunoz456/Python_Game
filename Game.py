import pygame
import player_enemy_module
# add main character to the screen
all_sprites = pygame.sprite.Group()
char = player_enemy_module.Player()
enemy = player_enemy_module.Enemy()
# setting variables for the screen
width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
FPS = 60
clock = pygame.time.Clock()
# the character
all_sprites.add(char)
all_sprites.add(enemy)
def game_loop():
    running = True
    while running:
        start_ticks = pygame.time.get_ticks()  # starter tick
        clock.tick(FPS)
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if char.in_air == True:
            char.speedy += 0.2
        else:
            char.speedy = 0
        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        print(char.speedy)
game_loop()