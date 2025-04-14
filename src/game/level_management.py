from src.sprites.ghost import Blinky, Pinky, Inky, Clyde
import pygame
from src.utils.movement_ultils import update_matrix

class LevelManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.current_level = 1
        # Center position for ghost
        self.ghost_center_pos = (17, 19)
        # Ghost positions in the original map (just one ghost is active in level 1-4)
        self.all_ghost_positions = {
            'Blinky': None,
            'Pinky': None,
            'Inky': None,
            'Clyde': None
        }

    def get_ghost_classes_for_level(self, level):
        # Each level has only one ghost active
        if level == 1:
            return {
                'Inky': Inky  # BFS
            }
        elif level == 2:
            return {
                'Pinky': Pinky  # DFS
            }
        elif level == 3:
            return {
                'Clyde': Clyde  # UCS
            }
        elif level == 4:
            return {
                'Blinky': Blinky  # A*
            }
        else:  # Levels 5 + 6
            return {
                'Blinky': Blinky,
                'Pinky': Pinky,
                'Inky': Inky,
                'Clyde': Clyde
            }
            
    def get_ghost_positions_for_level(self, level, original_positions):
        positions = original_positions.copy()
        
        # Set ghost positions in the original map
        for ghost_name, pos in positions.items():
            self.all_ghost_positions[ghost_name] = pos
        
        # Set ghost positions in the middle of the "ghost room"
        if level == 1:
            # Level 1 - only Inky active
            positions['Inky'] = self.ghost_center_pos
            
        elif level == 2:
            # Level 2 - only Pinky active
            positions['Pinky'] = self.ghost_center_pos
            
        elif level == 3:
            # Level 3 - only Clyde active
            positions['Clyde'] = self.ghost_center_pos
            
        elif level == 4:
            # Level 4 - only Blinky active
            positions['Blinky'] = self.ghost_center_pos
        
        return positions
        
    def create_ghosts_for_level(self, level, ghost_manager, original_positions):
        ghost_classes = self.get_ghost_classes_for_level(level)
        ghost_positions = self.get_ghost_positions_for_level(level, original_positions)
        
        # Remove all ghosts from the matrix
        for ghost_name, pos in self.all_ghost_positions.items():
            if pos and ghost_name not in ghost_classes:
                update_matrix(self.game_state.matrix, pos, False, 2)
        
        ghost_list = []
        
        for ghost_name, ghost_class in ghost_classes.items():
            ghost_pos = ghost_positions[ghost_name]
            ghost_list.append(ghost_class(ghost_name, self.game_state))
            
        return ghost_list 