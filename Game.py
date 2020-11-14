import pygame
import player_enemy_module
# Game text
pygame.font.init()
font = pygame.font.SysFont('none', 30)
pda_font = pygame.font.SysFont('none', 20)
menu = font.render('press space to start', False, (0, 0, 0))
control_press = font.render('enter for controls', False, (0, 0, 0))
controls = font.render(f'''Arrow keys for movement Space to dash''', False, (255, 255, 255))
menu_return = font.render('Backspace to return to the menu', False, (255, 255, 255))
control_menu = controls.get_width() / 2
start_text = menu.get_width() / 2
control_text = control_press.get_width() / 2
return_placement = menu_return.get_width() / 2

dialogue = ["> It's night, people will need help I should get moving.",
            "> use the arrow keys to move ",
            "This cliff is high, but I should be able to jump over it.",
            "> press the up arrow key to jump",
            "If I focus my energy I should be able to burst forward.",
            "> press space to dash ",
            "Thank you so much I cant offer you much, please take this.",
            "I appreciate the help, you will be handsomely rewarded. "]
# color
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
# add sprites to the screen
all_sprites = pygame.sprite.Group()
char = player_enemy_module.Player()
bad_dudes = player_enemy_module.red_her()
help_him = player_enemy_module.goal()
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
all_sprites.add(help_him)

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
def start_screen():
    running = True
    control_screen = False
    start = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    control_screen = True
                if event.key == pygame.K_BACKSPACE:
                    control_screen = False
                if event.key == pygame.K_UP:
                    start = True
        if control_screen:
            display.fill(black)
            display.blit(controls, (250 - control_menu, 220))
            display.blit(menu_return, (250 - return_placement, 250))
            surface = pygame.transform.scale(display, (width, height))
            screen.blit(surface, (0, 0))
            pygame.display.flip()
        elif control_screen == False:
            display.fill(white)
            display.blit(control_press, (250 - control_text, 250))
            display.blit(menu, (250 - start_text, 100))
            surface = pygame.transform.scale(display, (width, height))
            screen.blit(surface, (0, 0))
            pygame.display.flip()
        if start:
            running = False
            tutorial()
def tutorial():
    round = 0
    facing_left = False
    facing_right = True
    dash = True
    cooldown = 300
    use = 20
    running = True
    text = True
    left = False
    right = False
    jump = False
    air_timer = 0
    game_map = load_map('tutorial_level')
    checkpoint = pygame.Rect(272, 320, 16, 16)
    checkpoint1 = pygame.Rect(128, 320, 16, 16)
    checkpoint2 = pygame.Rect(149, 240, 16, 16)
    while running:
        clock.tick(FPS)
        display.fill(black)

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
                    facing_left = False
                    facing_right = True
                if event.key == pygame.K_LEFT:
                    left = True
                    facing_left = True
                    facing_right = False
                if event.key == pygame.K_UP:
                    if air_timer < 4:
                        jump = True
                if event.key == pygame.K_SPACE:
                    if cooldown <= 0:
                        dash = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
        if help_him.rect.colliderect(char.rect):
            level_complete = True
        char.rect, collisions = move(char.rect, char.movement, tile_rects)
        if air_timer > 4:
            jump = False
        if right:
            char.movement[0] = 3
        elif left:
            char.movement[0] = -3
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
        if dash:
            if facing_right:
                char.movement[0] = 8
                char.movement[1] = 0
                cooldown = 300
            elif facing_left:
                char.movement[0] = -8
                char.movement[1] = 0
                cooldown = 300
        if use == 0:
            dash = False
            use = 20
        if dash:
            use -= 1
        cooldown -= 1
        if cooldown < 0:
            cooldown = 0
        all_sprites.update()
        all_sprites.draw(display)
        surface = pygame.transform.scale(display, (width, height))
        screen.blit(surface, (0, 0))
        if checkpoint.colliderect(char.rect):
            pda = True
            while pda:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pda = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        checkpoint.move_ip(200,200)
                        checkpoint.inflate_ip(1, 1)
                        pygame.event.clear()
                        pda = False

                display.fill((0, 20, 0))
                text1 = pda_font.render(dialogue[0], False, (green))
                text2 = pda_font.render(dialogue[1], False, (white))
                display.blit(text1,(2, 0))
                display.blit(text2, (2, 15))
                surface = pygame.transform.scale(display, (width, height))
                screen.blit(surface, (0, 0))
                pygame.display.flip()
        if checkpoint1.colliderect(char.rect):
            pda = True
            while pda:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pda = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        checkpoint1.move_ip(200,200)
                        checkpoint1.inflate_ip(1, 1)
                        pygame.event.clear()
                        pda = False

                display.fill((0, 20, 0))
                text1 = pda_font.render(dialogue[0], False, (green))
                text2 = pda_font.render(dialogue[1], False, (white))
                text3 = pda_font.render(dialogue[2], False, (green))
                text4 = pda_font.render(dialogue[3], False, (white))
                display.blit(text1,(2, 0))
                display.blit(text2, (2, 15))
                display.blit(text3, (2, 30))
                display.blit(text4, (2, 45))
                surface = pygame.transform.scale(display, (width, height))
                screen.blit(surface, (0, 0))
                pygame.display.flip()

        if checkpoint2.colliderect(char.rect):
            pda = True
            while pda:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pda = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        checkpoint2.move_ip(200, 200)
                        checkpoint2.inflate_ip(1, 1)
                        pygame.event.clear()
                        pda = False

                display.fill((0, 20, 0))
                text1 = pda_font.render(dialogue[0], False, (green))
                text2 = pda_font.render(dialogue[1], False, (white))
                text3 = pda_font.render(dialogue[2], False, (green))
                text4 = pda_font.render(dialogue[3], False, (white))
                text5 = pda_font.render(dialogue[4], False, (green))
                text6 = pda_font.render(dialogue[5], False, (white))
                display.blit(text1, (2, 0))
                display.blit(text2, (2, 15))
                display.blit(text3, (2, 30))
                display.blit(text4, (2, 45))
                display.blit(text5, (2, 60))
                display.blit(text6, (2, 75))
                surface = pygame.transform.scale(display, (width, height))
                screen.blit(surface, (0, 0))
                pygame.display.flip()
        if bad_dudes.rect.colliderect(char.rect):
            pda = True
            while pda:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pda = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        checkpoint2.move_ip(200, 200)
                        checkpoint2.inflate_ip(1, 1)
                        pygame.event.clear()
                        pda = False

                display.fill((0, 20, 0))
                text1 = pda_font.render(dialogue[0], False, (green))
                text2 = pda_font.render(dialogue[1], False, (white))
                text3 = pda_font.render(dialogue[2], False, (green))
                text4 = pda_font.render(dialogue[3], False, (white))
                text5 = pda_font.render(dialogue[4], False, (green))
                text6 = pda_font.render(dialogue[5], False, (white))
                text7 = pda_font.render(dialogue[7], False, (blue))
                wide = text7.get_width()
                display.blit(text1, (2, 0))
                display.blit(text2, (2, 15))
                display.blit(text3, (2, 30))
                display.blit(text4, (2, 45))
                display.blit(text5, (2, 60))
                display.blit(text6, (2, 75))
                display.blit(text7, (500 - wide, 90))
                surface = pygame.transform.scale(display, (width, height))
                screen.blit(surface, (0, 0))
                pygame.display.flip()


        pygame.display.flip()
        print(char.rect.topleft)
        pygame.display.flip()
def game_loop():
    seconds = 30
    level_complete = False
    running = True
    left = False
    right = False
    jump = False
    air_timer = 0
    while running:
        display.fill((50, 0, 255))
        clock.tick(FPS)
        level = 0
        timer = font.render(str(seconds), False, (black))
        game_map = load_map('level_1')
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
        if help_him.rect.colliderect(char.rect):
            level_complete = True
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


start_screen()
