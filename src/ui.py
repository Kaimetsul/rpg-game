import pygame

class UI:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("RPG Game")
        self.title_font = pygame.font.Font(None, 48)
        self.class_font = pygame.font.Font(None, 36)
        self.attack_font = pygame.font.Font(None, 24)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.gray = (100, 100, 100)

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
        
        # Enemy health bar on the left
        enemy_text = self.class_font.render(f"Enemy HP: {enemy_hp}", True, self.white)
        self.screen.blit(enemy_text, (20, 50))
        
        # Health bar visualization
        bar_width = 200
        bar_height = 20
        health_percentage = max(0, enemy_hp / 1000)  # Assuming max HP is 1000
        pygame.draw.rect(self.screen, self.red, (20, 80, bar_width * health_percentage, bar_height))
        pygame.draw.rect(self.screen, self.white, (20, 80, bar_width, bar_height), 2)
        
        # Attacks on the right with clickable buttons
        attack_rects = []
        for i, attack in enumerate(selected_class.attacks):
            # Create a button rectangle
            button_rect = pygame.Rect(self.window_width - 250, 150 + i * 50, 200, 40)
            attack_rects.append(button_rect)
            
            # Draw button background
            pygame.draw.rect(self.screen, self.gray, button_rect)
            pygame.draw.rect(self.screen, self.white, button_rect, 2)
            
            # Draw attack text
            attack_text = self.attack_font.render(f"{i+1}. {attack['name']} - {attack['damage']} damage", True, self.white)
            text_rect = attack_text.get_rect(center=button_rect.center)
            self.screen.blit(attack_text, text_rect)
        
        # Add instructions
        instructions = self.attack_font.render("Click an attack or press 1-4", True, self.white)
        self.screen.blit(instructions, (self.window_width - 250, 400))
        
        pygame.display.flip()
        return attack_rects

    def draw_maze_level(self, current_path):
        self.screen.fill(self.black)
        
        # Draw maze title
        title_text = self.title_font.render("Maze Level", True, self.white)
        title_rect = title_text.get_rect(center=(self.window_width // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw current path
        path_text = self.class_font.render(f"Current Path: {' -> '.join(current_path)}", True, self.white)
        path_rect = path_text.get_rect(center=(self.window_width // 2, 150))
        self.screen.blit(path_text, path_rect)
        
        # Draw direction choices
        left_text = self.class_font.render("Press LEFT for Left", True, self.white)
        right_text = self.class_font.render("Press RIGHT for Right", True, self.white)
        
        left_rect = left_text.get_rect(center=(self.window_width // 2, 250))
        right_rect = right_text.get_rect(center=(self.window_width // 2, 300))
        
        self.screen.blit(left_text, left_rect)
        self.screen.blit(right_text, right_rect)
        
        pygame.display.flip()

    def draw_death_screen(self):
        self.screen.fill(self.black)
        death_text = self.title_font.render("YOU DIED", True, self.red)
        restart_text = self.class_font.render("Press SPACE to restart", True, self.white)
        
        death_rect = death_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))
        restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 50))
        
        self.screen.blit(death_text, death_rect)
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()

    def draw_title(self):
        title_text = self.title_font.render("Choose Your Character", True, self.white)
        title_rect = title_text.get_rect(center=(self.window_width // 2, 50))
        self.screen.blit(title_text, title_rect) 