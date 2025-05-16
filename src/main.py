# Jenkins Polling Test - This comment was added to test automatic builds
import pygame
import sys
from src.game import CHARACTER_CLASSES, Battle
from src.ui import UI

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
    game_state = "character_select"  # States: character_select, battle, maze, death
    attack_rects = []
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(attack_rects):
                        if rect.collidepoint(event.pos):
                            attack_name, damage, enemy_hp = battle.attack(i)
                            if battle.is_enemy_defeated():
                                battle.enter_maze()
                                game_state = "maze"
            
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
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
