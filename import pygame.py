import pygame # Importeert pygame zodat je dit kan gebruiken
import sys # Importeert de sys module wat nodig is om het programma af te sluiten
import random # Importeert de random module wat wordt gebruikt voor willekeurige getallen, zoals tijdens aanvallen

pygame.init() # opent pygame zodat je dit kunt gebruiken

info = pygame.display.Info()
SCHERM_BREEDTE = 1600 # Breedte van het scherm
SCHERM_HOOGTE = 1200 # Hoogte van het scherm
FPS = 60  # Snelheid van het spel in Frames Per Seconde

# Kleuren van het spel in de RGB (Rood, Groen, Blauw) module
WIT = (255, 255, 255)
ZWART = (0, 0, 0)
ROOD = (255, 0, 0)
GROEN = (0, 255, 0)
BLAUW = (0, 0, 255)

scherm = pygame.display.set_mode((SCHERM_BREEDTE, SCHERM_HOOGTE)) # Maakt een venster met de aangegeven grootte van hierboven
pygame.display.set_caption("Pokémon Map") # Zet de titel van het venster op

pokemon_afbeelding = pygame.image.load("Trainer.png") # Laadt de afbeelding "Trainer.png"
pokemon_afbeelding = pygame.transform.scale(pokemon_afbeelding, (80, 80))  # Verkleint de afbeelding naar 40x40 pixels
pokemon_rect = pokemon_afbeelding.get_rect() # Maakt een rechthoek (rect) om de afbeelding waarmee je de positie en botsingen kunt bepalen

gras_afbeelding = pygame.image.load("gras.jpg") # Laadt de afbeelding voor gras
gras_afbeelding = pygame.transform.scale(gras_afbeelding, (80, 80)) # Verkleint de afbeelding
steen_afbeelding = pygame.image.load("steen.jpg") # Laadt de afbeelding voor steen
steen_afbeelding = pygame.transform.scale(steen_afbeelding, (80, 80)) # Verkleint de afbeelding
vijhand_afbeelding = pygame.image.load("vijhand.png") # Laadt de afbeelding voor vijand
vijhand_afbeelding = pygame.transform.scale(vijhand_afbeelding, (80, 80)) # Verkleint de afbeelding

TILE_SIZE = 80 # Grootte van elke tegel in het spel
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
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

snelheid = 8 # Snelheid waarmee de speler beweegt

pokemon_rect.x = TILE_SIZE # Startpositie van de speler in de X-richting
pokemon_rect.y = TILE_SIZE # Startpositie van de speler in de Y-richting

class Pokemon: # Klasse "pokemon"
    def __init__(self, name, max_hp, attack, image):
        self.name = name # Naam van de pokemon
        self.max_hp = max_hp # Maximaal aantal levenspunten
        self.current_hp = max_hp # Huidige levenspunten
        self.attack = attack # Aanvallen 
        self.image = image # Afbeelding van de pokémon

    def take_damage(self, damage): # Vermindering van levenspunten
        self.current_hp = max(0, self.current_hp - damage) # Vermindert de levenspunten, maar nooit onder 0

    def is_fainted(self): # Controleert of een pokémon geen HP meer heeft
        return self.current_hp == 0 # Returnt "True" als de pokémon verloren heeft, en anders "False"

player_pokemon = Pokemon("Charmander", 100, {"Scratch": 15, "Ember": 20}, pygame.image.load("charmander.png")) # Speler pokémon: foto, hp en aanvallen
opponent_pokemon = Pokemon("Bulbasaur", 120, {"Tackle": 10, "Vine Whip": 15}, pygame.image.load("bulbasaur.png")) # Tegenstander pokémon: foto, hp en aanvallen

def teken_map(): 
    for rij_index, rij in enumerate(map_data): # Controleert welke rij in de map wordt verwerkt
        for kolom_index, tegel in enumerate(rij): # Bepaalt welke tegel wordt verwerkt
            x = kolom_index * TILE_SIZE # Plaatst de tegel op de juiste (horizontale) plek
            y = rij_index * TILE_SIZE # Plaatst de tegel op de juiste (verticale) plek
            if tegel == 1: # Bepaalt welke afbeelding getekent moet worden
                scherm.blit(steen_afbeelding, (x, y)) # Tekent een steenafbeelding op x, y op het scherm
            elif tegel == 2: # Bepaalt of een vijand-afbeelding getekent moet worden
                scherm.blit(vijhand_afbeelding, (x, y)) # Tekent een vijand-afbeelding op x, y op het scherm
            else: # Wordt uitgevoerd als de tegel geen steen of vijand is
                scherm.blit(gras_afbeelding, (x, y)) # Tekent een gras-afbeelding op x, y op het scherm

def controleer_botsing(rect): # Start de funcite voor de controle van een botsing
    for rij_index, rij in enumerate(map_data): # Bekijkt op welke plekken obstakels staan
        for kolom_index, tegel in enumerate(rij): # Bekijkt of er op de locatie die hierboven bepaalt is daadwerkelijk een obstakel staat
            if tegel == 1: # Zorgt ervoor dat je niet over stenen heen kunt lopen
                obstakel_rect = pygame.Rect( # Tekent een rechthoek (obstakel_rect) die overeenkomt met de locatie en grootte van de obstakel tegel
                    kolom_index * TILE_SIZE, rij_index * TILE_SIZE, TILE_SIZE, TILE_SIZE # Tekent een rechthoek (obstakel_rect) die overeenkomt met de locatie en grootte van de obstakel tegel
                )
                if rect.colliderect(obstakel_rect): # Bepaalt of een beweging geblokkeerd moet worden
                    return True # Geeft aan dat een beweging geblokkeerd moet worden
    return False  # Geeft aan dat bewegingen zijn toegestaan

def controleer_vijhand(rect): # Start de functie controleer_vijand
    for rij_index, rij in enumerate(map_data): # Controleert alle rijen in de kaart
        for kolom_index, tegel in enumerate(rij): # Controleert alle tegels in een rij
            if tegel == 2: # Controleert of de tegel van een vijand is (waarde 2)
                vijhand_rect = pygame.Rect( # Maakt een rechthoek (vijand_rect) die overeenkomt met de plaats en grootte van de vijand-tegel
                    kolom_index * TILE_SIZE, rij_index * TILE_SIZE, TILE_SIZE, TILE_SIZE
                )
                if rect.colliderect(vijhand_rect): # Controleert of de speler botst met een tegel van de vijand
                    return True # Activeert een gevecht als de speler botst met een vijand-tegel
    return False # Als een speler niet botst met een vijand-tegel, wordt er geen gevecht gestart

def flits_scherm(): # laat het scherm flitsen als er een gevecht begint
    for _ in range(6): # Herhaalt de flits 6 keer
        scherm.fill(ROOD) # Kleurt het hele scherm rood
        pygame.display.update() # Laat de flits zien
        pygame.time.delay(100) # Zorgt voor een korte pauze van 100 miliseconden tussen de flitsen door
        scherm.fill(WIT) # Maakt het hele scherm wit
        pygame.display.update() # Laat de tweede flits zien
        pygame.time.delay(100) # Zorgt voor een korte pauze van 100 miliseconden tussen de flitsen door

def start_gevecht(): # Start de functie van start_gevecht
    running = True # Slaat de variabele "running" op als "true". Dit controleert of het gevecht actief is
    player_turn = True # Houdt bij of de speler aan de beurt is
    selected_attack = None # Houdt bij welke aanval de speler kiest
    battle_log = [] # Houdt bij welke aanvallen er zijn gekozen gedurende het hele gevecht

    while running: # Zorgt ervoor dat het gevecht blijft doorgaan tot het spel wordt afgesloten
        scherm.fill(WIT) # Maakt het scherm wit of een nieuw venster op te starten

        for event in pygame.event.get(): # Hierdoor kan je het venster afsluiten
            if event.type == pygame.QUIT: # Hierdoor kan je het venster afsluiten
                pygame.quit() # Zorgt ervoor dat pygame correct wordt afgesloten
                sys.exit() # Sluit het hele programma af

            if event.type == pygame.KEYDOWN: # Controleert of er toetsen worden aangeslagen op het toetsenbord
                if player_turn and not selected_attack: # Zorgt ervoor dat de juiste aanval wordt gebruikt op basis van de toets die is ingedrukt op het toetsenbord
                    if event.key == pygame.K_1: # Als 1 wordt ingetoetst
                        selected_attack = "Scratch" # Aanval bij toets 1
                    elif event.key == pygame.K_2: # Als 2 wordt ingetoetst
                        selected_attack = "Ember" # Aanval bij toets 2

        player_pokemon.image = pygame.transform.scale(player_pokemon.image, (SCHERM_BREEDTE // 4, SCHERM_HOOGTE // 4)) # Schaal van de afbeeldingen, aangepast op het formaat van het scherm
        opponent_pokemon.image = pygame.transform.scale(opponent_pokemon.image, (SCHERM_BREEDTE // 6, SCHERM_HOOGTE // 5)) # Schaal van de afbeeldingen, aangepast op het formaat van het scherm

        scherm.blit(player_pokemon.image, (SCHERM_BREEDTE - SCHERM_BREEDTE, SCHERM_HOOGTE - SCHERM_HOOGTE // 3)) # Tekent de pokémons op de juiste plaats op het scherm
        scherm.blit(opponent_pokemon.image, (SCHERM_BREEDTE - SCHERM_BREEDTE // 5, SCHERM_HOOGTE // 6)) # Tekent de pokémons op de juiste plaats op het scherm

        def draw_health_bar(pokemon, x, y): # Tekent een rood gezondheidsbalkje bij de pokémon
            bar_width = 200 # Breedte van de balk
            bar_height = 20 # Hoogte van de balk
            health_ratio = pokemon.current_hp / pokemon.max_hp # Controleert het de hp-hoogte van de pokémon
            pygame.draw.rect(scherm, ROOD, (x, y, bar_width, bar_height)) # Tekent de balk
            pygame.draw.rect(scherm, GROEN, (x, y, bar_width * health_ratio, bar_height)) # Tekent de balk

        draw_health_bar(player_pokemon, SCHERM_BREEDTE // 50, SCHERM_HOOGTE - (4 * (SCHERM_HOOGTE // 11))) # Toont de huidige gezondheid van de pokémon
        draw_health_bar(opponent_pokemon, SCHERM_BREEDTE - 2 * (SCHERM_BREEDTE // 11), SCHERM_HOOGTE // 10 ) # Toont de huidige gezondheid van de vijandelijke pokémon

        font = pygame.font.Font(None, 32) # Lettertype voor alle geschreven tekst in de game

        def display_text(text, x, y): # Coördinaten waar de tekst moet worden weergegeven
            rendered_text = font.render(text, True, ZWART) # Rendert de tekst in het opgegeven lettertype en in de kleur zwart
            scherm.blit(rendered_text, (x, y)) # Tekent de tekst op de juiste positie

        display_text(f"{player_pokemon.name}", SCHERM_BREEDTE // 50, SCHERM_HOOGTE - (4 * (SCHERM_HOOGTE // 10))) # Positie van de naam van de speler pokémon
        display_text(f"{opponent_pokemon.name}", SCHERM_BREEDTE - 2 * (SCHERM_BREEDTE // 11), SCHERM_HOOGTE // 14) # Positie van de naam van de vijandelijke pokémon

        y_offset = 10 * (SCHERM_HOOGTE // 60) # Positie van de laatste tekst van het gevechtslog
        for log in battle_log[-5:]: # Doorloopt de laatste 5 berichten uit het gevechtslog
            display_text(log, SCHERM_BREEDTE // 50, y_offset) # Toont alle tekst van het logboek op het scherm
            y_offset += (SCHERM_HOOGTE // 30) # Zorgt ervoor dat de tekst verschuift zodat alle tekst op het scherm past

        if player_turn and not player_pokemon.is_fainted() and not opponent_pokemon.is_fainted(): # Als de speler aan de beurt is wordt er gecontroleerd of beide pokémons nog in leven zijn
            if not selected_attack: # Als de speler nog in leven is krijg je de onderstaande opties aan aanvallen
                display_text("Kies je aanval:", SCHERM_BREEDTE // 50, SCHERM_HOOGTE // 50)
                display_text("1: Scratch (15 dmg)", SCHERM_BREEDTE // 50, 3 * (SCHERM_HOOGTE // 60))
                display_text("2: Ember (20 dmg)", SCHERM_BREEDTE // 50, 5 * (SCHERM_HOOGTE // 60))
            else: # Als de speler een aanval heeft gekozen
                damage = player_pokemon.attack[selected_attack] + random.randint(-5, 5) # De schade wordt berekend
                opponent_pokemon.take_damage(damage) # Laat de vijandelijke pokémon schade oplopen
                battle_log.append(f"{player_pokemon.name} gebruikt {selected_attack}! Schade: {damage}") # Voegt tekst toe aan de gevechtslog
                player_turn = False # Wisselt de beurt naar de vijand
                selected_attack = None # Reset de geselecteerde aanval

        elif not player_turn and not player_pokemon.is_fainted() and not opponent_pokemon.is_fainted(): # Controleert of het niet de beurt van de speler is, of de speler niet is verslagen en of de vrijandelijke pokémon niet is verslagen
            pygame.time.delay(1000) # Pauzeert het spel voor 1000 miliseconden
            attack_name = random.choice(list(opponent_pokemon.attack.keys())) # Selecteerd een willekeurige aanval uit de beschikbare aanvallen van de vijandelijke pokémon
            damage = opponent_pokemon.attack[attack_name] + random.randint(-5, 5) # Berkent de schade die is opgelopen bij de speler door de aanval van de tegenstander
            player_pokemon.take_damage(damage) # Laat de pokémon van de speler de berekende schade oplopen
            battle_log.append(f"{opponent_pokemon.name} gebruikt {attack_name}! Schade: {damage}") # Voegt een bericht toe aan de gevechtslog met details over de aanval
            player_turn = True # Zet de beurt om naar de speler

        if player_pokemon.is_fainted(): # Controleert of de pokémon van de speler is verslagen
            display_text("Je hebt verloren!", SCHERM_BREEDTE // 2 - 100, SCHERM_HOOGTE // 2) # Geeft de tekst weer "Je hebt verloren!" in de aangegeven grootte
            running = False # Stopt het gevecht als de pokémon van de speler is verlslagen
        elif opponent_pokemon.is_fainted(): # Controleert of de vijandelijke pokémon is verslagen
            display_text("Je hebt gewonnen!", SCHERM_BREEDTE // 2 - 100, SCHERM_HOOGTE // 2) # Geeft de tekst weer "Je hebt gewonnen!" in de aangegeven grootte
            running = False # Stopt het gevecht als de vijandelijke pokémon is verlslagen
            pygame.display.update() # Ververst het scherm om de tekst "Je hebt gewonnen!" zichtbaar te maken
            pygame.time.delay(2000) # Pauzeert het spel voor 2000 miliseconden
            return True # Geeft aan dat de speler heeft gewonnen

        pygame.display.flip() # Ververst het scherm

def game_loop(): # Begint de hoofd-game-lus, waarin het grootste gedeelte van het spel plaatsvindt.
    klok = pygame.time.Clock() # Berekent de snelheid van de game-lus.

# Zorgt ervoor dat de spelers pokémon in de juiste startpositie komt op de kaart
    pokemon_rect.x = TILE_SIZE # 
    pokemon_rect.y = TILE_SIZE

    while True: # Een while-lus die continu open staat 
        for event in pygame.event.get(): # Verwerkt alle inputs van de gebruiker, zoals welke toetsen je aanslaat
            if event.type == pygame.QUIT: # Controleert of de speler het venster probeert te sluiten
                pygame.quit() # Sluit pygame correct af
                sys.exit() # Sluit hele programma af

        keys = pygame.key.get_pressed() # Controleert welke toetsen op het toetsenbord worden aangeslagen
        oude_pos = pokemon_rect.topleft # Slaat de huidige positie van de speler-pokémon op

# Toetsen op toetsenbord voor het besturen van de pokémon
        if keys[pygame.K_LEFT]:
            pokemon_rect.x -= snelheid
        if keys[pygame.K_RIGHT]:
            pokemon_rect.x += snelheid
        if keys[pygame.K_UP]:
            pokemon_rect.y -= snelheid
        if keys[pygame.K_DOWN]:
            pokemon_rect.y += snelheid

        if controleer_botsing(pokemon_rect): # Controleert of de pokémon een obstakel heeft geraakt
            pokemon_rect.topleft = oude_pos # Zet de pokémon terug op zijn oude positie

        if controleer_vijhand(pokemon_rect): # Controleert of de pokémon op een vijand-tegel staat
            flits_scherm() # Commando voor de functie om het scherm te laten flitsen
            if start_gevecht(): # Commando voor het starten van het gevecht
# Zet de pokémon op de juiste plek op de kaart
                pokemon_rect.x = TILE_SIZE
                pokemon_rect.y = TILE_SIZE

        scherm.fill(WIT) # Maakt de achtergrondkleur van het hele scherm wit
        teken_map() # Geeft de kaart weer
        scherm.blit(pokemon_afbeelding, pokemon_rect) # Tekent de pokémon van de speler op het scherm op basis van de huidige positie

        pygame.display.update() # Ververst alleen de delen van het scherm die zijn veranderd

        klok.tick(FPS) # Beperkt het aantal keren dat de game-lus per seconden wordt uitgevoerd

game_loop() # Start de game loop