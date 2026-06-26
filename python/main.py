import display

import json

notes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
accidental = {'flat': 'b', 'sharp': '#'}

FRET_COUNT = 12
STRING_COUNT = 6
STRING_NOTES = ['E', 'A', 'D', 'G', 'B', 'E']
TEXT_COLOR = "white"
CIRCLE_COLORS = ["red", "blue"]

diatonic_notes = []
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


def generate_diatonic_notes(accidental_type: str) -> list:
    ''' Returns diatonic notes (including specified accidentals). '''
    accidental_notes = []
    for i in range(len(notes)):
        # Append the sharp to each element in the list
        if accidental_type == 'sharp':
            accidental_notes.append(notes[i] + accidental[accidental_type])

        if accidental_type == 'flat':
            # Shift the accidentals list by one element
            # preventing the ordering A Ab B Bb...
            reorder = notes[1:] + notes[:1]
            accidental_notes.append(reorder[i] + accidental[accidental_type])

        # Add the natural note
        diatonic_notes.append(notes[i])
        # Then add the appropriate accidental note
        diatonic_notes.append(accidental_notes[i])

    # Remove enharmonic notes (notes that should be skipped)
    if accidental_type == 'sharp':
        diatonic_notes.remove('E#')
        diatonic_notes.remove('B#')

    if accidental_type == 'flat':
        diatonic_notes.remove('Fb')
        diatonic_notes.remove('Cb')

    return diatonic_notes


def get_note_idx(note: str) -> int:
    ''' Returns the starting index
        of a given note.
        @param1 - note: the note we would like to find the index of
    '''
    # The index (int) for the chosen note
    return diatonic_notes.index(note)


def order_diatonic_notes(root_idx: int) -> list:
    ''' Order notes starting with the given start_note
        @param1: start_note: where we begin the list of notes (or tonal center)
        @param2: frets: the number of frets we are working with
    '''
    ordered_notes = []

    for i in range(FRET_COUNT + 1):
        # circularly linked list using modulo %
        # Append notes starting at the circular_idx
        circular_idx = (i + root_idx) % len(diatonic_notes)
        ordered_notes.append(diatonic_notes[circular_idx])

    return ordered_notes


def set_fretboard_notes(STRING_COUNT: int, STRING_NOTES: list) -> list:
    ''' Create a nested list with all notes on the fretboard '''
    fretboard_notes = []

    # NOTE: We reverse the E,A,D,G,B,E because the index 0,0 is the low E string
    # thus it's flipped. So either we flip the indices so high E is 0,0
    # or we just flip the string_notes
    string_notes = STRING_NOTES[::-1]

    for string in range(STRING_COUNT):
        note_idx = get_note_idx(string_notes[string])  # int
        ordered_notes = order_diatonic_notes(note_idx)  # list

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


# helper function to set the distance between frets
# FIX: looks disgustin
def get_offset(fret_number):
    if fret_number == 0:
        return 0
    if fret_number == 1:
        return 46
    if fret_number == 2:
        return 39
    if fret_number == 3:
        return 39
    if fret_number == 4:
        return 36
    if fret_number == 5:
        return 36
    if fret_number == 6:
        return 40
    if fret_number == 7:
        return 50
    if fret_number == 8:
        return 57
    if fret_number == 9:
        return 72
    if fret_number == 10:
        return 85
    if fret_number == 11:
        return 105
    if fret_number == 12:
        return 125


def map_fretboard_notes(fretboard_notes):
    ''' Maps each note to a coordinate on the fretboard. '''
    fretboard_map = {}
    # for i in range(len(diatonic_notes)):
    x_offset = 0
    for note in range(len(diatonic_notes)):
        fret_positions = fretboard_notes.get(diatonic_notes[note])  # all lists

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
                    x_offset = get_offset(fret_number)
                    x_pos = x_i + (fret_number * x_bar) - x_offset

            note_position = ((x_pos, y_pos))
            positions.append(note_position)

        fretboard_map[diatonic_notes[note]] = positions

    return fretboard_map


def set_intervals(diatonic_notes: list, key: str) -> dict:
    intervals = ['root', 'm2', 'M2', 'm3', 'M3',
                 'P4', 'tritone', 'P5', 'm6', 'M6', 'm7', 'M7']

    start_note = get_note_idx(key)

    for i in range(len(diatonic_notes)):
        # TODO: Reusing circular_idx, turn into function
        circular_idx = (i+start_note) % len(diatonic_notes)
        interval[intervals[i]] = diatonic_notes[circular_idx]

    return interval


def get_chord(chord_type: str, interval: dict) -> list:
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
    interval = set_intervals(diatonic_notes, root)
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
    interval = set_intervals(diatonic_notes, root)
    scale = get_scale(interval, desired_scale)
    return scale


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


def display_circles(fretboard_map, notes: list) -> None:
    for i in range(len(notes)):  # 12
        notes_lists = fretboard_map.get(notes[i])  # all lists

        for j in range(len(notes_lists)):  # 6
            position = notes_lists[j]  # all tuples
            x, y = position[0], position[1]

            # Describe circle attributes for PIL to draw
            if i == 0:
                color = CIRCLE_COLORS[0]
            if i > 0:
                color = CIRCLE_COLORS[1]

            circles = display.Circle(x, y, r, color)
            circles.drawCircle()

    display.show_image()


def display_text(fretboard_map: dict, notes: list) -> None:
    for i in range(len(notes)):
        notes_lists = fretboard_map.get(notes[i])

        for j in range(len(notes_lists)):
            position = notes_lists[j]

            text = str(notes[i])
            x, y = position[0], position[1]

            # So we can center the notes with a accidental
            if len(text) == 2:
                x -= 20
            else:
                x -= 18

            y -= 20

            text_attr = display.Text(x, y, text, TEXT_COLOR)
            text_attr.drawText()

    display.show_image()


def display_all(fretboard_map: dict, notes: list) -> None:
    display_circles(fretboard_map, notes)
    display_text(fretboard_map, notes)


def create_fretboard():
    ''' Helper function to return the completed fretboard map. '''
    # Create fretboard grid as a list
    notes = set_fretboard_notes(STRING_COUNT, STRING_NOTES)

    # Get a dict of all notes/positions
    fretboard_map = get_fretboard_notes(notes)

    # Map coordinates of all notes to fretboard
    fretboard = map_fretboard_notes(fretboard_map)

    return fretboard


""" End of helper functions """


def main():
    # Set preferred accidental
    preferred_accidental = 'flat'

    # Generate diatonic notes with preffered accidentals
    generate_diatonic_notes(preferred_accidental)

    # "fretboard" has mapped notes to positions
    fretboard = create_fretboard()

    # Display scale notes
    desired_scale = create_scale('C', 'major')
    display_all(fretboard, desired_scale)

    rel_key = get_relative_key('E', 'major')
    print(rel_key)


if __name__ == "__main__":
    main()
