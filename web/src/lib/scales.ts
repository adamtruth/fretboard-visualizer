import { addIntervals, getIntervals } from './notes';

export const SCALE_TYPES = [
  'major', 'natural minor', 'harmonic minor',
  'major pentatonic', 'minor pentatonic',
  'major blues', 'minor blues',
  'bebop major', 'bebop dominant', 'bebop minor',
  'diminished', 'augmented', 'whole tone',
] as const;

export type ScaleType = typeof SCALE_TYPES[number];

export function getScale(interval: Record<string, string>, selected: string): string[] {
  const scale: string[] = [interval['root']];

  if (selected === 'major')
    scale.push(...addIntervals(interval, ['M2', 'M3', 'P4', 'P5', 'M6', 'M7']));
  if (selected === 'natural minor')
    scale.push(...addIntervals(interval, ['M2', 'm3', 'P4', 'P5', 'm6', 'm7']));
  if (selected === 'harmonic minor')
    scale.push(...addIntervals(interval, ['M2', 'm3', 'P4', 'P5', 'm6', 'M7']));
  if (selected === 'diminished')
    scale.push(...addIntervals(interval, ['M2', 'm3', 'P4', 'P5', 'm7']));
  if (selected === 'augmented')
    scale.push(...addIntervals(interval, ['M2', 'm3', 'P4', 'P5', 'm7']));
  if (selected === 'major pentatonic')
    scale.push(...addIntervals(interval, ['M2', 'M3', 'P5', 'M6']));
  if (selected === 'minor pentatonic')
    scale.push(...addIntervals(interval, ['M2', 'm3', 'P4', 'P5', 'm7']));
  if (selected === 'major blues')
    scale.push(...addIntervals(interval, ['M2', 'M3', 'P4', 'P5', 'M6']));
  if (selected === 'minor blues')
    scale.push(...addIntervals(interval, ['m3', 'P4', 'm6', 'm7']));
  if (selected === 'bebop major')
    scale.push(...addIntervals(interval, ['M2', 'M3', 'P4', 'P5', 'm6', 'M6', 'M7']));
  if (selected === 'bebop dominant')
    scale.push(...addIntervals(interval, ['M2', 'M3', 'P4', 'P5', 'M6', 'm7', 'M7']));
  if (selected === 'bebop minor')
    scale.push(...addIntervals(interval, ['M2', 'm3', 'P4', 'P5', 'M6', 'm7', 'M7']));
  if (selected === 'whole tone')
    scale.push(...addIntervals(interval, ['M2', 'M3', 'tritone', 'm6', 'm7']));

  return scale;
}

export function createScale(scaleNotes: string[], root: string, selected: string): string[] {
  const interval = getIntervals(scaleNotes, root);
  return getScale(interval, selected);
}
