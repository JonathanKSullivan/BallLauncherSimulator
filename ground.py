import pygame


class Ground:
    """
    Represents the ground in the simulation environment.

    Attributes:
        screen_width (int): The width of the screen, which determines the
            width of the ground.
        ground_height (int): The height from the bottom of the screen to the
            top of the ground.
        ground_y (int): The y-coordinate of the top of the ground on the
            screen.
        color (tuple): The RGB color of the ground.
    """

    def __init__(self, screen_width, ground_height, color=(0, 155, 0)):
        """
        Initializes the Ground with its size and color.

        Args:
            screen_width (int): The width of the screen.
            ground_height (int): The height of the ground from the bottom.
            color (tuple, optional): The RGB color of the ground. Defaults to
            a shade of green.

        Raises:
            ValueError: If screen_width or ground_height is non-positive.
        """
        if screen_width <= 0:
            raise ValueError("Screen width must be positive.")
        if ground_height <= 0:
            raise ValueError("Ground height must be positive.")

        self.screen_width = screen_width
        self.ground_height = ground_height
        self.color = color
        self.ground_y = None

    def draw(self, screen):
        """
        Draws the ground on the provided Pygame screen.
        Calculates the y-coordinate for the top of the ground dynamically
        based on the screen size.

        Parameters:
            screen (pygame.Surface): The Pygame screen object where the ground
                will be drawn.
        """
        if (
            self.ground_y is None
            or screen.get_height() != self.ground_y + self.ground_height
        ):
            self.ground_y = screen.get_height() - self.ground_height

        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(0, self.ground_y, self.screen_width, self.ground_height),
        )

    def handle_resize(self, new_screen_width, new_screen_height):
        """
        Updates the dimensions of the ground in response to a screen resize
        event.

        Parameters:
            new_screen_width (int): The new width of the screen.
            new_screen_height (int): The new height of the screen.
        """
        self.screen_width = new_screen_width
        self.ground_y = new_screen_height - self.ground_height
