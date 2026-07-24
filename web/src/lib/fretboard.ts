import { orderNotes as notesOrderNotes } from './notes';

export const STRINGS = ['E', 'A', 'D', 'G', 'B', 'E'] as const;
export const FRET_COUNT = 12;

// Coordinate constants for mapping fret positions to image pixels
const X_I = 32;
const Y_I = 42;
const X_BAR = 120;
const Y_BAR = 45;

const FRET_OFFSETS: Record<number, number> = {
  0: 0, 1: 46, 2: 39, 3: 39, 4: 36, 5: 36,
  6: 40, 7: 50, 8: 57, 9: 72, 10: 85, 11: 105, 12: 125,
};

export function getOffset(fret: number): number {
  return FRET_OFFSETS[fret] ?? 0;
}

export type FretboardGrid = string[][];
export type NotePositions = Record<string, [number, number][]>;

export function buildGrid(desiredNotes: string[]): FretboardGrid {
  return [...STRINGS].reverse().map((string) =>
    notesOrderNotes(desiredNotes, string, FRET_COUNT)
  );
}

function getPositions(grid: FretboardGrid, note: string): [number, number][] {
  const positions: [number, number][] = [];
  for (let stringIdx = 0; stringIdx < grid.length; stringIdx++) {
    for (let fretIdx = 0; fretIdx < grid[stringIdx].length; fretIdx++) {
      if (grid[stringIdx][fretIdx] === note) {
        positions.push([stringIdx, fretIdx]);
      }
    }
  }
  return positions;
}

export function getNotes(desiredNotes: string[], grid: FretboardGrid): Record<string, [number, number][]> {
  return Object.fromEntries(desiredNotes.map((note) => [note, getPositions(grid, note)]));
}

export function mapNotes(desiredNotes: string[], fretboardNotes: Record<string, [number, number][]>): NotePositions {
  const result: NotePositions = {};
  for (const note of desiredNotes) {
    result[note] = fretboardNotes[note].map(([stringIdx, fretIdx]) => [
      X_I + fretIdx * X_BAR - getOffset(fretIdx),
      Y_I + stringIdx * Y_BAR,
    ]);
  }
  return result;
}

export function createFretboard(desiredNotes: string[]): NotePositions {
  const grid = buildGrid(desiredNotes);
  const fretboardNotes = getNotes(desiredNotes, grid);
  return mapNotes(desiredNotes, fretboardNotes);
}
