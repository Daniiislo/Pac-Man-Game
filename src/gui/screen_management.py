from src.gui.pacman_map import PacmanMap
from src.sprites.pacman import Pacman
from src.sprites.ghost import GhostManager
from src.gui.menu import Menu
from src.game.level_management import LevelManager
from src.utils.screen_utils import display_performance_metrics
from src.utils.movement_ultils import copy_matrix, update_matrix
import pygame
import time
import math
from src.gui.menu import TestCaseSelector

class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        self._screen = screen
        self._game_state = game_state
        self._all_sprites = all_sprites
        
        # Add reference to event handler
        from src.game.event_management import EventHandler
        self._event_handler = EventHandler(screen, game_state, self)
        
        # Initialize level manager
        self.level_manager = LevelManager(game_state)
        
        # Initialize menu
        self.menu = Menu(screen, game_state)
        
        # Add test case selector (initialize as None)
        self.test_case_selector = None
        
        # Initialize map
        self._map = PacmanMap(self._game_state)
        self._map_surface = self._map.render_map_surface()
        
        # Initialize ghost manager
        self.ghosts = GhostManager(self._game_state)
        
        # Initialize font for READY!
        self.ready_font = pygame.font.SysFont('Arial', 36, bold=True)
        # Initialize font for GAME OVER
        self.game_over_font = pygame.font.SysFont('Arial', 60, bold=True)
        self.instruction_font = pygame.font.SysFont('Arial', 24, bold=False)
        # Game over start time
        self.game_over_start_time = 0
        # Animation variables
        self.animation_scale = 1.0
        self.animation_direction = 1
        self.color_value = 0
        
        # Create dark overlay surface for game over effect
        self.dark_overlay = pygame.Surface((self._screen.get_width(), self._screen.get_height()), pygame.SRCALPHA)
        self.dark_overlay.fill((0, 0, 0, 180))  # RGBA: Black with 70% opacity
        
        
    def reset_screen_state(self):
        """Reset screen manager state"""
        # Reset game over related variables
        self.game_over_start_time = 0
        self.animation_scale = 1.0
        self.animation_direction = 1
        self.color_value = 0
        
        # Reset sprite groups
        self._all_sprites.empty()

        self.ghosts.ghosts_list.clear()
        self.pacman = None

        # Also reset test case selector
        self.test_case_selector = None
        
    def init_level(self, level, test_case):
        """Init game level with specific test case"""
        self._game_state.current_level = level
        self._game_state.selected_test_case = test_case

        # Load pacman and ghosts positions for the level from JSON file with the specified test case
        self.level_manager.load_positions_for_level(level, test_case)

        # Initialize the matrix for the level
        self._game_state.matrix = copy_matrix(self._map.original_matrix)
        
        ghost_classes = self.level_manager.get_ghost_classes_for_level(level)

        # Create new ghosts based on level
        for ghost_name, ghost_class in ghost_classes.items():
            self.ghosts.ghosts_list.append(ghost_class(ghost_name, self._game_state))
        
        self.pacman = Pacman(self._game_state, self._game_state.pacman_pos)

        self._all_sprites.add(self.pacman)
        
        # Add ghosts to sprite group
        for ghost in self.ghosts.ghosts_list:
            self._all_sprites.add(ghost)

        # Update matrix with ghost positions
        for ghost in ghost_classes.keys():
            pos = self._game_state.ghosts_pos_list[ghost]
            if pos:
                update_matrix(self._game_state.matrix, pos, True, 2)

            
        # Set READY! state
        self._game_state.show_ready = True
        self._game_state.ready_start_time = time.time()
        self._game_state.game_started = True
        # Ensure game_over is reset when starting new level
        self._game_state.game_over = False

    def process_menu(self, events=None):
        """Process menu"""
        # If test case selector is active, process it instead of main menu
        if self.test_case_selector is not None:
            # Use event handler instead of direct method call
            result = self._event_handler.handle_test_case_selector_events(events, self.test_case_selector)
            
            if result == "back":
                # Go back to level selection
                self.test_case_selector = None
                return None
            elif result is not None and 1 <= result <= 5:
                # User selected a test case, init the level with it
                self.init_level(self.menu.selected_level, result)
                self.test_case_selector = None
                return True
            elif result is False:  # Player has quit
                return False
            
            # Draw test case selector
            self.test_case_selector.draw()
            return None
            
        # Process main menu as before, but use event handler
        if events:
            result = self._event_handler.handle_menu_events(events, self.menu)
        else:
            events = pygame.event.get()
            result = self._event_handler.handle_menu_events(events, self.menu)
        
        if result is True:  # Player has selected a level
            # For levels 5 and 6, automatically use test case 6 without showing selector
            if self.menu.selected_level in [5, 6]:
                self.init_level(self.menu.selected_level, 6)
                return True
            else:
                # For levels 1-4, show test case selector
                self.test_case_selector = TestCaseSelector(self._screen, self._game_state, self.menu.selected_level)
                return None
        elif result is False:  # Player has quit
            return False
        
        # Draw menu
        self.menu.draw()
        return None

    def draw_map(self):
        """Draw game screen"""
        # Draw map
        self._screen.blit(self._map_surface, (0, 0))
        
    def draw_ready_message(self):
        """Display READY! text in the center of screen"""
        if self._game_state.show_ready:
            ready_text = self.ready_font.render("READY!", True, (255, 255, 0))
            text_rect = ready_text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2 + 50))
            self._screen.blit(ready_text, text_rect)
            
            # Display for 2 seconds
            if time.time() - self._game_state.ready_start_time > 2:
                self._game_state.show_ready = False
                
    def apply_dark_overlay(self):
        """Apply dark overlay to create dimming effect"""
        # Apply overlay with pulsating effect for more drama
        current_time = time.time() - self.game_over_start_time
        overlay_alpha = min(180, int(180 * min(1.0, current_time / 0.5)))  # Fade in over 0.5 seconds
        
        # Pulsating effect after fade in
        if current_time > 0.5:
            pulse = (math.sin(current_time * 1.5) * 15) + 180  # Oscillate between 165-195 alpha
            overlay_alpha = int(min(pulse, 195))
        
        # Update overlay alpha
        self.dark_overlay.set_alpha(overlay_alpha)
        self._screen.blit(self.dark_overlay, (0, 0))
                
    def draw_game_over_message(self):
        """Display GAME OVER text in the center of screen with enhanced visual effects"""
        if self._game_state.game_over:
            # Save start time if not set
            if self.game_over_start_time == 0:
                self.game_over_start_time = time.time()
            
            # Apply dark overlay effect
            self.apply_dark_overlay()
                
            # Create animation effect for GAME OVER
            current_time = time.time() - self.game_over_start_time
            
            # Animation effect for GAME OVER
            self.animation_scale += 0.03 * self.animation_direction
            if self.animation_scale > 1.15:
                self.animation_direction = -1
            elif self.animation_scale < 0.95:
                self.animation_direction = 1
                
            # Gradient color effect from red to orange
            self.color_value = (math.sin(current_time * 3) + 1) * 127.5
            color = (255, min(self.color_value, 255), 0)
            
            # Draw shadow effect for text
            shadow_offset = 4
            shadow_color = (40, 40, 40)
            base_font_size = 60
            animated_size = int(base_font_size * self.animation_scale)
            game_over_font = pygame.font.SysFont('Arial', animated_size, bold=True)
            
            # Display "GAME OVER" with shadow
            game_over_text = game_over_font.render("GAME OVER", True, color)
            shadow_text = game_over_font.render("GAME OVER", True, shadow_color)
            
            # Position of text
            center_x = self._screen.get_width() // 2
            center_y = self._screen.get_height() // 2 - 20
            
            # Draw shadow before text
            shadow_rect = shadow_text.get_rect(center=(center_x + shadow_offset, center_y + shadow_offset))
            self._screen.blit(shadow_text, shadow_rect)
            
            # Draw main text
            text_rect = game_over_text.get_rect(center=(center_x, center_y))
            self._screen.blit(game_over_text, text_rect)
            
            # Add instruction to return to menu
            instruction_opacity = int(math.sin(current_time * 5) * 127.5 + 127.5)  # Flicker between 0-255
            instruction_color = (255, 255, instruction_opacity)
            instruction_text = self.instruction_font.render("Press ESC to return to Menu", True, instruction_color)
            instruction_rect = instruction_text.get_rect(center=(center_x, center_y + 70))
            self._screen.blit(instruction_text, instruction_rect)
            
            # Display performance metrics for levels 1-4
            display_performance_metrics(self._screen, self._game_state, center_x, center_y)
            
            # After 60 seconds, automatically return to menu
            if time.time() - self.game_over_start_time > 60:
                # Use reset_game function instead of manual setup
                self._game_state.reset_game()
                self.reset_screen_state()
        
    def draw_screens(self, events=None):
        """Handle displaying the appropriate screen (menu or game)"""
        if not self._game_state.game_started:
            result = self.process_menu(events)
            if result is False:
                self._game_state.running = False
        else:
            # Draw map
            self.draw_map()
            
            # Draw all sprites in game
            self._all_sprites.draw(self._screen)
            
            if self._game_state.game_over:
                self.draw_game_over_message()
            else:
                self.draw_ready_message()
