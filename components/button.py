from typing import Optional
import pygame

from config.constants import MAGENTA


class Button:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)

    def inside(self, x: int, y: int) -> bool:
        return (
            x >= self.x
            and x < self.x + self.width
            and y >= self.y
            and y < self.y + self.height
        )

    def render(
        self,
        surface: pygame.Surface,
        colour: Optional[pygame.Color] = None,
        border_colour: Optional[pygame.Color] = MAGENTA,
        border_width: int = 5,
    ) -> None:
        if colour is not None:
            pygame.draw.rect(surface, colour, self.rect)
        if border_colour is not None:
            pygame.draw.rect(surface, border_colour, self.rect, border_width)
