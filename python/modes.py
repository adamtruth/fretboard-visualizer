import notes

TYPES: list[str] = ['ionian', 'dorian', 'phrygian', 'lydian',
                    'mixolydian', 'aeolian', 'locrian']


# We should probably turn this into a dictionary
def get_mode(interval: dict, selected: str) -> list:
    mode: list[list[str]] = [interval['root']]
    if selected == 'ionian':
        mode += notes.add_intervals(interval,
                                    ['M2', 'M3', 'P4', 'P5', 'M6', 'M7'])

    if selected == 'dorian':
        mode += notes.add_intervals(interval,
                                    ['M2', 'm3', 'P4', 'P5', 'M6', 'm7'])

    if selected == 'phrygian':
        mode += notes.add_intervals(interval,
                                    ['m2', 'm3', 'P4', 'P5', 'm6', 'm7'])

    if selected == 'lydian':
        mode += notes.add_intervals(interval,
                                    ['M2', 'M3', 'tritone', 'P5', 'M6', 'M7'])

    if selected == 'mixolydian':
        mode += notes.add_intervals(interval,
                                    ['M2', 'M3', 'P4', 'P5', 'M6', 'm7'])

    if selected == 'aeolian':
        mode += notes.add_intervals(interval,
                                    ['M2', 'm3', 'P4', 'P5', 'm6', 'm7'])

    if selected == 'locrian':
        mode += notes.add_intervals(interval,
                                    ['m2', 'm3', 'P4', 'tritone', 'm6', 'm7'])

    return mode


def create(mode_tones: list, root: str, selected: str) -> list:
    interval = notes.get_intervals(mode_tones, root)
    return get_mode(interval, selected)
