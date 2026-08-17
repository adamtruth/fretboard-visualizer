NOTES: tuple = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
ACCIDENTAL: dict = {'flat': 'b', 'sharp': '#'}


def generate_notes(selected_accidental: str) -> list:
    ''' Returns diatonic notes (including specified accidentals). '''
    notes = []
    accidentals = []

    for i in range(len(NOTES)):
        if selected_accidental == 'sharp':
            accidentals.append(NOTES[i] + ACCIDENTAL[selected_accidental])

        if selected_accidental == 'flat':
            # Shift by one to prevent ordering A Ab B Bb...
            shift = NOTES[1:] + NOTES[:1]
            accidentals.append(shift[i] + ACCIDENTAL[selected_accidental])

        notes.append(NOTES[i])
        notes.append(accidentals[i])

    if selected_accidental == 'sharp':
        notes.remove('E#')
        notes.remove('B#')

    if selected_accidental == 'flat':
        notes.remove('Fb')
        notes.remove('Cb')

    return notes


def get_note_idx(notes: list, note: str) -> int:
    ''' Returns the index of a given note. e.g. E -> 7 '''
    return notes.index(note)


def order_notes(notes: list, root: str, frets: int) -> list:
    ''' Returns notes ordered starting from root, wrapping circularly. '''
    root_idx = get_note_idx(notes, root)
    return [notes[(i + root_idx) % len(notes)] for i in range(frets + 1)]


def add_intervals(interval: dict, keys: list) -> list:
    ''' Returns a list of note values for the given interval keys. '''
    return [interval[k] for k in keys]


def get_intervals(notes: list, key: str) -> dict:
    # FIX: reverse the ordering of parameters
    ''' Returns interval dict e.g. {'root': 'A', 'm2': 'Bb', ...} '''
    interval_names = ['root', 'm2', 'M2', 'm3', 'M3',
                      'P4', 'tritone', 'P5', 'm6', 'M6', 'm7', 'M7']
    root_idx = get_note_idx(notes, key)
    return {interval_names[i]: notes[(i + root_idx) % len(notes)]
            for i in range(len(interval_names))}
