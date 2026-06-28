import notes as nt

TYPES = ['ionian', 'dorian', 'phrygian', 'lydian',
         'mixolydian', 'aeolian', 'locrian']


def get_mode(interval: dict, desired_mode: str) -> list:
    mode = [interval['root']]
    if desired_mode == 'ionian':
        mode += nt.add_intervals(interval, ['M2', 'M3', 'P4', 'P5', 'M6', 'M7'])

    if desired_mode == 'dorian':
        mode += nt.add_intervals(interval, ['M2', 'm3', 'P4', 'P5', 'M6', 'm7'])

    if desired_mode == 'phrygian':
        mode += nt.add_intervals(interval, ['m2', 'm3', 'P4', 'P5', 'm6', 'm7'])

    if desired_mode == 'lydian':
        mode += nt.add_intervals(interval, ['M2', 'M3', 'tritone', 'P5', 'M6', 'M7'])

    if desired_mode == 'mixolydian':
        mode += nt.add_intervals(interval, ['M2', 'M3', 'P4', 'P5', 'M6', 'm7'])

    if desired_mode == 'aeolian':
        mode += nt.add_intervals(interval, ['M2', 'm3', 'P4', 'P5', 'm6', 'm7'])

    if desired_mode == 'locrian':
        mode += nt.add_intervals(interval, ['m2', 'm3', 'P4', 'tritone', 'm6', 'm7'])

    return mode


def create_mode(notes: list, root: str, desired_mode: str) -> list:
    interval = nt.get_interval(notes, root)
    return get_mode(interval, desired_mode)
