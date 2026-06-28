import notes

TYPES = ['major', 'minor', 'major pentatonic', 'minor pentatonic',
         'diminished', 'augmented', 'whole tone']


# We should probably turn this into a dictionary
def get_scale(interval: dict, selected: str) -> list:
    scale = [interval['root']]
    if selected == 'major':
        scale += notes.add_intervals(interval,
                                     ['M2', 'M3', 'P4', 'P5', 'M6', 'M7'])

    if selected == 'minor':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm6', 'm7'])

    if selected == 'major pentatonic':
        scale += notes.add_intervals(interval, ['M2', 'M3', 'P5', 'M6'])

    if selected == 'minor pentatonic':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm7'])

    if selected == 'diminished':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm7'])

    if selected == 'augmented':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm7'])

    if selected == 'whole tone':
        scale += notes.add_intervals(interval,
                                     ['M2', 'M3', 'tritone', 'm6', 'm7'])

    return scale


def create(scale_tones: list, root: str, selected: str) -> list:
    interval = notes.get_intervals(scale_tones, root)
    return get_scale(interval, selected)
