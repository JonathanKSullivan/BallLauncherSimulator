"""
This module contains the Launcher class, a simulation tool for modeling the
dynamics of a mechanical launcher. The Launcher class is designed to simulate
the launching mechanics of a projectile, specifically a ball, in a
physics-based simulation environment. It includes functionality for applying
torque, calculating velocity and acceleration components, updating the
launcher's state, drawing its representation on a screen, and resetting its
state.

The class utilizes mathematical models to simulate real-world physics
phenomena such as angular momentum and acceleration due to applied forces. It
is intended for use in educational tools, games, or any software requiring
simulation of  projectile launching mechanics.

The module uses Pygame for rendering, making it necessary to have Pygame
installed and properly configured to use this module.

Attributes:
    HALF_PI (float): A constant representing half of the value of pi, used for
                     trigonometric calculations within the class.

Classes:
    Launcher: Represents the mechanical structure of a launcher capable of
    hurling projectiles. It handles the physical properties of the launcher
    such as length, mass, and angular velocities, and provides methods for
    simulating and visualizing the launching process.


Dependencies:
    pygame: Required for rendering the launcher in a graphical window.
"""

import math
import pygame


class Launcher:
    """
    A class to represent a mechanical launcher that simulates the launching of
    a ball.

    Attributes:
        length (float): Length of the launcher arm in meters.
        mass (float): Mass of the launcher arm in kilograms.
        moment_of_inertia (float): Calculated moment of inertia of the
            launcher arm.
        angle (float): Current angle of the launcher arm in radians.
        angular_velocity (float): Current angular velocity of the launcher arm
            in radians per second.
        max_angular_velocity (float): Maximum angular velocity of the launcher
            arm in radians per second.
        angular_acceleration (float): Current angular acceleration of the
            launcher arm in radians per second squared.
        HALF_PI (float): Half of pi, commonly used in trigonometric
            calculations.
    """

    ALUMINUM_DENSITY = 2700
    HALF_PI = math.pi / 2

    def __init__(
        self,
        length,
        max_angular_velocity,
        ground_y,
        ball_size,
        scale_factor,
        launch_angle=0,
    ):
        """
        Initializes the Launcher with the specified length, mass, and maximum angular velocity.

        Parameters:
            length (float): The length of the launcher arm.
            mass (float): The mass of the launcher arm.
            max_angular_velocity (float): The maximum angular velocity.
        """
        self.length = length
        self.width = 1
        self.thickness = 1
        self.volume = length * self.width * self.thickness * scale_factor**3

        self.mass = self.volume * Launcher.ALUMINUM_DENSITY / scale_factor**3
        self.moment_of_inertia = (1 / 3) * self.mass * (length) ** 2
        self.angle = launch_angle
        self.angular_velocity = 0
        self.max_angular_velocity = max_angular_velocity
        self.angular_acceleration = 0
        self.stand_height = ground_y + 1
        self.ballholder_thickness = 2
        self.ball_holder_radius = ball_size + self.ballholder_thickness
        self.release_angle = launch_angle
        self.scale_factor = scale_factor

    def set_launch_angle(self, angle):
        """Set the launch angle for the launcher."""
        self.angle = angle

    def set_release_angle(self, angle):
        """Set the release angle for the launcher."""
        self.release_angle = angle

    def apply_torque(self, torque, friction_coefficient=0.05):
        """
        Applies a torque to the launcher arm, calculating the resultant
        angular acceleration and considering frictional losses. Frictional
        torque is modeled as a function of angular velocity and a friction
        coefficient.

        Parameters:
            torque (float): The torque to apply in Newton-meters.
            friction_coefficient (float): Coefficient representing the  mechanical friction in the system, which affects the net torque.
                Frictional torque opposes the direction of angular velocity and is proportional to it.
        """
        friction_torque = friction_coefficient * self.angular_velocity
        net_torque = torque - friction_torque
        self.angular_acceleration = net_torque / self.moment_of_inertia

    def launch_ball(self, desired_release_angle, desired_release_angular_velocity):
        """
        Determine if the ball can be launched based on the desired release
        angle and angular velocity.

        Parameters:
            desired_release_angle (float): The target angle in radians at
                which to release the ball.
            desired_release_angular_velocity (float): The target angular
                velocity in radians per second at which to release the ball.

        Returns:
            bool: True if the ball can be launched, False otherwise.
        """
        speed_condition = self.angular_velocity >= desired_release_angular_velocity
        angle_diff = abs(self.angle - desired_release_angle)
        angle_condition = angle_diff <= math.radians(1)
        return speed_condition and angle_condition

    def calculate_ball_velocity_components(self):
        cos_val = math.cos(self.angle + self.HALF_PI)
        sin_val = math.sin(self.angle + self.HALF_PI)
        vx = self.length * self.angular_velocity * cos_val
        vy = -self.length * self.angular_velocity * sin_val
        return (vx, vy)

    def calculate_ball_acceleration_components(self):
        """
        Calculates the acceleration components of the ball, both tangential
        and radial, at the current launcher configuration.

        Returns:
            tuple: The acceleration components (ax, ay) in meters per second
                squared.
        """
        tangential_acceleration = self.length * self.angular_acceleration
        radial_acceleration = self.length * self.angular_velocity**2

        atx = tangential_acceleration * math.cos(self.angle + math.pi / 2)
        aty = tangential_acceleration * math.sin(self.angle + math.pi / 2)

        arx = radial_acceleration * math.cos(self.angle + math.pi)
        ary = radial_acceleration * math.sin(self.angle + math.pi)

        return (atx + arx, aty + ary)

    def update(self, time_step):
        """
        Updates the state of the launcher over a specified time step,
        adjusting the angle and angular velocity.

        Parameters:
            time_step (float): The time step over which to update the launcher
                state in seconds.
        """
        self.angular_velocity += self.angular_acceleration * time_step
        self.angular_velocity = min(self.angular_velocity, self.max_angular_velocity)
        self.angle += self.angular_velocity * time_step
        self.angle = self.angle % (2 * math.pi)

    def draw(self, screen, origin_x, origin_y, font, ball_size, text_x=500, text_y=100):
        """
        Draws the launcher arm, the release angle line, and the status text on
        the given screen.

        Parameters:
            screen (pygame.Surface): The screen surface where the launcher is
                to be drawn.
            origin_x (int): The x-coordinate of the launcher's pivot.
            origin_y (int): The y-coordinate of the launcher's pivot.
            font (pygame.Font): The font used for drawing the status text.
            ball_size (float): The radius of the ball that adjusts the
                endpoint of the launcher.
            text_x (int): The x-coordinate for the status text.
            text_y (int): The y-coordinate for the status text.
        """
        end_x, end_y = self.get_launcher_tip_pos(origin_x, origin_y, self.scale_factor)

        pygame.draw.line(
            screen, (0, 0, 0), (origin_x, origin_y), (end_x, end_y), self.width
        )

        stand_rect = pygame.Rect(origin_x - 5, origin_y, 10, self.stand_height)
        pygame.draw.rect(screen, (0, 0, 0), stand_rect)

        release_end_x = origin_x + self.length * self.scale_factor * math.cos(
            self.release_angle
        )
        release_end_y = origin_y - self.length * self.scale_factor * math.sin(
            self.release_angle
        )
        pygame.draw.line(
            screen,
            (255, 0, 0, 127),
            (origin_x, origin_y),
            (release_end_x, release_end_y),
            2,
        )

        ball_holder_radius = self.ball_holder_radius
        bounding_rect = pygame.Rect(
            end_x - ball_holder_radius,
            end_y - ball_holder_radius,
            2 * ball_holder_radius,
            2 * ball_holder_radius,
        )
        pygame.draw.arc(
            screen,
            (0, 0, 0),
            bounding_rect,
            self.angle + math.pi,
            self.angle + 2 * math.pi,
            2,
        )

        status_text = f"Launcher: Angle={self.angle:.2f} rad, Angular Velocity={self.angular_velocity:.2f} rad/s, Speed={self.angular_velocity * self.length:.2f} m/s"
        text_surf = font.render(status_text, True, (0, 0, 0))
        screen.blit(text_surf, (text_x, text_y))

    def reset(self):
        """
        Resets the launcher to its initial state, setting the angle, angular
        velocity, and angular acceleration to zero.
        """
        self.angle = 0
        self.angular_velocity = 0
        self.angular_acceleration = 0

    def get_launcher_tip_pos(self, origin_x, origin_y, scale_factor):
        """
        Calculates the tip position of the launcher arm based on its current
        angle and a given scale factor.

        Parameters:
            origin_x (int): The x-coordinate of the launcher's pivot point.
            origin_y (int): The y-coordinate of the launcher's pivot point.
            scale_factor (float): A factor to scale the launcher arm's length
                for display purposes.

        Returns:
            tuple: The (x, y) coordinates of the launcher's tip.
        """
        end_x = origin_x + self.length * scale_factor * math.cos(self.angle)
        end_y = origin_y - self.length * scale_factor * math.sin(self.angle)

        return end_x, end_y
