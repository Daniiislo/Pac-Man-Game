from src.config import *
from src.config import FPS

class GameState:
    def __init__(self):
        self.__fps = FPS
        self.__running = True
        self.__current_time = None
        self.__matrix = None
        self.__current_direction = ""
        self.__next_direction = ""
        self.__pacman_pos = None
        self.__current_level = 1
        self.__game_started = False
        self.__show_ready = False
        self.__ready_start_time = 0
        self.__ghosts_pos_list = None
        self.__all_ghosts = None  # Reference to all ghost instances
        self.__game_over = False  # Game over state

    @property
    def fps(self):
        return self.__fps
    
    @fps.setter
    def fps(self, fps):
        self.__fps = fps

    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self, running):
        self.__running = running

    @property
    def current_time(self):
        return self.__current_time
    
    @current_time.setter
    def current_time(self, current_time):
        self.__current_time = current_time

    @property
    def matrix(self):
        return self.__matrix
    
    @matrix.setter
    def matrix(self, matrix):
        self.__matrix = matrix

    @property
    def current_direction(self):
        return self.__current_direction
    
    @current_direction.setter
    def direction(self, direction):
        self.__current_direction = direction

    @property
    def next_direction(self):
        return self.__next_direction
    
    @next_direction.setter
    def next_direction(self, next_direction):
        self.__next_direction = next_direction

    @property
    def pacman_pos(self):
        return self.__pacman_pos
    
    @pacman_pos.setter
    def pacman_pos(self, pacman_pos):
        self.__pacman_pos = pacman_pos

    @property
    def ghosts_pos_list(self):
        return self.__ghosts_pos_list
    
    @ghosts_pos_list.setter
    def ghosts_pos_list(self, ghosts_pos_list):
        self.__ghosts_pos_list = ghosts_pos_list
        
    def get_all_ghosts(self):
        """Get a list of all ghost instances"""
        return self.__all_ghosts or []
    
    def set_all_ghosts(self, ghosts):
        """Set the list of all ghost instances"""
        self.__all_ghosts = ghosts
        
    @property
    def current_level(self):
        return self.__current_level
    
    @current_level.setter
    def current_level(self, level):
        self.__current_level = level
        
    @property
    def game_started(self):
        return self.__game_started
    
    @game_started.setter
    def game_started(self, started):
        self.__game_started = started
        
    @property
    def show_ready(self):
        return self.__show_ready
    
    @show_ready.setter
    def show_ready(self, show):
        self.__show_ready = show
        
    @property
    def ready_start_time(self):
        return self.__ready_start_time
    
    @ready_start_time.setter
    def ready_start_time(self, time):
        self.__ready_start_time = time
        
    @property
    def game_over(self):
        return self.__game_over
    
    @game_over.setter
    def game_over(self, game_over):
        self.__game_over = game_over
        
    def reset_game(self):
        """Reset game state"""
        # Reset all states to initial values
        self.__current_direction = ""
        self.__next_direction = ""
        self.__current_level = 1
        self.__game_started = False
        self.__show_ready = False
        self.__ready_start_time = 0
        self.__game_over = False
        
        # Other states will be reset when loading map and ghosts