from pygame.sprite import Sprite
from abc import ABC, abstractmethod
import pygame

from src.utils.movement_ultils import check_collision, calculate_coords
from src.sprites.sprite_configs import GHOST_PATHS
from src.config import GHOST, CELL_SIZE, GHOST_SPEED, STEP_SIZE
from src.algorithm.General import State
from src.algorithm.BFS import BFS

class Ghost(Sprite, ABC):
    def __init__(self, name, game_state, ghost_pos):
        super().__init__()
        self.name = name
        self.game_state = game_state
        self.ghost_pos = ghost_pos
        self.matrix = game_state.matrix
        self.ghost_coords = calculate_coords(self.ghost_pos)
        self.target_pos = game_state.pacman_pos
        self.pixel_pos = {
            'x': ghost_pos[0] * CELL_SIZE[0], 
            'y': ghost_pos[1] * CELL_SIZE[1]
        }
        self.load_images()
        self.algorithm = None
        self.path = []
        self.move_direction = None

    def load_images(self):
        ghost_image = GHOST_PATHS[self.name]
        self.image = pygame.transform.scale(pygame.image.load(ghost_image).convert_alpha(), GHOST)
        self.rect = self.image.get_rect(topleft=self.ghost_coords)


    @abstractmethod
    def find_path(self, target_pos):
        pass


    def move(self):
        if self.target_pos != self.game_state.pacman_pos:
            self.target_pos = self.game_state.pacman_pos
            self.path = self.find_path(self.target_pos)

        if not self.path:
            return
        
        if self.move_direction is None:
            self.move_direction = self.path[0]

        if not check_collision(self.pixel_pos['x'], self.pixel_pos['y'], self.move_direction, GHOST_SPEED, GHOST, self.matrix):
            if self.move_direction == "l":
                self.pixel_pos['x'] -= GHOST_SPEED
            elif self.move_direction == "r":
                self.pixel_pos['x'] += GHOST_SPEED
            elif self.move_direction == "u":
                self.pixel_pos['y'] -= GHOST_SPEED
            elif self.move_direction == "d":
                self.pixel_pos['y'] += GHOST_SPEED

            if self.check_changed_pos():
                self.update_ghost_pos()

                #the ghost has moved 1 step, update the path
                self.path.pop(0)
                if self.path:
                    self.move_direction = self.path[0]
                else:
                    self.move_direction = None

            self.ghost_coords = (self.pixel_pos['x'], self.pixel_pos['y'])
            self.rect.topleft = self.ghost_coords
        else:
            self.move_direction = None

        
    def check_changed_pos(self):
        if abs(self.pixel_pos['x'] - (self.ghost_pos[0] * CELL_SIZE[0])) >= GHOST[0] or abs(self.pixel_pos['y'] - (self.ghost_pos[1] * CELL_SIZE[1])) >= GHOST[1]:
            return True

    def update_ghost_pos(self):
        self.ghost_pos = (self.pixel_pos['x'] // CELL_SIZE[0], self.pixel_pos['y'] // CELL_SIZE[1])

    def update(self, dt):
        self.move()

    
class Blinky(Ghost):
    def __init__(self, name, game_state, ghost_pos):
        super().__init__(name, game_state, ghost_pos)
        self.algorithm = BFS(self.matrix)
        self.path = self.find_path(self.target_pos)
        
    def find_path(self, target_pos):
        start = State(self.ghost_pos)
        goal = target_pos
        
        return self.algorithm.solve(start, goal)

class Blinky(Ghost):
    def __init__(self, name, game_state, ghost_pos):
        super().__init__(name, game_state, ghost_pos)
        self.algorithm = BFS(self.matrix)
        self.path = self.find_path(self.target_pos)
        
    def find_path(self, target_pos):
        start = State(self.ghost_pos)
        goal = target_pos
        
        return self.algorithm.solve(start, goal)
    
class Inky(Ghost):
    def __init__(self, name, game_state, ghost_pos):
        super().__init__(name, game_state, ghost_pos)
        self.algorithm = BFS(self.matrix)
        self.path = self.find_path(self.target_pos)
        
    def find_path(self, target_pos):
        start = State(self.ghost_pos)
        goal = target_pos
        
        return self.algorithm.solve(start, goal)
    
class Clyde(Ghost):
    def __init__(self, name, game_state, ghost_pos):
        super().__init__(name, game_state, ghost_pos)
        self.algorithm = BFS(self.matrix)
        self.path = self.find_path(self.target_pos)
        
    def find_path(self, target_pos):
        start = State(self.ghost_pos)
        goal = target_pos
        
        return self.algorithm.solve(start, goal)

class GhostManager:
    def __init__(self, game_state):
        self._game_state = game_state

        self.ghosts_list = []

    def load_ghosts(self, ghost_pos_list):
        ghosts = [('blinky', Blinky), ('pinky', Blinky), ('inky', Inky), ('clyde', Clyde)]
        for ghost_name, ghost_class in ghosts:
            ghost_pos = ghost_pos_list[ghost_name]
            self.ghosts_list.append(ghost_class(ghost_name, self._game_state, ghost_pos))
        return self.ghosts_list
            


