# import Chord
# import Notes
import time
import json

notes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
accidental = { 'flat': 'b', 'sharp': '#' }

numberOfFrets = 12
numberOfStrings = 6
fretboardStrings = ['E', 'A', 'D', 'G', 'B', 'E']

# instaniating empty lists
diatonicNotes = []
accidentalNotes = []

def GenerateNotes(accidentalType) -> list:
    for note in range(len(notes)):
        if accidentalType == 'flat':
            # Shift the accidentals list by one element
            # to prevent A Ab B Bb...
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
    orderedNotes = []
    ''' Order notes starting with the given noteIndex '''
    for i in range(numOfFrets + 1):
        # circularly linked list using modulo %
        circularIndex = (i+noteIndex) % len(diatonicNotes)
        # Append notes starting at the circularIndex
        orderedNotes.append(diatonicNotes[circularIndex])
    return orderedNotes

def getNoteId(stringNote) -> int:
    ''' Returns the starting index 
        of a given note.
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
    ''' Returns a dict of a single note
        and its positions on the fretboard.
     '''
    positions = []
    instances = {}
    for i in range(len(fretboard)):
        for j in range(len(fretboard[i])):
            if fretboard[i][j] == note:
                positions.append((i,j))
    instances = { note: positions }
    return instances 

def getFretboardMap(fretboard) -> dict:
    ''' Returns a dict:
        all diatonic notes as keys.
        all fretboard positions as values.
    '''
    noteDict = {}
    for note in range(len(diatonicNotes)):
        # Combine noteDict with each iteration using | (operator)
        noteDict = noteDict | getNoteIndices(fretboard, diatonicNotes[note])
    return noteDict

def formatJSON(noteDict) -> dict:
    ''' Returns a dict that newlines
        after each key-value pair.
    '''
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
