import pygame
from pygame.sprite import Sprite

from src.config import PACMAN, CELL_SIZE, PACMAN_SPEED, STEP_SIZE
from src.sprites.sprite_configs import PACMAN_PATHS
from src.utils.movement_ultils import check_collision, calculate_coords

class Pacman(Sprite):
    def __init__(self, game_state, pacman_pos):
        super().__init__()
        self.game_state = game_state
        self.pacman_pos = pacman_pos
        self.matrix = game_state.matrix
        self.pacman_coords = calculate_coords(self.pacman_pos)
        self.load_all_frames()
        self.load_image()
        self.frame_delay = 5
        self.pixel_pos = {
            'x': self.pacman_pos[0] * CELL_SIZE[0], 
            'y': self.pacman_pos[1] * CELL_SIZE[1]
        }
        self.next_direction = self.game_state.next_direction

    def load_all_frames(self):
        def frame_helper(direction):
            return [pygame.transform.scale(pygame.image.load(path).convert_alpha(), PACMAN)
                    for path in PACMAN_PATHS[direction]]
        
        self.current_frame_idx = 0
        self.left_frames = frame_helper("left")
        self.right_frames = frame_helper("right")
        self.up_frames = frame_helper("up")
        self.down_frames = frame_helper("down")
        self.pacman = frame_helper("pacman")

        self.direction_mapper = {
            "l": self.left_frames,
            "r": self.right_frames,
            "u": self.up_frames,
            "d": self.down_frames
        }

        #Set default frames and direction
        self.frames = self.pacman
        self.move_direction = ""


    def load_image(self):
        self.image = self.frames[self.current_frame_idx]
        self.rect = self.image.get_rect(topleft=self.pacman_coords)

    
    def frame_update(self):
        self.frame_delay -= 1
        if self.frame_delay <= 0:
            self.frame_delay = 5
            self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_idx]

    def frame_direction_update(self):
        if self.move_direction != "":
            self.frames = self.direction_mapper[self.move_direction]
        else:
            self.frames = self.pacman
            self.current_frame_idx = 0

    def update_next_direction(self):
        if self.game_state.next_direction != "" and (self.next_direction == "" or self.next_direction != self.game_state.next_direction):
            self.next_direction = self.game_state.next_direction

    def move(self):
        # check if can move to next direction, change direction
        if self.next_direction != "" and not check_collision(self.pixel_pos['x'], self.pixel_pos['y'], self.next_direction, PACMAN_SPEED, PACMAN, self.matrix):
            self.move_direction = self.next_direction
            self.next_direction = ""
            self.game_state.next_direction = ""

        if self.move_direction == "":
            return
        
        # Check if can move in the current direction
        # If not, stop moving and reset the direction
        if not check_collision(self.pixel_pos['x'], self.pixel_pos['y'], self.move_direction, PACMAN_SPEED, PACMAN, self.matrix):

            if self.move_direction == "l":
                self.pixel_pos['x'] -= PACMAN_SPEED
            elif self.move_direction == "r":
                self.pixel_pos['x'] += PACMAN_SPEED
            elif self.move_direction == "u":
                self.pixel_pos['y'] -= PACMAN_SPEED
            elif self.move_direction == "d":
                self.pixel_pos['y'] += PACMAN_SPEED

            self.update_pacman_pos(self.pixel_pos['x'], self.pixel_pos['y'])

            # Update rect
            self.pacman_coords = (self.pixel_pos['x'], self.pixel_pos['y'])
            self.rect.topleft = self.pacman_coords
        else:
            self.move_direction = ""
            self.next_direction = ""
            self.game_state.next_direction = ""

    def update_pacman_pos(self, pixel_x, pixel_y):
        new_x = pixel_x // CELL_SIZE[0]
        new_y = pixel_y // CELL_SIZE[1]

        if abs(new_x - self.pacman_pos[0]) >= STEP_SIZE or abs(new_y - self.pacman_pos[1]) >= STEP_SIZE:
            self.pacman_pos = (new_x, new_y)
            self.game_state.pacman_pos = self.pacman_pos
    
    def update(self, dt):
        self.update_next_direction()
        self.frame_update()
        self.move()
        self.frame_direction_update()

