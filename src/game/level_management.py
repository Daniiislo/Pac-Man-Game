from src.sprites.Ghost import Blinky, Pinky, Inky, Clyde, Ghost
from src.utils.algorithm_utils import State
import pygame

class StaticGhost(Ghost):
    """Static Ghost class for initial levels where ghosts don't move"""
    def __init__(self, name, game_state, ghost_pos):
        super().__init__(name, game_state, ghost_pos)
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
                'blinky': StaticGhost,
                'pinky': StaticGhost,
                'inky': Inky,  # Blue ghost uses BFS
                'clyde': StaticGhost
            }
        elif level == 2:
            return {
                'blinky': StaticGhost,
                'pinky': Pinky,  # Pink ghost uses DFS
                'inky': StaticGhost,
                'clyde': StaticGhost
            }
        elif level == 3:
            return {
                'blinky': StaticGhost,
                'pinky': StaticGhost,
                'inky': StaticGhost,
                'clyde': Clyde  # Orange ghost uses UCS
            }
        elif level == 4:
            return {
                'blinky': Blinky,  # Red ghost uses A*
                'pinky': StaticGhost,
                'inky': StaticGhost,
                'clyde': StaticGhost
            }
        else:  # Levels 5 and 6
            return {
                'blinky': Blinky,
                'pinky': Pinky,
                'inky': Inky,
                'clyde': Clyde
            }
            
    def get_ghost_positions_for_level(self, level, original_positions):
        """Returns ghost positions based on level"""
        positions = original_positions.copy()
        
        # Define ghost positions based on level
        # Position ghosts in the "room" like in the reference image
        if level == 1:
            # Positions for level 1 - only blue ghost (inky) is active
            positions['blinky'] = (self.ghost_left_pos[0], self.ghost_left_pos[1])    # Left position
            positions['pinky'] = (self.ghost_center_pos[0], self.ghost_center_pos[1]) # Center position
            positions['clyde'] = (self.ghost_right_pos[0], self.ghost_right_pos[1])   # Right position
            positions['inky'] = (self.ghost_move_pos[0], self.ghost_move_pos[1])      # Moving position

        elif level == 2:
            # Positions for level 2 - only pink ghost (pinky) is active
            positions['blinky'] = (self.ghost_left_pos[0], self.ghost_left_pos[1])
            positions['inky'] = (self.ghost_center_pos[0], self.ghost_center_pos[1])
            positions['clyde'] = (self.ghost_right_pos[0], self.ghost_right_pos[1])
            positions['pinky'] = (self.ghost_move_pos[0], self.ghost_move_pos[1])
            
        elif level == 3:
            # Positions for level 3 - only orange ghost (clyde) is active
            positions['blinky'] = (self.ghost_left_pos[0], self.ghost_left_pos[1])
            positions['pinky'] = (self.ghost_center_pos[0], self.ghost_center_pos[1])
            positions['inky'] = (self.ghost_right_pos[0], self.ghost_right_pos[1])
            positions['clyde'] = (self.ghost_move_pos[0], self.ghost_move_pos[1])
            
        elif level == 4:
            # Positions for level 4 - only red ghost (blinky) is active
            positions['inky'] = (self.ghost_left_pos[0], self.ghost_left_pos[1])
            positions['pinky'] = (self.ghost_center_pos[0], self.ghost_center_pos[1])
            positions['clyde'] = (self.ghost_right_pos[0], self.ghost_right_pos[1])
            positions['blinky'] = (self.ghost_move_pos[0], self.ghost_move_pos[1])
        
        return positions
        
    def create_ghosts_for_level(self, level, ghost_manager, original_positions):
        """Creates ghosts based on current level"""
        ghost_classes = self.get_ghost_classes_for_level(level)
        ghost_positions = self.get_ghost_positions_for_level(level, original_positions)
        
        ghost_list = []
        
        for ghost_name, ghost_class in ghost_classes.items():
            ghost_pos = ghost_positions[ghost_name]
            ghost_list.append(ghost_class(ghost_name, self.game_state, ghost_pos))
            
        return ghost_list 