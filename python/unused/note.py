NOTES = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
FRET_COUNT = 12
accidental = {'flat': 'b', 'sharp': '#'}

notes = []
interval = {}


def generate_notes(accidental_type: str) -> list:
    ''' Returns diatonic notes (including specified accidentals). '''
    notes = []
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


def set_interval(notes: list, key: str) -> dict:
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
