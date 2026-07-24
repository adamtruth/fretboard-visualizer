import { addIntervals, getIntervals } from './notes';

export const CHORD_TYPES = [
  'maj', 'm', 'dim', 'aug', 'sus2', 'sus4',
  '7', 'maj7', 'm7', 'ø7', 'o7',
  '6', 'm6',
  '9', 'm9',
  '6/9', '13',
  '7b9b13', '7b9',
] as const;

export type ChordType = typeof CHORD_TYPES[number];

export function getChord(chordType: string, interval: Record<string, string>): string[] {
  const chord: string[] = [interval['root']];

  if (chordType === 'maj')    chord.push(...addIntervals(interval, ['M3', 'P5']));
  if (chordType === 'm')      chord.push(...addIntervals(interval, ['m3', 'P5']));
  if (chordType === 'dim')    chord.push(...addIntervals(interval, ['m3', 'tritone']));
  if (chordType === 'aug')    chord.push(...addIntervals(interval, ['M3', 'm6']));
  if (chordType === 'sus2')   chord.push(...addIntervals(interval, ['M2', 'P5']));
  if (chordType === 'sus4')   chord.push(...addIntervals(interval, ['P4', 'P5']));
  if (chordType === '7')      chord.push(...addIntervals(interval, ['M3', 'P5', 'm7']));
  if (chordType === 'maj7')   chord.push(...addIntervals(interval, ['M3', 'P5', 'M7']));
  if (chordType === 'm7')     chord.push(...addIntervals(interval, ['m3', 'P5', 'm7']));
  if (chordType === 'ø7')     chord.push(...addIntervals(interval, ['m3', 'tritone', 'm7']));
  if (chordType === 'o7')     chord.push(...addIntervals(interval, ['m3', 'tritone', 'M6']));
  if (chordType === '6')      chord.push(...addIntervals(interval, ['M3', 'P5', 'M6']));
  if (chordType === 'm6')     chord.push(...addIntervals(interval, ['m3', 'P5', 'M6']));
  if (chordType === '9')      chord.push(...addIntervals(interval, ['m3', 'P5', 'M7', 'M2']));
  if (chordType === 'm9')     chord.push(...addIntervals(interval, ['m3', 'P5', 'M7', 'm2']));
  if (chordType === '13')     chord.push(...addIntervals(interval, ['M3', 'm7', 'M2', 'P4', 'M6']));
  if (chordType === '6/9')    chord.push(...addIntervals(interval, ['M3', 'P5', 'M6', 'M2']));
  if (chordType === '7b9b13') chord.push(...addIntervals(interval, ['M3', 'm7', 'm2', 'm6']));
  if (chordType === '7b9')    chord.push(...addIntervals(interval, ['M3', 'm7', 'm2']));

  return chord;
}

export function createChord(chordNotes: string[], root: string, chordType: string): string[] {
  const interval = getIntervals(chordNotes, root);
  return getChord(chordType, interval);
}
