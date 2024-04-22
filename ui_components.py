"""
UI Components

This module defines the UIComponents class, which is responsible for managing
the user interface in a Pygame and Pygame GUI-based simulation environment.
The class facilitates interactive control over simulation parameters such as
torque, launch angles, and speed, which are essential for a launcher mechanism
in mechanical system simulations. It simplifies the complexities associated
with GUI management by utilizing the pygame_gui library for event handling and
UI rendering.
"""

import pygame
import pygame_gui
import math


class UIComponents:
    """
    Manages UI components within a simulation environment, leveraging Pygame
    and Pygame GUI to handle user interactions and display controls.

    Attributes:
        sliders (dict): Stores slider widgets and their associated value
            labels for controlling simulation parameters.
        descriptions (dict): Maps slider identifiers to their descriptive
            labels to clarify their functions.
        manager (pygame_gui.UIManager): Manages and organizes UI elements
            within the Pygame GUI framework.
        screen_size (tuple): Current dimensions of the display window, which        influence the positioning of UI elements.
    """

    def __init__(self, manager, screen_size):
        """
        Initializes a new UIComponents instance, setting up the Pygame GUI
        environment and preparing UI elements.

        Parameters:
            manager (pygame_gui.UIManager): The UI manager responsible for
                handling Pygame GUI elements.
            screen_size (tuple): Initial dimensions of the application window
                used for layout calculations.
        """
        self.sliders = {}
        self.descriptions = {}
        self.manager = manager
        self.screen_size = screen_size
        self.init_constants()
        self.init_ui_elements()

    def init_constants(self):
        """
        Sets up constant values used throughout the UI such as dimensions and
        spacing for sliders and buttons.
        """
        self.font = pygame.font.SysFont(None, 24)
        self.slider_width = 150
        self.slider_height = 40
        self.label_width = 100
        self.left_align_x = self.screen_size[0] // 40
        self.vertical_start_y = 75
        self.vertical_spacing = self.screen_size[1] // 12
        self.button_width = self.slider_width + 2 * self.label_width
        self.button_height = 40
        self.button_vertical_offset = 180

    def init_ui_elements(self):
        """
        Creates and initializes the UI components including sliders and
        buttons necessary for simulation control.
        """
        self.create_sliders()
        self.create_buttons()

    def create_sliders(self):
        """
        Constructs sliders for adjusting simulation parameters and links them
        with descriptive labels.
        """
        slider_info = {
            "torque": ("Torque (Nm)", 0.0, 2.0, "0 Nm"),
            "launch_angle": ("Launch Angle (rad)", 0.0, 2.0 * math.pi, "0 rad"),
            "release_angle": ("Release Angle (rad)", 0.0, 2.0 * math.pi, "0 rad"),
            "speed": ("Angular Velocity (rad/s)", 0.0, 20.0, "0 rad/s"),
            "drag_coefficient": (
                "Drag Coefficient",
                0.1,
                0.6,
                "0.47",
            ),
            "spin_rate": (
                "Spin Rate (rad/s)",
                0.0,
                100.0,
                "0 rad/s",
            ),
            "air_density": (
                "Air Density (kg/m³)",
                1.0,
                1.3,
                "1.225 kg/m³",
            ),
        }
        for key, (label, min_val, max_val, initial_text) in slider_info.items():
            y_pos = self.vertical_start_y + len(self.sliders) * self.vertical_spacing
            slider, value_label = self.create_slider_with_label(
                label, min_val, max_val, initial_text, y_pos
            )
            self.sliders[key] = (
                slider,
                value_label,
            )
            self.descriptions[key] = label

    def create_slider_with_label(
        self, text, start_value, max_value, value_text, y_position
    ):
        """
        Generates a slider with an associated label and value label, arranging
        them vertically based on the provided position.

        Parameters:
            text (str): Description of what the slider controls.
            start_value (float): Minimum value for the slider.
            max_value (float): Maximum value for the slider.
            value_text (str): Initial text displayed next to the slider,
                typically showing the value.
            y_position (int): Vertical start position for the slider on the
                screen.

        Returns:
            tuple: A tuple containing the slider and its corresponding value
                label.
        """
        label_height = self.slider_height
        slider_y_position = y_position + (label_height // 2)

        label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (self.left_align_x, y_position),
                (self.label_width, label_height),
            ),
            text=text.split(" (")[0],
            manager=self.manager,
        )
        slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (self.left_align_x + self.label_width + 10, slider_y_position),
                (self.slider_width, self.slider_height),
            ),
            start_value=start_value,
            value_range=(start_value, max_value),
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@slider"),
        )
        value_label_width = 100
        value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (
                    self.left_align_x + self.label_width + self.slider_width + 20,
                    slider_y_position,
                ),
                (value_label_width, self.slider_height),
            ),
            text=value_text,
            manager=self.manager,
        )
        return slider, value_label

    def create_buttons(self):
        """
        Creates button components for controlling the simulation (e.g.,
        running and resetting).
        """
        self.run_button = self.create_button(
            "Run Simulation",
            self.vertical_start_y
            + 4 * self.vertical_spacing
            + self.button_vertical_offset,
        )
        self.reset_button = self.create_button(
            "Reset Simulation",
            self.vertical_start_y
            + 5 * self.vertical_spacing
            + self.button_vertical_offset,
        )
        self.reset_button.disable()

    def create_button(self, text, y_position):
        """
        Creates a single button with specified text and position.

        Parameters:
            text (str): The text to display on the button.
            y_position (int): The vertical position for the button in the
                window.

        Returns:
            UIButton: The created button object.
        """
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.left_align_x, y_position), (self.button_width, self.button_height)
            ),
            text=text,
            manager=self.manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button"),
        )
        return button

    def reset_controls(self):
        """
        Resets all sliders to their initial values and updates their
        associated labels accordingly.
        """
        for key, slider in self.sliders.items():
            initial_value = slider[0].value_range[0]
            slider[0].set_current_value(initial_value)
            description = self.descriptions[key]
            unit = self.extract_unit(description)
            formatted_value = self.pi_formatter(initial_value, unit)
            value_label = self.sliders[key][1]
            value_label.set_text(formatted_value)

    def extract_unit(self, description):
        """
        Extracts the unit from a slider description.

        Parameters:
            description (str): The description from which to extract the unit.

        Returns:
            str: The extracted unit, including a leading space for separation.
        """
        parts = description.split("(")
        if len(parts) > 1 and len(parts[1].strip()):
            return " " + parts[1].strip().split()[-1][:-1]
        return ""

    def toggle_controls(self, enable=True):
        """
        Toggles the enable/disable state of all controls based on the
        specified flag.

        Parameters:
            enable (bool): True to enable the controls, False to disable them.
        """
        method = "enable" if enable else "disable"
        for _, (slider, _) in self.sliders.items():
            getattr(slider, method)()

        getattr(self.run_button, method)()
        if not enable:
            self.reset_button.enable()
        else:
            self.reset_button.disable()

    def start_simulation(self):
        """
        Handles actions to start the simulation, such as disabling certain
        controls.
        """
        self.toggle_controls(False)

    def reset_simulation(self):
        """
        Handles actions to reset the simulation, including enabling controls
        and resetting sliders.
        """
        self.toggle_controls(True)
        self.reset_controls()

    def pi_formatter(self, value, unit):
        """
        Formats values as multiples of pi if they are proportional to pi.

        Parameters:
            value (float): The value to format.
            unit (str): The unit associated with the value.

        Returns:
            str: The formatted string with pi notation if applicable.
        """
        if "rad" in unit:
            value /= math.pi
            if value == int(value):
                return f"{int(value)}π {unit}" if value != 1 else f"π {unit}"
            return f"{value:.2f}π {unit}"
        return f"{value:.3f} {unit}"

    def handle_events(self, event):
        """
        Handles incoming Pygame events related to UI components, such as resizing and slider movements.

        Parameters:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.VIDEORESIZE:
            self.screen_size = (event.w, event.h)
            self.update_ui_elements()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element in [slider for slider, _ in self.sliders.values()]:
                    for key, (slider, value_label) in self.sliders.items():
                        if slider == event.ui_element:
                            unit = self.extract_unit(self.descriptions[key])
                            new_value = slider.get_current_value()
                            formatted_value = self.pi_formatter(new_value, unit)
                            value_label.set_text(formatted_value)
                            break

    def update_ui_elements(self):
        """
        Updates positions and sizes of all UI elements based on the current screen size.
        """
        for key, (slider, value_label) in self.sliders.items():
            y_pos = (
                self.vertical_start_y
                + list(self.sliders.keys()).index(key) * self.vertical_spacing
            )
            slider.relative_rect.x = self.left_align_x + self.label_width + 10
            slider.relative_rect.y = y_pos
            slider.relative_rect.width = self.slider_width
            slider.rebuild()
            value_label.relative_rect.x = (
                self.left_align_x + self.label_width + self.slider_width + 20
            )
            value_label.relative_rect.y = y_pos
            value_label.rebuild()

        y_pos_run = (
            self.vertical_start_y
            + 4 * self.vertical_spacing
            + self.button_vertical_offset
        )
        self.run_button.relative_rect.y = y_pos_run
        self.run_button.rebuild()

        y_pos_reset = (
            self.vertical_start_y
            + 5 * self.vertical_spacing
            + self.button_vertical_offset
        )
        self.reset_button.relative_rect.y = y_pos_reset
        self.reset_button.rebuild()
