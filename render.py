class Render:
    def __init__(self, screen, player, sprites):
        self.screen = screen
        self._player = player
        self.sprites = sprites

    def render(self):
        self.sprites.draw(self.screen)
