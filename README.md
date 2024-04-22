# Ball Launcher Simulator README

## Overview

The Ball Launcher Simulator is a Python-based simulation designed for Standard Bots as part of the software and hardware development process for a new ball launcher product. This simulator allows you to model launch distances based on various parameters such as starting angle, motor torque, and ball release angle. It assists the software team in aiming for specific travel distances and the hardware team in selecting appropriate motor specifications.

## Installation

To run the simulator, you will need Python and several libraries. Here are the steps to set up your environment:

### Prerequisites

- Python 3.8 or higher
- `pygame` library
- `pygame_gui` library
- `numpy` library
- `matplotlib` library for plotting (optional)

### Setting Up Your Environment

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/downloads/).

2. **Install Libraries**: Open your command line interface (CLI) and install the required libraries using pip:

   ```bash
   pip install pygame pygame_gui numpy matplotlib
   ```

## Running the Simulator

Once you have installed the necessary software, you can run the simulation by following these steps:

1. **Navigate to the Project Directory**: Use the command line to navigate to the folder containing the simulator files.

2. **Run the Simulation**:
   - Execute the `main.py` file using Python:

   ```bash
   python main.py
   ```

   This command launches the GUI for the Ball Launcher Simulator.

## Using the Simulator

The GUI provides various controls to interact with the simulation:

- **Torque Slider**: Adjusts the torque applied by the motor.
- **Launch Angle Slider**: Sets the initial angle of the launcher arm.
- **Release Angle Slider**: Configures the angle at which the ball is released.
- **Angular Velocity Slider**: Controls the maximum angular velocity of the launcher arm.
- **Drag Coefficient Slider**: Alters the drag coefficient of the ball.
- **Spin Rate Slider**: Modifies the spin rate of the ball, affecting its trajectory.
- **Air Density Slider**: Changes the air density, which influences drag calculations.

### Buttons

- **Run Simulation**: Starts the simulation with the current settings.
- **Reset Simulation**: Resets all settings to their default values and prepares the system for a new simulation run.

## Output

The simulation visually represents the trajectory of the ball based on the input parameters. Adjustments to the sliders update the trajectory in real-time, allowing for immediate feedback on how changes affect the ball's path.

## Further Development

For those looking to extend this project or use it as a foundation for more complex simulations, consider adding features such as:

- **Parameter Optimization**: Implement algorithms to automatically adjust parameters to achieve desired launch distances.
- **Data Logging**: Add functionality to log simulation data for further analysis.
- **Enhanced Visualizations**: Integrate more detailed graphical representations of the trajectory and other physics-related data.

## Conclusion

This simulator serves as a practical tool for understanding and demonstrating the dynamics of a ball launcher. It provides valuable insights into how various parameters influence the performance of the launcher, aiding both software and hardware teams in their development processes.