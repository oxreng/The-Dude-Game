import os
import pygame

"""
Загрузка и отображение картинки
"""


def load_image(path, file_name, color_key=None):
    fullname = os.path.join(path, file_name)
    image = pygame.image.load(fullname)

    if color_key == -1:
        color_key = image.get_at((0, 0))

    image.set_colorkey(color_key)
    return image
