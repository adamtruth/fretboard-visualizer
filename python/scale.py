import notes as nt


def get_scale(interval: dict, desired_scale: str) -> list:
    scale = [interval['root']]
    if desired_scale == 'major':
        scale += [interval['M2'], interval['M3'], interval['P4'],
                  interval['P5'], interval['M6'], interval['M7']]

    if desired_scale == 'minor':
        scale += [interval['M2'], interval['m3'], interval['P4'],
                  interval['P5'], interval['m6'], interval['m7']]

    if desired_scale == 'major pentatonic':
        scale += [interval['M2'], interval['M3'], interval['P5'],
                  interval['M6']]

    if desired_scale == 'minor pentatonic':
        scale += [interval['M2'], interval['m3'], interval['P4'],
                  interval['P5'], interval['m7']]

    if desired_scale == 'diminished':
        scale += [interval['M2'], interval['m3'], interval['P4'],
                  interval['P5'], interval['m7']]

    if desired_scale == 'augmented':
        scale += [interval['M2'], interval['m3'], interval['P4'],
                  interval['P5'], interval['m7']]

    if desired_scale == 'whole tone':
        scale += [interval['M2'], interval['M3'], interval['tritone'],
                  interval['m6'], interval['m7']]

    return scale


def create_scale(notes: list, root: str, desired_scale: str) -> list:
    interval = nt.get_interval(notes, root)
    return get_scale(interval, desired_scale)
