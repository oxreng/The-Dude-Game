import pygame

"""Объекты, с которыми можно взаимодействовать"""


class InteractionObject:
    def __init__(self, rect, name, type):
        self.rect = rect
        self.name = name
        self.type = type


class DoorObject(InteractionObject):
    def __init__(self, rect, name, type, where, destination_x, destination_y):
        super().__init__(rect, name, type)
        self.where = where
        self.destination_x = destination_x
        self.destination_y = destination_y


collide_areas = {'level_1': [
    DoorObject(pygame.Rect((330, -140,), (80, 140)), 'door', 'change_level', 'level_2', 550, 10),
    InteractionObject(pygame.Rect((50, -60), (100, 100)), 'oven', 'switch_animation'),
    InteractionObject(pygame.Rect((720, -150), (60, 200)), 'wardrobe', 'change_outfit')],
    'level_2': [DoorObject(pygame.Rect((510, -140,), (80, 140)), 'door', 'change_level', 'level_1', 370, 10),
                DoorObject(pygame.Rect((1800, 720,), (80, 180)), 'door', 'minigame', 'level_3', 370, 10),
                InteractionObject(pygame.Rect((1338, -45), (200, 100)), 'healer', 'heal')],
    'level_3': [DoorObject(pygame.Rect((0, -100,), (200, 200)), 'ladder', 'change_level', 'level_2', 1740, 780),
                InteractionObject(pygame.Rect((790, -80), (400, 400)), 'spawn_interaction', 'spawn_enemy'),
                InteractionObject(pygame.Rect((990, -120), (220, 140)), 'end_button', 'end_event')]}
