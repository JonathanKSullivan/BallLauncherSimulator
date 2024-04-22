"""
This module defines the Simulation class that orchestrates a ball launcher 
simulation. The simulation includes a graphical user interface and dynamic
interactions within a Pygame environment. It integrates mechanical physics and
control systems to simulate the realistic behavior of launching a ball with a
mechanized launcher, which is controlled by a motor for angular adjustments.

The Simulation class manages the main simulation loop, processes user
interactions, and visualizes the state of the simulation components, including
the launcher, ball, and motor. It also provides UI elements to control the
simulation parameters like torque, launch angle, and angular velocity,
enabling real-time interaction and adjustments.

Classes:
    Simulation: Manages the overall simulation environment, integrating all
        components, handling user input, and updating the visual display.

Dependencies:
    pygame: Used for creating the graphical user interface and rendering the
        simulation components.
    pygame_gui: Provides tools for building interactive UI elements like
        buttons and sliders.
    math: Provides access to mathematical functions needed for physical
        calculations.
    Launcher, Motor, Ball, UIComponents: Custom classes representing different
        parts of the simulation.

How to Run:
    The simulation can be started by creating an instance of the Simulation class and calling its `run` method. This initializes the Pygame framework, sets up the UI, and enters the main event loop.
"""

from ground import Ground
import pygame_gui
import math
import pygame
from launcher import Launcher
from motor import Motor
from ball import Ball
from ui_components import UIComponents
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import logging


class Simulation:
    """
    Manages the overall simulation environment for a ball launcher scenario.
    This class integrates components like the launcher, motor, and ball, and
    handles the user interface for interaction.

    Attributes:
        screen_size (tuple): The current width and height of the display
            window.
        screen (pygame.Surface): The main display surface where all visual
            elements are drawn.
        manager (pygame_gui.UIManager): Manages and draws user interface
            elements.
        clock (pygame.time.Clock): Clock for managing update rates.
        launcher (Launcher): The launcher object used in the simulation.
        motor (Motor): The motor object providing dynamics to the launcher.
        ball (Ball): The ball object being launched in the simulation.
        is_simulation_started (bool): Flag to check if the simulation has
            started.
        ui_components (UIComponents): Container for UI elements like buttons
            and sliders.
        scale_factor (float): Scale factor for drawing to adjust the size of
            visual elements relative to the display.
        origin_x (float): X-coordinate for the central pivot point of the
            launcher.
        origin_y (float): Y-coordinate for the central pivot point of the
            launcher.
    """

    def __init__(self):
        """
        Initializes the simulation, setting up the pygame environment, screen,
        UI components, and simulation objects.
        """
        try:
            pygame.init()
            info = pygame.display.Info()
            self.screen_size = (
                info.current_w,
                info.current_h,
            )
            self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
            pygame.display.set_caption("Ball Launcher Simulator")
            self.scale_factor = 50
            theme_path = "./theme.json"
            self.manager = pygame_gui.UIManager(self.screen_size, theme_path)
            self.clock = pygame.time.Clock()
            arm_length = 1.0
            self.motor = Motor(
                max_torque=2 * self.scale_factor, max_angular_velocity=20
            )
            self.ball_size = 0.2
            self.is_simulation_started = False
            self.ui_components = UIComponents(self.manager, self.screen_size)
            self.origin_x = 9 * self.screen_size[0] / 10
            self.ground_y = 50
            self.origin_y = (
                self.screen.get_height()
                - self.ground_y
                - arm_length * self.scale_factor
            )
            self.ground = Ground(self.screen_size[0], self.ground_y)
            self.launcher = Launcher(
                length=arm_length,
                max_angular_velocity=20,
                ground_y=self.ground_y,
                ball_size=self.ball_size * self.scale_factor,
                scale_factor=self.scale_factor,
            )
            self.ball = Ball(
                position=[
                    self.origin_x + self.launcher.length * self.scale_factor,
                    self.origin_y,
                ],
                ball_size=self.ball_size,
                scale_factor=self.scale_factor,
            )
            self.ball_positions = []
            self.position_plot = None
        except Exception as e:
            logging.error(f"Failed to initialize the simulation: {e}")
            raise Exception(f"Initialization failed due to: {e}") from e

    def handle_window_resize(self, event):
        """
        Handles window resizing events to adjust the display and UI components accordingly.

        Parameters:
            event (pygame.event.Event): The resize event containing new dimensions.
        """
        if event.type == pygame.VIDEORESIZE:
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.screen_size = (event.w, event.h)
            self.manager.set_window_resolution(self.screen_size)
            self.ui_components.screen_size = self.screen_size
            self.ui_components.update_ui_elements()

    def plot_trajectory(self, screen, positions):
        """Plot the trajectory of the ball with error handling."""
        try:
            fig, ax = plt.subplots()
            ax.plot(positions[:, 0], positions[:, 1], "r-")
            ax.set_title("Ball Trajectory")
            ax.set_xlabel("Horizontal Position (meters)")
            ax.set_ylabel("Vertical Position (meters)")
            ax.grid(True)

            canvas = FigureCanvas(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()
            size = canvas.get_width_height()
            surf = pygame.image.fromstring(raw_data, size, "RGB")

            plt.close(fig)
            return surf

        except Exception as e:
            logging.error(f"Error plotting trajectory: {e}")
            plt.close(fig)
            return None

    def process_events(self):
        """
        Processes all events from the event queue including user interactions
        and system events.

        Returns:
            bool: False if the window is closed, True otherwise to continue
                the simulation loop.
        """
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                self.ui_components.handle_events(event)
                self.manager.process_events(event)
                self.process_ui_events(event)
                self.handle_window_resize(event)

                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    self.handle_slider_movement(event)

        except pygame.error as e:
            logging.error(f"Pygame error occurred: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during event processing: {e}")
        return True

    def handle_slider_movement(self, event):
        """
        Handle slider movements for different simulation parameters.
        """
        try:
            if event.ui_element == self.ui_components.sliders["release_angle"][0]:
                new_angle = event.ui_element.get_current_value()
                self.launcher.set_release_angle(new_angle)
            elif event.ui_element == self.ui_components.sliders["launch_angle"][0]:
                new_angle = event.ui_element.get_current_value()
                self.launcher.set_launch_angle(new_angle)
            elif event.ui_element == self.ui_components.sliders["drag_coefficient"][0]:
                new_drag_coefficient = event.ui_element.get_current_value()
                self.ball.set_drag_coefficient(new_drag_coefficient)
            elif event.ui_element == self.ui_components.sliders["spin_rate"][0]:
                new_spin_rate = event.ui_element.get_current_value()
                self.ball.set_spin_rate(new_spin_rate)
            elif event.ui_element == self.ui_components.sliders["air_density"][0]:
                new_air_density = event.ui_element.get_current_value()
                self.ball.set_air_density(new_air_density)
            self.update_display(0)
        except Exception as e:
            logging.error(f"Error handling slider movement: {e}")

    def process_ui_events(self, event):
        """
        Handles specific user interface events like button presses.

        Parameters:
            event (pygame.event.Event): The event to be processed.
        """
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.ui_components.run_button:
                self.start_simulation()
            elif event.ui_element == self.ui_components.reset_button:
                self.reset_simulation()

    def update_display(self, time_delta):
        """
        Updates the screen display by redrawing all visual and UI components.

        Parameters:
            time_delta (float): The elapsed time since the last frame in
                seconds.
        """
        self.screen.fill((255, 255, 255))
        self.ball_positions.append(self.ball.position.copy())

        font = pygame.font.SysFont(None, 24)

        self.draw()
        self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def update_simulation(self, time_delta):
        """
        Updates the simulation state based on the current user input values.

        Parameters:
            time_delta (float): The time increment for the simulation update.
        """
        try:
            applied_torque = (
                self.ui_components.sliders["torque"][0].get_current_value()
                * self.scale_factor
            )
            desired_launch_angle = self.ui_components.sliders["launch_angle"][
                0
            ].get_current_value()
            desired_release_angle = self.ui_components.sliders["release_angle"][
                0
            ].get_current_value()
            desired_release_angular_velocity = self.ui_components.sliders["speed"][
                0
            ].get_current_value()

            self.update(
                time_delta,
                desired_launch_angle,
                desired_release_angle,
                desired_release_angular_velocity,
            )

            self.update_plots()

        except ValueError as e:
            logging.error(f"Error updating simulation parameters: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during simulation update: {e}")

    def update_plots(self):
        if self.ball.ball_has_landed or self.update_needed:
            self.position_plot = self.plot_trajectory(
                self.screen, np.array(self.ball_positions)
            )
            self.update_needed = False

    def run(self):
        """
        Main loop that keeps the simulation running. It processes events,
        updates the UI manager, and redraws the screen.
        """
        running = True
        while running:
            try:
                time_delta = self.clock.tick(60) / 1000.0

                if not self.process_events():
                    break

                self.manager.update(time_delta)
                self.update_display(time_delta)
                self.update_simulation(time_delta)

            except Exception as e:
                logging.error(f"An error occurred during the simulation loop: {e}")
                running = self.handle_critical_error(e)

    def handle_critical_error(self, error):
        """
        Handle any critical errors that occur during the simulation loop.
        This could involve logging the error, notifying the user, and deciding
        whether to terminate the simulation.

        Parameters:
            error (Exception): The exception that was raised.

        Returns:
            bool: True if the simulation should continue running, False if it
                should terminate.
        """
        logging.error(f"Critical simulation error: {error}", exc_info=True)
        return False

    def start_simulation(self):
        """
        Starts the simulation processes.
        """
        self.is_simulation_started = True
        self.ui_components.start_simulation()

    def reset_simulation(self):
        """
        Resets the simulation to initial state, stopping any ongoing
        simulation and resetting all components.
        """
        self.is_simulation_started = False
        self.ball.has_been_launched = False
        self.ui_components.reset_simulation()
        self.launcher.reset()
        self.ball.reset(
            initial_position=[
                self.origin_x + self.launcher.length * self.scale_factor,
                self.origin_y,
            ]
        )

    def update(
        self,
        time_step,
        desired_launch_angle,
        desired_release_angle,
        desired_release_angular_velocity,
    ):
        """
        Performs a simulation update cycle.

        Parameters:
            time_step (float): The time increment for updating the simulation.
            desired_launch_angle (float): The target launch angle set by the
                user.
            desired_release_angle (float): The target release angle set by the
                user.
            desired_release_angular_velocity (float): The target release
                angular velocity set by the user.
        """
        if self.is_simulation_started:
            self.handle_launcher_update(time_step, desired_release_angular_velocity)
            self.handle_ball_launching(
                desired_release_angle, desired_release_angular_velocity, time_step
            )
            self.update_ball_physics(time_step)

    def handle_launcher_update(self, time_step, desired_release_angular_velocity):
        """
        Updates the launcher's state by applying torque and updating its
        angular velocity.

        Parameters:
            time_step (float): The time increment for updating the launcher.
            desired_release_angular_velocity (float): The target release
                angular velocity.
        """
        if not self.ball.has_been_launched:
            torque = self.motor.apply_torque(
                self.launcher.angular_velocity,
                self.motor.max_torque,
                desired_release_angular_velocity,
            )
            self.launcher.apply_torque(torque)
        else:
            if self.launcher.angular_velocity > 0:
                self.launcher.apply_torque(-self.motor.max_torque)
            else:
                self.launcher.angular_velocity = 0

        self.launcher.update(time_step)

    def handle_ball_launching(
        self, desired_release_angle, desired_release_angular_velocity, time_step
    ):
        """
        Determines if the ball should be launched based on the launcher's
        state.

        Parameters:
            desired_release_angle (float): The target release angle.
            desired_release_angular_velocity (float): The target release
                angular velocity.
            time_step (float): The time increment for updating the simulation.
        """
        should_launch = (
            self.launcher.launch_ball(
                desired_release_angle, desired_release_angular_velocity
            )
            and self.is_simulation_started
        )

        if should_launch and not self.ball.has_been_launched:
            self.ball.launch_ball(time_step)

    def update_ball_physics(self, time_step):
        """
        Updates the ball's physical state based on the current simulation
        settings.

        Parameters:
            time_step (float): The time increment for updating the ball's
            physics.
        """
        current_time = pygame.time.get_ticks() / 1000.0
        self.ball.update(
            current_time,
            self.launcher.get_launcher_tip_pos(
                self.origin_x, self.origin_y, self.scale_factor
            ),
            self.launcher.calculate_ball_velocity_components(),
            self.launcher.calculate_ball_acceleration_components(),
            time_step,
            self.scale_factor,
            self.ground_y,
            self.screen,
        )

    def draw_clouds(self):
        color = (255, 255, 255)
        cloud_positions = [
            (500, 100),
            (900, 150),
            (700, 50),
        ]
        for pos in cloud_positions:
            pygame.draw.ellipse(
                self.screen, color, pygame.Rect(pos[0], pos[1], 100, 50)
            )
            pygame.draw.ellipse(
                self.screen, color, pygame.Rect(pos[0] + 50, pos[1] - 20, 120, 60)
            )
            pygame.draw.ellipse(
                self.screen, color, pygame.Rect(pos[0] + 100, pos[1], 90, 50)
            )

    def draw(self):
        """
        Draws all simulation components to the screen. This includes the launcher, ball, and motor information.
        """
        sky_blue = (135, 206, 235)
        self.screen.fill(sky_blue)

        self.draw_clouds()
        end_x, end_y = self.launcher.get_launcher_tip_pos(
            self.origin_x, self.origin_y, self.scale_factor
        )

        font = pygame.font.SysFont(None, 24)

        self.ball.draw(self.screen, (end_x, end_y), self.scale_factor, font)
        self.launcher.draw(
            self.screen,
            self.origin_x,
            self.origin_y,
            font,
            ball_size=self.ball_size * self.scale_factor,
        )
        self.motor.draw(self.screen, font)
        self.ground.draw(self.screen)

        if self.position_plot:
            plot_position = (700, 100)
            self.screen.blit(self.position_plot, plot_position)
