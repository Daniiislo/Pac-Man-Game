from src.sprites.ghost import Blinky, Pinky, Inky, Clyde
import pygame
from src.utils.movement_ultils import update_matrix
from src.utils.map_utils import get_json

class LevelManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.current_level = 1
        # Ghost positions in the original map
        self.all_ghost_positions = {
            'Blinky': None,
            'Pinky': None,
            'Inky': None,
            'Clyde': None
        }
        # Load real game positions
        self.real_game_positions = self.load_real_game_positions()

    def load_real_game_positions(self):
        """Load positions from real_game_position.json"""
        real_game_path = "map/real_game_position.json"
        return get_json(real_game_path)

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
        
        if level in [1, 2, 3, 4]:
            # Levels 1-4 - use positions from test case
            # Only keep the active ghost's position
            active_ghost = list(self.get_ghost_classes_for_level(level).keys())[0]
            for ghost_name in positions:
                if ghost_name != active_ghost:
                    positions[ghost_name] = None
        
        elif level in [5, 6]:
            # Levels 5 and 6 - use real game positions
            # Reset all positions first
            positions = {
                'Blinky': None,
                'Pinky': None,
                'Inky': None,
                'Clyde': None
            }
            
            # Set positions from real_game_position.json
            for ghost_name in positions:
                ghost_data = self.real_game_positions['ghosts'].get(ghost_name)
                if ghost_data:
                    positions[ghost_name] = (
                        ghost_data['start_x'],
                        ghost_data['start_y']
                    )
            
            # Update Pacman's position from JSON
            pacman_data = self.real_game_positions.get('pacman')
            if pacman_data:
                self.game_state.pacman_pos = (
                    pacman_data['start_x'],
                    pacman_data['start_y']
                )
        
        # Update all_ghost_positions
        for ghost_name, pos in positions.items():
            self.all_ghost_positions[ghost_name] = pos
        
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
            if ghost_pos:  # Only create ghost if position is not None
                ghost_list.append(ghost_class(ghost_name, self.game_state))
            
        return ghost_list 