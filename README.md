# Milo

Milo is a fun, interactive Python application that creates a floating snake animation on your screen. The snake follows your mouse cursor, creating a mesmerizing visual effect with smoothly changing colors.

## Features

- **Floating Snake**: A snake composed of segments that smoothly follow your mouse cursor.
- **Dynamic Colors**: Each segment of the snake changes color over time using HSV color blending.
- **Full-Screen Experience**: Runs in a transparent, borderless window covering the entire screen.
- **Interactive Popup**: Starts with a friendly greeting popup to launch the snake or quit.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)
- Windows OS (uses Windows-specific APIs for cursor position and screen metrics)

## Installation

1. Clone or download the repository.
2. Ensure Python is installed on your system.

## Usage

Run the script directly:

```bash
python milo.py
```

A popup window will appear. Click "Play 🐍" to start the snake animation. The snake will follow your mouse cursor across the screen.

To stop the animation, close the window or use your system's task manager.

## Building an Executable

The project includes a PyInstaller spec file (`milo.spec`) for building a standalone executable.

To build:

1. Install PyInstaller if not already installed:
   ```bash
   pip install pyinstaller
   ```

2. Run PyInstaller with the spec file:
   ```bash
   pyinstaller milo.spec
   ```

The executable will be created in the `dist/` folder.

## Customization

You can modify various parameters in the script to customize the behavior:

- `snake_length`: Number of segments in the snake.
- `segment_char`: Character used for each segment (default: "*").
- `move_speed`, `float_speed`, `inertia`: Control movement dynamics.
- `color_blend_speed`, `target_change_speed`: Control color changing behavior.

## Troubleshooting

- If the script doesn't run, ensure Python and Tkinter are properly installed.
- The application is designed for Windows; it may not work on other operating systems due to Windows-specific API calls.
- If the window doesn't appear transparent, check your system's graphics settings.

## License

This project is for educational and entertainment purposes. Feel free to modify and distribute.