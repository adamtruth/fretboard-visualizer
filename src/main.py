import display as dp
import notes
import fretboard
import chords
import scales
import modes


def main():
    # default configuration
    # accidental (flat) and scale (C major)
    default_notes = notes.Notes('flat')
    default_scale = scales.create(default_notes, 'C', 'major')

    # initialize fretboard with default configuration
    fb = fretboard.create(default_notes)

    def draw(key, type_value, mode_setting, accidental):
        notes_list = notes.Notes(accidental)
        fb_map = fretboard.create(notes_list)

        if mode_setting == 'chord':
            result = chords.create(notes_list, key, type_value)
        elif mode_setting == 'scale':
            result = scales.create(notes_list, key, type_value)
        elif mode_setting == 'mode':
            result = modes.create(notes_list, key, type_value)
        else:
            result = default_scale

        dp.draw_notes(fb_map, result)

    # create the window with the default scale
    dp.start(fb, default_scale, draw)


if __name__ == "__main__":
    main()
