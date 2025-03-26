from src.config import *
from src.config import FPS

class GameState:
    def __init__(self):
        self.__fps = FPS
        self.__running = True
        self.__current_time = None
        self.__matrix = None

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