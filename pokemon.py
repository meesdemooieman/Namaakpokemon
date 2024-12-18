import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimension
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Pokémon Blue")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 32)  # Adjusted font size

# Load and scale images for Pokémon
charmander_img = pygame.image.load("charmander.png")
bulbasaur_img = pygame.image.load("bulbasaur.png")
charmander_img = pygame.transform.scale(charmander_img, (350, 350))  # Resize Charmander
bulbasaur_img = pygame.transform.scale(bulbasaur_img, (300, 300))    # Resize Bulbasaur

# Pokémon stats and attacks
class Pokemon:
    def __init__(self, name, max_hp, attack, image):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.image = image

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    def is_fainted(self):
        return self.current_hp == 0

# Player's Pokémon
player_pokemon = Pokemon("Charmander", 100, {"Scratch": 15, "Ember": 20}, charmander_img)

# Opponent's Pokémon
opponent_pokemon = Pokemon("Bulbasaur", 120, {"Tackle": 10, "Vine Whip": 15}, bulbasaur_img)

def draw_health_bar(pokemon, x, y):
    bar_width = 200
    bar_height = 20
    health_ratio = pokemon.current_hp / pokemon.max_hp
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_ratio, bar_height))

def display_text(text, x, y):
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (x, y))

def display_image(image, x, y):
    screen.blit(image, (x, y))

# Game loop
running = True
player_turn = True
selected_attack = None
battle_log = []

while running:
    screen.fill(WHITE)  # Corrected `fill` method

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if player_turn and not selected_attack:
                if event.key == pygame.K_1:
                    selected_attack = "Scratch"
                elif event.key == pygame.K_2:
                    selected_attack = "Ember"

    # Display Pokémon stats, images, and health bars
    display_image(player_pokemon.image, 50, HEIGHT - 350)  # Place Charmander at bottom left
    display_text(f"{player_pokemon.name}", 50, HEIGHT - 400)
    draw_health_bar(player_pokemon, 50, HEIGHT - 380)

    display_image(opponent_pokemon.image, WIDTH - 350, 100)  # Place Bulbasaur at top right corner
    display_text(f"{opponent_pokemon.name}", WIDTH - 250, 50)
    draw_health_bar(opponent_pokemon, WIDTH - 250, 70)

    # Battle log display
    y_offset = 150
    for log in battle_log[-5:]:  # Show the last 5 battle events
        display_text(log, 50, y_offset)
        y_offset += 30  # Adjusted spacing for text

    # Player's turn
    if player_turn and not player_pokemon.is_fainted() and not opponent_pokemon.is_fainted():
        if not selected_attack:
            display_text("Choose your attack:", 50, 50)
            display_text("1: Scratch (15 dmg)", 50, 75)
            display_text("2: Ember (20 dmg)", 50, 100)
        else:
            damage = player_pokemon.attack[selected_attack] + random.randint(-5, 5)
            opponent_pokemon.take_damage(damage)
            battle_log.append(f"{player_pokemon.name} used {selected_attack} and dealt {damage} damage!")
            player_turn = False
            selected_attack = None

    # Opponent's turn
    elif not player_turn and not player_pokemon.is_fainted() and not opponent_pokemon.is_fainted():
        pygame.time.delay(1000)  # Pause for 1 second
        attack_name = random.choice(list(opponent_pokemon.attack.keys()))
        damage = opponent_pokemon.attack[attack_name] + random.randint(-5, 5)
        player_pokemon.take_damage(damage)
        battle_log.append(f"{opponent_pokemon.name} used {attack_name} and dealt {damage} damage!")
        player_turn = True

    # Check for end of battle
    if player_pokemon.is_fainted():
        display_text("You lost the battle!", WIDTH // 2 - 100, HEIGHT // 2)
    elif opponent_pokemon.is_fainted():
        display_text("You won the battle!", WIDTH // 2 - 100, HEIGHT // 2)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
