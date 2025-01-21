import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 760, 580
TILE_SIZE = 20
FPS = 60
FONT_COLOR = (255, 255, 255)

# Colors
FIRE_COLOR = (255, 0, 0)
WATER_COLOR = (0, 0, 255)
GROUND_COLOR = (200, 200, 200)
WALL_COLOR = (120, 85, 50)

# Physics constants
GRAVITY = 0.3
JUMP_HEIGHT_TILES = 4.5  # Desired jump height in tiles
JUMP_STRENGTH = -(2 * GRAVITY * (JUMP_HEIGHT_TILES * TILE_SIZE))**0.5
TERMINAL_VELOCITY = 5

# Load images
fireboy_image = pygame.image.load("resources/pngs/Fireboy-0.png")
watergirl_image = pygame.image.load("resources/pngs/Watergirl2-0.png")
lava_image = pygame.image.load("resources/pngs/lava_small.png")
water_image = pygame.image.load("resources/pngs/water_small.png")
green_stuff_image = pygame.image.load("resources/pngs/green_stuff_small.png")
exit_fire_image = pygame.image.load("resources/pngs/door_fireboy.png")
exit_water_image = pygame.image.load("resources/pngs/door_watergirl.png")
tile_image = pygame.image.load("resources/pngs/tile.png")
background_image = pygame.image.load("resources/pngs/level_background.png")

# Scale images
fireboy_image = pygame.transform.scale(fireboy_image, (35,50))
watergirl_image = pygame.transform.scale(watergirl_image, (35,50))
lava_image = pygame.transform.scale(lava_image, (5 * TILE_SIZE, TILE_SIZE))
water_image = pygame.transform.scale(water_image, (5 * TILE_SIZE, TILE_SIZE))
green_stuff_image = pygame.transform.scale(green_stuff_image, (5 * TILE_SIZE, TILE_SIZE))
exit_fire_image = pygame.transform.scale(exit_fire_image, (2.5 * TILE_SIZE, 3 *TILE_SIZE))
exit_water_image = pygame.transform.scale(exit_water_image, (2.5 * TILE_SIZE, 3 *TILE_SIZE))
tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
current_level = 0

# Draw level
def draw_level(level, fireboy, watergirl):
    hazard_positions = []  # Keep track of hazard positions and their full width
    for row_index, row in enumerate(level):
        col_index = 0
        while col_index < len(row):
            tile = row[col_index]
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if tile == "#":
                screen.blit(tile_image, (x, y))
            elif tile == "F":
                if fireboy.x == 0 and fireboy.y == 0:
                    fireboy.x = x
                    fireboy.y = y
            elif tile == "W":
                if watergirl.x == 0 and watergirl.y == 0:
                    watergirl.x = x
                    watergirl.y = y
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

            col_index += 1
    return hazard_positions


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

    def move(self, level):
        """Apply movement and collisions."""
        self.rect.x += self.dx  # Apply horizontal movement
        self.on_ground = False  # Reset on_ground flag at the start of the move

        # Check for horizontal collisions with all tiles
        for row_index, row in enumerate(level):
            for col_index, tile in enumerate(row):
                if tile == "#":  # Solid tile
                    tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):  # Horizontal collision
                        if self.dx > 0:  # Moving right
                            self.rect.right = tile_rect.left
                        elif self.dx < 0:  # Moving left
                            self.rect.left = tile_rect.right

        # Apply gravity and vertical movement
        self.dy += GRAVITY
        if self.dy > TERMINAL_VELOCITY:
            self.dy = TERMINAL_VELOCITY
        self.rect.y += self.dy

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
                        elif tile == "G":
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
                    return True  # Watergirl dies
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


# Main game loop
def main():
    global current_level
    fireboy = Player(0, 0, 35, 50, fireboy_image, "fireboy")
    watergirl = Player(0, 0, 35, 50, watergirl_image, "watergirl")
    level = levels[current_level]

    fireboy_speed = 4
    watergirl_speed = 4

    while True:
        draw_level(level, fireboy.rect, watergirl.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update positions
        fireboy.move(level)
        watergirl.move(level)

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
            fireboy.jump()

        # Watergirl movement
        if keys[pygame.K_a]:
            watergirl.dx = -watergirl_speed
        if keys[pygame.K_d]:
            watergirl.dx = watergirl_speed
        if keys[pygame.K_w] and watergirl.on_ground:  # Jump if on ground
            watergirl.jump()

        screen.blit(background_image, (0, 0))  # Draw the background image
        hazard_positions = draw_level(level, fireboy.rect, watergirl.rect)

        # Check for hazards
        if fireboy.check_hazards(hazard_positions, "fireboy"):
            print("Fireboy died!")
            return
        if watergirl.check_hazards(hazard_positions, "watergirl"):
            print("Watergirl died!")
            return

        # Draw everything
        fireboy.draw(screen)
        watergirl.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

# Start the game
if __name__ == "__main__":
    main()
