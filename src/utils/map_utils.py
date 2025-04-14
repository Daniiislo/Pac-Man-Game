import pygame
from src.config import ASSETS_MAP
import json

def get_json(path):
    with open(path) as f:
        payload = json.load(f)
    return payload

def decode_tile_id(id):
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

def transform_asset(asset, h_flip, v_flip, d_flip):
    if h_flip or v_flip or d_flip:
        asset = asset.copy()
        if d_flip:
            asset = pygame.transform.rotate(asset, 90)
            asset = pygame.transform.flip(asset, False, True)
        asset = pygame.transform.flip(asset, h_flip, v_flip)
    return asset

def decode_map_data_to_original_id(map_data):
    layer = map_data.get('layers', [])[0]
    map = []
    if layer.get('type') == 'tilelayer':
        data  = layer.get('data', [])
        width = layer.get('width', 0)
        height = layer.get('height', 0)

        for y in range(height):
            row = []
            for x in range(width):
                raw_id = data[y * width + x]
                if raw_id > 0:
                    original_id, h_flip, v_flip, d_flip = decode_tile_id(raw_id)
                    # if this is a space, we want to set it to False, otherwise set to True
                    if original_id in ASSETS_MAP and ASSETS_MAP[original_id] == 'space.png':
                        row.append(False)
                    else:
                        row.append(True)
            map.append(row)
    return map
