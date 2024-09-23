# Set Up for SMARTERS

This project provides a setup tool for configuring and initializing SMARTERS, an Autonomous Robot Simulator. It allows users to define the simulation environment, robot parameters, and other settings before running the main simulator application.

## Main Features

### Robot Configuration

- Selection of predefined robot types or manual configuration of parameters:
  - Autonomy
  - Speed
  - Cutting diameter

- Predefined list of robot types:
  - Husqvarna Automower 450X
  - Husqvarna Automower 405X  
  - Husqvarna Automower 415X
  - Husqvarna Automower 430X

- Movement modes: systematic or random
- Bounce modes: ping pong or random

### Simulation Configuration

- Set simulation runtime duration in minutes
- Define square tile size for dividing the simulation field
- Specify number of maps to create
- Number of simulation repetitions on each map

### Environment Configuration

- Configure through forms or drawing
- Field simulation characteristics:
  - Length and width
  - Blocked areas (square or circular)
  - Isolated areas

### GUI Output

The output generated by the GUI is produced in JSON format, containing all the information configured through the graphical interface.

## Extensions and Personalization

The simulator supports extensions through Python files implementing the MovementPlugin class. These files can be loaded directly via the graphical interface or inserted into the Plugin folder of the project.

## License

This project is distributed under Apache license. For details on the license, please consult the LICENSE file included in the repository.
