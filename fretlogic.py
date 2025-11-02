from mingus.core import notes, scales
from config import scale_type, root, useFlats, convert_to_flat

def to_flat(note):
    """Convert sharp note to flat equivalent if applicable, ignore octave."""
    base_note = ''.join(filter(str.isalpha, note)).upper()
    return convert_to_flat.get(base_note, base_note)

def note_at_fret(open_note, fret):
    base_note = ''.join(filter(str.isalpha, open_note)).upper()
    return notes.int_to_note((notes.note_to_int(base_note) + fret) % 12)

def get_scale_notes():
    if scale_type == 'major':
        scale_notes = scales.Major(root).ascending()
    elif scale_type == 'minor':
        scale_notes = scales.NaturalMinor(root).ascending()
    else:
        raise ValueError("Unsupported scale type")

    if useFlats:
        scale_notes = [to_flat(n) for n in scale_notes]

    return scale_notes

def build_fretboard(tuning, num_frets):
    if useFlats:
        return [
            [to_flat(note_at_fret(s, f)) for f in range(num_frets + 1)]
            for s in tuning
        ]
    else:
        return [
            [note_at_fret(s, f) for f in range(num_frets + 1)]
            for s in tuning
        ]

