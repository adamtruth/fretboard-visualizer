# Fretboard Visualizer

A Guitar Fretboard Visualizer in Python.

Package Manager: [uv](https://docs.astral.sh/uv/)

GUI: [tkinter](https://docs.python.org/3/library/tkinter.html)

Shape Rendering: [pillow](https://pypi.org/project/pillow/)

## Prequisites

Install the `uv` package manager.

### MacOS
Homebrew Installation
```bash
brew install uv
```

## Usage
```bash
git clone https://github.com/adamtruth/fretboard-visualizer.git
cd fretboard-visualizer/
uv sync
make
```

## TODO
* Make the modules Object-Oriented (currently procedural)
* Swap out Tkinter with something more modern, such as PyQt
* Mode to draw notes on the fretboard and determine chords similar to [this](https://www.oolimo.com/en/guitar-chords/analyze).
* Might create a piano visualizer from the note logic I've already created here.
