"""
This module defines the Ball class used in physics simulations, specifically
designed to simulate the dynamics of a ball in environments influenced by
factors like drag and gravity. The Ball class incorporates realistic physics
behaviors including mass-based motion, air resistance, and external forces to
provide a detailed simulation suitable for educational, gaming, or scientific
applications.

The Ball class supports various operations such as launching, resetting,
updating based on physical laws, and rendering its state in a Pygame window.
It utilizes numpy for numerical operations and Pygame for visualization,
making it a versatile tool for demonstrating concepts in physics and 
engineering.
"""

import pygame
import numpy as np
import math


class Ball:
    """
    Represents a simulated ball in a physics-based environment, incorporating
    factors like drag, mass, and acceleration.

    Attributes:
        mass (float): Mass of the ball in kilograms.
        position (numpy.ndarray): Current position of the ball as a 2D vector.
        velocity (numpy.ndarray): Current velocity of the ball as a 2D vector.
        acceleration (numpy.ndarray): Current acceleration of the ball as a 2D
            vector.
        drag_coefficient (float): Coefficient of drag for the ball, affecting
            its motion through air.
        cross_sectional_area (float): Cross-sectional area of the ball in
            square meters, relevant to drag calculations.
        air_density (float): Density of air in kg/m^3, used in drag force
            calculations. Default is set to 1.225 kg/m^3 at sea level.
        has_been_launched (bool): Flag indicating whether the ball has been
            launched.
        launch_time (float or None): Timestamp of when the ball was launched,
            used for calculating motion updates.
    """

    STEEL_DENSITY = 7870  # kg/m^3 for 1018 steel
    GRAVITY = 9.81
    DRAG_CONSTANT = 0.5
    KINEMATIC_CONSTANT = 0.5
    VELOCITY_VECTOR_SCALE = 10
    ACCELERATION_VECTOR_SCALE = 50
    ARROWHEAD_SIZE = 4
    ARROWHEAD_ANGLE = math.pi / 6
    DEFAULT_TEXT_X = 500
    DEFAULT_TEXT_Y = 130

    def __init__(
        self,
        position,
        ball_size,
        scale_factor,
        drag_coefficient=0.47,
        cross_sectional_area=0.001,
    ):
        """
        Initializes a new instance of the Ball class, setting up the physical
        properties and initial conditions for a simulated ball. This includes
        defining its size, mass, drag characteristics, and initial motion
        state.

        Parameters:
            position (list or np.ndarray): The initial position of the ball,
                specified as a two-element list or array
                representing the x and y coordinates. This position should be
                in simulation-specific units that relate to the real-world
                scale via the scale_factor.
            ball_size (float): The diameter of the ball in meters. This value
                is used to calculate the ball's radius and, subsequently, its
                volume and mass assuming a spherical shape and uniform density.
            scale_factor (float): A coefficient used to scale physical
                dimensions within the simulation environment. For instance,
                this factor can be used to convert real-world measurements
                (like meters) to simulation units (like pixels).
            drag_coefficient (float, optional): The coefficient of drag for
                the ball, which affects how air resistance influences its
                motion. This is a unitless coefficient typically ranging from
                0 (no drag) to 1 (high drag), with a default of 0.47
                appropriate for a sphere in a fluid like air.
            cross_sectional_area (float, optional): The cross-sectional area
            of the ball in square meters, used in drag force calculations. It
            is essential for determining how much air resistance the ball
            encounters, with a default of 0.001 square meters typically
            suitable for small objects.

        Raises:
            ValueError: If any of the inputs are out of their expected ranges,
            such as a non-positive ball size,
                a non-two-element position, or an invalid scale factor.

        Notes:
            The mass of the ball is calculated based on the volume derived
            from the ball_size and assuming a density typical of steel
            (7870 kg/m^3), which can be adjusted if different materials are
            simulated. The initial
            velocity and acceleration are set to zero, indicating the ball
            starts at rest unless otherwise specified.
        """
        # Validate inputs
        if not isinstance(position, (list, np.ndarray)) or len(position) != 2:
            raise ValueError(
                "Position must be a list or numpy array with two elements."
            )
        if not isinstance(ball_size, (int, float)) or ball_size <= 0:
            raise ValueError("Ball size must be a positive number.")
        if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
            raise ValueError("Scale factor must be a positive number.")
        if not isinstance(drag_coefficient, float) or not (0 <= drag_coefficient <= 1):
            raise ValueError("Drag coefficient must be a float between 0 and 1.")
        if not isinstance(cross_sectional_area, float) or cross_sectional_area <= 0:
            raise ValueError("Cross-sectional area must be a positive float.")

        # Set instance attributes based on validated inputs
        self.radius = ball_size / 2
        self.volume = (4 / 3) * math.pi * (self.radius**3)
        self.mass = (
            self.volume * Ball.STEEL_DENSITY
        )  # Calculated based on steel density
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.acceleration = np.array([0, 0], dtype=np.float64)
        self.drag_coefficient = drag_coefficient
        self.cross_sectional_area = cross_sectional_area
        self.air_density = 1.225  # Default air density at sea level in kg/m^3
        self.spin_rate = 0
        self.has_been_launched = False
        self.launch_time = None
        self.ball_size = ball_size
        self.ball_has_landed = False
        self.velocity_norm = np.linalg.norm(self.velocity)

    def reset(self, initial_position=None):
        """
        Resets the ball to an initial state or a new specified position,
        setting all motion-related properties to zero.

        Parameters:
            initial_position (list or numpy.ndarray, optional): The position
                to reset the ball to. If None, resets to the origin [0, 0].
        """
        if initial_position is not None:
            self.position = np.array(initial_position, dtype=np.float64)
        else:
            self.position.fill(0)

        self.velocity.fill(0)
        self.acceleration.fill(0)
        self.has_been_launched = False
        self.ball_has_landed = False

    def set_drag_coefficient(self, coeff):
        """
        Sets the drag coefficient for the ball.

        The drag coefficient affects how strongly air resistance slows down
        the ball's motion. A higher drag coefficient indicates more
        resistance. Typical values range from 0.1 for streamlined objects to
        0.9 for blunt bodies.

        Parameters:
            coeff (float): The drag coefficient, must be between 0 and 1
                (exclusive).

        Raises:
            ValueError: If the coefficient is not a float or is outside the
                allowed range (0, 1).
        """
        if not isinstance(coeff, float) or not (0 < coeff < 1):
            error = "Drag coefficient must be a float between 0 and 1"
            raise ValueError()
        self.drag_coefficient = coeff

    def set_air_density(self, density):
        """
        Sets the air density experienced by the ball.

        Air density impacts the calculation of drag force acting on the ball.
        Higher air density increases the drag force, which can significantly
        affect the ball's trajectory and speed, especially in high-speed
        scenarios.

        Parameters:
            density (float): The air density in kilograms per cubic meter
            (kg/m³), must be positive.

        Raises:
            ValueError: If the density is not a float or is non-positive.
        """
        if not isinstance(density, float) or density <= 0:
            raise ValueError("Air density must be a positive float")
        self.air_density = density

    def set_spin_rate(self, rate):
        """
        Sets the spin rate of the ball, affecting how lift forces are
        calculated.

        The spin rate contributes to the Magnus effect, which can curve the
        path of the ball through the air. This is particularly noticeable in
        sports like baseball, tennis, or golf, where spin plays a crucial role
        in the game dynamics.

        Parameters:
            rate (float): The spin rate in radians per second.

        Raises:
            ValueError: If the rate is not a float.
        """
        if not isinstance(rate, float):
            raise ValueError("Spin rate must be a float")
        self.spin_rate = rate

    def launch_ball(self, current_time):
        """
        Marks the ball as launched and records the launch time, enabling
        motion calculations to begin based on the time of launch. This method
        should only be called once per instance unless the ball is reset.
        Calling this method on an already launched ball will raise an
        exception.

        Parameters:
            current_time (float): The system time or simulation time at which
                the ball is considered to be launched. This time is crucial
                for calculating the progression of the ball's motion in
                subsequent updates.

        Raises:
            RuntimeError: If the ball has already been launched, indicating
                that it cannot be launched again without resetting.
            TypeError: If the current_time is not a numeric value, which is
                necessary for time calculations.

        Note:
            This method sets the 'has_been_launched' flag to True and records
            the 'launch_time'. Subsequent calls to update the ball's position
            will use this time as the base for calculating elapsed time.
        """
        if self.has_been_launched:
            raise RuntimeError("Ball has already been launched.")
        if not isinstance(current_time, (int, float)):
            raise TypeError("Current time must be a numeric value.")

        self.has_been_launched = True
        self.launch_time = current_time

    def calculate_drag_force(self):
        """
        Calculates the drag force exerted on the ball. The drag force is
        calculated using the formula:

        Fd = 0.5 * Cd * ρ * A * |v| * v

        where Fd is the drag force vector, Cd is the drag coefficient, ρ is
        the air density,

        A is the cross-sectional area of the ball, |v| is the magnitude of the
        velocity vector, and v is the velocity vector itself.

        Returns:
            numpy.ndarray: The drag force vector, which opposes the direction
            of the velocity.
        """
        drag_force = (
            self.DRAG_CONSTANT
            * self.drag_coefficient
            * self.air_density
            * self.cross_sectional_area
            * self.velocity_norm
            * self.velocity
        )
        return drag_force

    def calculate_lift_force(self):
        """
        Calculates the lift force exerted on the ball due to its spin, based
        on the Magnus effect. The lift force is given by:

        Fl = π * r^2 * ρ * |v| * ω * d

        where Fl is the lift force vector, r is the radius of the ball, ρ is
        the air density, |v| is the magnitude of the velocity, ω is the
        angular velocity (spin rate), and d is the direction perpendicular to
        the velocity.

        Returns:
            numpy.ndarray: The lift force vector, which is perpendicular to
                the velocity vector. Returns a zero vector if the ball is not
                moving.
        """
        if self.velocity_norm == 0:
            return np.array([0.0, 0.0])

        omega = self.spin_rate
        lift_direction = (
            np.array([-self.velocity[1], self.velocity[0]]) / self.velocity_norm
        )
        lift_force = (
            np.pi
            * self.radius**2
            * self.air_density
            * self.velocity_norm
            * omega
            * lift_direction
        )
        return lift_force

    def update_physics(self, time_step, scale_factor):
        """
        Updates the ball's physical state including its velocity and position
        based on the net forces acting on it, the time step for the
        simulation, and a scale factor for the simulation environment.

        Parameters:
            time_step (float): The time increment over which the state is
                updated, in seconds. Must be a positive number.
            scale_factor (float): A scale factor used to adjust the
                computations to the simulation scale. Must be a positive
                number.

        Raises:
            ValueError: If `time_step` or `scale_factor` is not a positive
                number.

        This method applies the calculated drag and lift forces, updates the
        velocity and position based on these forces, and adjusts these values
        according to the provided time_step and scale_factor.
        """
        if time_step <= 0:
            raise ValueError("Time step must be a positive number")
        if scale_factor <= 0:
            raise ValueError("Scale factor must be a positive number")

        self.velocity_norm = np.linalg.norm(self.velocity)
        drag_force = self.calculate_drag_force()
        lift_force = self.calculate_lift_force()

        # Net acceleration including gravitational, drag, and lift forces
        self.acceleration = (
            np.array([0, self.GRAVITY])
            - drag_force / self.mass
            + lift_force / self.mass
        )

        # Update velocity and position
        self.velocity += self.acceleration * time_step
        self.position += (
            self.velocity * time_step * scale_factor
            - self.KINEMATIC_CONSTANT
            * scale_factor
            * self.acceleration
            * (time_step**2)
        )

    def check_ground_collision(self, max_pos_y, coefficient_of_restitution=0.8):
        """
        Checks for and handles collisions with the ground, adjusting the
        ball's position and motion state accordingly. Incorporates energy loss
        using the coefficient of restitution, which affects the rebound
        velocity.

        Parameters:
            max_pos_y (float): The maximum y-coordinate representing the
                ground level, beyond which the ball should not move.
            coefficient_of_restitution (float): Defines the elasticity of the
                collision, where 1 is perfectly elastic and 0 is perfectly
                inelastic.

        This method modifies the ball's velocity based on the coefficient of
        restitution when a collision is detected.
        """
        if self.position[1] >= max_pos_y:
            self.position[1] = max_pos_y
            self.velocity[1] = -coefficient_of_restitution * self.velocity[1]
            self.velocity[0] *= coefficient_of_restitution
            self.acceleration = np.array([0, 0])
            self.ball_has_landed = self.velocity[1] == 0

    def update(
        self,
        current_time,
        launcher_tip_pos,
        ball_init_velocity,
        ball_init_acceleration,
        time_step,
        scale_factor,
        ground_y,
        screen,
    ):
        """
        Updates the ball's position and velocity based on its current state,
        physical properties, and the conditions of the simulation environment.

        Parameters:
            current_time (float): The current simulation time used to
                calculate the duration the ball has been in motion.
            launcher_tip_pos (tuple or numpy.ndarray): The position from which
                the ball is considered to have been launched.
            ball_init_velocity (tuple or numpy.ndarray): The initial velocity
                of the ball at the time of launch, used if the ball has not been launched yet.
            ball_init_acceleration (tuple or numpy.ndarray): The initial
                acceleration of the ball at the time of launch.
            time_step (float): The time increment over which to update the
                ball's state, in seconds.
            scale_factor (float): A factor used to scale the simulation's
                spatial dimensions for display purposes.
            ground_y (float): The y-coordinate that represents the ground
                level, below which the ball should not pass.
            screen (pygame.Surface): The Pygame display surface where the ball
                and other objects are drawn.

        Effects:
            Updates the ball's position and velocity based on applied forces
            including gravity, drag, and any lift due to spin. Checks for
            collision with the ground and updates the ball's state accordingly.
        """
        try:
            if self.has_been_launched and not self.ball_has_landed:
                self.update_physics(time_step, scale_factor)
                max_pos_y = (
                    screen.get_height() - ground_y - self.ball_size * scale_factor
                )
                self.check_ground_collision(max_pos_y)
            elif not self.has_been_launched:
                self.position, self.velocity, self.acceleration = (
                    np.array(launcher_tip_pos),
                    np.array(ball_init_velocity),
                    np.array(ball_init_acceleration),
                )
        except Exception as e:
            logging.error(f"Error updating ball physics: {str(e)}")
            raise

    def draw(
        self,
        screen,
        launcher_tip_pos,
        scale_factor,
        font,
        text_x=DEFAULT_TEXT_X,
        text_y=DEFAULT_TEXT_Y,
    ):
        """
        Draws the ball and its motion vectors on the provided Pygame screen.
        This method visualizes the ball's current position, velocity, and
        acceleration, enhancing the understanding of its dynamics.

        Parameters:
            screen (pygame.Surface): The Pygame screen object on which to draw.
            launcher_tip_pos (tuple): Coordinates (x, y) representing the
                launcher's tip position, used as a reference for drawing.
            scale_factor (float): A scaling factor used to adjust the
                visualization of the ball's size and vectors.
            font (pygame.Font): A Pygame Font object used to render textual
                information on the screen.
            text_x (int, optional): The x-coordinate on the screen for drawing
                the status text. Defaults to 500.
            text_y (int, optional): The y-coordinate on the screen for drawing
                the status text. Defaults to 130.

        Displays:
            Renders the ball as a circle, with lines indicating the direction
                and magnitude of velocity and acceleration.
            Textual information about the ball's current position, velocity,
                and acceleration is also displayed.
        """
        ball_screen_x = self.position[0]
        ball_screen_y = self.position[1]

        # Draw the ball as a red circle
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (int(ball_screen_x), int(ball_screen_y)),
            int(self.ball_size * scale_factor),
        )

        if not self.has_been_launched:

            # Draw velocity vector if there is significant movement
            if self.velocity_norm > 0:
                end_x = ball_screen_x + self.velocity[0] * self.VELOCITY_VECTOR_SCALE
                end_y = ball_screen_y - self.velocity[1] * self.VELOCITY_VECTOR_SCALE
                pygame.draw.line(
                    screen,
                    (255, 0, 0),
                    (int(ball_screen_x), int(ball_screen_y)),
                    (int(end_x), int(end_y)),
                    2,
                )

                # Draw an arrowhead at the end of the velocity vector
                pygame.draw.polygon(
                    screen,
                    (255, 0, 0),
                    [
                        (int(end_x), int(end_y)),
                        (
                            int(
                                end_x
                                - self.ARROWHEAD_SIZE
                                * math.cos(
                                    math.atan2(-self.velocity[1], self.velocity[0])
                                    + math.pi / 6
                                )
                            ),
                            int(
                                end_y
                                + 4
                                * math.sin(
                                    math.atan2(-self.velocity[1], self.velocity[0])
                                    + self.ARROWHEAD_ANGLE
                                )
                            ),
                        ),
                        (
                            int(
                                end_x
                                - self.ARROWHEAD_SIZE
                                * math.cos(
                                    math.atan2(-self.velocity[1], self.velocity[0])
                                    - math.pi / 6
                                )
                            ),
                            int(
                                end_y
                                + 4
                                * math.sin(
                                    math.atan2(-self.velocity[1], self.velocity[0])
                                    - self.ARROWHEAD_ANGLE
                                )
                            ),
                        ),
                    ],
                )

            # Draw acceleration vector if significant
            if np.linalg.norm(self.acceleration) > 0:
                end_ax = (
                    ball_screen_x
                    + self.acceleration[0] * self.ACCELERATION_VECTOR_SCALE
                )
                end_ay = (
                    ball_screen_y
                    - self.acceleration[1] * self.ACCELERATION_VECTOR_SCALE
                )
                pygame.draw.line(
                    screen,
                    (0, 255, 0),
                    (int(ball_screen_x), int(ball_screen_y)),
                    (int(end_ax), int(end_ay)),
                    2,
                )

                # Draw an arrowhead at the end of the acceleration vector
                pygame.draw.polygon(
                    screen,
                    (0, 255, 0),
                    [
                        (int(end_ax), int(end_ay)),
                        (
                            int(
                                end_ax
                                - self.ARROWHEAD_SIZE
                                * math.cos(
                                    math.atan2(
                                        -self.acceleration[1], self.acceleration[0]
                                    )
                                    + math.pi / 6
                                )
                            ),
                            int(
                                end_ay
                                + 4
                                * math.sin(
                                    math.atan2(
                                        -self.acceleration[1], self.acceleration[0]
                                    )
                                    + self.ARROWHEAD_ANGLE
                                )
                            ),
                        ),
                        (
                            int(
                                end_ax
                                - self.ARROWHEAD_SIZE
                                * math.cos(
                                    math.atan2(
                                        -self.acceleration[1], self.acceleration[0]
                                    )
                                    - math.pi / 6
                                )
                            ),
                            int(
                                end_ay
                                + 4
                                * math.sin(
                                    math.atan2(
                                        -self.acceleration[1], self.acceleration[0]
                                    )
                                    - self.ARROWHEAD_ANGLE
                                )
                            ),
                        ),
                    ],
                )

        # Display status text
        status_text = f"Ball: Pos=({self.position[0]:.2f}, {self.position[1]:.2f}) ,Vel=({self.velocity[0]:.2f}, {self.velocity[1]:.2f}), Acc=({self.acceleration[0]:.2f}, {self.acceleration[1]:.2f})"
        text_surf = font.render(status_text, True, (0, 0, 0))
        screen.blit(text_surf, (text_x, text_y + 20))
