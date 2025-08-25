# Dark Ages Presenter

A Python application that automatically sends keystrokes from a text file to X.org windows containing "dark ages" in their class name.

## Features

- Automatically finds Dark Ages windows by class name
- Sends text character by character with configurable delay
- Pause/resume functionality with spacebar
- Command-line interface
- UTF-8 text file support

## Setup

1. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

## Usage

```bash
python main.py <text_file> [--delay <seconds>]
```

### Arguments

- `text_file`: Path to the text file containing content to type
- `--delay`: Delay between keystrokes in seconds (default: 0.1)

### Examples

```bash
# Basic usage
python main.py example.txt

# With custom delay
python main.py my_script.txt --delay 0.05
```

## Controls

- **Spacebar**: Pause/resume typing
- **Ctrl+C**: Stop the program

## Requirements

- Linux with X.org
- Python 3.6+
- Dark Ages window must be running and visible

## Dependencies

- `python-xlib`: For X11 window management
- `pynput`: For keyboard input detection
```

This project provides:

1. **Window Detection**: Automatically finds windows with "dark ages" in the class name
2. **Text File Input**: Reads any UTF-8 text file specified via command line
3. **Keystroke Simulation**: Sends characters one by one to the target window
4. **Pause/Resume**: Press spacebar to pause/resume typing
5. **Configurable Delay**: Adjust typing speed with `--delay` parameter

To use:

1. Run `chmod +x setup.sh && ./setup.sh` to set up the environment
2. Activate with `source venv/bin/activate`
3. Run with `python main.py your_text_file.txt`

The program will search for Dark Ages windows, load your text file, give you a 3-second countdown, then start typing. Press spacebar anytime to pause/resume.
