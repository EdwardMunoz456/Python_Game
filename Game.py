import pygame
import player_enemy_module

# add sprites to the screen
all_sprites = pygame.sprite.Group()
char = player_enemy_module.Player()
bad_dudes = player_enemy_module.red_her()

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
all_sprites.add(bad_dudes)

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


def collision_test(rect, tiles):
    collide_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            collide_list.append(tile)
    return collide_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    collide_list = collision_test(rect, tiles)
    for tile in collide_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    collide_list = collision_test(rect, tiles)
    for tile in collide_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


def game_loop():
    running = True
    left = False
    right = False
    jump = False
    air_timer = 0
    while running:
        display.fill((0, 0, 40))
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_UP:
                    if air_timer < 4:
                        jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
        char.rect, collisions = move(char.rect, char.movement, tile_rects)
        if air_timer > 4:
            jump = False
        if right:
            char.movement[0] = 4
        elif left:
            char.movement[0] = -4
        else:
            char.movement[0] = 0
        char.movement[1] += char.speedy
        if jump:
            char.movement[1] = -5
        char.speedy += 0.2
        if char.movement[1] >= 5:
            char.movement[1] = 5
        if collisions['bottom']:
            char.speedy = 0
            air_timer = 0
        elif collisions['top']:
            char.movement[1] = -char.movement[1]
        else:
            air_timer += 1
        all_sprites.update()
        all_sprites.draw(display)
        surface = pygame.transform.scale(display, (width, height))
        screen.blit(surface, (0, 0))
        pygame.display.flip()


game_loop()
