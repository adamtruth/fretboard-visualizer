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
interval = {}

# GUI-related Globals
window_title = 'Fretboard Visualizer'
image_path = 'assets/fretboard.png'
image = Image.open(image_path)
screen_resolution = (3456, 2090)  # current resolution
draw = ImageDraw.Draw(image)

# Circle attributes

# Initial starting location (Open low E string)
x_i, y_i = 45, 52
# Distance between frets (x) and STRING_COUNT (y)
x_bar, y_bar = 120, 45
# radius
r = 15
# offset delta string/fret distances
x_offset, y_offset = 10, 10

chord_types = ['major', 'minor']


def get_intervals(diatonic_notes, key):
    intervals = ['root', 'm2', 'M2', 'm3', 'M3',
                 'P4', 'tritone', 'P5', 'm6', 'M6', 'm7', 'M7']
    start_note = get_starting_note(key)
    for i in range(len(diatonic_notes)):
        # TODO: Reusing circular_idx, turn into function
        circular_idx = (i+start_note) % len(diatonic_notes)
        interval[intervals[i]] = diatonic_notes[circular_idx]

    return interval


class Chord:
    def __init__(self, root, chord_type):
        self.root = root
        self.chord_type = chord_type


def create_chord(chord_type, interval):
    chord = []
    for chord_type in chord_types:
        if chord_type == 'major':
            chord = [interval['root'], interval['M3'], interval['P5']]
            return chord
        if chord_type == 'minor':
            chord = [interval['root'], interval['m3'], interval['P5']]
            return chord


def generate_diatonic_notes(accidental_type: str) -> list:
    ''' Returns diatonic notes (including specified accidentals). '''
    for note in range(len(notes)):
        if accidental == 'flat':
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


def get_starting_note(note: str) -> int:
    ''' Returns the starting index
        of a given note.
        @param1 - note: the note we would like to find the index of
    '''
    # The index (int) for the chosen note
    return diatonic_notes.index(note)


def order_diatonic_notes(start_note: int) -> list:
    ''' Order notes starting with the given start_note
        @param1: start_note: where we begin the list of notes (or tonal center)
        @param2: frets: the number of frets we are working with
    '''
    ordered_notes = []

    for i in range(FRET_COUNT + 1):
        # circularly linked list using modulo %
        # Append notes starting at the circular_idx
        circular_idx = (i+start_note) % len(diatonic_notes)
        ordered_notes.append(diatonic_notes[circular_idx])

    return ordered_notes


def set_fretboard_notes(STRING_COUNT: int, STRING_NOTES: list) -> list:
    ''' Create a nested list with all notes on the fretboard '''
    fretboard_notes = []

    # We reverse the E,A,D,G,B,E because the index 0,0 is the low E string
    # thus it's flipped. So either we flip the indices so high E is 0,0
    # or we just flip the string_notes
    string_notes = STRING_NOTES[::-1]

    for string in range(STRING_COUNT):
        note = get_starting_note(string_notes[string])  # int
        ordered_notes = order_diatonic_notes(note)  # list

        # Appends the ordered_notes list to fretboard list
        fretboard_notes.append(ordered_notes)

    return fretboard_notes


def get_fret_positions(fretboard: list, note: str) -> dict:
    ''' Returns a dict with key as note
        and values positions on the fretboard.
        e.g. E: [(0,0), (2, 5), (3,2), ...]
    '''
    positions = []
    fret_positions = {}

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
    fret_positions = {note: positions}

    return fret_positions


def get_fretboard_notes(fret_positions) -> dict:
    ''' Returns a dict of all notes
        and their respective indices on the fretboard.
    '''
    fretboard = {}
    for note in range(len(diatonic_notes)):
        # Combine fretboard with each iteration using the intersection operator
        fretboard = fretboard | get_fret_positions(
                fret_positions, diatonic_notes[note])

    return fretboard


def map_fretboard_notes(fretboard_notes):
    ''' Maps each note to a coordinate on the fretboard. '''
    note_map = {}
    x_offset = 0
    # for i in range(len(diatonic_notes)):
    for note in range(len(diatonic_notes)):
        fret_positions = fretboard_notes.get(diatonic_notes[note])  # all lists

        positions = []

        for fret in range(len(fret_positions)):
            frets = fret_positions[fret]  # all tuples

            x_pos, y_pos = None, None

            for k in range(len(frets)):
                fret_number = frets[k]  # accessing the tuple indices
                x_offset = 0
                # lessen the the distance between fret 0 and 1
                if k == 1:
                    if fret_number == 1:
                        x_offset = 46
                    elif fret_number > 1 and fret_number <= 9:
                        x_offset += 49
                    elif fret_number > 9 and fret_number <= 11:
                        x_offset += 77
                    elif fret_number >= 12:
                        x_offset += 85

                if k == 0:  # k=0 is string
                    y_pos = y_i + (fret_number * y_bar)
                if k == 1:  # k=1 is fret
                    x_pos = x_i + (fret_number * x_bar) - x_offset

            note_position = ((x_pos, y_pos))
            positions.append(note_position)

        note_map[diatonic_notes[note]] = positions
        # print(f'{fret_number}: {x_offset}')

    return note_map


# Helper function to format dictionaries with newlines
def format_json(fretboard) -> dict:
    ''' Returns a formatted dict that newlines after each key-value pair. '''
    lines = []
    for key, value in fretboard.items():
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


def display_image(note_map, notes: list) -> None:
    for i in range(len(notes)):  # 12
        notes_lists = note_map.get(notes[i])  # all lists

        for j in range(len(notes_lists)):  # 6
            position = notes_lists[j]  # all tuples

            # Describe circle attributes for PIL to draw
            circle_attr = Circle(position[0], position[1], r, COLORS[i])
            Circle.drawCircle(circle_attr)

    # image.show()


def main():
    selected_root = 'E'

    # Set the preferred accidental
    accidental = 'sharp'

    # Generate diatonic notes with accidentals
    generate_diatonic_notes(accidental)

    # Create fretboard grid as a list
    notes = set_fretboard_notes(STRING_COUNT, STRING_NOTES)

    # Get a dict of all notes/positions
    fretboard = get_fretboard_notes(notes)

    # Coordinates of all fretboard notes
    note_map = map_fretboard_notes(fretboard)

    selected_notes = ['G', 'A#', 'D']
    display_image(note_map, selected_notes)

    get_intervals(diatonic_notes, selected_root)
    chord2 = create_chord('major', interval)
    chord1 = create_chord('minor', interval)
    print(chord1)
    print(chord2)


if __name__ == "__main__":
    main()
