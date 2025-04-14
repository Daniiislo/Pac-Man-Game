import json
import pygame
import os

from src.utils.map_utils import decode_tile_id, transform_asset, decode_map_data_to_original_id, get_json
from src.utils.movement_ultils import update_matrix

from src.config import MAP_FILE, CELL_SIZE, ASSETS_MAP, ASSETS_PATH, TESTCASE

class PacmanMap:
    def __init__(self, game_state):
        self._game_state = game_state
        self.map_data = self.load_map_data()
        self.test_case_data = self.load_test_case_data()
        self.assets = self.load_assets()
        self._game_state.matrix = decode_map_data_to_original_id(self.map_data)
        self._game_state.ghosts_pos_list = self.load_ghosts_pos()
        self._game_state.pacman_pos = self.load_pacman_pos()
        self.update_matrix()

    
    def load_map_data(self):
        map_path = f"map/{MAP_FILE}"
        map_data = get_json(map_path)
        return map_data

    def load_test_case_data(self):
        test_case_path = f"map/{TESTCASE}.json"
        test_case_data = get_json(test_case_path)
        return test_case_data

    def load_assets(self):
        assets = {}

        for id, image_file in ASSETS_MAP.items():
            asset_path = os.path.join(ASSETS_PATH, "map/", image_file)
            assets[id] = pygame.image.load(asset_path).convert_alpha()
            assets[id] = pygame.transform.scale(assets[id], CELL_SIZE)
        return assets   

    def load_pacman_pos(self):
        pacman_data = self.test_case_data.get('pacman', {})
        x = pacman_data.get('start_x', 1)
        y = pacman_data.get('start_y', 1)
        return (x, y)

    def load_ghosts_pos(self):
        ghosts = {}
        for ghost_name, ghost_data in self.test_case_data.get('ghosts', {}).items():
            x = ghost_data.get('start_x', 1)
            y = ghost_data.get('start_y', 1)
            ghosts[ghost_name] = (x, y)
        return ghosts

    def update_matrix(self):
        """Update game_state.matrix with the ghosts positions."""
        for ghost_name, ghost_pos in self._game_state.ghosts_pos_list.items():
            update_matrix(self._game_state.matrix, ghost_pos, True, 2)

    def render_map_surface(self):
        for layer in self.map_data.get('layers', []):
            x_offset = layer.get('x', 0)
            y_offset = layer.get('y', 0)
            if layer.get('type') == 'tilelayer':
                data = layer.get('data', [])
                width = layer.get('width', 0)
                height = layer.get('height', 0)

                map_surface = pygame.Surface((width * CELL_SIZE[0], height * CELL_SIZE[1]))

                for y in range(height):
                    for x in range(width):
                        raw_id = data[y * width + x]
                        if raw_id > 0:
                            original_id, h_flip, v_flip, d_flip = decode_tile_id(raw_id)
                            if original_id in ASSETS_MAP:
                                asset = self.assets[original_id]
                                asset = transform_asset(asset, h_flip, v_flip, d_flip)
                                map_surface.blit(asset, (x_offset + x * CELL_SIZE[0], y_offset + y * CELL_SIZE[1]))
                return map_surface