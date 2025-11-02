# Fretworks
[Fretworks Github](https://github.com/adamtruth/fretworks)

fretworks/
├──────── config.py
├──────── fretlogic.py
├──────── plot.py
├──────── main.py

Using PyCairo and PyQt6.

## TODO list
1. Add buttons to select the scale from a dropdown
2. Fix the sharps to flats logic
3. At "fret 0" move the name of the string. Color in the string.


The intention is to display a fretboard with all the possible notes in a key. Highlighting which notes are the root 3rd, 5th, 7th, extensions, etc.

I'm looking to use python with an interface using jinja2 and django potentially.

Inspirations for this project are fretjam on YouTube because his fretboard visualizations are quite nice.

# Tables
## Chords
* Major
* Minor
* Power chords
* Shell voicings
* 7 - Dominant Chords
* sus2
* sus4
* Neopolitan
* maj7
* maj6
* 11
* 13


| Chord Tonality  | Chord Tones |
| --------------- | ----------- |
| Major           | 1-3-5       |
| Minor           | 1-b3-5      |
| Diminshed       | 1-3-b5      |
| Augmented       | 1-3-#5      |
| sus4            | 1-bb3-5     |
| sus2            | 1-#3-5      |
| Half-diminished | 1-b3-5-b7   |
| 7               | 1-3-5-b7    |
| 13              | 1-3-5/b7-13 |
| 7b9b13          |             |
| maj9, 9, min9   |             |
| 11              |             |
| 11              |             |
| 11              |             |
|                 |             |
## Scales
    Major
    Minor
        Natural Minor (b3, b6, b7)
        Harmonic Minor (b3, b6)
        Melodic Minor (Ascending: b3, 6) (Descending: b3, b6)
    Pentatonic
        Major Pentatonic (I, II, III, V, VI)
        Suspended (I, II, IV, V, bVII)
        Blues minor (I, bIII, IV, bVI, bVII)
        Blues major (I, II, IV, V, VI)
        Minor pentatonic (I, IIIb, IV, V, VII)
    Hexatonic
        Augmented (b2, 2, 4, b5, omit 6, 7)
        Prometheus
        Blues (omit 2, b3, b5, omit 6, b7)
        Tritone (b2, omit 4, b5, 5, b7)
        Major (omit 7)
        Minor (b3, omit 6, b7)
        Ritsu Onkai (b2, b3, omit5, b6, b7)
        Raga Kumud (omit 4)
        Mixolydian hexatonic (omit 3, b7)
    Diminished (
    Whole Tone

Best way to map the guitar neck is probably using a 2D-matrix:
6 strings x 12 frets to start indexing starts at 0 with the starting note
for that particular tuning

Initially was going to do Vue.js stuff for the frontend but I somewhat decided against it because I think I can do all of it in Python.
