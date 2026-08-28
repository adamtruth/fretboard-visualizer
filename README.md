# Fretboard Visualizer

A Guitar Fretboard Visualizer in Python.

GUI: [tkinter](https://docs.python.org/3/library/tkinter.html)

Shape Rendering: [pillow](https://pypi.org/project/pillow/)

## Prerequisites

`tkinter` requires a Python built against Tcl/Tk — it can't be installed via pip, so pick
one of the setups below. Whichever you use, `make run` just runs `python3 ./src/main.py`,
so it works as long as `python3` on your `PATH` resolves to an interpreter with `tkinter`
and `pillow` available.

### Option 1: Nix (recommended)
```bash
nix develop
```
This drops you into a shell with `tkinter` and `pillow` already available — nothing else to install.

### Option 2: Plain pip + venv
```bash
sudo apt install python3-tk      # Debian/Ubuntu; dnf/pacman/brew equivalents also work
python3 -m venv .venv
source .venv/bin/activate
pip install pillow
```

### Option 3: uv
`uv`'s own downloaded interpreters generally don't have working `tkinter` support on Linux,
so point it at your system Python instead and give the venv access to its site-packages:
```bash
sudo apt install python3-tk
cd src
uv venv --system-site-packages --python $(which python3)
uv sync --active
source .venv/bin/activate
cd ..
```

## Usage
```bash
git clone https://github.com/adamtruth/fretboard-visualizer.git
cd fretboard-visualizer/
make run
```

## TODO
* Make the modules Object-Oriented (currently procedural)
* Swap out Tkinter with something more modern, such as PyQt
* Mode to draw notes on the fretboard and determine chords similar to [this](https://www.oolimo.com/en/guitar-chords/analyze).
* Might create a piano visualizer from the note logic I've already created here.
