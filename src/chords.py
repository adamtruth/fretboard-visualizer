import notes

# TODO: 'm13' if it exists
# TODO: Add sus extension chords 6sus2, 6sus4, 9sus2 9sus4 13sus2 13sus4
TYPES: list[str] = [
                    # Triads (three note chords)
                     'maj',
                     'm',
                     'dim',
                     'aug',
                     'sus2',
                     'sus4',

                     # Sevenths chords (Four note chords)
                     '7',
                     'maj7',
                     'm7',
                     'ø7',
                     'o7',
                     '6',
                     'm6',
                     '9',
                     'm9',
                     '6/9',
                     '13',
                     '7b9b13',
                     '7b9' ]



# TODO: We should probably turn this into a dictionary
def get_chord(chord_type: str, interval: dict) -> list:
    ''' Returns chord notes e.g. ['A', 'C#', 'E'] '''

    chord: list[list[str]] = [interval['root']]

    # NOTE: notes.py -- add the intervals extensions for M9, P11, M13
    # instead of M2, P4, M6, etc. (enharmonic)
    # Ideally we would want to allow chord construction with either
    # leaving it to preference.

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
    if chord_type == 'sus2':
        chord += notes.add_intervals(interval,
                                     ['M2', 'P5'])
    if chord_type == 'sus4':
        chord += notes.add_intervals(interval,
                                     ['P4', 'P5'])

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
    # half-dimished
    if chord_type == 'ø7':
        chord += notes.add_intervals(interval,
                                     ['m3', 'tritone', 'm7'])
    # fully diminished
    if chord_type == 'o7':
        chord += notes.add_intervals(interval,
                                     ['m3', 'tritone', 'M6'])

    if chord_type == '6':
        chord += notes.add_intervals(interval,
                                     # M9, P11, M13
                                     ['M3', 'P5', 'M6'])
    if chord_type == 'm6':
        chord += notes.add_intervals(interval,
                                     # M9, P11, M13
                                     ['m3', 'P5', 'M6'])
    if chord_type == '9':
        chord += notes.add_intervals(interval,
                                     ['m3', 'P5', 'M7', 'M2'])
    if chord_type == 'm9':
        chord += notes.add_intervals(interval,
                                     # 9th == m2
                                     ['m3', 'P5', 'M7', 'm2'])
    if chord_type == '13':
        chord += notes.add_intervals(interval,
                                     # M9, P11, M13, omit P5
                                     ['M3', 'm7', 'M2', 'P4', 'M6'])
    if chord_type == '6/9':
        chord += notes.add_intervals(interval,
                                     ['M3', 'P5', 'M6', 'M2'])  # 9th
    if chord_type == '7b9b13':
        chord += notes.add_intervals(interval,
                                     # M9, P11, M13, omit P5
                                     ['M3', 'm7', 'm2', 'm6'])
    if chord_type == '7b9':
        chord += notes.add_intervals(interval,
                                     # M9, P11, M13, omit P5
                                     ['M3', 'm7', 'm2'])

    return chord


def create(chord_notes: notes.Notes, root: str, chord_type: str) -> list:
    interval = notes.get_intervals(chord_notes, root)
    return get_chord(chord_type, interval)
