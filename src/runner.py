import sys

import pygame
import json

from src.config import *
from src.game.state_management import GameState
from src.game.event_management import EventHandler
from src.gui.screen_management import ScreenManager

from src.algorithm.BFS import BFS
from src.algorithm.General import *
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
        dt = None

        while self.game_state.running:
            self.game_state.current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                self.events.handle_events(event)

            self.screen.fill((0, 0, 0))
            self.gui.draw_screens()

            self.all_sprites.draw(self.screen)
            self.all_sprites.update(dt)
            pygame.display.flip()
            dt = clock.tick(self.game_state.fps)
            dt /= 1000

        pygame.quit()
        sys.exit()
        

        #write matrix to txt file
        with open("matrix.txt", "w") as file:
            for row in self.game_state.matrix:
                for cell in row:
                    file.write(str(cell) + "\t")
                file.write("\n")


        bfs = BFS(self.game_state.matrix)

        startState = State((15, 11))
        print(bfs.solve(startState, (39, 33)))

        
        