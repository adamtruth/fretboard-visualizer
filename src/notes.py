# NOTES: tuple = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
# ACCIDENTAL: dict = {'flat': 'b', 'sharp': '#'}
#
class Notes:
    NOTES: tuple = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    ACCIDENTAL: dict = {'flat': 'b', 'sharp': '#'}

    def __init__(self, selected_accidental: str):
        self.selected_accidental = selected_accidental
        self.notes = self._generate_notes(selected_accidental)


    def _generate_notes(self, selected_accidental: str) -> list:
        ''' Returns diatonic notes (including specified accidentals). '''
        notes = []
        accidentals = []

        for i in range(len(self.NOTES)):
            if selected_accidental == 'sharp':
                accidentals.append(self.NOTES[i] + self.ACCIDENTAL[selected_accidental])

            if selected_accidental == 'flat':
                # Shift by one to prevent ordering A Ab B Bb...
                shift = self.NOTES[1:] + self.NOTES[:1]
                accidentals.append(shift[i] + self.ACCIDENTAL[selected_accidental])

            notes.append(self.NOTES[i])
            notes.append(accidentals[i])

        # Remove enharmonic notes
        if selected_accidental == 'sharp':
            notes.remove('E#')
            notes.remove('B#')

        if selected_accidental == 'flat':
            notes.remove('Fb')
            notes.remove('Cb')

        return notes


    def get_note_idx(self, note: str) -> int:
        ''' Returns the index of a given note. e.g. E -> 7 '''
        return self.notes.index(note)


    def order_notes(self, root: str, frets: int) -> list:
        ''' Returns notes ordered starting from root, wrapping circularly. '''
        root_idx = self.get_note_idx(root)
        return [self.notes[(i + root_idx) % len(self.notes)]
                for i in range(frets + 1)]


def add_intervals(interval: dict, keys: list) -> list:
    ''' Returns a list of note values for the given interval keys. '''
    return [interval[k] for k in keys]


def get_intervals(self, key: str) -> dict:
    ''' Returns interval dict e.g. {'root': 'A', 'm2': 'Bb', ...} '''
    interval_names = ['root', 'm2', 'M2', 'm3', 'M3',
                      'P4', 'tritone', 'P5', 'm6', 'M6', 'm7', 'M7']
    root_idx = self.get_note_idx(key)
    return {interval_names[i]: self.notes[(i + root_idx) % len(self.notes)]
            for i in range(len(interval_names))}
