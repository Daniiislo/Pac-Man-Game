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

    def main(self):
        clock = pygame.time.Clock()
        dt = 0

        while self.game_state.running:
            self.game_state.current_time = pygame.time.get_ticks()

            # Xử lý sự kiện khi đã bắt đầu game
            if self.game_state.game_started:
                for event in pygame.event.get():
                    self.events.handle_events(event)
            
            self.screen.fill((0, 0, 0))
            self.gui.draw_screens()

            # Cập nhật các sprite khi game đã bắt đầu
            if self.game_state.game_started:
                # Update Pacman separately
                self.gui.pacman.update(dt)
                
                # Update ghosts using the synchronized approach
                self.gui.ghosts.update_ghosts(dt)
                
                # Draw all sprites
                self.all_sprites.draw(self.screen)
            
            pygame.display.flip()
            dt = clock.tick(self.game_state.fps) / 1000

        pygame.quit()
        sys.exit()    