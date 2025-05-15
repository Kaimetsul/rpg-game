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
    clock = pygame.time.Clock()
    selected_class = None
    battle = None
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected_class is None:
                    # Check if any character class was clicked
                    for char_class in CHARACTER_CLASSES:
                        if char_class.rect.collidepoint(mouse_pos):
                            selected_class = char_class
                            battle = Battle(char_class)
                            print(f"Selected: {char_class.name}")
                else:
                    # Handle attack selection
                    for i, attack in enumerate(selected_class.attacks):
                        attack_rect = pygame.Rect(50, 150 + i * 50, 200, 30)
                        if attack_rect.collidepoint(mouse_pos):
                            attack_name, damage, enemy_hp = battle.attack(i)
                            print(f"Used {attack_name} for {damage} damage. Enemy HP: {enemy_hp}")
                            if battle.is_enemy_defeated():
                                print("Enemy defeated!")
                                # TODO: Handle enemy defeat
        
        if selected_class is None:
            # Clear the screen
            ui.screen.fill(ui.black)  # Completely black background
            
            # Draw title
            ui.draw_title()
            
            # Draw character boxes
            for char_class in CHARACTER_CLASSES:
                is_hovered = char_class.rect.collidepoint(mouse_pos)
                ui.draw_character_box(char_class, is_hovered)
        else:
            ui.draw_battle_screen(selected_class, battle.enemy_hp)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
