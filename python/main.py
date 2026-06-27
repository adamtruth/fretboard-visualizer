import notes as nt
import fretboard as fb
import chords as ch
import scale as sc
import display as dp


def main():
    note_list = nt.generate_notes('flat')
    fretboard = fb.create_fretboard(note_list)

    def on_apply(key, chord_type):
        chord = ch.create_chord(note_list, key, chord_type)
        dp.draw_notes(fretboard, chord)

    default_scale = sc.create_scale(note_list, 'C', 'major')
    # default_chord = ch.create_chord(note_list, 'C', 'major')

    dp.display(fretboard, default_scale, on_apply)


if __name__ == "__main__":
    main()
