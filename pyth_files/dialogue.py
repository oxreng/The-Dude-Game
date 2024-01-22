import sys
import pygame
from pyth_files.sprite import *


class Dialogue:
    def __init__(self, screen, clock, title, level):
        self.screen = screen
        self.clock = clock
        self.level = level
        self.skipable = False
        self.running = True

        self.font = pygame.font.Font(GAME_FONT, GAME_FONT_SIZE)
        self.full_message = dialogue_text[title]
        self.lines = self.make_lines()
        self.text_pos_x = 20
        self.text_pos_y = SCREEN_HEIGHT - 180
        self.skip_text = self.font.render('Нажмите любую кнопку для пропуска', True, WHITE)
        pos = (self.skip_text.get_width() - SCREEN_WIDTH, self.skip_text.get_height() - SCREEN_HEIGHT)
        self.last_screen_to_text = pygame.Surface(self.skip_text.get_size())
        self.last_screen_to_text.blit(self.screen.copy(), pos)
        self.alpha_screen_to_text = pygame.Surface(
            self.skip_text.get_size(),
            pygame.SRCALPHA, 32)
        self.alpha_screen_to_text.fill((0, 0, 0, 200))
        self.skip_text_alpha = 255
        self.alpha_completed = False
        self.alpha_screen = pygame.Surface((SCREEN_SIZE[0], self.font.get_height() * len(self.lines) + 200),
                                           pygame.SRCALPHA, 32)
        self.alpha_screen.fill((0, 0, 0, 200))

    def run(self):
        self.screen.blit(self.alpha_screen, (0, SCREEN_HEIGHT - 200))
        BLITLETTEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(BLITLETTEREVENT, 40)
        lines = self.make_lines()
        current_line = lines.pop(0)
        current_text = ''
        while self.running:
            self.draw_skip_text()
            text = self.font.render(current_text, True, WHITE)
            self.screen.blit(text, (self.text_pos_x, self.text_pos_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == BLITLETTEREVENT:
                    if len(current_text) < len(current_line):
                        current_text = current_line[:len(current_text) + 1]
                    else:
                        if len(lines) > 0:
                            current_line = lines.pop(0)
                            current_text = ''
                            self.text_pos_y = self.text_pos_y + text.get_height()
                        else:
                            self.skipable = True
                            pygame.time.set_timer(BLITLETTEREVENT, 0)
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if self.skipable:
                        self.running = False
                    else:
                        current_text = current_line[:]

            pygame.display.flip()
            self.clock.tick(30)

    def make_lines(self):
        lines = [[]]
        words = self.full_message.split()
        space = self.font.size(' ')[0]
        x, y = 20, SCREEN_HEIGHT - 200
        for word in words:
            word_surface = self.font.render(word, True, WHITE)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= SCREEN_WIDTH - 300:
                x = 20
                y += word_height
                lines.append([])
            lines[-1].append(word)
            x += (word_width + space)
        return ['  '.join(line) for line in lines]

    def draw_skip_text(self):
        pygame.time.delay(20)
        self.screen.blit(self.last_screen_to_text,
                         (SCREEN_WIDTH - self.skip_text.get_width(), SCREEN_HEIGHT - self.skip_text.get_height()))
        self.screen.blit(self.alpha_screen_to_text,
                         (SCREEN_WIDTH - self.skip_text.get_width(), SCREEN_HEIGHT - self.skip_text.get_height()))
        if 255 >= self.skip_text_alpha > 0 and not self.alpha_completed:
            self.skip_text_alpha -= DIALOG_ALPHA_SPEED
        else:
            self.skip_text_alpha += DIALOG_ALPHA_SPEED
        if self.skip_text_alpha >= 255:
            self.alpha_completed = False
        elif self.skip_text_alpha <= 0:
            self.alpha_completed = True
        self.skip_text.set_alpha(self.skip_text_alpha)
        self.screen.blit(self.skip_text,
                         (SCREEN_WIDTH - self.skip_text.get_width(), SCREEN_HEIGHT - self.skip_text.get_height()))
