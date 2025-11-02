import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QImage
import cairo
from plot import draw_fretboard
from mingus.core import notes, scales
from config import scale_colors

# Build fretboard data
tuning = ['E', 'A', 'D', 'G', 'B', 'E']
num_frets = 18
root = 'A'
scale_type = 'major'

# Sharp/flat conversion (user preference)
useFlats = False
sharp_to_flat = {
        'C#':'Db',
        'D#':'Eb',
        'F#':'Gb',
        'G#':'Ab',
        'A#':'Bb' }

def to_flat(note):
    base_note = ''.join(filter(str.isalpha, note)).upper()
    return sharp_to_flat.get(base_note, base_note)

def note_at_fret(open_note, fret):
    base_note = ''.join(filter(str.isalpha, open_note)).upper()
    return notes.int_to_note((notes.note_to_int(base_note) + fret) % 12)

# Get scale notes
if scale_type.lower() == 'major':
    scale_notes = scales.Major(root).ascending()
elif scale_type.lower() == 'minor':
    scale_notes = scales.NaturalMinor(root).ascending()
else:
    raise ValueError("Unsupported scale type")

if useFlats:
    scale_notes = [to_flat(n) for n in scale_notes]

# Build fretboard
if useFlats:
    fretboard = [[to_flat(note_at_fret(s, f)) for f in range(num_frets + 1)] for s in tuning]
else:
    fretboard = [[note_at_fret(s, f) for f in range(num_frets + 1)] for s in tuning]

# Map note -> scale degree
degree_map = {note: deg for deg, note in enumerate(scale_notes, start=1)}

# PyQt6 widget
class FretboardWidget(QWidget):
    def __init__(self, fretboard, tuning, degree_map, root, scale_type, num_frets=18):
        super().__init__()
        self.fretboard = fretboard
        self.tuning = tuning
        self.degree_map = degree_map
        self.root = root
        self.scale_type = scale_type
        self.num_frets = num_frets

    def _cairo_to_qimage(self, surface):
        width = surface.get_width()
        height = surface.get_height()
        data = surface.get_data()
        return QImage(data, width, height, QImage.Format.Format_ARGB32)

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        # Draw fretboard using plot.py
        draw_fretboard(
            ctx=ctx,
            width=width,
            height=height,
            fretboard=self.fretboard,
            tuning=self.tuning,
            num_frets=self.num_frets,
            degree_map=self.degree_map,
            root=self.root,
            scale_type=self.scale_type
        )

        painter = QPainter(self)
        qimage = self._cairo_to_qimage(surface)
        painter.drawImage(0, 0, qimage)
        painter.end()

# Main window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fretboard (PyQt + Cairo)")
        self.resize(1000, 300)

        self.fretboard_widget = FretboardWidget(
            fretboard=fretboard,
            tuning=tuning,
            degree_map=degree_map,
            root=root,
            scale_type=scale_type,
            num_frets=num_frets
        )
        self.fretboard_widget.setParent(self)
        self.fretboard_widget.setGeometry(0, 0, self.width(), self.height())

# Run app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

