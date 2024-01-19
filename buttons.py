import pygame
from config import *
from sound import SpritesSound


class Button(pygame.sprite.Sprite):  # Создание кнопок
    def __init__(self, group, pos, text, image_default, hover_image=None, image_down=None):
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
        self.rect = self.image.get_rect(topleft=pos)

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
            SpritesSound.button_sound(2)
        elif event.type == pygame.MOUSEBUTTONUP and self.is_down:
            self.is_down = False
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            if self.is_hovered:
                return True
        return False


class Slider(pygame.sprite.Sprite):  # Создание слайдера
    def __init__(self, group, pos, size, initial_value, min_value, max_value):
        super().__init__(group)
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0]
        self.slider_right_pos = self.pos[0] + size[0]
        self.slider_top_pos = self.pos[1]

        self.min_value = min_value
        self.max_value = max_value
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_value  # Процент для отображения

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos - 5, 10,
                                       self.size[1] + 10)

        self.is_down = False

    def draw(self, screen):
        pygame.draw.rect(screen,  UI_BG_COLOR, self.container_rect)
        pygame.draw.rect(screen, WHITE, self.container_rect, 1)
        current_rect = self.container_rect.copy()
        current_rect.width = self.button_rect.centerx - self.container_rect.x
        pygame.draw.rect(screen, WHITE, self.container_rect)
        pygame.draw.rect(screen, ORANGE, current_rect)
        pygame.draw.rect(screen, ORANGE, self.button_rect)

    def check_event(self, mouse_pos, event):  # Наведена ли мышка на кнопку
        if event.type == pygame.MOUSEBUTTONDOWN and self.container_rect.collidepoint(mouse_pos):
            self.is_down = True
        elif event.type == pygame.MOUSEBUTTONUP and self.is_down:
            self.is_down = False
        if self.is_down and self.slider_left_pos <= mouse_pos[0] <= self.slider_right_pos:
            self.button_rect.centerx = mouse_pos[0]
            return self.get_value()

    def get_value(self):
        value_range = self.slider_right_pos - self.slider_left_pos - 1
        button_value = self.button_rect.centerx - self.slider_left_pos
        return (button_value / value_range) * (self.max_value - self.min_value) + self.min_value
