import { addIntervals, getIntervals } from './notes';

export const MODE_TYPES = [
  'ionian', 'dorian', 'phrygian', 'lydian',
  'mixolydian', 'aeolian', 'locrian',
] as const;

export type ModeType = typeof MODE_TYPES[number];

export function getMode(interval: Record<string, string>, selected: string): string[] {
  const mode: string[] = [interval['root']];

  if (selected === 'ionian')      mode.push(...addIntervals(interval, ['M2', 'M3', 'P4', 'P5', 'M6', 'M7']));
  if (selected === 'dorian')      mode.push(...addIntervals(interval, ['M2', 'm3', 'P4', 'P5', 'M6', 'm7']));
  if (selected === 'phrygian')    mode.push(...addIntervals(interval, ['m2', 'm3', 'P4', 'P5', 'm6', 'm7']));
  if (selected === 'lydian')      mode.push(...addIntervals(interval, ['M2', 'M3', 'tritone', 'P5', 'M6', 'M7']));
  if (selected === 'mixolydian')  mode.push(...addIntervals(interval, ['M2', 'M3', 'P4', 'P5', 'M6', 'm7']));
  if (selected === 'aeolian')     mode.push(...addIntervals(interval, ['M2', 'm3', 'P4', 'P5', 'm6', 'm7']));
  if (selected === 'locrian')     mode.push(...addIntervals(interval, ['m2', 'm3', 'P4', 'tritone', 'm6', 'm7']));

  return mode;
}

export function createMode(modeTones: string[], root: string, selected: string): string[] {
  const interval = getIntervals(modeTones, root);
  return getMode(interval, selected);
}
