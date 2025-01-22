import pygame
import sys

from pygame.cursors import diamond

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 760, 580
TILE_SIZE = 20
FPS = 60

# Colors
FONT_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (150, 150, 150)

# Fonts
font = pygame.font.Font(None, 36)  # Default Pygame font
large_font = pygame.font.Font(None, 72)

# Physics constants
GRAVITY = 0.3
JUMP_HEIGHT_TILES = 4.5  # Desired jump height in tiles
JUMP_STRENGTH = -(2 * GRAVITY * (JUMP_HEIGHT_TILES * TILE_SIZE)) ** 0.5
TERMINAL_VELOCITY = 5

# Load images
fireboy_image = pygame.image.load("resources/pngs/Fireboy-0.png")
watergirl_image = pygame.image.load("resources/pngs/Watergirl2-0.png")
lava_image = pygame.image.load("resources/pngs/lava_small.png")
water_image = pygame.image.load("resources/pngs/water_small.png")
green_stuff_image = pygame.image.load("resources/pngs/green_stuff_small.png")
exit_fire_image = pygame.image.load("resources/pngs/door_fireboy.png")
exit_water_image = pygame.image.load("resources/pngs/door_watergirl.png")
tile_image = pygame.image.load("resources/pngs/tile2.png")
background_image = pygame.image.load("resources/pngs/level_background.png")
blue_gem_image = pygame.image.load("resources/pngs/blue_gem.png")
red_gem_image = pygame.image.load("resources/pngs/red_gem.png")
ramp_left_image = pygame.image.load("resources/pngs/ramp_left.png")
ramp_right_image = pygame.image.load("resources/pngs/ramp_right.png")
cube_image = pygame.image.load("resources/pngs/cube.png")
platform_blue_image = pygame.image.load("resources/pngs/platform_blue.png")
platform_orange_image = pygame.image.load("resources/pngs/platform_orange.png")
lever_orange_image = pygame.image.load("resources/pngs/lever_orange.png")
lever_blue_image = pygame.image.load("resources/pngs/lever_blue.png")
button_blue_image = pygame.image.load("resources/pngs/button_blue.png")
button_orange_image = pygame.image.load("resources/pngs/button_orange.png")
menu_background_image = pygame.image.load("resources/pngs/TempleHallForest_menu_background.jpg")

# Scale images
fireboy_image = pygame.transform.scale(fireboy_image, (35, 50))
watergirl_image = pygame.transform.scale(watergirl_image, (35, 50))
lava_image = pygame.transform.scale(lava_image, (5 * TILE_SIZE, TILE_SIZE))
water_image = pygame.transform.scale(water_image, (5 * TILE_SIZE, TILE_SIZE))
green_stuff_image = pygame.transform.scale(green_stuff_image, (5 * TILE_SIZE, TILE_SIZE))
exit_fire_image = pygame.transform.scale(exit_fire_image, (2.5 * TILE_SIZE, 3 * TILE_SIZE))
exit_water_image = pygame.transform.scale(exit_water_image, (2.5 * TILE_SIZE, 3 * TILE_SIZE))
tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_background_image = pygame.transform.scale(menu_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
blue_gem_image = pygame.transform.scale(blue_gem_image, (TILE_SIZE * 1.5, TILE_SIZE * 1.3))
red_gem_image = pygame.transform.scale(red_gem_image, (TILE_SIZE * 1.5, TILE_SIZE * 1.3))
ramp_left_image = pygame.transform.scale(ramp_left_image, (TILE_SIZE, TILE_SIZE))
ramp_right_image = pygame.transform.scale(ramp_right_image, (TILE_SIZE, TILE_SIZE))
ramp_right_rotated_image = pygame.transform.rotate(ramp_left_image, 180)
ramp_left_rotated_image = pygame.transform.rotate(ramp_right_image, 180)
cube_image = pygame.transform.scale(cube_image, (2 * TILE_SIZE, 2 * TILE_SIZE))
platform_blue_image = pygame.transform.scale(platform_blue_image, (4 * TILE_SIZE, TILE_SIZE))
platform_orange_image = pygame.transform.scale(platform_orange_image, (4 * TILE_SIZE, TILE_SIZE))
lever_orange_image = pygame.transform.scale(lever_orange_image, (2 * TILE_SIZE, 2 * TILE_SIZE))
lever_blue_image = pygame.transform.scale(lever_blue_image, (2 * TILE_SIZE, 2 * TILE_SIZE))
button_blue_image = pygame.transform.scale(button_blue_image, (2 * TILE_SIZE, TILE_SIZE))
button_orange_image = pygame.transform.scale(button_orange_image, (2 * TILE_SIZE, TILE_SIZE))

# Sounds
menu_music = pygame.mixer.Sound("resources/music/menu_music.mp3")
level_music = pygame.mixer.Sound("resources/music/level_music.mp3")
level_over_sound = pygame.mixer.Sound("resources/music/level_music_over.mp3")
level_finish_sound = pygame.mixer.Sound("resources/music/level_music_finish.mp3")
death_sound = pygame.mixer.Sound("resources/music/death.mp3")
diamond_collect_sound = pygame.mixer.Sound("resources/music/diamond.mp3")
fireboy_jump_sound = pygame.mixer.Sound("resources/music/jump_fireboy.mp3")
watergirl_jump_sound = pygame.mixer.Sound("resources/music/jump_watergirl.mp3")

menu_music.set_volume(0.5)
level_music.set_volume(0.5)
level_finish_sound.set_volume(0.5)
level_over_sound.set_volume(0.5)
death_sound.set_volume(0.5)
diamond_collect_sound.set_volume(0.5)
fireboy_jump_sound.set_volume(0.5)
watergirl_jump_sound.set_volume(0.5)

# Create game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fireboy and Watergirl")
clock = pygame.time.Clock()


# Load levels
def load_levels(filename):
    with open(filename, "r") as file:
        levels = file.read().split("\n\n")  # Separate levels by blank lines
    return [level.splitlines() for level in levels]


levels = load_levels("resources/levels.txt")


# Draw level
def draw_level(level, fireboy, watergirl, cube, diamonds):
    hazard_positions = []  # Keep track of hazard positions and their full width
    for row_index, row in enumerate(level):
        col_index = 0
        while col_index < len(row):
            tile = row[col_index]
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if tile == "#":
                transparent_tile = tile_image.copy()  # Copy the original tile image
                transparent_tile.set_alpha(160)  # Set transparency (0 = fully transparent, 255 = fully opaque)

                screen.blit(transparent_tile, (x, y))
            elif tile == "F":
                if fireboy.x == 0 and fireboy.y == 0:
                    fireboy.x = x
                    fireboy.y = y
            elif tile == "W":
                if watergirl.x == 0 and watergirl.y == 0:
                    watergirl.x = x
                    watergirl.y = y
            elif tile == "C":
                if cube.x == 0 and cube.y == 0:
                    cube.x = x
                    cube.y = y
            elif tile in "LOG":  # Lava, Water, or Green stuff
                image = None
                if tile == "L":
                    image = lava_image
                elif tile == "O":
                    image = water_image
                elif tile == "G":
                    image = green_stuff_image

                screen.blit(image, (x, y))
                hazard_positions.append((x, y, tile, 5 * TILE_SIZE))
                col_index += 4  # Skip the next 4 tiles
            elif tile == "$":
                screen.blit(exit_fire_image, (x, y + 5))
            elif tile == "%":
                screen.blit(exit_water_image, (x, y + 5))
            elif tile == "R":
                if not any(diamond.rect.topleft == (x - 5, y) for diamond in diamonds):
                    diamonds.append(Diamond(x - 5, y, red_gem_image, "red"))
            elif tile == "B":
                if not any(diamond.rect.topleft == (x - 5, y) for diamond in diamonds):
                    diamonds.append(Diamond(x - 5, y, blue_gem_image, "blue"))
            elif tile == "/":
                transparent_ramp_right = ramp_right_image.copy()
                transparent_ramp_right.set_alpha(160)

                screen.blit(transparent_ramp_right, (x, y))
            elif tile == "\\":
                transparent_ramp_left = ramp_left_image.copy()
                transparent_ramp_left.set_alpha(160)

                screen.blit(transparent_ramp_left, (x, y))
            elif tile == "*":
                screen.blit(ramp_right_rotated_image, (x, y))
            elif tile == "-":
                screen.blit(platform_blue_image, (x, y))
                col_index += 3
            elif tile == "_":
                screen.blit(platform_orange_image, (x, y))
                col_index += 3
            elif tile == "l":
                screen.blit(lever_orange_image, (x, y + 7))
            elif tile == "b":
                screen.blit(button_blue_image, (x, y + 4))

            col_index += 1
    return hazard_positions, diamonds


# Button class
class MenuButton:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()


# Menu screen function
def menu_screen():
    """Displays the menu screen with level selection."""
    # Create buttons for each level
    buttons = []
    button_width = 200
    button_height = 50
    button_spacing = 20
    start_y = (SCREEN_HEIGHT - (len(levels) * (button_height + button_spacing))) // 2

    for i, level in enumerate(levels):
        x = (SCREEN_WIDTH - button_width) // 2
        y = start_y + i * (button_height + button_spacing)
        buttons.append(
            MenuButton("Level " + str(i + 1), x, y, button_width, button_height, lambda l=level: load_level(l)))

    menu_music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in buttons:
                    button.check_click(mouse_pos)

        screen.blit(menu_background_image, (0, 0))
        # Draw title
        title = large_font.render("Select a Level", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Draw buttons
        for button in buttons:
            # Change button color on hover
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.color = HOVER_COLOR
            else:
                button.color = GRAY
            button.draw(screen)

        pygame.display.flip()


# Load level function
def load_level(level_name):
    """Loads the selected level."""
    main_game(level_name)


class Player:
    def __init__(self, x, y, width, height, image, element_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.dx = 0  # Horizontal velocity
        self.dy = 0  # Vertical velocity
        self.image = image
        self.element_type = element_type  # "fireboy" or "watergirl"
        self.on_ground = False  # To check if player is on the ground or platform
        self.score = 0

    def move(self, level, cube, diamonds):
        """Apply movement and collisions."""
        self.rect.x += self.dx  # Apply horizontal movement

        # Check cube collision horizontally
        if self.rect.colliderect(cube.rect):
            if self.dx > 0:  # Moving right
                self.rect.right = cube.rect.left
                cube.push(self)
            elif self.dx < 0:  # Moving left
                self.rect.left = cube.rect.right
                cube.push(self)

        # Check for horizontal collisions with all tiles
        for row_index, row in enumerate(level):
            for col_index, tile in enumerate(row):
                tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == "#":  # Solid tile
                    if self.rect.colliderect(tile_rect):  # Horizontal collision
                        if self.dx > 0:  # Moving right
                            self.rect.right = tile_rect.left
                        elif self.dx < 0:  # Moving left
                            self.rect.left = tile_rect.right
                if tile == "L":
                    if self.rect.colliderect(tile_rect):  # Horizontal collision
                        if self.dx > 0:  # Moving right
                            self.rect.right = tile_rect.left
                        elif self.dx < 0:  # Moving left
                            self.rect.left = tile_rect.right
                if tile == "O":
                    if self.rect.colliderect(tile_rect):  # Horizontal collision
                        if self.dx > 0:  # Moving right
                            self.rect.right = tile_rect.left
                        elif self.dx < 0:  # Moving left
                            self.rect.left = tile_rect.right
                if tile == "G":
                    if self.rect.colliderect(tile_rect):  # Horizontal collision
                        if self.dx > 0:  # Moving right
                            self.rect.right = tile_rect.left
                        elif self.dx < 0:  # Moving left
                            self.rect.left = tile_rect.right

        # Diamond collection
        for diamond in diamonds:
            if self.rect.colliderect(diamond.rect) and not diamond.collected:
                if diamond.diamond_type == "red" and self.element_type == "fireboy":
                    diamond.collected = True
                    self.score += 10  # Add to score
                    diamond_collect_sound.play()
                elif diamond.diamond_type == "blue" and self.element_type == "watergirl":
                    diamond.collected = True
                    self.score += 10
                    diamond_collect_sound.play()

        # Apply gravity and vertical movement
        self.dy += GRAVITY
        if self.dy > TERMINAL_VELOCITY:
            self.dy = TERMINAL_VELOCITY
        self.rect.y += self.dy
        self.on_ground = False

        # Check cube collision vertically
        if self.rect.colliderect(cube.rect):
            if self.dy > 0:  # Landing on cube
                self.rect.bottom = cube.rect.top
                self.on_ground = True
                self.dy = 0
            elif self.dy < 0:  # Hitting cube from below
                self.rect.top = cube.rect.bottom
                self.dy = 0

        # Vertical collision (ground and liquid collisions)
        for row_index, row in enumerate(level):
            col_index = 0
            while col_index < len(row):
                tile = row[col_index]
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if tile == "#":
                    tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        if self.dy > 0:  # Falling
                            self.rect.bottom = tile_rect.top
                            self.dy = 0
                            self.on_ground = True
                        elif self.dy < 0:  # Jumping
                            self.rect.top = tile_rect.bottom
                            self.dy = 0
                elif tile in "LOG":  # Handle hazards as 5-tile-wide platforms
                    hazard_rect = pygame.Rect(x, y, 5 * TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(hazard_rect):
                        if tile == "O" and self.element_type == "watergirl":  # Watergirl can stand on water
                            if self.dy > 0:
                                self.rect.bottom = hazard_rect.top
                                self.dy = 0
                                self.on_ground = True
                            elif self.dy < 0:
                                self.rect.top = hazard_rect.bottom
                                self.dy = 0
                        elif tile == "L" and self.element_type == "fireboy":  # Fireboy can stand on lava
                            if self.dy > 0:
                                self.rect.bottom = hazard_rect.top
                                self.dy = 0
                                self.on_ground = True
                            elif self.dy < 0:
                                self.rect.top = hazard_rect.bottom
                                self.dy = 0
                        elif tile == "O" and self.element_type == "fireboy":  # Fireboy can hit the bottom of the water
                            if self.dy < 0:
                                self.rect.top = hazard_rect.bottom
                                self.dy = 0
                        elif tile == "L" and self.element_type == "watergirl":  # Watergirl can hit the bottom of the lava
                            if self.dy < 0:
                                self.rect.top = hazard_rect.bottom
                                self.dy = 0
                        elif tile == "G":  # Both can hit the bottom of the green liquid
                            if self.dy < 0:
                                self.rect.top = hazard_rect.bottom
                                self.dy = 0
                    col_index += 4  # Skip the next 4 tiles since we handled the full width
                col_index += 1

        return self.on_ground

    def jump(self):
        """Make the player jump."""
        if self.on_ground:  # Only allow jump when on the ground
            self.dy = JUMP_STRENGTH

    def check_hazards(self, hazard_positions, player_type):
        """Check for hazards and handle interactions."""
        for x, y, hazard_type, width in hazard_positions:
            hazard_rect = pygame.Rect(x, y, width, TILE_SIZE)
            if self.rect.colliderect(hazard_rect):
                if hazard_type == "L":  # Lava
                    if player_type == "fireboy":
                        return False  # Safe for Fireboy
                    else:
                        if self.dy > 0:
                            self.rect.bottom = hazard_rect.top
                            self.dy = 0
                            return True
                        elif self.dy < 0:
                            self.rect.top = hazard_rect.bottom
                            self.dy = 0
                elif hazard_type == "O":  # Water
                    if player_type == "watergirl":
                        return False  # Safe for Watergirl
                    return True  # Fireboy dies
                elif hazard_type == "G":  # Green liquid
                    return True  # Both die
        return False

    def draw(self, screen):
        # Draw the image at the player's position
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Cube:
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.dx = 0  # Horizontal velocity
        self.dy = 0  # Vertical velocity
        self.image = image
        self.on_ground = False
        self.friction = 0.7

    def push(self, player):
        """Transfer player's momentum to the cube"""
        push_factor = 0.8  # Adjust this to change how much of the player's momentum transfers to the cube

        # Optional: Add a small vertical boost when pushed to make it feel more dynamic
        if abs(player.dx) > 0:  # Only push if player is moving
            self.dx = player.dx * push_factor

    def move(self, level, players):
        # Apply horizontal movement
        self.rect.x += self.dx

        # Check wall collisions horizontally
        for row_index, row in enumerate(level):
            for col_index, tile in enumerate(row):
                if tile == "#":
                    tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        if self.dx > 0:
                            self.rect.right = tile_rect.left
                            self.dx = 0
                        elif self.dx < 0:
                            self.rect.left = tile_rect.right
                            self.dx = 0

        # Check player collisions
        for player in players:
            if self.rect.colliderect(player.rect):
                if self.dx > 0:
                    self.rect.right = player.rect.left
                    self.dx = 0
                elif self.dx < 0:
                    self.rect.left = player.rect.right
                    self.dx = 0

        # Apply gravity
        self.dy += GRAVITY
        if self.dy > TERMINAL_VELOCITY:
            self.dy = TERMINAL_VELOCITY
        self.rect.y += self.dy
        self.on_ground = False

        # Check ground collisions
        for row_index, row in enumerate(level):
            for col_index, tile in enumerate(row):
                tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == "#":
                    if self.rect.colliderect(tile_rect):
                        if self.dy > 0:
                            self.rect.bottom = tile_rect.top
                            self.on_ground = True
                            self.dy = 0
                        elif self.dy < 0:
                            self.rect.top = tile_rect.bottom
                            self.dy = 0
                if tile == "O":
                    if self.rect.colliderect(tile_rect):
                        if self.dy > 0:
                            self.rect.bottom = tile_rect.top
                            self.on_ground = True
                            self.dy = 0
                        elif self.dy < 0:
                            self.rect.top = tile_rect.bottom
                            self.dy = 0
                elif tile == "L":
                    if self.rect.colliderect(tile_rect):
                        if self.dy > 0:
                            self.rect.bottom = tile_rect.top
                            self.on_ground = True
                            self.dy = 0
                        elif self.dy < 0:
                            self.rect.top = tile_rect.bottom
                            self.dy = 0
                elif tile == "G":
                    if self.rect.colliderect(tile_rect):
                        if self.dy > 0:
                            self.rect.bottom = tile_rect.top
                            self.on_ground = True
                            self.dy = 0
                        elif self.dy < 0:
                            self.rect.top = tile_rect.bottom
                            self.dy = 0

        # Apply friction when on ground
        if self.on_ground:
            self.dx *= self.friction
            if abs(self.dx) < 0.1:
                self.dx = 0

    def draw(self, screen):
        # Draw the image at the player's position
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Diamond:
    def __init__(self, x, y, image, diamond_type):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.image = image
        self.collected = False
        self.diamond_type = diamond_type  # "red" for Fireboy, "blue" for Watergirl

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, (self.rect.x, self.rect.y))


class Platform:
    def __init__(self, x, y, width, height, image, movement_range, speed, horizontal=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.movement_range = movement_range  # How far the platform moves
        self.speed = speed  # Speed of the platform
        self.horizontal = horizontal  # True for horizontal, False for vertical
        self.active = False  # Whether the platform is moving
        self.start_pos = (x, y)  # Starting position

    def update(self):
        if not self.active:
            return

        if self.horizontal:
            self.rect.x += self.speed
            if abs(self.rect.x - self.start_pos[0]) > self.movement_range:
                self.speed *= -1  # Reverse direction
        else:
            self.rect.y += self.speed
            if abs(self.rect.y - self.start_pos[1]) > self.movement_range:
                self.speed *= -1  # Reverse direction

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Lever:
    def __init__(self, x, y, width, height, image, linked_platforms):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.active = False
        self.linked_platforms = linked_platforms  # List of platforms this lever controls

    def toggle(self):
        self.active = not self.active
        for platform in self.linked_platforms:
            platform.active = self.active

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Button:
    def __init__(self, x, y, width, height, image, linked_platforms):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.linked_platforms = linked_platforms
        self.active = False

    def check_activation(self, players, cube):
        self.active = any(player.rect.colliderect(self.rect) for player in players) or self.rect.colliderect(cube.rect)
        for platform in self.linked_platforms:
            platform.active = self.active

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Main game loop
def main_game(level):
    fireboy = Player(0, 0, 35, 50, fireboy_image, "fireboy")
    watergirl = Player(0, 0, 35, 50, watergirl_image, "watergirl")
    cube = Cube(0, 0, 2 * TILE_SIZE, 2 * TILE_SIZE, cube_image)
    platform_blue = Platform(0, 0, 4 * TILE_SIZE, TILE_SIZE, platform_blue_image, 100, 2)
    platform_orange = Platform(0, 0, 4 * TILE_SIZE, TILE_SIZE, platform_orange_image, 100, 2)

    fireboy_speed = 4
    watergirl_speed = 4

    diamonds = []
    hazard_positions, diamonds = draw_level(level, fireboy.rect, watergirl.rect, cube.rect, diamonds)

    menu_music.stop()
    level_music.play(-1)

    while True:
        screen.blit(background_image, (0, 0))  # Draw the background image
        hazard_positions, _ = draw_level(level, fireboy.rect, watergirl.rect, cube.rect, diamonds)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update positions
        fireboy.move(level, cube, diamonds)
        watergirl.move(level, cube, diamonds)

        # Controls
        keys = pygame.key.get_pressed()
        fireboy.dx = 0
        watergirl.dx = 0

        # Fireboy movement
        if keys[pygame.K_LEFT]:
            fireboy.dx = -fireboy_speed
        if keys[pygame.K_RIGHT]:
            fireboy.dx = fireboy_speed
        if keys[pygame.K_UP] and fireboy.on_ground:  # Jump if on ground
            fireboy_jump_sound.play()
            fireboy.jump()

        # Watergirl movement
        if keys[pygame.K_a]:
            watergirl.dx = -watergirl_speed
        if keys[pygame.K_d]:
            watergirl.dx = watergirl_speed
        if keys[pygame.K_w] and watergirl.on_ground:  # Jump if on ground
            watergirl_jump_sound.play()
            watergirl.jump()

        # Check for hazards
        if fireboy.check_hazards(hazard_positions, "fireboy"):
            level_music.stop()
            death_sound.play()
            pygame.time.wait(int(death_sound.get_length() * 1000))
            level_over_sound.play()
            pygame.time.wait(int(level_over_sound.get_length() * 500))
            menu_screen()
        if watergirl.check_hazards(hazard_positions, "watergirl"):
            level_music.stop()
            death_sound.play()
            pygame.time.wait(int(death_sound.get_length() * 1000))
            level_over_sound.play()
            pygame.time.wait(int(level_over_sound.get_length() * 500))
            menu_screen()

        # Draw everything
        fireboy.draw(screen)
        watergirl.draw(screen)
        cube.move(level, [fireboy, watergirl])
        cube.draw(screen)
        for diamond in diamonds:
            diamond.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# Start the game
if __name__ == "__main__":
    menu_screen()
