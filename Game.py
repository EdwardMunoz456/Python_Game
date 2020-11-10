import pygame
import player_enemy_module

# add sprites to the screen
all_sprites = pygame.sprite.Group()
char = player_enemy_module.Player()
enemy = player_enemy_module.Enemy()

# setting variables for the screen
width = 1000
height = 1000

# the screen and display
screen = pygame.display.set_mode((width, height))
display = pygame.Surface((500, 500))

# timekeeping code
FPS = 60
clock = pygame.time.Clock()

# the character
all_sprites.add(char)
all_sprites.add(enemy)

# map tiles
grass_tile = pygame.image.load("tile000.png")
dirt_tile = pygame.image.load("tile002.png")
tile_size = grass_tile.get_width()


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map('tutorial_level')


def game_loop():
    running = True
    while running:
        display.fill((0, 100, 225))
        clock.tick(FPS)
        tile_rects = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(dirt_tile, (x * tile_size, y * tile_size))
                if tile == '2':
                    display.blit(grass_tile, (x * tile_size, y * tile_size))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
                x += 1
            y += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if char.in_air:
            char.speedy += 0.2
        else:
            char.speedy = 0
        all_sprites.update()
        all_sprites.draw(display)
        surface = pygame.transform.scale(display, (width, height))
        screen.blit(surface, (0, 0))
        pygame.display.flip()


game_loop()
