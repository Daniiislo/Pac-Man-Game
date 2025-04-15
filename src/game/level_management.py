from src.sprites.ghost import Blinky, Pinky, Inky, Clyde
import pygame
from src.utils.movement_ultils import update_matrix
from src.utils.map_utils import get_json

class LevelManager:
    def __init__(self, game_state):
        self.game_state = game_state
        
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
            
    def load_positions_for_level(self, level, test_case=1):
        """
        Load pacman and ghosts positions from a JSON file, then update game state
        
        Args:
            level: The game level
            test_case: The test case number (1-5). If None, default is 1
        """
        # If test_case is not specified, use the level number
        if test_case is None:
            test_case = level
            
        positions_path = f"map/test_case_{test_case}.json"
        positions_data = get_json(positions_path)

        ghosts_pos = {}
        for ghost_name, ghost_data in positions_data.get('ghosts', {}).items():
            x = ghost_data.get('start_x', 1)
            y = ghost_data.get('start_y', 1)
            ghosts_pos[ghost_name] = (x, y)
        
        self.game_state.ghosts_pos_list = ghosts_pos

        self.game_state.pacman_pos = (
            positions_data.get('pacman', {}).get('start_x', 1),
            positions_data.get('pacman', {}).get('start_y', 1)
        )