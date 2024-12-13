import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load assets (placeholder colors for now)
PLAYER_SPRITE = pygame.Surface((TILE_SIZE, TILE_SIZE))
PLAYER_SPRITE.fill(GREEN)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon Blue Clone")

# Game Clock
clock = pygame.time.Clock()

# Sample Map (2D grid with tiles)
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Wild Pokémon encounter zones (map coordinates with encounter probability)
ENCOUNTER_ZONES = [(x, y) for y, row in enumerate(game_map) for x, tile in enumerate(row) if tile == 0]

# Player position
player_x, player_y = 1, 1

# Movement speed (in tiles)
player_speed = 1

# Wild Pokémon logic
def check_wild_encounter():
    if (player_x, player_y) in ENCOUNTER_ZONES and random.random() < 0.1:  # 10% chance
        return True
    return False

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y

    if keys[pygame.K_UP]:
        new_y -= player_speed
    if keys[pygame.K_DOWN]:
        new_y += player_speed
    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed

    # Prevent walking through walls
    if game_map[new_y][new_x] == 0:  # Check if tile is walkable
        player_x, player_y = new_x, new_y

    # Check for wild Pokémon encounter
    if check_wild_encounter():
        print("A wild Pokémon appeared!")

    # Rendering
    screen.fill(WHITE)  # Clear screen

    # Draw map
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            color = GREEN if tile == 0 else BLACK
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player
    screen.blit(PLAYER_SPRITE, (player_x * TILE_SIZE, player_y * TILE_SIZE))

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()