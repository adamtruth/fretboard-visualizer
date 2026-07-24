export const NOTES = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] as const;
export const ACCIDENTAL: Record<string, string> = { flat: 'b', sharp: '#' };

export type Accidental = 'flat' | 'sharp';

export function generateNotes(selectedAccidental: Accidental): string[] {
  const notes: string[] = [];
  const accidentals: string[] = [];

  for (let i = 0; i < NOTES.length; i++) {
    if (selectedAccidental === 'sharp') {
      accidentals.push(NOTES[i] + ACCIDENTAL[selectedAccidental]);
    }
    if (selectedAccidental === 'flat') {
      // Shift by one to prevent ordering A Ab B Bb...
      const shift = [...NOTES.slice(1), NOTES[0]];
      accidentals.push(shift[i] + ACCIDENTAL[selectedAccidental]);
    }
    notes.push(NOTES[i]);
    notes.push(accidentals[i]);
  }

  if (selectedAccidental === 'sharp') {
    notes.splice(notes.indexOf('E#'), 1);
    notes.splice(notes.indexOf('B#'), 1);
  }
  if (selectedAccidental === 'flat') {
    notes.splice(notes.indexOf('Fb'), 1);
    notes.splice(notes.indexOf('Cb'), 1);
  }

  return notes;
}

export function getNoteIdx(notes: string[], note: string): number {
  return notes.indexOf(note);
}

export function orderNotes(notes: string[], root: string, frets: number): string[] {
  const rootIdx = getNoteIdx(notes, root);
  return Array.from({ length: frets + 1 }, (_, i) => notes[(i + rootIdx) % notes.length]);
}

export function addIntervals(interval: Record<string, string>, keys: string[]): string[] {
  return keys.map((k) => interval[k]);
}

export function getIntervals(notes: string[], key: string): Record<string, string> {
  const intervalNames = ['root', 'm2', 'M2', 'm3', 'M3', 'P4', 'tritone', 'P5', 'm6', 'M6', 'm7', 'M7'];
  const rootIdx = getNoteIdx(notes, key);
  return Object.fromEntries(
    intervalNames.map((name, i) => [name, notes[(i + rootIdx) % notes.length]])
  );
}
