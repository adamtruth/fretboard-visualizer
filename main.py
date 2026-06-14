# import Chord
# import Notes
import time
import json

notes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
accidental = { 'flat': 'b', 'sharp': '#' }

numberOfFrets = 12
numberOfStrings = 6
fretboardStrings = ['E', 'A', 'D', 'G', 'B', 'E']

diatonicNotes = []
accidentalNotes = []

def GenerateNotes(accidentalType) -> list:
    for note in range(len(notes)):
        if accidentalType == 'flat':
            # Shift the accidentals list by one element 
            # preventing the ordering A Ab B Bb... 
            reorder = notes[1:] + notes[:1]
            accidentalNotes.append(reorder[note] + accidental[accidentalType])

        if accidentalType == 'sharp':
            # Append the sharp to each element in the list
            accidentalNotes.append(notes[note] + accidental[accidentalType])

        # Add the natural note
        diatonicNotes.append(notes[note])
        # Then add the appropriate accidental note
        diatonicNotes.append(accidentalNotes[note])

    # Remove enharmonic notes (notes that should be skipped)
    if accidentalType == 'sharp':
        diatonicNotes.remove('E#')
        diatonicNotes.remove('B#')

    if accidentalType == 'flat':
        diatonicNotes.remove('Fb')
        diatonicNotes.remove('Cb')

    return diatonicNotes

def OrderNotes(noteIndex, numOfFrets) -> list:
    ''' Order notes starting with the given noteIndex 
        @param1: noteIndex: where we begin the list of notes (or tonal center)
        @param2: numOfFrets: the number of frets we are working with
    '''
    orderedNotes = []

    for i in range(numOfFrets + 1):
        # circularly linked list using modulo %
        circularIndex = (i+noteIndex) % len(diatonicNotes)
        # Append notes starting at the circularIndex
        orderedNotes.append(diatonicNotes[circularIndex])

    return orderedNotes

def getNoteId(stringNote) -> int:
    ''' Returns the starting index 
        of a given note.
        @param1 - stringNote: the note we would like to find the index of
    '''
    # The index for the chosen note
    id = diatonicNotes.index(stringNote)
    return id

def CreateFretboard(int: numberOfStrings, list: fretboardStrings) -> list:
    ''' Create a nested list with all notes on the fretboard '''
    fretboard = []
    for string in range(numberOfStrings):
        noteId = getNoteId(fretboardStrings[string]) # int
        orderedNotes = OrderNotes(noteId, numberOfFrets) # list
        # Appends the orderedNotes list to fretboard list
        fretboard.append(orderedNotes)
    return fretboard

def getNoteIndices(fretboard, note) -> dict:
    ''' Returns a dict of a single note and its positions on the fretboard. '''
    positions = []
    notePositions = {}

    # This part was a bit tricky
    # We are iterating through the frets and the strings.
    # The string index is [i]
    # The fret index is [j]
    # So [i][j] is the [string_index][fret_index]
    for i in range(len(fretboard)):
        for j in range(len(fretboard[i])):
            if fretboard[i][j] == note:
                positions.append((i,j))

    notePositions = { note: positions } # mapping the list of lists to the dict

    return notePositions

def getFretboardMap(fretboard) -> dict:
    ''' Returns a dict of all notes and their respective indices on the fretboard. '''
    noteDict = {}
    for note in range(len(diatonicNotes)):
        # Combine noteDict with each iteration using the intersection operator |
        noteDict = noteDict | getNoteIndices(fretboard, diatonicNotes[note])
    return noteDict

def formatJSON(noteDict) -> dict:
    ''' Returns a formatted dict that newlines after each key-value pair. '''
    lines = []
    for key, value in noteDict.items():
        k = json.dumps(key)
        v = json.dumps(value)
        lines.append(f'    {k}: {v}')
    custom_json = "{\n" + ",\n".join(lines) + "\n}"
    return custom_json


def main():
   # Set the preferred accidental
    accidentalType = 'sharp'

    # Generate diatonic notes with accidentals
    GenerateNotes(accidentalType)

    # Create fretboard grid as a list
    fretboard = CreateFretboard(numberOfStrings, fretboardStrings)

    # Get a dict of all notes/positions
    noteDict = getFretboardMap(fretboard)

    # Format the dictionary and print
    print(formatJSON(noteDict))

if __name__ == "__main__":
    main()
