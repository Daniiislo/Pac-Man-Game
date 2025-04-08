from src.gui.pacman_map import PacmanMap
from src.sprites.pacman import Pacman
from src.sprites.Ghost import GhostManager
class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        self._screen = screen
        self._game_state = game_state
        self.all_sprites = all_sprites

        self._map = PacmanMap(self._game_state)
        self._map_surface = self._map.render_map_surface()

        self.pacman = Pacman(self._game_state, self._game_state.pacman_pos)

        self.ghosts = GhostManager(self._game_state)
        self.ghosts.load_ghosts()

        self.all_sprites.add(self.pacman)
        for ghost in self.ghosts.ghosts_list:
            self.all_sprites.add(ghost)

    def draw_screens(self):
        #draw map surface
        self._screen.blit(self._map_surface, (0, 0))
