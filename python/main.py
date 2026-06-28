import notes as nt
import fretboard as fb
import chords as ch
import scale as sc
import modes as mo
import display as dp


def main():
    note_list = nt.generate_notes('flat')
    fretboard = fb.create_fretboard(note_list)
    default_scale = sc.create_scale(note_list, 'C', 'major')

    def on_apply(key, type_value, mode_setting, accidental):
        nl = nt.generate_notes(accidental)
        fb_map = fb.create_fretboard(nl)
        if mode_setting == 'chord':
            result = ch.create_chord(nl, key, type_value)
        elif mode_setting == 'scale':
            result = sc.create_scale(nl, key, type_value)
        elif mode_setting == 'mode':
            result = mo.create_mode(nl, key, type_value)
        else:
            result = default_scale
        dp.draw_notes(fb_map, result)

    dp.display(fretboard, default_scale, on_apply)


if __name__ == "__main__":
    main()
