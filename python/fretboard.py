import notes

STRINGS = ['E', 'A', 'D', 'G', 'B', 'E']
FRET_COUNT = 12

# Coordinate constants for mapping fret positions to image pixels
x_i, y_i = 45, 57
x_bar, y_bar = 120, 45


def get_offset(fret: int) -> int:
    ''' Returns the pixel offset for a given fret
        because frets are not equal width. '''
    offsets = {0: 0, 1: 46, 2: 39, 3: 39, 4: 36, 5: 36,
               6: 40, 7: 50, 8: 57, 9: 72, 10: 85, 11: 105, 12: 125}
    return offsets.get(fret, 0)


def order_notes(desired_notes: list, strings: list = STRINGS) -> list:
    ''' Creates a nested list of all desired_notes on the fretboard. '''
    return [notes.order_notes(desired_notes, string, FRET_COUNT)
            for string in reversed(strings)]


def get_positions(fretboard: list, note: str) -> dict:
    ''' Returns {note: [(string_idx, fret_idx), ...]} for a single note. '''
    positions = [
        (string_idx, fret_idx)
        for string_idx, string in enumerate(fretboard)
        for fret_idx, n in enumerate(string)
        if n == note
    ]
    return {note: positions}


def get_notes(desired_notes: list, fretboard: list) -> dict:
    ''' Returns {note: [(string_idx, fret_idx), ...]}
        for all desired_notes.
    '''
    result = {}
    for note in desired_notes:
        result |= get_positions(fretboard, note)
    return result


def map_notes(desired_notes: list, fretboard_notes: dict) -> dict:
    ''' Maps each note to pixel coordinates on the fretboard image. '''
    fretboard_map = {}
    for note in desired_notes:
        fret_positions = fretboard_notes[note]
        positions = []
        for string_idx, fret_idx in fret_positions:
            y_pos = y_i + (string_idx * y_bar)
            x_pos = x_i + (fret_idx * x_bar) - get_offset(fret_idx)
            positions.append((x_pos, y_pos))
        fretboard_map[note] = positions
    return fretboard_map


def create(desired_notes: list) -> dict:
    ''' Returns the completed fretboard coordinate map. '''
    fretboard_grid = order_notes(desired_notes)
    fretboard_notes = get_notes(desired_notes, fretboard_grid)
    return map_notes(desired_notes, fretboard_notes)
