import pygame


class InteractionObject:
    def __init__(self, rect, name, type):
        self.rect = rect
        self.name = name
        self.type = type


class DoorObject(InteractionObject):
    def __init__(self, rect, name, type, where):
        super().__init__(rect, name, type)
        self.where = where


collide_areas = {'level_1': [
    DoorObject(pygame.Rect((320, -140,), (80, 140)), 'door', 'change_level', 'level_2'),
    InteractionObject(pygame.Rect((40, -60), (100, 100)), 'oven', 'switch_animation'),
    InteractionObject(pygame.Rect((720, -150), (60, 200)), 'wardrobe', 'change_outfit')],
    'level_2': [DoorObject(pygame.Rect((320, -140,), (80, 140)), 'door', 'change_level', 'level_1')]}
