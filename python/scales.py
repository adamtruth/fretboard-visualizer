import notes

TYPES = ['major', 'natural minor', 'harmonic minor',
         'major pentatonic', 'minor pentatonic',
         'major blues', 'minor blues',
         'bebop major', 'bebop dominant', 'bebop minor',
         'diminished', 'augmented', 'whole tone']


# We should probably turn this into a dictionary - beyond 15 conditions
def get_scale(interval: dict, selected: str) -> list:
    scale = [interval['root']]
    if selected == 'major':
        scale += notes.add_intervals(interval,
                                     ['M2', 'M3', 'P4', 'P5', 'M6', 'M7'])

    if selected == 'natural minor':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm6', 'm7'])

    if selected == 'harmonic minor':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm6', 'M7'])

    # NOTE: Melodic is interesting because the ascent includes a m3 and M6
    #       and descending is m3 and m6
    # if selected == 'melodic minor':
    #     scale += notes.add_intervals(interval,
    #                                  ['M2', 'm3', 'P4', 'P5', 'm6', 'M7'])

    if selected == 'diminished':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm7'])

    if selected == 'augmented':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm7'])

    if selected == 'major pentatonic':
        scale += notes.add_intervals(interval, ['M2', 'M3', 'P5', 'M6'])

    if selected == 'minor pentatonic':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5', 'm7'])

    # Is this right?
    if selected == 'major blues':
        scale += notes.add_intervals(interval,
                                     ['M2', 'M3', 'P4', 'P5', 'M6'])

    if selected == 'minor blues':
        scale += notes.add_intervals(interval,
                                     ['m3', 'P4', 'm6', 'm7'])

    if selected == 'bebop major':
        scale += notes.add_intervals(interval,
                                     ['M2', 'M3', 'P4', 'P5',
                                      'm6', 'M6', 'M7'])

    if selected == 'bebop dominant':
        scale += notes.add_intervals(interval,
                                     ['M2', 'M3', 'P4', 'P5',
                                      'M6', 'm7', 'M7'])

    if selected == 'bebop minor':
        scale += notes.add_intervals(interval,
                                     ['M2', 'm3', 'P4', 'P5',
                                      'M6', 'm7', 'M7'])

    if selected == 'bebop major':
        scale += notes.add_intervals(interval,
                                     ['M2', 'M3', 'P4', 'm6', 'M6', 'M7'])

    if selected == 'whole tone':
        scale += notes.add_intervals(interval,
                                     ['M2', 'M3', 'tritone', 'm6', 'm7'])

    return scale


def create(scale_tones: list, root: str, selected: str) -> list:
    interval = notes.get_intervals(scale_tones, root)
    return get_scale(interval, selected)
