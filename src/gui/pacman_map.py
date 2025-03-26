import json
import pygame
import os

from src.config import MAP_FILE, NUM_COLS, NUM_ROWS, CELL_SIZE, ASSETS_MAP, ASSETS_PATH

class PacmanMap:
    def __init__(self, screen, game_state):
        self._screen = screen
        self._game_state = game_state
        
    def get_json(self, path):
        with open(path) as f:
            payload = json.load(f)
        return payload
    
    def load_map(self):
        map_path = f"map/{MAP_FILE}"
        self.map_data = self.get_json(map_path)


    def load_assets(self):
        
        self.assets = {}

        for id, image_file in ASSETS_MAP.items():
            asset_path = os.path.join(ASSETS_PATH, image_file)
            self.assets[id] = pygame.image.load(asset_path).convert_alpha()
            self.assets[id] = pygame.transform.scale(self.assets[id], CELL_SIZE)

    def decode_id(self, id):
        # Constants for bit flags
        FLIPPED_HORIZONTALLY_FLAG = 0x80000000
        FLIPPED_VERTICALLY_FLAG = 0x40000000
        FLIPPED_DIAGONALLY_FLAG = 0x20000000
        
        # Extract flip information
        h_flip = bool(id & FLIPPED_HORIZONTALLY_FLAG)
        v_flip = bool(id & FLIPPED_VERTICALLY_FLAG)
        d_flip = bool(id & FLIPPED_DIAGONALLY_FLAG)
        
        # Get the actual tile ID (clear the flip bits)
        original_id = id & ~(FLIPPED_HORIZONTALLY_FLAG | FLIPPED_VERTICALLY_FLAG | FLIPPED_DIAGONALLY_FLAG)
        
        return original_id, h_flip, v_flip, d_flip

    def render_map(self):
        #load map
        self.load_map()
        
        #load assets
        self.load_assets()
        
        for layer in self.map_data.get('layers', []):
            x_offset = layer.get('x', 0)
            y_offset = layer.get('y', 0)
            if layer.get('type') == 'tilelayer':
                data  = layer.get('data', [])
                width = layer.get('width', 0)
                height = layer.get('height', 0)

                for y in range(height):
                    for x in range(width):
                        raw_id = data[y * width + x]
                        if raw_id > 0:
                            original_id, h_flip, v_flip, d_flip = self.decode_id(raw_id)
                            if original_id in ASSETS_MAP:
                                sprite = self.assets[original_id]
                                if h_flip or v_flip or d_flip:
                                    sprite = sprite.copy()
                                    if d_flip:
                                        sprite = pygame.transform.rotate(sprite, 90)
                                        sprite = pygame.transform.flip(sprite, False, True)
                                    sprite = pygame.transform.flip(sprite, h_flip, v_flip)
                                self._screen.blit(sprite, (x_offset + x * CELL_SIZE[0], y_offset + y * CELL_SIZE[1]))




