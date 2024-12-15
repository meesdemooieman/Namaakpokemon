import pygame
import sys

# Initialiseer Pygame
pygame.init()

# Game instellingen
SCHERM_BREEDTE = 800
SCHERM_HOOGTE = 600
FPS = 60  # Frames per seconde

# Kleuren
WIT = (255, 255, 255)

# Maak een scherm
scherm = pygame.display.set_mode((SCHERM_BREEDTE, SCHERM_HOOGTE))
pygame.display.set_caption("Pokémon Map")

# Laad en schaal Pokémon sprite
pokemon_afbeelding = pygame.image.load("bulbasaur2.jpg")
pokemon_afbeelding = pygame.transform.scale(pokemon_afbeelding, (40, 40))  # Verklei naar 40x40 pixels
pokemon_rect = pokemon_afbeelding.get_rect()

# Laad tegelafbeeldingen
gras_afbeelding = pygame.image.load("gras.jpg")
gras_afbeelding = pygame.transform.scale(gras_afbeelding, (40, 40))
steen_afbeelding = pygame.image.load("steen.jpg")
steen_afbeelding = pygame.transform.scale(steen_afbeelding, (40, 40))

# Map configuratie
TILE_SIZE = 40
map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Speler snelheid
snelheid = 5

# Beginpositie van de Pokémon
pokemon_rect.x = TILE_SIZE
pokemon_rect.y = TILE_SIZE

# Functie om de map te tekenen
def teken_map():
    for rij_index, rij in enumerate(map_data):
        for kolom_index, tegel in enumerate(rij):
            x = kolom_index * TILE_SIZE
            y = rij_index * TILE_SIZE
            if tegel == 1:
                scherm.blit(steen_afbeelding, (x, y))
            else:
                scherm.blit(gras_afbeelding, (x, y))

# Functie om botsingen met obstakels te controleren
def controleer_botsing(rect):
    for rij_index, rij in enumerate(map_data):
        for kolom_index, tegel in enumerate(rij):
            if tegel == 1:
                obstakel_rect = pygame.Rect(
                    kolom_index * TILE_SIZE, rij_index * TILE_SIZE, TILE_SIZE, TILE_SIZE
                )
                if rect.colliderect(obstakel_rect):
                    return True
    return False

# Game loop
def game_loop():
    klok = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        oude_pos = pokemon_rect.topleft

        if keys[pygame.K_LEFT]:
            pokemon_rect.x -= snelheid
        if keys[pygame.K_RIGHT]:
            pokemon_rect.x += snelheid
        if keys[pygame.K_UP]:
            pokemon_rect.y -= snelheid
        if keys[pygame.K_DOWN]:
            pokemon_rect.y += snelheid

        if controleer_botsing(pokemon_rect):
            pokemon_rect.topleft = oude_pos

        scherm.fill(WIT)
        teken_map()
        scherm.blit(pokemon_afbeelding, pokemon_rect)

        pygame.display.update()

        klok.tick(FPS)

# Start de game loop
game_loop()
