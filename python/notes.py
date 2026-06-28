NOTES = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
accidental = {'flat': 'b', 'sharp': '#'}


def generate_notes(accidental_type: str) -> list:
    ''' Returns diatonic notes (including specified accidentals). '''
    notes = []
    accidental_notes = []
    for i in range(len(NOTES)):
        if accidental_type == 'sharp':
            accidental_notes.append(NOTES[i] + accidental[accidental_type])

        if accidental_type == 'flat':
            # Shift by one to prevent ordering A Ab B Bb...
            shift = NOTES[1:] + NOTES[:1]
            accidental_notes.append(shift[i] + accidental[accidental_type])

        notes.append(NOTES[i])
        notes.append(accidental_notes[i])

    if accidental_type == 'sharp':
        notes.remove('E#')
        notes.remove('B#')

    if accidental_type == 'flat':
        notes.remove('Fb')
        notes.remove('Cb')

    return notes


def get_note_idx(notes: list, note: str) -> int:
    ''' Returns the index of a given note. e.g. E -> 7 '''
    return notes.index(note)


def order_notes(notes: list, root: str, fret_count: int) -> list:
    ''' Returns notes ordered starting from root, wrapping circularly. '''
    root_idx = get_note_idx(notes, root)
    return [notes[(i + root_idx) % len(notes)] for i in range(fret_count + 1)]


def add_intervals(interval: dict, keys: list) -> list:
    ''' Returns a list of note values for the given interval keys. '''
    added_intervals = []
    for key in keys:
        added_intervals.append(interval[key])
    return added_intervals


def get_intervals(notes: list, key: str) -> dict:
    # FIX: reverse the ordering of parameters
    ''' Returns interval dict e.g. {'root': 'A', 'm2': 'Bb', ...} '''
    interval_names = ['root', 'm2', 'M2', 'm3', 'M3',
                      'P4', 'tritone', 'P5', 'm6', 'M6', 'm7', 'M7']
    root_idx = get_note_idx(notes, key)
    return {interval_names[i]: notes[(i + root_idx) % len(notes)]
            for i in range(len(interval_names))}
