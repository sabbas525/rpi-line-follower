# rpi-line-follower

A Python-based robot controller that uses computer vision to follow a line. Fully simulated — no hardware needed.

## Background

During my bachelor's degree, I built a line-following robot car for the DLD course project using hardware components. This repo is a software simulation of the same concept, built to revisit and extend that work using Python, OpenCV, and Pygame.

## Tech Stack

- Python 3.11+, OpenCV, Pygame, NumPy

## Setup & Installation

```bash
# Clone the repo
git clone https://github.com/sabbas525/rpi-line-follower.git
cd rpi-line-follower

# Install dependencies
pip install -r requirements.txt

# Generate the synthetic track video
python tracks/generate_track.py
```

## Usage

```bash
# Run with Pygame visualization
python src/main.py --simulate

# Run with a specific video file
python src/main.py --video tracks/track1.mp4 --simulate

# Log steering decisions to CSV
python src/main.py --log output.csv

# Adjust proportional gain
python src/main.py --kp 0.8 --simulate

# Headless mode (no display, logging only)
python src/main.py --headless --log output.csv
```

## Project Structure

```
rpi-line-follower/
  src/
    vision.py        # Frame processing, line detection
    controller.py    # Proportional steering logic
    simulator.py     # Pygame visualization
    main.py          # Entry point, CLI args
  tracks/
    generate_track.py  # Generates synthetic track video
  tests/
    test_vision.py
    test_controller.py
  requirements.txt
  requirements-dev.txt
```

## Running Tests

```bash
pip install -r requirements-dev.txt
PYTHONPATH=. pytest
```
