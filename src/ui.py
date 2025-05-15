import pygame

class UI:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("RPG Character Selection")
        self.title_font = pygame.font.Font(None, 48)
        self.class_font = pygame.font.Font(None, 36)
        self.attack_font = pygame.font.Font(None, 24)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def draw_character_box(self, char_class, is_hovered=False):
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
        pygame.draw.polygon(self.screen, self.white, points)
        pygame.draw.polygon(self.screen, self.black, points, 2)
        
        name_text = self.class_font.render(char_class.name, True, self.black)
        name_rect = name_text.get_rect(center=(rect.centerx, rect.centery))
        self.screen.blit(name_text, name_rect)

    def draw_battle_screen(self, selected_class, enemy_hp):
        self.screen.fill(self.black)
        
        enemy_text = self.class_font.render(f"Enemy HP: {enemy_hp}", True, self.white)
        self.screen.blit(enemy_text, (50, 50))
        
        for i, attack in enumerate(selected_class.attacks):
            attack_text = self.attack_font.render(f"{attack['name']} - {attack['damage']} damage", True, self.white)
            self.screen.blit(attack_text, (50, 150 + i * 50))
        
        pygame.display.flip()

    def draw_title(self):
        title_text = self.title_font.render("Choose Your Character", True, self.white)
        title_rect = title_text.get_rect(center=(self.window_width // 2, 50))
        self.screen.blit(title_text, title_rect) 