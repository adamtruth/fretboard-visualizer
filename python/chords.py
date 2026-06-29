import notes

TYPES = ['maj', 'm', 'dim', 'aug',
         '7', 'maj7', 'm7', 'ø7', 'o7']

# '6', 'maj6', 'm6',
# '9', 'm9', 'maj9',
# '13', '6/9',
# '7b9b13', '7b9', 'neopolitan', 'maj/min']

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

    # Double check these
    if chord_type == '6':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == 'maj6':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == 'm6':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == '9':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == 'm9':
        chord += notes.add_intervals(interval,
                                     ['m3', 'P5', 'M7', 'm2'])  # 9th == m2
    if chord_type == 'maj9':
        chord += notes.add_intervals(interval,
                                     ['m3', 'P5', 'M7', 'M2'])  # 9th == m2
    if chord_type == '13':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == '6/9':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == '7b9b13':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == '7b9':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == 'neopolitan':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    if chord_type == 'maj/min':
        chord += notes.add_intervals(interval,
                                     ['', '', ''])
    return chord


def create(desired_notes: list, root: str, chord_type: str) -> list:
    interval = notes.get_intervals(desired_notes, root)
    return get_chord(chord_type, interval)
