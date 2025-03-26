from src.gui.pacman_map import PacmanMap

class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        self._screen = screen
        self._game_state = game_state
        self.all_sprites = all_sprites
        self._map = PacmanMap(self._game_state)
        self._map_surface = self._map.render_map_surface()

        self.all_sprites.add()

    def draw_screens(self):
        #draw map surface
        self._screen.blit(self._map_surface, (0, 0))
