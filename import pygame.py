import pygame # Importeert pygame zodat je dit kan gebruiken
import sys # Importeert de sys module wat nodig is om het programma af te sluiten
import random # Importeert de random module wat wordt gebruikt voor willekeurige getallen, zoals tijdens aanvallen

pygame.init() # opent pygame zodat je dit kunt gebruiken

info = pygame.display.Info()
SCHERM_BREEDTE = info.current_w # Breedte van het scherm
SCHERM_HOOGTE = info.current_h # Hoogte van het scherm
FPS = 60  # Snelheid van het spel in Frames Per Seconde

# Kleuren van het spel in de RGB (Rood, Groen, Blauw) module
WIT = (255, 255, 255)
ZWART = (0, 0, 0)
ROOD = (255, 0, 0)
GROEN = (0, 255, 0)
BLAUW = (0, 0, 255)

scherm = pygame.display.set_mode((SCHERM_BREEDTE, SCHERM_HOOGTE)) # Maakt een venster met de aangegeven grootte van hierboven
pygame.display.set_caption("Pokémon Map") # Zet de titel van het venster op

pokemon_afbeelding = pygame.image.load("charmander.png") # Laadt de afbeelding "charmander.png"
pokemon_afbeelding = pygame.transform.scale(pokemon_afbeelding, (40, 40))  # Verkleint de afbeelding naar 40x40 pixels
pokemon_rect = pokemon_afbeelding.get_rect() # Maakt een rechthoek (rect) om de afbeelding waarmee je de positie en botsingen kunt bepalen

gras_afbeelding = pygame.image.load("gras.jpg") # Laadt de afbeelding voor gras
gras_afbeelding = pygame.transform.scale(gras_afbeelding, (40, 40)) # Verkleint de afbeelding
steen_afbeelding = pygame.image.load("steen.jpg") # Laadt de afbeelding voor steen
steen_afbeelding = pygame.transform.scale(steen_afbeelding, (40, 40)) # Verkleint de afbeelding
vijhand_afbeelding = pygame.image.load("vijhand.png") # Laadt de afbeelding voor vijand
vijhand_afbeelding = pygame.transform.scale(vijhand_afbeelding, (40, 40)) # Verkleint de afbeelding

TILE_SIZE = 40 # Grootte van elke tegel in het spel
map_data = [ # Lijsten
# 0 = gras (kan je overheen lopen)
# 1 = steen (kan je niet overheen lopen)
# 2 = vijand (start een gevecht)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

snelheid = 5 # Speler snelheid

# Beginpositie van de pokémon
pokemon_rect.x = TILE_SIZE 
pokemon_rect.y = TILE_SIZE

class Pokemon: # Klasse "pokemon"
    def __init__(self, name, max_hp, attack, image):
        self.name = name # Naam van de pokemon
        self.max_hp = max_hp # Maximaal aantal levenspunten
        self.current_hp = max_hp # Huidige levenspunten
        self.attack = attack # Aanvallen 
        self.image = image

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    def is_fainted(self):
        return self.current_hp == 0

player_pokemon = Pokemon("Charmander", 100, {"Scratch": 15, "Ember": 20}, pokemon_afbeelding)
opponent_pokemon = Pokemon("Bulbasaur", 120, {"Tackle": 10, "Vine Whip": 15}, pygame.image.load("bulbasaur.png"))

# Functie om de map te tekenen
def teken_map():
    for rij_index, rij in enumerate(map_data):
        for kolom_index, tegel in enumerate(rij):
            x = kolom_index * TILE_SIZE
            y = rij_index * TILE_SIZE
            if tegel == 1:
                scherm.blit(steen_afbeelding, (x, y))
            elif tegel == 2:
                scherm.blit(vijhand_afbeelding, (x, y))
            else:
                scherm.blit(gras_afbeelding, (x, y))

# Functie om botsingen met obstakels te controleren
def controleer_botsing(rect):
    for rij_index, rij in enumerate(map_data):
        for kolom_index, tegel in enumerate(rij):
            if tegel == 1:  # Only block on "rock" tiles (value 1)
                obstakel_rect = pygame.Rect(
                    kolom_index * TILE_SIZE, rij_index * TILE_SIZE, TILE_SIZE, TILE_SIZE
                )
                if rect.colliderect(obstakel_rect):
                    return True  # Block movement
    return False  # No collision detected, movement allowed

# Functie om te controleren of speler op een vijhand-tegel staat
def controleer_vijhand(rect):
    for rij_index, rij in enumerate(map_data):
        for kolom_index, tegel in enumerate(rij):
            if tegel == 2:
                vijhand_rect = pygame.Rect(
                    kolom_index * TILE_SIZE, rij_index * TILE_SIZE, TILE_SIZE, TILE_SIZE
                )
                if rect.colliderect(vijhand_rect):
                    return True
    return False

# Functie voor het flitsen van het scherm
def flits_scherm():
    for _ in range(6):
        scherm.fill(ROOD)
        pygame.display.update()
        pygame.time.delay(100)
        scherm.fill(WIT)
        pygame.display.update()
        pygame.time.delay(100)

# Functie om een gevecht te starten
def start_gevecht():
    running = True
    player_turn = True
    selected_attack = None
    battle_log = []

    while running:
        scherm.fill(WIT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if player_turn and not selected_attack:
                    if event.key == pygame.K_1:
                        selected_attack = "Scratch"
                    elif event.key == pygame.K_2:
                        selected_attack = "Ember"

        # Vergroot de Pokémon afbeeldingen voor de strijd
        player_pokemon.image = pygame.transform.scale(player_pokemon.image, (150, 150))
        opponent_pokemon.image = pygame.transform.scale(opponent_pokemon.image, (150, 150))

        # Toon Pokémon stats, afbeeldingen en health bars
        scherm.blit(player_pokemon.image, (50, SCHERM_HOOGTE - 350))
        scherm.blit(opponent_pokemon.image, (SCHERM_BREEDTE - 350, 100))

        def draw_health_bar(pokemon, x, y):
            bar_width = 200
            bar_height = 20
            health_ratio = pokemon.current_hp / pokemon.max_hp
            pygame.draw.rect(scherm, ROOD, (x, y, bar_width, bar_height))
            pygame.draw.rect(scherm, GROEN, (x, y, bar_width * health_ratio, bar_height))

        draw_health_bar(player_pokemon, 50, SCHERM_HOOGTE - 380)
        draw_health_bar(opponent_pokemon, SCHERM_BREEDTE - 250, 70)

        font = pygame.font.Font(None, 32)

        def display_text(text, x, y):
            rendered_text = font.render(text, True, ZWART)
            scherm.blit(rendered_text, (x, y))

        display_text(f"{player_pokemon.name}", 50, SCHERM_HOOGTE - 400)
        display_text(f"{opponent_pokemon.name}", SCHERM_BREEDTE - 250, 50)

        y_offset = 150
        for log in battle_log[-5:]:
            display_text(log, 50, y_offset)
            y_offset += 30

        if player_turn and not player_pokemon.is_fainted() and not opponent_pokemon.is_fainted():
            if not selected_attack:
                display_text("Kies je aanval:", 50, 50)
                display_text("1: Scratch (15 dmg)", 50, 75)
                display_text("2: Ember (20 dmg)", 50, 100)
            else:
                damage = player_pokemon.attack[selected_attack] + random.randint(-5, 5)
                opponent_pokemon.take_damage(damage)
                battle_log.append(f"{player_pokemon.name} gebruikt {selected_attack}! Schade: {damage}")
                player_turn = False
                selected_attack = None

        elif not player_turn and not player_pokemon.is_fainted() and not opponent_pokemon.is_fainted():
            pygame.time.delay(1000)
            attack_name = random.choice(list(opponent_pokemon.attack.keys()))
            damage = opponent_pokemon.attack[attack_name] + random.randint(-5, 5)
            player_pokemon.take_damage(damage)
            battle_log.append(f"{opponent_pokemon.name} gebruikt {attack_name}! Schade: {damage}")
            player_turn = True

        if player_pokemon.is_fainted():
            display_text("Je hebt verloren!", SCHERM_BREEDTE // 2 - 100, SCHERM_HOOGTE // 2)
            running = False
        elif opponent_pokemon.is_fainted():
            display_text("Je hebt gewonnen!", SCHERM_BREEDTE // 2 - 100, SCHERM_HOOGTE // 2)
            running = False
            pygame.display.update()
            pygame.time.delay(2000)
            return True  # Return True to indicate the player won the battle

        pygame.display.flip()

# Game loop
def game_loop():
    klok = pygame.time.Clock()

    # Reset Pokémon position to the start
    pokemon_rect.x = TILE_SIZE
    pokemon_rect.y = TILE_SIZE

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
            pokemon_rect.topleft = oude_pos  # Prevent movement if there's a collision

        if controleer_vijhand(pokemon_rect):
            flits_scherm()
            if start_gevecht():
                # Reset the position after battle
                pokemon_rect.x = TILE_SIZE
                pokemon_rect.y = TILE_SIZE

        scherm.fill(WIT)
        teken_map()
        scherm.blit(pokemon_afbeelding, pokemon_rect)

        pygame.display.update()

        klok.tick(FPS)

# Start de game loop
game_loop()