# Jenkins Polling Test - This comment was added to test automatic builds
import pygame
import sys
import random
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

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the UI
ui = UI(WINDOW_WIDTH, WINDOW_HEIGHT)

# Character classes
for char_class in CHARACTER_CLASSES:
    char_class.rect = pygame.Rect(300, 150 + CHARACTER_CLASSES.index(char_class) * 70, 200, 50)

# Font setup
title_font = pygame.font.Font(None, 48)
class_font = pygame.font.Font(None, 36)
attack_font = pygame.font.Font(None, 24)

# Initialize inventory and quest manager
inventory = Inventory()
quest_manager = QuestManager()

# Add a sample quest
sample_quest = Quest(
    "Defeat the Dragon",
    "Slay the dragon terrorizing the village",
    ["Kill 5 enemies", "Collect dragon scales"],
    reward={"gold": 100, "experience": 50}
)
quest_manager.add_quest(sample_quest)

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
    pygame.draw.polygon(ui.screen, WHITE, points)
    pygame.draw.polygon(ui.screen, BLACK, points, 2)
    
    # Draw the text
    name_text = class_font.render(char_class.name, True, BLACK)
    name_rect = name_text.get_rect(center=(rect.centerx, rect.centery))
    ui.screen.blit(name_text, name_rect)

def draw_battle_screen(selected_class, enemy_hp):
    ui.screen.fill(BLACK)
    
    # Draw enemy HP
    enemy_text = class_font.render(f"Enemy HP: {enemy_hp}", True, WHITE)
    ui.screen.blit(enemy_text, (50, 50))
    
    # Draw attacks
    for i, attack in enumerate(selected_class.attacks):
        attack_text = attack_font.render(f"{attack['name']} - {attack['damage']} damage", True, WHITE)
        ui.screen.blit(attack_text, (50, 150 + i * 50))
    
    pygame.display.flip()

def draw_inventory():
    ui.screen.fill(BLACK)
    title = title_font.render("Inventory", True, WHITE)
    ui.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
    y = 150
    for item in inventory.items:
        item_text = class_font.render(f"{item.name} ({item.type})", True, WHITE)
        ui.screen.blit(item_text, (WINDOW_WIDTH // 2 - item_text.get_width() // 2, y))
        y += 50
    pygame.display.flip()

def draw_quests():
    ui.screen.fill(BLACK)
    title = title_font.render("Quests", True, WHITE)
    ui.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
    y = 150
    for quest in quest_manager.get_active_quests():
        quest_text = class_font.render(f"{quest.title}: {quest.description}", True, WHITE)
        ui.screen.blit(quest_text, (WINDOW_WIDTH // 2 - quest_text.get_width() // 2, y))
        y += 50
    pygame.display.flip()

def draw_how_to_play():
    ui.screen.fill(BLACK)
    title = title_font.render("How to Play", True, WHITE)
    ui.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
    instructions = [
        "Press 'I' to open inventory",
        "Press 'Q' to view quests"
    ]
    y = 150
    for instruction in instructions:
        instruction_text = class_font.render(instruction, True, WHITE)
        ui.screen.blit(instruction_text, (WINDOW_WIDTH // 2 - instruction_text.get_width() // 2, y))
        y += 50
    pygame.display.flip()

def main():
    pygame.init()
    window_width = 800
    window_height = 600
    ui = UI(window_width, window_height)
    
    # Character selection setup
    char_boxes = []
    box_width = 150
    box_height = 100
    spacing = 50
    total_width = (box_width * 4) + (spacing * 3)
    start_x = (window_width - total_width) // 2
    
    for i, char_class in enumerate(CHARACTER_CLASSES):
        x = start_x + (i * (box_width + spacing))
        y = window_height // 2
        char_class.rect = pygame.Rect(x, y, box_width, box_height)
        char_boxes.append(char_class)
    
    selected_class = None
    battle = None
    game_state = "character_select"  # States: character_select, battle, maze, death, inventory, quests, how_to_play
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
                    if game_state == "how_to_play":
                        game_state = "character_select"
                    else:
                        game_state = "how_to_play"
            
            if game_state == "character_select":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for char_class in char_boxes:
                        if char_class.rect.collidepoint(event.pos):
                            selected_class = char_class
                            battle = Battle(selected_class)
                            game_state = "battle"
            
            elif game_state == "battle":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        attack_index = event.key - pygame.K_1
                        if attack_index < len(selected_class.attacks):
                            attack_name, damage, enemy_hp = battle.attack(attack_index)
                            if battle.is_enemy_defeated():
                                battle.enter_maze()
                                game_state = "maze"
                                # Give a health potion after battle
                                inventory.add_item(Item("Health Potion", "Consumable", 10))
                                # 10% chance to drop a weapon
                                if random.random() < 0.1:
                                    inventory.add_item(Item("Weapon", "Weapon", 10))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(attack_rects):
                        if rect.collidepoint(event.pos):
                            attack_name, damage, enemy_hp = battle.attack(i)
                            if battle.is_enemy_defeated():
                                battle.enter_maze()
                                game_state = "maze"
                                # Give a health potion after battle
                                inventory.add_item(Item("Health Potion", "Consumable", 10))
                                # 10% chance to drop a weapon
                                if random.random() < 0.1:
                                    inventory.add_item(Item("Weapon", "Weapon", 10))
            
            elif game_state == "maze":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if battle.make_choice("left"):
                            if len(battle.current_path) == len(battle.correct_path):
                                game_state = "character_select"
                                battle.reset()
                    elif event.key == pygame.K_RIGHT:
                        if battle.make_choice("right"):
                            if len(battle.current_path) == len(battle.correct_path):
                                game_state = "character_select"
                                battle.reset()
                    if battle.is_dead:
                        game_state = "death"
            
            elif game_state == "death":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "character_select"
                        battle.reset()
        
        # Drawing
        if game_state == "character_select":
            ui.screen.fill(ui.black)
            ui.draw_title()
            for char_class in char_boxes:
                ui.draw_character_box(char_class)
        
        elif game_state == "battle":
            attack_rects = ui.draw_battle_screen(selected_class, battle.enemy_hp)
        
        elif game_state == "maze":
            ui.draw_maze_level(battle.current_path)
        
        elif game_state == "death":
            ui.draw_death_screen()
        
        elif game_state == "inventory":
            draw_inventory()
        
        elif game_state == "quests":
            draw_quests()
        
        elif game_state == "how_to_play":
            draw_how_to_play()
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
