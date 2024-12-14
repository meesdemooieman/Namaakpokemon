import pygame # Haalt pygame binnen
import sys # Haalt de sys module binnen. Dit zorgt ervoor dat je de game kunt sluiten

pygame.init() # Haalt alle onderdelen van pygame binnen zodat je dit kunt gebruiken

# Game instellingen
SCHERM_BREEDTE = 800 # Grootte van het (spel)scherm
SCHERM_HOOGTE = 600 # Grootte van het (spel)scherm
FPS = 60  # Snelheid van het spel in frames per seconde

# Kleuren
WIT = (255, 255, 255)
ZWART = (0, 0, 0)

scherm = pygame.display.set_mode((SCHERM_BREEDTE, SCHERM_HOOGTE)) # Maakt een venster in de gegeven grootte waarin het spel wordt weergegeven
pygame.display.set_caption("Pokémon Game") # Zet de titel van het venster op

pokemon_afbeelding = pygame.image.load("pokemon_sprite.png") # Laadt het plaatje genaamt pokemon_sprite.pgn
pokemon_rect = pokemon_afbeelding.get_rect() #

# Speler snelheid
snelheid = 5

# Game loop
def game_loop():
    klok = pygame.time.Clock()

    # Beginpositie van de Pokémon
    pokemon_rect.center = (SCHERM_BREEDTE // 2, SCHERM_HOOGTE // 2)

    while True:
        # Events controleren
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Toetsen indrukken om te bewegen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pokemon_rect.x -= snelheid
        if keys[pygame.K_RIGHT]:
            pokemon_rect.x += snelheid
        if keys[pygame.K_UP]:
            pokemon_rect.y -= snelheid
        if keys[pygame.K_DOWN]:
            pokemon_rect.y += snelheid

        # Zorg ervoor dat Pokémon niet uit het scherm gaat
        if pokemon_rect.left < 0:
            pokemon_rect.left = 0
        if pokemon_rect.right > SCHERM_BREEDTE:
            pokemon_rect.right = SCHERM_BREEDTE
        if pokemon_rect.top < 0:
            pokemon_rect.top = 0
        if pokemon_rect.bottom > SCHERM_HOOGTE:
            pokemon_rect.bottom = SCHERM_HOOGTE

        # Vul het scherm met wit
        scherm.fill(WIT)

        # Teken de Pokémon
        scherm.blit(pokemon_afbeelding, pokemon_rect)

        # Update het scherm
        pygame.display.update()

        # Beperk de frames per seconde
        klok.tick(FPS)

# Start de game loop
game_loop()

import pygame
import sys
import random

# Initialiseer Pygame
pygame.init()

# Game instellingen
SCHERM_BREEDTE = 800
SCHERM_HOOGTE = 600
FPS = 60  # Frames per seconde

# Kleuren
WIT = (255, 255, 255)
ZWART = (0, 0, 0)
BLAUW = (0, 0, 255)
ROOD = (255, 0, 0)

# Maak een scherm
scherm = pygame.display.set_mode((SCHERM_BREEDTE, SCHERM_HOOGTE))
pygame.display.set_caption("Pokémon Game")

# Laad Pokémon sprite (je kunt je eigen afbeelding gebruiken)
pokemon_afbeelding = pygame.image.load("pokemon_sprite.png")
pokemon_rect = pokemon_afbeelding.get_rect()

# Speler snelheid
snelheid = 5

# Gevecht functie
def start_gevecht():
    gevecht_actief = True
    gevecht_keuzes = ["Aanvallen", "Verdedigen", "Vluchten"]
    speler_hp = 100
    tegenstander_hp = 100

    while gevecht_actief:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Toetsen indrukken om een keuze te maken
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            keuze = "Aanvallen"
        elif keys[pygame.K_2]:
            keuze = "Verdedigen"
        elif keys[pygame.K_3]:
            keuze = "Vluchten"
        else:
            keuze = None

        # Gevecht logica
        if keuze:
            if keuze == "Aanvallen":
                schade = random.randint(10, 30)
                tegenstander_hp -= schade
                print(f"Je hebt de tegenstander aangevallen! Schaden: {schade}")
            elif keuze == "Verdedigen":
                print("Je hebt je verdedigd!")
            elif keuze == "Vluchten":
                print("Je vlucht uit het gevecht!")
                gevecht_actief = False

            if tegenstander_hp <= 0:
                print("Je hebt de tegenstander verslagen!")
                gevecht_actief = False
            if speler_hp <= 0:
                print("Je bent verslagen!")
                gevecht_actief = False

        # Vul het scherm met wit
        scherm.fill(WIT)

        # Teken de Pokémon
        scherm.blit(pokemon_afbeelding, pokemon_rect)

        # Toon gevechtsinformatie
        font = pygame.font.Font(None, 36)
        tekst = font.render(f"Tegenstander HP: {tegenstander_hp} | Speler HP: {speler_hp}", True, ZWART)
        scherm.blit(tekst, (10, 10))

        # Toon gevechtskeuzes
        keuzes_tekst = font.render("Keuzes: 1) Aanvallen 2) Verdedigen 3) Vluchten", True, BLAUW)
        scherm.blit(keuzes_tekst, (10, 50))

        # Update het scherm
        pygame.display.update()

        # Beperk de frames per seconde
        pygame.time.delay(500)

# Game loop
def game_loop():
    klok = pygame.time.Clock()

    # Beginpositie van de Pokémon
    pokemon_rect.center = (SCHERM_BREEDTE // 2, SCHERM_HOOGTE // 2)

    while True:
        # Events controleren
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Toetsen indrukken om te bewegen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pokemon_rect.x -= snelheid
        if keys[pygame.K_RIGHT]:
            pokemon_rect.x += snelheid
        if keys[pygame.K_UP]:
            pokemon_rect.y -= snelheid
        if keys[pygame.K_DOWN]:
            pokemon_rect.y += snelheid

        # Game menu (start gevecht)
        if keys[pygame.K_SPACE]:
            start_gevecht()

        # Vul het scherm met wit
        scherm.fill(WIT)

        # Teken de Pokémon
        scherm.blit(pokemon_afbeelding, pokemon_rect)

        # Update het scherm
        pygame.display.update()

        # Beperk de frames per seconde
        klok.tick(FPS)

# Start de game loop
game_loop()