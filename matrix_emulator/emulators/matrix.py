import pygame

class RGBMatrix:
    __PIXEL_SIZE = 4

    def __init__(self, options = {}):
        self.options = options
        self.size = (self.options.cols * self.__PIXEL_SIZE, self.options.rows * self.__PIXEL_SIZE)
        
        self.__load_emulator_window()

    def __load_emulator_window(self):
        pygame.display.set_mode(self.size)
        pygame.init()