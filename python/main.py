import notes as nt
import fretboard as fb
import chords as ch
import scale as sc
import display as dp


def main():
    note_list = nt.generate_notes('flat')
    fretboard = fb.create_fretboard(note_list)

    def on_apply(key, type_value, mode, accidental):
        nl = nt.generate_notes(accidental)
        fb_map = fb.create_fretboard(nl)
        if mode == 'chord':
            result = ch.create_chord(nl, key, type_value)
        else:
            result = sc.create_scale(nl, key, type_value)
        dp.draw_notes(fb_map, result)

    default_scale = sc.create_scale(note_list, 'C', 'major')
    # default_chord = ch.create_chord(note_list, 'C', 'major')

    dp.display(fretboard, default_scale, on_apply)


if __name__ == "__main__":
    main()
