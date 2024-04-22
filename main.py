"""
Main module for launching and running the ball launcher simulation.

This module imports and utilizes the Simulation class from the simulation
module to initialize and run a simulation environment for a ball launcher
system. It is designed to be the entry point of the application, where the
simulation is set up and executed.

Attributes:
    Simulation (class): A class imported from simulation module that manages 
        the simulation setup and execution.
"""

from simulation import Simulation


def main():
    """
    Main entry function for the simulation application.

    Initializes an instance of the Simulation class and starts the simulation
    process. This function serves as the starting point for the simulation
    execution, setting up the necessary environment and entering the main
    event loop ofthe simulation.
    """
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()
