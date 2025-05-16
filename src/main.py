"""
Author: Deny Mudashiru
File: main.py
Purpose: Main game logic and UI handling for the D&D RPG game
Dependencies:
    - pygame==2.1.2: Required for game window and graphics
    - pytest==6.2.5: Required for testing
    - pytest-cov==2.12.1: Required for test coverage
    - flake8==4.0.1: Required for code linting
    - pylint==2.12.2: Required for code analysis
"""

# Jenkins Polling Test - This comment was added to test automatic builds
import pygame
import sys
import random
import os
try:
    from src.game import CHARACTER_CLASSES, Battle
    from src.ui import UI
    from src.inventory import Inventory, Item
    from src.quest import Quest, QuestManager
except ImportError:
    from game import CHARACTER_CLASSES, Battle
    from ui import UI
    from inventory import Inventory, Item
    from quest import Quest, QuestManager

# Initialize Pygame
pygame.init()

# Constants for character selection
SELECTION_WIDTH = 800
SELECTION_HEIGHT = 600

# Load background image for battle
BACKGROUND_IMAGE = pygame.image.load("Rpg Background.jpg")
BATTLE_WIDTH = BACKGROUND_IMAGE.get_width()
BATTLE_HEIGHT = BACKGROUND_IMAGE.get_height() + 100  # Add extra height for attack buttons

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

# Load images
def load_image(name, scale=1.0):
    try:
        image = pygame.image.load(name)
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except:
        print(f"Could not load image: {name}")
        return None

# Load character images
CHARACTER_IMAGES = {
    "Hunter": load_image("Hunter.png", 0.5),
    "Tank": load_image("Tank.png", 0.5),
    "Beast": load_image("Beast.png", 0.5)
}
ENEMY_IMAGE = load_image("Enemy.png", 0.5)
OGRE_IMAGE = load_image("Enemy.png", 0.7)  # Using enemy image for ogre temporarily

# Set up the UI with selection size initially
ui = UI(SELECTION_WIDTH, SELECTION_HEIGHT)

# Character classes
for char_class in CHARACTER_CLASSES:
    char_class.rect = pygame.Rect(300, 150 + CHARACTER_CLASSES.index(char_class) * 70, 200, 50)

# Font setup
title_font = pygame.font.Font(None, 48)
class_font = pygame.font.Font(None, 36)
attack_font = pygame.font.Font(None, 24)
hp_font = pygame.font.Font(None, 32)

# Initialize inventory and quest manager
inventory = Inventory()
quest_manager = QuestManager()

# Add the ogre quest
ogre_quest = Quest(
    "Defeat the Ogre",
    "Slay the ogre terrorizing the village",
    ["Kill 3 enemies", "Collect ogre teeth"],
    reward={"gold": 200, "experience": 100}
)
quest_manager.add_quest(ogre_quest)

def draw_button(text, rect, color=BLUE, hover_color=GREEN):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    
    # Draw button background
    pygame.draw.rect(ui.screen, hover_color if is_hovered else color, rect)
    pygame.draw.rect(ui.screen, WHITE, rect, 2)  # White border
    
    # Draw text
    text_surface = class_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    ui.screen.blit(text_surface, text_rect)
    
    return is_hovered

def draw_character_box(char_class, is_hovered=False):
    # Draw the octagon
    rect = char_class.rect
    points = [
        (rect.left, rect.top + 10),
        (rect.left + 10, rect.top),
        (rect.right - 10, rect.top),
        (rect.right, rect.top + 10),
        (rect.right, rect.bottom - 10),
        (rect.right - 10, rect.bottom),
        (rect.left + 10, rect.bottom),
        (rect.left, rect.bottom - 10)
    ]
    color = GREEN if is_hovered else BLUE
    pygame.draw.polygon(ui.screen, color, points)
    pygame.draw.polygon(ui.screen, WHITE, points, 2)
    
    # Draw the text
    name_text = class_font.render(char_class.name, True, WHITE)
    name_rect = name_text.get_rect(center=(rect.centerx, rect.centery))
    ui.screen.blit(name_text, name_rect)
    
    # Draw character image
    char_image = CHARACTER_IMAGES.get(char_class.name)
    if char_image:
        image_rect = char_image.get_rect(midtop=(rect.centerx, rect.top - 100))
        ui.screen.blit(char_image, image_rect)

def draw_battle_screen(selected_class, enemy_hp):
    # Draw background
    ui.screen.blit(BACKGROUND_IMAGE, (0, 0))
    
    # Draw player character
    player_image = CHARACTER_IMAGES.get(selected_class.name)
    if player_image:
        player_rect = player_image.get_rect(midleft=(100, BATTLE_HEIGHT - 150))
        ui.screen.blit(player_image, player_rect)
    
    # Draw enemy
    if ENEMY_IMAGE:
        enemy_rect = ENEMY_IMAGE.get_rect(midright=(BATTLE_WIDTH - 100, BATTLE_HEIGHT - 150))
        ui.screen.blit(ENEMY_IMAGE, enemy_rect)
    
    # Draw enemy HP
    enemy_hp_text = hp_font.render(f"Enemy HP: {enemy_hp}", True, WHITE)
    enemy_hp_rect = enemy_hp_text.get_rect(midtop=(BATTLE_WIDTH // 2, 50))
    ui.screen.blit(enemy_hp_text, enemy_hp_rect)
    
    # Draw black area for attacks
    attack_area = pygame.Rect(0, BATTLE_HEIGHT - 100, BATTLE_WIDTH, 100)
    pygame.draw.rect(ui.screen, BLACK, attack_area)
    
    # Draw attacks in boxes
    attack_rects = []
    button_width = 200
    button_height = 60
    spacing = 20
    total_width = (button_width * 4) + (spacing * 3)
    start_x = (BATTLE_WIDTH - total_width) // 2
    button_y = BATTLE_HEIGHT - 80
    
    for i, attack in enumerate(selected_class.attacks):
        # Draw button box
        button_rect = pygame.Rect(start_x + (i * (button_width + spacing)), button_y, button_width, button_height)
        pygame.draw.rect(ui.screen, GRAY, button_rect)
        pygame.draw.rect(ui.screen, WHITE, button_rect, 2)  # White border
        
        # Draw attack text
        attack_text = attack_font.render(f"{attack['name']} - {attack['damage']} damage", True, WHITE)
        text_rect = attack_text.get_rect(center=button_rect.center)
        ui.screen.blit(attack_text, text_rect)
        
        attack_rects.append(button_rect)
    
    pygame.display.flip()
    return attack_rects

def draw_inventory():
    ui.screen.fill(BLACK)
    title = title_font.render("Inventory", True, WHITE)
    ui.screen.blit(title, (SELECTION_WIDTH // 2 - title.get_width() // 2, 50))
    y = 150
    for item in inventory.items:
        item_text = class_font.render(f"{item.name} ({item.type})", True, WHITE)
        ui.screen.blit(item_text, (SELECTION_WIDTH // 2 - item_text.get_width() // 2, y))
        y += 50
    pygame.display.flip()

def draw_quests():
    ui.screen.fill(BLACK)
    title = title_font.render("Quests", True, WHITE)
    ui.screen.blit(title, (SELECTION_WIDTH // 2 - title.get_width() // 2, 50))
    y = 150
    for quest in quest_manager.get_active_quests():
        quest_text = class_font.render(f"{quest.title}: {quest.description}", True, WHITE)
        ui.screen.blit(quest_text, (SELECTION_WIDTH // 2 - quest_text.get_width() // 2, y))
        y += 50
    pygame.display.flip()

def draw_help_screen():
    ui.screen.fill(BLACK)
    title = title_font.render("Game Controls", True, WHITE)
    ui.screen.blit(title, (SELECTION_WIDTH // 2 - title.get_width() // 2, 50))
    
    # Game controls and instructions
    instructions = [
        "Character Selection:",
        "- Click on a character to select",
        "- Each character has unique abilities",
        "",
        "Battle Controls:",
        "- Use number keys 1-4 to attack",
        "- Or click the attack buttons",
        "",
        "Maze Navigation:",
        "- Use LEFT and RIGHT arrow keys",
        "- Choose the correct path",
        "",
        "Menu Controls:",
        "- Press I or click Inventory button",
        "- Press Q or click Quests button",
        "- Press H or click Help button",
        "",
        "After defeating enemies:",
        "- You'll receive health potions",
        "- Chance to get weapon drops",
        "- Complete quests for rewards"
    ]
    
    y = 120
    for instruction in instructions:
        instruction_text = class_font.render(instruction, True, WHITE)
        ui.screen.blit(instruction_text, (SELECTION_WIDTH // 2 - instruction_text.get_width() // 2, y))
        y += 40
    
    # Draw back button
    back_rect = pygame.Rect(20, 20, 100, 40)
    if draw_button("Back", back_rect):
        if pygame.mouse.get_pressed()[0]:
            return "character_select"
    
    pygame.display.flip()
    return "help"

def draw_final_battle(selected_class, enemy_hp):
    # Draw background
    ui.screen.blit(BACKGROUND_IMAGE, (0, 0))
    
    # Draw player character
    player_image = CHARACTER_IMAGES.get(selected_class.name)
    if player_image:
        player_rect = player_image.get_rect(midleft=(100, BATTLE_HEIGHT - 150))
        ui.screen.blit(player_image, player_rect)
    
    # Draw final boss
    if OGRE_IMAGE:
        enemy_rect = OGRE_IMAGE.get_rect(midright=(BATTLE_WIDTH - 100, BATTLE_HEIGHT - 150))
        ui.screen.blit(OGRE_IMAGE, enemy_rect)
    
    # Draw boss HP
    boss_hp_text = hp_font.render(f"Ogre King HP: {enemy_hp}", True, WHITE)
    boss_hp_rect = boss_hp_text.get_rect(midtop=(BATTLE_WIDTH // 2, 50))
    ui.screen.blit(boss_hp_text, boss_hp_rect)
    
    # Draw black area for attacks
    attack_area = pygame.Rect(0, BATTLE_HEIGHT - 100, BATTLE_WIDTH, 100)
    pygame.draw.rect(ui.screen, BLACK, attack_area)
    
    # Draw attacks in boxes
    attack_rects = []
    button_width = 200
    button_height = 60
    spacing = 20
    total_width = (button_width * 4) + (spacing * 3)
    start_x = (BATTLE_WIDTH - total_width) // 2
    button_y = BATTLE_HEIGHT - 80
    
    for i, attack in enumerate(selected_class.attacks):
        # Draw button box
        button_rect = pygame.Rect(start_x + (i * (button_width + spacing)), button_y, button_width, button_height)
        pygame.draw.rect(ui.screen, GRAY, button_rect)
        pygame.draw.rect(ui.screen, WHITE, button_rect, 2)
        
        # Draw attack text
        attack_text = attack_font.render(f"{attack['name']} - {attack['damage']} damage", True, WHITE)
        text_rect = attack_text.get_rect(center=button_rect.center)
        ui.screen.blit(attack_text, text_rect)
        
        attack_rects.append(button_rect)
    
    pygame.display.flip()
    return attack_rects

def draw_win_screen():
    ui.screen.fill(BLACK)
    title = title_font.render("You Win!", True, GREEN)
    ui.screen.blit(title, (SELECTION_WIDTH // 2 - title.get_width() // 2, SELECTION_HEIGHT // 2 - 50))
    
    subtitle = class_font.render("Press SPACE to continue", True, WHITE)
    ui.screen.blit(subtitle, (SELECTION_WIDTH // 2 - subtitle.get_width() // 2, SELECTION_HEIGHT // 2 + 50))
    
    pygame.display.flip()

def main():
    pygame.init()
    window_width = SELECTION_WIDTH
    window_height = SELECTION_HEIGHT
    ui = UI(window_width, window_height)
    
    # Character selection setup
    char_boxes = []
    box_width = 200
    box_height = 100
    spacing = 50
    total_width = (box_width * 3) + (spacing * 2)
    start_x = (window_width - total_width) // 2
    
    for i, char_class in enumerate(CHARACTER_CLASSES):
        x = start_x + (i * (box_width + spacing))
        y = window_height // 2
        char_class.rect = pygame.Rect(x, y, box_width, box_height)
        char_boxes.append(char_class)
    
    selected_class = None
    battle = None
    game_state = "character_select"  # States: character_select, battle, maze, death, inventory, quests, help, win
    attack_rects = []
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    if game_state == "inventory":
                        game_state = "character_select"
                    else:
                        game_state = "inventory"
                elif event.key == pygame.K_q:
                    if game_state == "quests":
                        game_state = "character_select"
                    else:
                        game_state = "quests"
                elif event.key == pygame.K_h:
                    if game_state == "help":
                        game_state = "character_select"
                    else:
                        game_state = "help"
                elif event.key == pygame.K_SPACE and game_state == "win":
                    game_state = "character_select"
                    pygame.display.set_mode((SELECTION_WIDTH, SELECTION_HEIGHT))
                    ui = UI(SELECTION_WIDTH, SELECTION_HEIGHT)
            
            if game_state == "character_select":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for char_class in char_boxes:
                        if char_class.rect.collidepoint(event.pos):
                            selected_class = char_class
                            battle = Battle(selected_class)
                            game_state = "battle"
                            pygame.display.set_mode((BATTLE_WIDTH, BATTLE_HEIGHT))
                            ui = UI(BATTLE_WIDTH, BATTLE_HEIGHT)
            
            elif game_state == "battle":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        attack_index = event.key - pygame.K_1
                        if attack_index < len(selected_class.attacks):
                            attack_name, damage, enemy_hp = battle.attack(attack_index)
                            if battle.is_enemy_defeated():
                                battle.enter_maze()
                                game_state = "maze"
                                inventory.add_item(Item("Health Potion", "Consumable", 10))
                                if random.random() < 0.1:
                                    inventory.add_item(Item("Weapon", "Weapon", 10))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(attack_rects):
                        if rect.collidepoint(event.pos):
                            attack_name, damage, enemy_hp = battle.attack(i)
                            if battle.is_enemy_defeated():
                                battle.enter_maze()
                                game_state = "maze"
                                inventory.add_item(Item("Health Potion", "Consumable", 10))
                                if random.random() < 0.1:
                                    inventory.add_item(Item("Weapon", "Weapon", 10))
            
            elif game_state == "maze":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if battle.make_choice("left"):
                            if len(battle.current_path) == len(battle.correct_path):
                                game_state = "battle"
                                battle = Battle(selected_class)
                                pygame.display.set_mode((BATTLE_WIDTH, BATTLE_HEIGHT))
                                ui = UI(BATTLE_WIDTH, BATTLE_HEIGHT)
                    elif event.key == pygame.K_RIGHT:
                        if battle.make_choice("right"):
                            if len(battle.current_path) == len(battle.correct_path):
                                game_state = "battle"
                                battle = Battle(selected_class)
                                pygame.display.set_mode((BATTLE_WIDTH, BATTLE_HEIGHT))
                                ui = UI(SELECTION_WIDTH, SELECTION_HEIGHT)
                    if battle.is_dead:
                        game_state = "death"
            
            elif game_state == "death":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "character_select"
                        battle.reset()
                        pygame.display.set_mode((SELECTION_WIDTH, SELECTION_HEIGHT))
                        ui = UI(SELECTION_WIDTH, SELECTION_HEIGHT)
        
        # Drawing
        if game_state == "character_select":
            ui.screen.fill(BLACK)
            ui.draw_title()
            
            # Draw character boxes
            for char_class in char_boxes:
                mouse_pos = pygame.mouse.get_pos()
                is_hovered = char_class.rect.collidepoint(mouse_pos)
                draw_character_box(char_class, is_hovered)
            
            # Draw menu buttons
            button_width = 150
            button_height = 40
            spacing = 20
            start_x = (SELECTION_WIDTH - (button_width * 3 + spacing * 2)) // 2
            button_y = SELECTION_HEIGHT - 100
            
            # Help button
            help_rect = pygame.Rect(start_x, button_y, button_width, button_height)
            if draw_button("Help (H)", help_rect):
                if pygame.mouse.get_pressed()[0]:
                    game_state = "help"
            
            # Inventory button
            inv_rect = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)
            if draw_button("Inventory (I)", inv_rect):
                if pygame.mouse.get_pressed()[0]:
                    game_state = "inventory"
            
            # Quests button
            quest_rect = pygame.Rect(start_x + (button_width + spacing) * 2, button_y, button_width, button_height)
            if draw_button("Quests (Q)", quest_rect):
                if pygame.mouse.get_pressed()[0]:
                    game_state = "quests"
        
        elif game_state == "battle":
            attack_rects = draw_battle_screen(selected_class, battle.enemy_hp)
            # Check if this is the second battle (after maze)
            if battle.is_enemy_defeated() and len(battle.current_path) > 0:
                game_state = "win"
                pygame.display.set_mode((SELECTION_WIDTH, SELECTION_HEIGHT))
                ui = UI(SELECTION_WIDTH, SELECTION_HEIGHT)
        
        elif game_state == "maze":
            ui.draw_maze_level(battle.current_path)
        
        elif game_state == "death":
            ui.draw_death_screen()
        
        elif game_state == "inventory":
            draw_inventory()
        
        elif game_state == "quests":
            draw_quests()
        
        elif game_state == "help":
            game_state = draw_help_screen()
        
        elif game_state == "win":
            draw_win_screen()
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
