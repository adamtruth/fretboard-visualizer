import display as dp

import json

NOTES = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
accidental = {'flat': 'b', 'sharp': '#'}

FRET_COUNT = 12
STRINGS = ['E', 'A', 'D', 'G', 'B', 'E']
TEXT_COLOR = "white"

notes = []
interval = {}
# GUI-related Globals
window_title = 'Fretboard Visualizer'

# Circle attributes
# Initial starting location (Open low E string)
x_i, y_i = 45, 57
# Distance between frets (x) and STRING_COUNT (y)
x_bar, y_bar = 120, 45
# radius
r = 15
# offset delta string/fret distances
x_offset, y_offset = 10, 10


def generate_notes(accidental_type: str) -> list:
    ''' Returns diatonic notes (including specified accidentals). '''
    accidental_notes = []
    for i in range(len(NOTES)):
        # Append the sharp to each element in the list
        if accidental_type == 'sharp':
            accidental_notes.append(NOTES[i] + accidental[accidental_type])

        if accidental_type == 'flat':
            # Shift the accidentals list by one element
            # preventing the ordering A Ab B Bb...
            shift = NOTES[1:] + NOTES[:1]
            accidental_notes.append(shift[i] + accidental[accidental_type])

        # Add the natural note
        notes.append(NOTES[i])
        # Then add the appropriate accidental note
        notes.append(accidental_notes[i])

    # Remove enharmonic notes (notes that should be skipped)
    if accidental_type == 'sharp':
        notes.remove('E#')
        notes.remove('B#')

    if accidental_type == 'flat':
        notes.remove('Fb')
        notes.remove('Cb')

    return notes


def get_note_idx(note: str) -> int:
    ''' Returns the starting index of a given note.
        e.g. E returns 7
    '''
    # The index (int) for the chosen note
    return notes.index(note)


def order_notes(root: str) -> list:
    ''' Order notes starting with the given start_note
    '''
    ordered_notes = []
    root_idx = get_note_idx(root)

    # Circularly linked list using modulo %
    # Append notes starting at the circular_idx
    for i in range(FRET_COUNT + 1):
        circular_idx = (i + root_idx) % len(notes)
        ordered_notes.append(notes[circular_idx])

    return ordered_notes


def set_fretboard_notes(STRINGS: list) -> list:
    ''' Create a nested list with all notes on the fretboard '''
    fretboard_notes = []

    # NOTE: We reverse the E,A,D,G,B,E
    # the index 0,0 is the low E string thus it's flipped
    # We could flip the indices so high E is 0,0
    # or we just flip the string_notes
    strings = STRINGS[::-1]

    for string in strings:
        ordered_notes = order_notes(string)  # list

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

    # NOTE: We are iterating through the frets and the STRING_COUNT
    # i := string index => 0 = E string
    # j := fret index => 0 = Open string
    # fretboard[string_index][fret_index]
    for string_idx in range(len(fretboard)):
        for fret_idx in range(len(fretboard[string_idx])):
            if fretboard[string_idx][fret_idx] == note:
                positions.append((string_idx, fret_idx))

    # mapping the list of lists to the dict
    fret_positions = {note: positions}

    return fret_positions


def get_fretboard_notes(fret_positions: list) -> dict:
    ''' Returns a dict of all notes
        and their respective indices on the fretboard.
        e.g. {'A': [(0,5), (1,0), ...], 'B':...}
    '''
    fretboard = {}
    for note in notes:
        # Combine fretboard with each iteration using the intersection operator
        fretboard = fretboard | get_fret_positions(
                fret_positions, note)

    return fretboard


def map_fretboard_notes(fretboard_notes):
    ''' Maps each note to a coordinate on the fretboard.
        e.g. {'A': [(x0,y0),(x1,y1),...], 'B':...}
    '''
    fretboard_map = {}
    # for i in range(len(notes)):
    x_offset = 0
    for note in notes:
        fret_positions = fretboard_notes.get(note)  # all lists

        positions = []

        for fret in range(len(fret_positions)):
            frets = fret_positions[fret]  # all tuples

            x_pos, y_pos = None, None

            for k in range(len(frets)):
                fret_number = frets[k]  # accessing the tuple indices
                # lessen the the distance between fret 0 and 1
                if k == 0:  # k=0 is string
                    y_pos = y_i + (fret_number * y_bar)
                if k == 1:  # k=1 is fret
                    x_offset = dp.get_offset(fret_number)
                    x_pos = x_i + (fret_number * x_bar) - x_offset

            note_position = ((x_pos, y_pos))
            positions.append(note_position)

        fretboard_map[note] = positions

    return fretboard_map


def get_interval(notes: list, key: str) -> dict:
    ''' Returns the list of intervals
        e.g. {'root': 'A', 'm2': 'Bb',...}
    '''
    intervals = ['root', 'm2', 'M2', 'm3', 'M3',
                 'P4', 'tritone', 'P5', 'm6', 'M6', 'm7', 'M7']

    root_idx = get_note_idx(key)

    for i in range(len(notes)):
        # TODO: Reusing circular_idx, turn into function
        circular_idx = (i + root_idx) % len(notes)
        interval[intervals[i]] = notes[circular_idx]

    return interval


def get_chord(chord_type: str, interval: dict) -> list:
    ''' Returns a chord
        e.g. ['A', 'C#', 'E']
    '''
    chord = [interval['root']]
    if chord_type == 'major':
        chord.append(interval['M3'])
        chord.append(interval['P5'])

    if chord_type == 'minor':
        chord.append(interval['m3'])
        chord.append(interval['P5'])

    if chord_type == '7':
        chord.append(interval['M3'])
        chord.append(interval['P5'])
        chord.append(interval['M7'])

    if chord_type == 'dim':
        chord.append(interval[''])
        chord.append(interval[''])

    if chord_type == 'aug':
        chord.append(interval[''])
        chord.append(interval[''])

    if chord_type == 'sus':
        chord.append(interval[''])
        chord.append(interval[''])

    return chord


def create_chord(root: str, chord_type: str) -> list:
    interval = get_interval(notes, root)
    chord = get_chord(chord_type, interval)
    return chord


def get_scale(interval: dict, desired_scale: str):
    scale = [interval['root']]
    if desired_scale == 'major':
        scale.append(interval['M2'])
        scale.append(interval['M3'])
        scale.append(interval['P4'])
        scale.append(interval['P5'])
        scale.append(interval['M6'])
        scale.append(interval['M7'])

    if desired_scale == 'minor':
        scale.append(interval['M2'])
        scale.append(interval['m3'])
        scale.append(interval['P4'])
        scale.append(interval['P5'])
        scale.append(interval['m6'])
        scale.append(interval['m7'])

    if desired_scale == 'major pentatonic':
        scale.append(interval['M2'])
        scale.append(interval['M3'])
        scale.append(interval['P5'])
        scale.append(interval['M6'])

    if desired_scale == 'minor pentatonic':
        scale.append(interval['M2'])
        scale.append(interval['m3'])
        scale.append(interval['P4'])
        scale.append(interval['P5'])
        scale.append(interval['m7'])

    return scale


def create_scale(root: str, desired_scale: str) -> list:
    interval = get_interval(notes, root)
    scale = get_scale(interval, desired_scale)
    return scale


def display(fretboard_map, notes: list) -> None:
    idx = 0
    for note in notes:
        notes_lists = fretboard_map.get(note)  # all lists

        if idx == 0:
            is_root = True
        else:
            is_root = False

        idx += 1

        for position in notes_lists:
            x, y = position[0], position[1]

            # Describe circle attributes for PIL to draw
            if is_root is True:
                color = 'red'
            else:
                color = 'blue'

            circles = dp.Circle(x, y, r, color)
            circles.drawCircle()

            # So we can center the notes with a accidental
            text = str(note)
            if len(text) == 2:
                x -= 20
            else:
                x -= 18

            y -= 20
            text = dp.Text(x, y, text, TEXT_COLOR)
            text.drawText()

    dp.show_image()


""" Helper functions """


def format_json(fretboard) -> dict:
    ''' Returns a formatted dict that newlines after each key-value pair. '''
    lines = []
    for key, value in fretboard.items():
        k = json.dumps(key)
        v = json.dumps(value)
        lines.append(f'    {k}: {v}')
    custom_json = "{\n" + ",\n".join(lines) + "\n}"

    return custom_json


def combine_str(str1: str, str2: str):
    return str1 + ' ' + str2


def split_str(combined_str: str) -> list:
    split_str = combined_str.split()
    return split_str


# TODO: Fix this function
def get_relative_key(key: str, scale_type: str) -> tuple:
    scale_idx = get_note_idx(key)
    scale = notes[scale_idx:] + notes[:scale_idx]
    if scale_type == 'major':
        rel_key = scale[2]
        rel_scale = 'minor'
    if scale_type == 'minor':
        rel_key = scale[5]
        rel_scale = 'major'

    return rel_key, rel_scale


def create_fretboard():
    ''' Helper function to return the completed fretboard map. '''
    # Create fretboard grid as a list
    fretboard_notes = set_fretboard_notes(STRINGS)

    # Get a dict of all notes/positions
    fretboard_map = get_fretboard_notes(fretboard_notes)

    # Map coordinates of all notes to fretboard
    fretboard = map_fretboard_notes(fretboard_map)

    return fretboard


""" End of helper functions """


def main():
    # Set preferred accidental
    preferred_accidental = 'flat'

    # Generate diatonic notes with preffered accidentals
    generate_notes(preferred_accidental)

    # "fretboard" has mapped notes to positions
    fretboard = create_fretboard()

    # Display scale notes
    desired_scale = create_scale('C', 'major')
    desired_chord = create_chord('C', 'major')
    display(fretboard, desired_scale)


if __name__ == "__main__":
    main()
