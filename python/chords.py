import notes as nt


def get_chord(chord_type: str, interval: dict) -> list:
    ''' Returns chord notes e.g. ['A', 'C#', 'E'] '''
    chord = [interval['root']]
    if chord_type == 'major':
        chord += [interval['M3'], interval['P5']]
    if chord_type == 'minor':
        chord += [interval['m3'], interval['P5']]
    if chord_type == '7':
        chord += [interval['M3'], interval['P5'], interval['M7']]
    if chord_type == 'dim':
        chord += [interval['m3'], interval['tritone']]
    if chord_type == 'aug':
        chord += [interval['M3'], interval['m6']]
    return chord


def create_chord(notes: list, root: str, chord_type: str) -> list:
    interval = nt.get_interval(notes, root)
    return get_chord(chord_type, interval)
