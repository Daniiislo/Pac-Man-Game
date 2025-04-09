from pygame import (K_DOWN, K_LEFT, K_RIGHT, K_UP, K_ESCAPE, KEYDOWN, QUIT)

class EventHandler:
    def __init__(self, screen, game_state):
        self._screen = screen
        self._game_state = game_state

    def pygame_quit(self):
        self._game_state.running = False

    def key_bindings(self, key):
        if key == K_LEFT:
            self._game_state.next_direction = "l"
        elif key == K_RIGHT:
            self._game_state.next_direction = "r"
        elif key == K_UP:
            self._game_state.next_direction = "u"
        elif key == K_DOWN:
            self._game_state.next_direction = "d"
        elif key == K_ESCAPE and self._game_state.game_over:
            # Reset game state when ESC is pressed in game over screen
            self._game_state.reset_game()

    def handle_events(self, event):
        if event.type == QUIT:
            self.pygame_quit()

        if event.type == KEYDOWN:
            self.key_bindings(event.key)
        