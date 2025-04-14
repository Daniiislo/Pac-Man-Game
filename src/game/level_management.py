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
            
    def load_positions_for_level(self, level):
        """Load pacman and ghosts positions for the level from JSON file, then update game state"""
        positions_path = f"map/test_case_{level}.json"
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