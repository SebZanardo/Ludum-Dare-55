import pygame
import random

from utilities.typehints import ActionBuffer, MouseBuffer
from config.input import InputState, MouseButton, Action
from baseclasses.scenemanager import Scene, SceneManager
from config.constants import MAGENTA, BLACK
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT

from config.assets import CHESS_PIECES


# Import the whole module of all scenes you want to switch to
import scenes.game


class FallingSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, speed, rotate_speed):
        super().__init__()
        self.original_image = image  # Store the original image for reference
        self.image = image.copy()  # Create a working copy for rotation
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.speed_y = speed
        self.angle = 0
        self.rotate_speed = rotate_speed

    def update(self, dt):
        self.rect.y += self.speed_y

        # Calculate half width and half height
        half_width = self.image.get_rect().width // 2
        half_height = self.image.get_rect().height// 2

        # Calculate maximum corner distance from center (diagonal)
        max_distance = (half_width**2 + half_height**2)**0.5

        # Calculate rotation speed based on desired speed and max distance
        self.angle += (self.rotate_speed) / max_distance

        # Rotate the working copy of the image using smoothscale
        # This is where the performance hit happens.
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Check for screen bottom and reset (optional)
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0


class MainMenu(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        super().__init__(scene_manager)
        self.square_size = 100
        self.piece_size = (self.square_size, self.square_size / 2 * 3)
        self.scaled_pieces = [
            pygame.transform.scale(sprite, self.piece_size) for sprite in CHESS_PIECES
        ]
        self.piece_offset = (0, -self.piece_size[1] // 2)
        falling_pieces = self.scaled_pieces
        self.pieces = []
        for i, image in enumerate(falling_pieces):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            speed = random.randint(1, 4)
            # trust
            rotate_speed = random.randint(25, 50) * random.choice((1, -1))
            self.pieces.append(FallingSprite(
                image=image, pos_x=x, pos_y=y, speed=speed, rotate_speed=rotate_speed))

    def handle_input(
        self, action_buffer: ActionBuffer, mouse_buffer: MouseBuffer
    ) -> None:
        if (
            action_buffer[Action.START][InputState.PRESSED]
            or mouse_buffer[MouseButton.LEFT][InputState.PRESSED]
        ):
            self.scene_manager.switch_scene(scenes.game.Game)

    def update(self, dt: float) -> None:
        for piece in self.pieces:
            piece.update(dt)
            if piece.rect.top > WINDOW_HEIGHT:
                piece.rect.bottom = 0

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(BLACK)
        for piece in self.pieces:
            surface.blit(piece.image, piece.rect.topleft)
