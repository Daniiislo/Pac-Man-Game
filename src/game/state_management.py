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