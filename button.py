import pygame
from config import *


class Button(pygame.sprite.Sprite):  # Создание кнопок
    def __init__(self, group, x, y, text, image_default, hover_image=None, image_down=None):
        super().__init__(group)
        self.text = text
        self.image = image_default

        # Картинка, если кнопка зажата
        self.hover_image = self.image
        if hover_image:
            self.hover_image = hover_image

        self.btn_down = self.image
        if image_down:
            self.btn_down = image_down
        self.rect = self.image.get_rect(topleft=(x, y))

        # Наведена ли мышка на кнопку
        self.is_hovered = False

        self.is_down = False

    def draw(self, screen):
        if self.is_down:
            current_image = self.btn_down
        elif self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)
        font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_event(self, mouse_pos, event):  # Наведена ли мышка на кнопку
        if not self.is_down:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and event.type == pygame.MOUSEBUTTONDOWN:
            self.is_down = True
        elif event.type == pygame.MOUSEBUTTONUP and self.is_down:
            self.is_down = False
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            if self.is_hovered:
                return True
        return False
