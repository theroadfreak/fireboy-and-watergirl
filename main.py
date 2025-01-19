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
fireboy_image = pygame.transform.scale(fireboy_image, (40,60))
watergirl_image = pygame.transform.scale(watergirl_image, (40,60))
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
    for row_index, row in enumerate(level):
        for col_index, tile in enumerate(row):
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
            elif tile == "L":
                screen.blit(lava_image, (x, y))
            elif tile == "O":
                screen.blit(water_image, (x, y))
            elif tile == "G":
                screen.blit(green_stuff_image, (x, y))
            elif tile == "$":
                screen.blit(exit_fire_image, (x, y + 5))
            elif tile == "%":
                screen.blit(exit_water_image, (x, y + 5))

    #Draw characters
    screen.blit(fireboy_image, (fireboy.x, fireboy.y))
    screen.blit(watergirl_image, (watergirl.x, watergirl.y))

# Main game loop
def main():
    global current_level
    fireboy = pygame.Rect(0, 0, 40, 60)
    watergirl = pygame.Rect(0, 0, 40, 60)
    level = levels[current_level]

    fireboy_speed = 5
    watergirl_speed = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controls
        keys = pygame.key.get_pressed()
        # Fireboy movement
        if keys[pygame.K_LEFT]:
            fireboy.x -= fireboy_speed
        if keys[pygame.K_RIGHT]:
            fireboy.x += fireboy_speed
        if keys[pygame.K_UP]:
            fireboy.y -= fireboy_speed
        if keys[pygame.K_DOWN]:
            fireboy.y += fireboy_speed
        # Watergirl movement
        if keys[pygame.K_a]:
            watergirl.x -= watergirl_speed
        if keys[pygame.K_d]:
            watergirl.x += watergirl_speed
        if keys[pygame.K_w]:
            watergirl.y -= watergirl_speed
        if keys[pygame.K_s]:
            watergirl.y += watergirl_speed

        # Check for hazards
        for row_index, row in enumerate(level):
            for col_index, tile in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        # Check for exits
        if tile == "E" and fireboy.colliderect(rect):
            print("Fireboy reached the exit!")
        if tile == "Q" and watergirl.colliderect(rect):
            print("Watergirl reached the exit!")
            current_level += 1
            if current_level >= len(levels):
                print("Game Complete!")
                pygame.quit()
                sys.exit()
            level = levels[current_level]  # Load next level

        # Draw everything
        screen.blit(background_image, (0, 0))  # Draw the background image
        draw_level(level, fireboy, watergirl)
        pygame.display.flip()
        clock.tick(FPS)


# Start the game
if __name__ == "__main__":
    main()
