from pygame.sprite import Sprite
from abc import ABC, abstractmethod
import pygame

from src.utils.movement_ultils import check_collision, calculate_coords, update_matrix, copy_matrix
from src.sprites.sprite_configs import GHOST_PATHS
from src.config import GHOST, CELL_SIZE, GHOST_SPEED, STEP_SIZE
from src.utils.algorithm_utils import State
from src.algorithm.BFS import BFS
from src.algorithm.DFS import DFS
from src.algorithm.AStar import AStar
from src.algorithm.UCS import UniformCostSearch

class Ghost(Sprite, ABC):
    def __init__(self, name, game_state):
        super().__init__()
        self.name = name
        self.game_state = game_state
        self.ghost_pos = self.game_state.ghosts_pos_list[name]
        self.matrix = game_state.matrix
        self.ghost_coords = calculate_coords(self.ghost_pos)
        self.target_pos = game_state.pacman_pos
        self.pixel_pos = {
            'x': self.ghost_pos[0] * CELL_SIZE[0], 
            'y': self.ghost_pos[1] * CELL_SIZE[1]
        }
        self.load_images()
        self.path = []
        self.move_direction = None
        self.next_pos = None
        self.previous_pos = None


    def load_images(self):
        ghost_image = GHOST_PATHS[self.name]
        self.image = pygame.transform.scale(pygame.image.load(ghost_image).convert_alpha(), GHOST)
        self.rect = self.image.get_rect(topleft=self.ghost_coords)
    
    @abstractmethod
    def find_path(self, target_pos, matrix=None, previous_pos=None):
        pass

    def get_next_pos(self, direction):
        if direction == "l":
            return (self.ghost_pos[0] - STEP_SIZE, self.ghost_pos[1])
        elif direction == "r":
            return (self.ghost_pos[0] + STEP_SIZE, self.ghost_pos[1])
        elif direction == "u":
            return (self.ghost_pos[0], self.ghost_pos[1] - STEP_SIZE)
        elif direction == "d":
            return (self.ghost_pos[0], self.ghost_pos[1] + STEP_SIZE)
        return None
    
    def has_reached_next_pos(self):
        if self.next_pos is None:
            return False
        if self.pixel_pos['x'] == self.next_pos[0] * CELL_SIZE[0] and self.pixel_pos['y'] == self.next_pos[1] * CELL_SIZE[1]:
            return True
        return False

    def plan_movement(self):
        if not self.path:
            self.target_pos = self.game_state.pacman_pos
            self.path = self.find_path(self.target_pos, previous_pos=self.previous_pos)

        if self.path:
            self.move_direction = self.path[0]
            self.next_pos = self.get_next_pos(self.move_direction)
        else:
            self.next_pos = None
            self.move_direction = None

    def execute_movement(self):
        if not self.move_direction or not self.next_pos:
            return

        new_pixel_x = self.pixel_pos['x']
        new_pixel_y = self.pixel_pos['y']
        
        if self.move_direction == "l":
            new_pixel_x -= GHOST_SPEED
        elif self.move_direction == "r":
            new_pixel_x += GHOST_SPEED
        elif self.move_direction == "u":
            new_pixel_y -= GHOST_SPEED
        elif self.move_direction == "d":
            new_pixel_y += GHOST_SPEED


        if (not check_collision(self.pixel_pos['x'], self.pixel_pos['y'], self.move_direction, GHOST_SPEED, GHOST, self.matrix)):
            
            self.pixel_pos['x'] = new_pixel_x
            self.pixel_pos['y'] = new_pixel_y
            
            if self.has_reached_next_pos():
                update_matrix(self.matrix, self.ghost_pos, False, 2)
                self.previous_pos = self.ghost_pos
                self.ghost_pos = self.next_pos
                self.game_state.ghosts_pos_list[self.name] = self.ghost_pos
                update_matrix(self.matrix, self.ghost_pos, True, 2)

                if self.path:
                    self.path.pop(0)

                #check is the target_pos changed
                if self.target_pos != self.game_state.pacman_pos:
                    self.target_pos = self.game_state.pacman_pos
                    # find new path
                    self.path = self.find_path(self.target_pos, previous_pos=self.previous_pos)

                if self.path:
                    self.move_direction = self.path[0]
                    self.next_pos = self.get_next_pos(self.move_direction)
                else:
                    self.move_direction = None
                    self.next_pos = None
            
            self.ghost_coords = (self.pixel_pos['x'], self.pixel_pos['y'])
            self.rect.topleft = self.ghost_coords

        else:
            print("collision")
        
    def update(self, dt):
        self.execute_movement()

class Blinky(Ghost):
    def __init__(self, name, game_state):
        super().__init__(name, game_state)
        self.algorithm = AStar(self.matrix, self.game_state)
        self.path = self.find_path(self.target_pos)
        
    def find_path(self, target_pos, matrix=None, previous_pos=None):
        # Create a fresh instance of the algorithm with the current matrix
        if matrix is None:
            matrix = self.matrix

        algorithm = AStar(matrix, self.game_state)  # Use self.game_state
        
        start = State(self.ghost_pos)
        goal = target_pos
        
        return algorithm.solve(start, goal)

class Pinky(Ghost):
    def __init__(self, name, game_state):
        super().__init__(name, game_state)
        self.algorithm = DFS(self.matrix, self.game_state)
        self.path = self.find_path(self.target_pos)
        
    def find_path(self, target_pos, matrix=None, previous_pos=None):
        # Create a fresh instance of the algorithm with the current matrix
        if matrix is None:
            matrix = self.matrix

        algorithm = DFS(matrix, self.game_state)  # Use self.game_state
        
        start = State(self.ghost_pos)
        goal = target_pos
        path = algorithm.solve(start, goal, previous_pos)
        if path is None or len(path) == 0:
            return []
        return path

class Inky(Ghost):
    def __init__(self, name, game_state):
        super().__init__(name, game_state)
        self.algorithm = BFS(self.matrix, self.game_state)
        self.path = self.find_path(self.target_pos)
        
    def find_path(self, target_pos, matrix=None, previous_pos=None):
        # Create a fresh instance of the algorithm with the current matrix
        if matrix is None:
            matrix = self.matrix

        algorithm = BFS(matrix, self.game_state)  # Use self.game_state
        
        start = State(self.ghost_pos)
        goal = target_pos
        
        return algorithm.solve(start, goal)
    
class Clyde(Ghost):
    def __init__(self, name, game_state):
        super().__init__(name, game_state)
        self.algorithm = UniformCostSearch(self.matrix, self.game_state)
        self.path = self.find_path(self.target_pos)
        
    def find_path(self, target_pos, matrix=None, previous_pos=None):
        # Create a fresh instance of the algorithm with the current matrix
        if matrix is None:
            matrix = self.matrix

        algorithm = UniformCostSearch(matrix, self.game_state)  # Use self.game_state
        
        start = State(self.ghost_pos)
        goal = target_pos

        return algorithm.solve(start, goal)

class GhostManager:
    def __init__(self, game_state):
        self._game_state = game_state
        self.ghosts_list = []
    
    def plan_all_movements(self):
        """First phase: All ghosts plan their movements simultaneously"""
        for ghost in self.ghosts_list:
            ghost.plan_movement()
            
    def resolve_collisions(self):
        """Detect and resolve potential collisions between ghosts"""
        # Create a temporary matrix and mark the positions of all ghosts
        temp_matrix = copy_matrix(self._game_state.matrix)
        ghost_positions = {}
        
        # Mark the current positions of all ghosts (2x2 area)
        for ghost in self.ghosts_list:
            main_pos = ghost.ghost_pos
            update_matrix(temp_matrix, main_pos, True, 2)
            ghost_positions[main_pos] = ghost

        
        # Process each ghost
        for ghost in self.ghosts_list:
            if not ghost.next_pos:
                continue
                
            # Check for collision with the current position of other ghost
            collision_detected = False
            for other_ghost in self.ghosts_list:
                if other_ghost != ghost:
                    # Check if the 2x2 area of next_pos overlaps with the 2x2 area of other ghost
                    if (abs(ghost.next_pos[0] - other_ghost.ghost_pos[0]) < 2 and 
                        abs(ghost.next_pos[1] - other_ghost.ghost_pos[1]) < 2):
                        collision_detected = True
                        break
            
            if collision_detected:
                # Find a new path with the marked matrix
                ghost.path = ghost.find_path(ghost.target_pos, temp_matrix)
                if ghost.path:
                    ghost.move_direction = ghost.path[0]
                    ghost.next_pos = ghost.get_next_pos(ghost.move_direction)
                else:
                    ghost.move_direction = None
                    ghost.next_pos = None
                    continue
            
            # Check for collision with next_pos of other ghost
            next_pos_collision = False
            for other_ghost in self.ghosts_list:
                if other_ghost != ghost and other_ghost.next_pos:
                    if (abs(ghost.next_pos[0] - other_ghost.next_pos[0]) < 2 and 
                        abs(ghost.next_pos[1] - other_ghost.next_pos[1]) < 2):
                        # Add the disputed position to the matrix
                        update_matrix(temp_matrix, ghost.next_pos, True, 2)
                        next_pos_collision = True
                        break
            
            if next_pos_collision:

                # Find new path with the marked matrix
                ghost.path = ghost.find_path(ghost.target_pos, temp_matrix)

                # Remove the disputed position from the matrix to avoid affecting the pathfinding of other ghosts
                update_matrix(temp_matrix, ghost.next_pos, False, 2)

                if ghost.path:
                    ghost.move_direction = ghost.path[0]
                    ghost.next_pos = ghost.get_next_pos(ghost.move_direction)
                else:
                    ghost.move_direction = None
                    ghost.next_pos = None

    def update_ghosts(self, dt):
        """Main update method called from the game loop"""
        # Phase 1: All ghosts plan their movements
        self.plan_all_movements()
        
        # Phase 2: Resolve potential collisions
        self.resolve_collisions()
        
        # Phase 3: Execute movements (this happens in sprite.update())
        for ghost in self.ghosts_list:
            ghost.update(dt)


    def set_original_positions(self):
        """Save the initial positions of the ghosts"""
        self.original_pos = self._game_state.ghosts_pos_list

    def reset_ghosts(self, ghost_list):
        """Remove all old ghosts and replace them with the new list of ghosts"""
        self.ghosts_list = ghost_list
        return self.ghosts_list
