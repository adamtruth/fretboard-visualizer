import notes as nt

TYPES = ['major', 'minor', 'major pentatonic', 'minor pentatonic',
         'diminished', 'augmented', 'whole tone']


def get_scale(interval: dict, desired_scale: str) -> list:
    scale = [interval['root']]
    if desired_scale == 'major':
        scale += nt.add_intervals(interval, ['M2', 'M3', 'P4', 'P5', 'M6', 'M7'])

    if desired_scale == 'minor':
        scale += nt.add_intervals(interval, ['M2', 'm3', 'P4', 'P5', 'm6', 'm7'])

    if desired_scale == 'major pentatonic':
        scale += nt.add_intervals(interval, ['M2', 'M3', 'P5', 'M6'])

    if desired_scale == 'minor pentatonic':
        scale += nt.add_intervals(interval, ['M2', 'm3', 'P4', 'P5', 'm7'])

    if desired_scale == 'diminished':
        scale += nt.add_intervals(interval, ['M2', 'm3', 'P4', 'P5', 'm7'])

    if desired_scale == 'augmented':
        scale += nt.add_intervals(interval, ['M2', 'm3', 'P4', 'P5', 'm7'])

    if desired_scale == 'whole tone':
        scale += nt.add_intervals(interval, ['M2', 'M3', 'tritone', 'm6', 'm7'])

    return scale


def create_scale(notes: list, root: str, desired_scale: str) -> list:
    interval = nt.get_interval(notes, root)
    return get_scale(interval, desired_scale)
