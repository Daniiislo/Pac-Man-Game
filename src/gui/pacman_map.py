import json
import pygame
import os

from src.utils.map_utils import decode_tile_id, transform_asset, decode_map_data_to_original_id, get_json

from src.config import MAP_FILE, CELL_SIZE, ASSETS_MAP, ASSETS_PATH, TESTCASE

class PacmanMap:
    def __init__(self, game_state):
        self._game_state = game_state
        self.map_data = self.load_map_data()
        self.assets = self.load_assets()
        self.original_matrix = decode_map_data_to_original_id(self.map_data)
    
    def load_map_data(self):
        map_path = f"map/{MAP_FILE}"
        map_data = get_json(map_path)
        return map_data


    def load_assets(self):
        assets = {}

        for id, image_file in ASSETS_MAP.items():
            asset_path = os.path.join(ASSETS_PATH, "map/", image_file)
            assets[id] = pygame.image.load(asset_path).convert_alpha()
            assets[id] = pygame.transform.scale(assets[id], CELL_SIZE)
        return assets   

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