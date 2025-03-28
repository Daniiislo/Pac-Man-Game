import pygame
from pygame.sprite import Sprite

from src.config import PACMAN, CELL_SIZE, PACMAN_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from src.sprites.sprite_configs import PACMAN_PATHS

class Pacman(Sprite):
    def __init__(self, screen, game_state, pacman_pos):
        super().__init__()
        self.screen = screen
        self.game_state = game_state
        self.pacman_pos = pacman_pos
        self.matrix = game_state.matrix
        self.pacman_coords = self.caculate_pacman_coords()
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

    def caculate_pacman_coords(self):
        x, y = self.pacman_pos
        return x * CELL_SIZE[0], y * CELL_SIZE[1]
    
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
        #if can move to next direction, change direction
        if self.check_next_direction():
            self.move_direction = self.next_direction
            self.next_direction = ""
            self.game_state.next_direction = ""

        if self.move_direction == "":
            return

        # new position
        new_pixel_x = self.pixel_pos['x']
        new_pixel_y = self.pixel_pos['y']

        if self.move_direction == "l":
            new_pixel_x -= PACMAN_SPEED
        elif self.move_direction == "r":
            new_pixel_x += PACMAN_SPEED
        elif self.move_direction == "u":
            new_pixel_y -= PACMAN_SPEED
        elif self.move_direction == "d":
            new_pixel_y += PACMAN_SPEED

        #if new is not colliding, update position
        if not self.check_collision(new_pixel_x, new_pixel_y):
            self.pixel_pos['x'] = new_pixel_x
            self.pixel_pos['y'] = new_pixel_y

            new_x = new_pixel_x // CELL_SIZE[0]
            new_y = new_pixel_y // CELL_SIZE[1]
            
            if abs(new_x - self.pacman_pos[0]) >= 2 or abs(new_y - self.pacman_pos[1]) >= 2:
                self.pacman_pos = (new_x, new_y)
            
            # Update rect
            self.pacman_coords = (self.pixel_pos['x'], self.pixel_pos['y'])
            self.rect.topleft = self.pacman_coords
        else:
            self.move_direction = ""
            self.next_direction = ""


    def check_collision(self, pixel_x, pixel_y):
        """Check if the next position collides with walls or out of bounds."""
        top_left = (pixel_x , pixel_y)
        top_right = (pixel_x + PACMAN[0] - 1, pixel_y)
        bottom_left = (pixel_x, pixel_y + PACMAN[1] - 1)
        bottom_right = (pixel_x + PACMAN[0] - 1, pixel_y + PACMAN[1] - 1)
        
        for pos in [top_left, top_right, bottom_left, bottom_right]:
            if pos[0] < 0 or pos[1] < 0 or pos[0] >= SCREEN_WIDTH or pos[1] >= SCREEN_HEIGHT:
                return True

            if self.matrix[pos[1] // CELL_SIZE[1]][pos[0] // CELL_SIZE[0]] == 1:
                return True

        return False

    def check_next_direction(self):
        """Check if the next position can be go with the next direction."""
        if self.next_direction == "":
            return False

        new_pixel_x = self.pixel_pos['x']
        new_pixel_y = self.pixel_pos['y']
        if self.next_direction == "l":
            new_pixel_x -= PACMAN_SPEED
        elif self.next_direction == "r":
            new_pixel_x += PACMAN_SPEED
        elif self.next_direction == "u":
            new_pixel_y -= PACMAN_SPEED
        elif self.next_direction == "d":
            new_pixel_y += PACMAN_SPEED

        return not self.check_collision(new_pixel_x, new_pixel_y)

    
    def update(self, dt):
        self.update_next_direction()
        self.frame_update()
        self.move()
        self.frame_direction_update()

