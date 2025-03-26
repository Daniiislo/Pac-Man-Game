from src.gui.pacman_map import PacmanMap

class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        self._screen = screen
        self._game_state = game_state
        self.all_sprites = all_sprites
        
        self.map = PacmanMap(self._screen, self._game_state)

    def draw_screens(self):
        self.map.render_map()
