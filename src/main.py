# Jenkins Polling Test - This comment was added to test automatic builds
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
HOVER_COLOR = (30, 30, 30)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("RPG Character Selection")
#BREAD
# Character classes
CHARACTER_CLASSES = [
    {
        "name": "Hunter",
        "description": "Expert in ranged combat and tracking",
        "rect": pygame.Rect(100, 150, 250, 300)
    },
    {
        "name": "Mage",
        "description": "Master of arcane arts and spells",
        "rect": pygame.Rect(450, 150, 250, 300)
    },
    {
        "name": "Beast Tamer",
        "description": "Controls and commands wild creatures",
        "rect": pygame.Rect(100, 470, 250, 300)
    },
    {
        "name": "Tank",
        "description": "Heavy armor and defensive specialist",
        "rect": pygame.Rect(450, 470, 250, 300)
    }
]

# Font setup
title_font = pygame.font.Font(None, 48)
class_font = pygame.font.Font(None, 36)
desc_font = pygame.font.Font(None, 24)

def draw_character_box(char_class, is_hovered=False):
    # Draw the box
    color = HOVER_COLOR if is_hovered else BLACK
    pygame.draw.rect(screen, color, char_class["rect"], border_radius=15)
    pygame.draw.rect(screen, GRAY, char_class["rect"], 2, border_radius=15)
    
    # Draw the text
    name_text = class_font.render(char_class["name"], True, WHITE)
    desc_text = desc_font.render(char_class["description"], True, WHITE)
    
    # Center the text
    name_rect = name_text.get_rect(center=(char_class["rect"].centerx, char_class["rect"].top + 50))
    desc_rect = desc_text.get_rect(center=(char_class["rect"].centerx, char_class["rect"].top + 100))
    
    screen.blit(name_text, name_rect)
    screen.blit(desc_text, desc_rect)

def main():
    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any character class was clicked
                for char_class in CHARACTER_CLASSES:
                    if char_class["rect"].collidepoint(mouse_pos):
                        print(f"Selected: {char_class['name']}")
                        # TODO: Handle character selection
        
        # Clear the screen
        screen.fill((26, 26, 26))  # Dark gray background
        
        # Draw title
        title_text = title_font.render("Choose Your Character", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Draw character boxes
        for char_class in CHARACTER_CLASSES:
            is_hovered = char_class["rect"].collidepoint(mouse_pos)
            draw_character_box(char_class, is_hovered)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
