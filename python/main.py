# import Chord
# import Notes
# import time
import json
from PIL import Image, ImageDraw

notes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
accidental = {'flat': 'b', 'sharp': '#'}

FRET_COUNT = 12
STRING_COUNT = 6
STRING_NOTES = ['E', 'A', 'D', 'G', 'B', 'E']
COLORS = ["red", "orange", "yellow",
          "green", "aqua", "blue", "navy", "purple"]

diatonic_notes = []
accidental_notes = []

# GUI-related Globals
window_title = 'Fretboard Visualizer'
image_path = 'assets/fretboard.png'
image = Image.open(image_path)
screen_resolution = (3456, 2090)  # current resolution
draw = ImageDraw.Draw(image)

# Circle attributes
# x_i, y_i = 55, 40  # Initial starting location of the (Open low E string)
# x_bar, y_bar = 45, 120  # Distance between frets (x) and STRING_COUNT (y)
x_i, y_i = 45, 97  # Initial starting location of the (Open low E string)
x_bar, y_bar = 120, 45  # Distance between frets (x) and STRING_COUNT (y)
r = 15  # radius
x_offset, y_offset = 10, 10  # offset delta string/fret distances


def generate_diatonic_notes(accidental_type: str) -> list:
    for note in range(len(notes)):
        if accidental_type == 'flat':
            # Shift the accidentals list by one element
            # preventing the ordering A Ab B Bb...
            reorder = notes[1:] + notes[:1]
            accidental_notes.append(
                    reorder[note] + accidental[accidental_type])

        # Append the sharp to each element in the list
        if accidental_type == 'sharp':
            accidental_notes.append(notes[note] + accidental[accidental_type])

        # Add the natural note
        diatonic_notes.append(notes[note])
        # Then add the appropriate accidental note
        diatonic_notes.append(accidental_notes[note])

    # Remove enharmonic notes (notes that should be skipped)
    if accidental_type == 'sharp':
        diatonic_notes.remove('E#')
        diatonic_notes.remove('B#')

    if accidental_type == 'flat':
        diatonic_notes.remove('Fb')
        diatonic_notes.remove('Cb')

    return diatonic_notes


def order_diatonic_notes(start_note: int, frets: int) -> list:
    ''' Order notes starting with the given start_note
        @param1: start_note: where we begin the list of notes (or tonal center)
        @param2: frets: the number of frets we are working with
    '''
    ordered_notes = []

    for i in range(frets + 1):
        # circularly linked list using modulo %
        circular_idx = (i+start_note) % len(diatonic_notes)
        # Append notes starting at the circular_idx
        ordered_notes.append(diatonic_notes[circular_idx])

    return ordered_notes


def get_start_note_id(note: str) -> int:
    ''' Returns the starting index
        of a given note.
        @param1 - note: the note we would like to find the index of
    '''
    # The index for the chosen note
    id = diatonic_notes.index(note)
    return id


def create_fretboard(STRING_COUNT: int, STRING_NOTES: list) -> list:
    ''' Create a nested list with all notes on the fretboard '''
    fretboard = []
    for string in range(STRING_COUNT):
        note_id = get_start_note_id(STRING_NOTES[string])  # int
        ordered_notes = order_diatonic_notes(note_id, FRET_COUNT)  # list

        # Appends the ordered_notes list to fretboard list
        fretboard.append(ordered_notes)

    return fretboard


def get_note_idx(fretboard: list, note: str) -> dict:
    ''' Returns a dict of a single note and its positions on the fretboard. '''
    positions = []
    note_positions = {}

    # This nested list was tricky
    # We are iterating through the frets and the STRING_COUNT.
    # i := string index (0: E string)
    # j := fret index (0: Open string)
    # So [i][j] is the [string_index][fret_index]
    for string_idx in range(len(fretboard)):
        for fret_idx in range(len(fretboard[string_idx])):
            if fretboard[string_idx][fret_idx] == note:
                positions.append((string_idx, fret_idx))

    # mapping the list of lists to the dict
    note_positions = {note: positions}

    return note_positions


def get_fretboard(fretboard: list) -> dict:
    ''' Returns a dict of all notes
        and their respective indices on the fretboard.
    '''
    note_dict = {}
    for note in range(len(diatonic_notes)):
        # Combine note_dict with each iteration using the intersection operator
        note_dict = note_dict | get_note_idx(fretboard, diatonic_notes[note])

    return note_dict


def map_fretboard_notes(note_dict):
    '''
    @param1: the note dict with all fretboard positions
    @param2: x position of the F note low E string
    @param3: y position of the F note on the low E string
    '''
    note_positions = {}
    x_offset = 0
    for i in range(len(diatonic_notes)):
        fret_positions = note_dict.get(diatonic_notes[i])  # all lists

        positions = []

        for j in range(len(fret_positions)):
            frets = fret_positions[j]  # all tuples
            x_pos, y_pos = None, None

            for k in range(len(frets)):
                fret_number = frets[k]  # accessing the tuple indices

                if fret_number >= 1 and k == 1:
                    shift = 48  # lessen the the distance between fret 0 and 1
                else:
                    shift = 0

                # if fret_number <= 8 and k == 1:
                #     x_offset -= 2

                if k == 0:  # k=0 is string
                    y_pos = y_i + ((fret_number-1) * y_bar)
                if k == 1:  # k=1 is fret
                    x_pos = x_i + (fret_number * x_bar) - shift - x_offset

            circle_coord = (x_pos, y_pos)
            positions.append(circle_coord)
        note_positions[diatonic_notes[i]] = positions
    return note_positions


def format_json(note_dict) -> dict:
    ''' Returns a formatted dict that newlines after each key-value pair. '''
    lines = []
    for key, value in note_dict.items():
        k = json.dumps(key)
        v = json.dumps(value)
        lines.append(f'    {k}: {v}')
    custom_json = "{\n" + ",\n".join(lines) + "\n}"

    return custom_json


class Circle():
    def __init__(self, x, y, r, color="red"):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def drawCircle(self):
        draw.circle(
                (self.x - self.r,
                 self.y - self.r,
                 self.x + self.r,
                 self.y + self.r),
                self.r,
                fill=self.color, outline=None, width=1)


def display_image(note_positions) -> None:
    # array of colors to select from

    for i in range(len(diatonic_notes)):  # 12
        notes_lists = note_positions.get(diatonic_notes[i])  # all lists
        # print(f'{i}: {notes_lists}')

        for j in range(len(notes_lists)):  # 6
            position = notes_lists[j]  # all tuples

            # Describe circle attributes for PIL to draw
            circle_attr = Circle(position[0], position[1], r, COLORS[4])
            Circle.drawCircle(circle_attr)

    image.show()


def main():
    # Set the preferred accidental
    accidental_type = 'sharp'

    # Generate diatonic notes with accidentals
    generate_diatonic_notes(accidental_type)

    # Create fretboard grid as a list
    fretboard = create_fretboard(STRING_COUNT, STRING_NOTES)

    # Get a dict of all notes/positions
    note_dict = get_fretboard(fretboard)
    # print(format_json(note_dict))

    note_positions = map_fretboard_notes(note_dict)
    # print(format_json(note_positions))
    display_image(note_positions)


if __name__ == "__main__":
    main()
