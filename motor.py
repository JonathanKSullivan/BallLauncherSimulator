"""Module for managing motor behavior in a simulation environment.

This module defines the Motor class which encapsulates the functionality for handling motor operations
including torque application and angular velocity limitations. It is designed to be used within a simulation
that requires realistic motor behavior such as a robotic arm or vehicle simulation. The class also includes
methods for rendering motor information on a Pygame display, aiding in debugging and visualization during development.
"""

import pygame


class Motor:
    """Represents a motor with constraints on maximum torque and angular velocity.

    Attributes:
        max_torque (float): The maximum torque the motor can apply, in Newton-meters.
        max_angular_velocity (float): The maximum angular velocity of the motor, in radians per second.
        text_position (tuple): The position on the screen to display the motor information.
        text_color (tuple): The color of the text used to display the motor information.
    """

    def __init__(
        self,
        max_torque,
        max_angular_velocity,
        text_position=(500, 50),
        text_color=(0, 0, 0),
    ):
        """Initializes the Motor with maximum torque and angular velocity constraints.

        Parameters:
            max_torque (float): The maximum torque the motor can handle, in Newton-meters.
            max_angular_velocity (float): The maximum angular velocity the motor can handle, in radians per second.
            text_position (tuple, optional): The x, y coordinates on the screen to place the text.
            text_color (tuple, optional): The RGB color of the text. Defaults to black.

        Raises:
            ValueError: If max_torque or max_angular_velocity is non-positive.
        """
        if max_torque <= 0 or max_angular_velocity <= 0:
            raise ValueError(
                "Max torque and max angular velocity must be positive values."
            )

        self.max_torque = max_torque
        self.max_angular_velocity = max_angular_velocity
        self.text_position = text_position
        self.text_color = text_color

    def apply_torque(self, angular_velocity, torque, desired_angular_velocity):
        """Applies torque based on the motor's current and desired angular velocities.

        This method decides the actual torque to be applied, not exceeding the motor's capabilities.
        If the current angular velocity is less than both the desired angular velocity and the motor's
        maximum angular velocity, it allows the requested torque up to the motor's limit.

        Parameters:
            angular_velocity (float): The current angular velocity of the motor, in radians per second.
            torque (float): The torque requested to be applied, in Newton-meters.
            desired_angular_velocity (float): The desired angular velocity to reach, in radians per second.

        Returns:
            float: The actual torque applied, in Newton-meters. This will be zero if the conditions are not met.
        """
        if (
            angular_velocity <= desired_angular_velocity
            and angular_velocity < self.max_angular_velocity
        ):
            return min(torque, self.max_torque)
        return 0

    def draw(self, screen, font):
        """Renders the motor's current status on the provided Pygame screen.

        This method displays a text representation of the motor's maximum torque and angular velocity
        at the specified position on the screen.

        Parameters:
            screen (pygame.Surface): The Pygame screen object where the motor information will be drawn.
            font (pygame.Font): The Pygame font object used to render text.
        """
        text_surf = font.render(
            f"Motor: Torque={self.max_torque} Nm, Max Speed={self.max_angular_velocity} rad/s",
            True,
            self.text_color,
        )
        screen.blit(text_surf, self.text_position)
