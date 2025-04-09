import pygame
from pygame import font

class Button:
    def __init__(self, x, y, width, height, text, color=(0, 0, 220), hover_color=(50, 50, 255), text_color=(255, 255, 255), outline_color=(0, 0, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = color
        self.font = pygame.font.SysFont('Arial', 28, bold=True)
        self.is_hovered = False
        self.outline_color = outline_color
        self.border_width = 3
        self.glow_value = 0
        self.glow_direction = 1

    def draw(self, screen):
        # Outer glow effect for hovered buttons
        if self.is_hovered:
            self.glow_value += 0.5 * self.glow_direction
            if self.glow_value >= 20:
                self.glow_direction = -1
            elif self.glow_value <= 0:
                self.glow_direction = 1
                
            glow_rect = pygame.Rect(
                self.rect.x - self.glow_value, 
                self.rect.y - self.glow_value,
                self.rect.width + self.glow_value * 2, 
                self.rect.height + self.glow_value * 2
            )
            # Use button color but adjust alpha to create glow effect
            r, g, b = self.color
            glow_color = (max(0, r-50), max(0, g-50), max(0, b-50), 128)
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=15)
            
        # Main button with rounded corners
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=12)
        
        # Button outline
        pygame.draw.rect(screen, self.outline_color, self.rect, width=self.border_width, border_radius=12)
        
        # Button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            self.is_hovered = True
        else:
            self.current_color = self.color
            self.is_hovered = False

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
            return True
        return False

class Menu:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.selected_level = None
        
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        self.title_font = pygame.font.SysFont('Arial', 80, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 30)
        
        # Create level buttons
        button_width = 360
        button_height = 60
        button_spacing = 25
        
        # Center buttons vertically in available space
        total_button_height = 6 * button_height + 5 * button_spacing
        start_y = (self.screen_height - total_button_height) // 2 + 30
        
        self.level_buttons = []
        level_titles = [
            "Level 1 - Blue Ghost (BFS)",
            "Level 2 - Pink Ghost (DFS)",
            "Level 3 - Orange Ghost (UCS)",
            "Level 4 - Red Ghost (A*)",
            "Level 5 - All Ghosts",
            "Level 6 - All Ghosts"
        ]
        
        button_colors = [
            (0, 255, 255),   # Blue
            (255, 51, 153), # Pink
            (255, 128, 0), # Orange
            (255, 0, 0),   # Red
            (153, 76, 0),   # Brown (Level 5)
            (0, 255, 0)    # Green (Level 6)
        ]
        
        # Hover color is darker than the button's main color
        button_hover_colors = []
        for color in button_colors:
            r, g, b = color
            button_hover_colors.append((max(0, r-70), max(0, g-70), max(0, b-70)))
        
        outline_colors = [
            (0, 150, 150),    # Darker cyan (for cyan button)
            (255, 0, 255),    # Pink
            (255, 140, 0),    # Orange
            (255, 0, 0),      # Red
            (0, 0, 0),        # Black (for white button)
            (0, 150, 0)       # Darker green (for green button)
        ]
        
        text_colors = (0, 0, 0)  # Black color for all buttons
        
        for i in range(6):
            y_pos = start_y + i * (button_height + button_spacing)
            self.level_buttons.append(
                Button(
                    (self.screen_width - button_width) // 2,
                    y_pos,
                    button_width,
                    button_height,
                    level_titles[i],
                    color=button_colors[i],
                    hover_color=button_hover_colors[i],
                    outline_color=outline_colors[i],
                    text_color=text_colors
                )
            )
            
        # Animation
        self.animation_frame = 0
        self.animation_speed = 0.2
    
    def draw(self):
        # Draw background
        self.screen.fill((0, 0, 0))
        
        # Update animation frame
        self.animation_frame += self.animation_speed
        
        # Draw decorative elements (pac-dots)
        for i in range(0, self.screen_width, 30):
            pygame.draw.circle(self.screen, (255, 255, 255), (i, 50), 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (i, self.screen_height - 50), 2)
        
        # Draw logo with pulsing effect
        pulse = (abs(pygame.time.get_ticks() % 2000 - 1000) / 1000) * 0.2 + 0.9  # Scale between 0.9 and 1.1
        logo_size = int(80 * pulse)
        logo_font = pygame.font.SysFont('Arial', logo_size, bold=True)
        logo_text = logo_font.render("PAC-MAN", True, (255, 255, 0))
        logo_rect = logo_text.get_rect(center=(self.screen_width // 2, 80))
        self.screen.blit(logo_text, logo_rect)
        
        # Draw level buttons
        for button in self.level_buttons:
            button.draw(self.screen)
    
    def handle_events(self, events=None):
        # If no events are passed, get from pygame
        if events is None:
            events = pygame.event.get()
            
        for event in events:
            if event.type == pygame.QUIT:
                return False
                
            mouse_pos = pygame.mouse.get_pos()
            
            for i, button in enumerate(self.level_buttons):
                button.check_hover(mouse_pos)
                
                if button.is_clicked(mouse_pos, event):
                    self.selected_level = i + 1
                    return True
        
        # Update hover effect for all buttons with current mouse position
        mouse_pos = pygame.mouse.get_pos()
        for button in self.level_buttons:
            button.check_hover(mouse_pos)
            
        return None 