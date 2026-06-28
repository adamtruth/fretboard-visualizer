import notes

TYPES = ['maj', 'm', 'dim', 'aug',
         '7', 'maj7', 'm7', 'ø7', 'o7']

TYPES = ['major', 'minor', '7', 'M7', 'm7', 'ø7', 'o7', 'dim', 'aug']


# We should probably turn this into a dictionary
def get_chord(chord_type: str, interval: dict) -> list:
    ''' Returns chord notes e.g. ['A', 'C#', 'E'] '''

    chord = [interval['root']]

    # Triads
    if chord_type == 'maj':
        chord += notes.add_intervals(interval,
                                     ['M3', 'P5'])
    if chord_type == 'm':
        chord += notes.add_intervals(interval,
                                     ['m3', 'P5'])
    if chord_type == 'dim':
        chord += notes.add_intervals(interval,
                                     ['m3', 'tritone'])
    if chord_type == 'aug':
        chord += notes.add_intervals(interval,
                                     ['M3', 'm6'])

    # Seventh chords
    if chord_type == '7':
        chord += notes.add_intervals(interval,
                                     ['M3', 'P5', 'm7'])
    if chord_type == 'maj7':
        chord += notes.add_intervals(interval,
                                     ['M3', 'P5', 'M7'])
    if chord_type == 'm7':
        chord += notes.add_intervals(interval,
                                     ['m3', 'P5', 'm7'])
    if chord_type == 'ø7':  # half-dimished
        chord += notes.add_intervals(interval,
                                     ['m3', 'tritone', 'm7'])
    if chord_type == 'o7':  # fully diminished
        chord += notes.add_intervals(interval,
                                     ['m3', 'tritone', 'M6'])

    return chord


def create(desired_notes: list, root: str, chord_type: str) -> list:
    interval = notes.get_interval(desired_notes, root)
    return get_chord(chord_type, interval)
