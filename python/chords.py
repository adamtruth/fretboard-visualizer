import notes as nt

TYPES = ['major', 'minor', '7', 'M7', 'm7', 'ø7', 'o7', 'dim', 'aug']


def get_chord(chord_type: str, interval: dict) -> list:
    ''' Returns chord notes e.g. ['A', 'C#', 'E'] '''

    chord = [interval['root']]

    # Triads
    if chord_type == 'major':
        chord += nt.add_intervals(interval,
                                  ['M3', 'P5'])
    if chord_type == 'minor':
        chord += nt.add_intervals(interval,
                                  ['m3', 'P5'])
    if chord_type == 'dim':
        chord += nt.add_intervals(interval,
                                  ['m3', 'tritone'])
    if chord_type == 'aug':
        chord += nt.add_intervals(interval,
                                  ['M3', 'm6'])

    # Seventh chords
    if chord_type == '7':
        chord += nt.add_intervals(interval,
                                  ['M3', 'P5', 'm7'])
    if chord_type == 'M7':
        chord += nt.add_intervals(interval,
                                  ['M3', 'P5', 'M7'])
    if chord_type == 'm7':
        chord += nt.add_intervals(interval,
                                  ['m3', 'P5', 'm7'])
    if chord_type == 'ø7':  # half-dimished
        chord += nt.add_intervals(interval,
                                  ['m3', 'tritone', 'm7'])
    if chord_type == 'o7':  # fully diminished
        chord += nt.add_intervals(interval,
                                  ['m3', 'tritone', 'M6'])

    return chord


def create_chord(notes: list, root: str, chord_type: str) -> list:
    interval = nt.get_interval(notes, root)
    return get_chord(chord_type, interval)
