import sys
import pygame

from src.config import *
from src.game.state_management import GameState
from src.game.event_management import EventHandler
from src.gui.screen_management import ScreenManager

class GameRun:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman Game")

        self.game_state = GameState()
        self.events = EventHandler(self.screen, self.game_state)
        self.all_sprites = pygame.sprite.Group()
        self.gui = ScreenManager(self.screen, self.game_state, self.all_sprites)
        
        # Flag to track if game has been reset
        self.was_game_over = False

    def check_collision_with_ghosts(self):
        """Kiểm tra va chạm giữa Pacman và các con ma"""
        if self.game_state.game_over:
            return False
            
        # Get Pacman's rectangle
        pacman_rect = self.gui.pacman.rect
        
        # Check each ghost
        for ghost in self.gui.ghosts.ghosts_list:
            if ghost.rect.colliderect(pacman_rect):
                return True
                
        return False

    def main(self):
        clock = pygame.time.Clock()
        dt = 0

        while self.game_state.running:
            self.game_state.current_time = pygame.time.get_ticks()
            
            # Get all events once
            events = pygame.event.get()
            
            # Process quit event
            for event in events:
                if event.type == pygame.QUIT:
                    self.game_state.running = False
            
            # Process events when game has started
            if self.game_state.game_started:
                for event in events:
                    self.events.handle_events(event)
            
            # Check if game has transitioned from game over to not game over
            if self.was_game_over and not self.game_state.game_over:
                # Game has been reset from game over state
                self.gui.reset_screen_state()
                self.was_game_over = False
            
            # Update current game over state
            if self.game_state.game_over:
                self.was_game_over = True
            
            self.screen.fill((0, 0, 0))

            # Update sprites when game has started and is not over
            if self.game_state.game_started and not self.game_state.game_over:
                # Update Pacman separately
                self.gui.pacman.update(dt)
                
                # Update ghosts using the synchronized approach
                self.gui.ghosts.update_ghosts(dt)
                
                # Check collision between Pacman and ghosts
                if self.check_collision_with_ghosts():
                    self.game_state.game_over = True
            
            # Draw game screen and process events in menu
            self.gui.draw_screens(events if not self.game_state.game_started else None)
            
            pygame.display.flip()
            dt = clock.tick(self.game_state.fps) / 1000

        pygame.quit()
        sys.exit()    