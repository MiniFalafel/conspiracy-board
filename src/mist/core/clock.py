import pygame

class Clock:

    # Static value. will be updated by the Application base class during the game loop
    __frame_dt = 0.0

    @staticmethod
    def delta_time():
        return Clock.__frame_dt

    @staticmethod
    def update(dt: float):
        """
        ONLY FOR USE BY THE "Application" BASE CLASS
        :return:
        """
        Clock.__frame_dt = pygame
