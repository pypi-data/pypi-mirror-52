# North Robotics `north_manager`

The `north_manager` utility is a command line and GUI application for managing and configuring North Robotics devices.
Currently it can check and update firmware on North Robotics C9 controllers.

## Installation

The CLI and UI can be installed with pip:

      $ pip install north-manager

## UI

The GUI can be launched by running:

      $ north_manager ui

## CLI

Along with a GUI, there is also a command line interface available.

### `north_manager firmware.info`

Prints information about connected devices, including firmware version and COM port.

### `north_manager firmware.list-versions <model>`

Prints all available firmware versions for the given controller model (Eg. `n9`, `spin`, `dev`).

### `north_manager firmware.update`

Updates firmware to latest version on any connected controllers.