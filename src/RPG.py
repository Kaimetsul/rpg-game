import pygame

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_MARGIN = 20

# Button positions
button_positions = [
    (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 2 * (BUTTON_HEIGHT + BUTTON_MARGIN)),
    (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - (BUTTON_HEIGHT + BUTTON_MARGIN)),
    (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2),
    (WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + (BUTTON_HEIGHT + BUTTON_MARGIN))
]

# Button texts
button_texts = ["Hunter", "Mage", "Tank", "Beast Tamer"]

# Font
font = pygame.font.SysFont(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill(BLACK)

    # Draw buttons
    for i, (x, y) in enumerate(button_positions):
        pygame.draw.rect(screen, WHITE, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        text = font.render(button_texts[i], True, BLACK)
        text_rect = text.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit() 