from src.sprites.ghost import Blinky, Pinky, Inky, Clyde, Ghost
from src.utils.algorithm_utils import State
import pygame

class StaticGhost(Ghost):
    """Static Ghost class for initial levels where ghosts don't move"""
    def __init__(self, name, game_state):
        super().__init__(name, game_state)
        self.path = []
        
    def find_path(self, target_pos):
        return []  # No movement
        
    def move(self):
        pass  # Ghost stays still
        
    def update(self, dt):
        pass  # No updates

class LevelManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.current_level = 1
        # Position in the middle of the ghost "room", as in the reference image
        self.ghost_left_pos = (15, 19)
        self.ghost_center_pos = (17, 19)
        self.ghost_right_pos = (19, 19)
        self.ghost_move_pos = (17, 15)

    def get_ghost_classes_for_level(self, level):
        """Returns a list of ghost classes activated for the level"""
        if level == 1:
            return {
                'Blinky': StaticGhost,
                'Pinky': StaticGhost,
                'Inky': Inky,  # Blue ghost uses BFS
                'Clyde': StaticGhost
            }
        elif level == 2:
            return {
                'Blinky': StaticGhost,
                'Pinky': Pinky,  # Pink ghost uses DFS
                'Inky': StaticGhost,
                'Clyde': StaticGhost
            }
        elif level == 3:
            return {
                'Blinky': StaticGhost,
                'Pinky': StaticGhost,
                'Inky': StaticGhost,
                'Clyde': Clyde  # Orange ghost uses UCS
            }
        elif level == 4:
            return {
                'Blinky': Blinky,  # Red ghost uses A*
                'Pinky': StaticGhost,
                'Inky': StaticGhost,
                'Clyde': StaticGhost
            }
        else:  # Levels 5 and 6
            return {
                'Blinky': Blinky,
                'Pinky': Pinky,
                'Inky': Inky,
                'Clyde': Clyde
            }
            
    def get_ghost_positions_for_level(self, level, original_positions):
        """Returns ghost positions based on level"""
        positions = original_positions.copy()
        
        # Define ghost positions based on level
        # Position ghosts in the "room" like in the reference image
        if level == 1:
            # Positions for level 1 - only blue ghost (Inky) is active
            positions['Blinky'] = (self.ghost_left_pos[0], self.ghost_left_pos[1])    # Left position
            positions['Pinky'] = (self.ghost_center_pos[0], self.ghost_center_pos[1]) # Center position
            positions['Clyde'] = (self.ghost_right_pos[0], self.ghost_right_pos[1])   # Right position
            positions['Inky'] = (self.ghost_move_pos[0], self.ghost_move_pos[1])      # Moving position

        elif level == 2:
            # Positions for level 2 - only pink ghost (Pinky) is active
            positions['Blinky'] = (self.ghost_left_pos[0], self.ghost_left_pos[1])
            positions['Inky'] = (self.ghost_center_pos[0], self.ghost_center_pos[1])
            positions['Clyde'] = (self.ghost_right_pos[0], self.ghost_right_pos[1])
            positions['Pinky'] = (self.ghost_move_pos[0], self.ghost_move_pos[1])
            
        elif level == 3:
            # Positions for level 3 - only orange ghost (Clyde) is active
            positions['Blinky'] = (self.ghost_left_pos[0], self.ghost_left_pos[1])
            positions['Pinky'] = (self.ghost_center_pos[0], self.ghost_center_pos[1])
            positions['Inky'] = (self.ghost_right_pos[0], self.ghost_right_pos[1])
            positions['Clyde'] = (self.ghost_move_pos[0], self.ghost_move_pos[1])
            
        elif level == 4:
            # Positions for level 4 - only red ghost (blinky) is active
            positions['Inky'] = (self.ghost_left_pos[0], self.ghost_left_pos[1])
            positions['Pinky'] = (self.ghost_center_pos[0], self.ghost_center_pos[1])
            positions['Clyde'] = (self.ghost_right_pos[0], self.ghost_right_pos[1])
            positions['Blinky'] = (self.ghost_move_pos[0], self.ghost_move_pos[1])
        
        return positions
        
    def create_ghosts_for_level(self, level, ghost_manager, original_positions):
        """Creates ghosts based on current level"""
        ghost_classes = self.get_ghost_classes_for_level(level)
        ghost_positions = self.get_ghost_positions_for_level(level, original_positions)
        
        ghost_list = []
        
        for ghost_name, ghost_class in ghost_classes.items():
            ghost_pos = ghost_positions[ghost_name]
            ghost_list.append(ghost_class(ghost_name, self.game_state))
            
        return ghost_list 