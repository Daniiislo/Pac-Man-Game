from src.gui.pacman_map import PacmanMap
from src.sprites.pacman import Pacman
from src.sprites.Ghost import GhostManager
from src.gui.menu import Menu
from src.game.level_management import LevelManager
import pygame
import time

class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        self._screen = screen
        self._game_state = game_state
        self.all_sprites = all_sprites
        
        # Initialize menu
        self.menu = Menu(screen, game_state)
        
        # Initialize map
        self._map = PacmanMap(self._game_state)
        self._map_surface = self._map.render_map_surface()
        
        # Initialize pacman
        self.pacman = Pacman(self._game_state, self._map.load_pacman_pos())
        self._game_state.pacman_pos = self._map.load_pacman_pos()
        
        # Initialize ghost manager
        self.ghosts = GhostManager(self._game_state)
        self.ghosts_pos_list = self._map.load_ghosts_pos()
        self.ghosts.set_original_positions(self.ghosts_pos_list)
        
        # Initialize level manager
        self.level_manager = LevelManager(self._game_state)
        
        # Initialize font for READY!
        self.ready_font = pygame.font.SysFont('Arial', 36, bold=True)
        
        # Add pacman to sprite group
        self.all_sprites.add(self.pacman)
        
    def load_level(self, level):
        """Load game level"""
        self._game_state.current_level = level
        
        # Remove all old ghosts
        for ghost in self.ghosts.ghosts_list:
            ghost.kill()
        self.ghosts.ghosts_list.clear()
        
        # Create new ghosts based on level
        ghost_list = self.level_manager.create_ghosts_for_level(
            level, 
            self.ghosts, 
            self.ghosts.original_pos
        )
        
        self.ghosts.reset_ghosts(ghost_list)
        
        # Add ghosts to sprite group
        for ghost in self.ghosts.ghosts_list:
            self.all_sprites.add(ghost)
            
        # Set READY! state
        self._game_state.show_ready = True
        self._game_state.ready_start_time = time.time()
        self._game_state.game_started = True

    def process_menu(self):
        """Process menu"""
        result = self.menu.handle_events()
        
        if result is True:  # Player has selected a level
            selected_level = self.menu.selected_level
            self.load_level(selected_level)
            return True
        elif result is False:  # Player has quit
            return False
            
        # Draw menu
        self.menu.draw()
        return None

    def draw_game(self):
        """Draw game screen"""
        # Draw map
        self._screen.blit(self._map_surface, (0, 0))
        
    def draw_ready_message(self):
        """Display READY! text in the center of screen"""
        if self._game_state.show_ready:
            ready_text = self.ready_font.render("READY!", True, (255, 255, 0))
            text_rect = ready_text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2 + 40))
            self._screen.blit(ready_text, text_rect)
            
            # Display for 2 seconds
            if time.time() - self._game_state.ready_start_time > 2:
                self._game_state.show_ready = False
        
    def draw_screens(self):
        """Handle displaying the appropriate screen (menu or game)"""
        if not self._game_state.game_started:
            result = self.process_menu()
            if result is False:
                self._game_state.running = False
        else:
            # Draw game screen
            self.draw_game()
            self.draw_ready_message()
