import { useEffect, useRef, useState } from 'react';
import { generateNotes, type Accidental } from './lib/notes';
import { createFretboard, type NotePositions } from './lib/fretboard';
import { createScale, SCALE_TYPES } from './lib/scales';
import { createChord, CHORD_TYPES } from './lib/chords';
import { createMode, MODE_TYPES } from './lib/modes';

type ModeSetting = 'chord' | 'scale' | 'mode';

const RADIUS = 15;

function drawNotes(ctx: CanvasRenderingContext2D, fretboardMap: NotePositions, notesList: string[]) {
  notesList.forEach((note, idx) => {
    const positions = fretboardMap[note];
    if (!positions) return;
    const isRoot = idx === 0;

    for (const [x, y] of positions) {
      ctx.beginPath();
      ctx.arc(x, y, RADIUS, 0, Math.PI * 2);
      ctx.fillStyle = isRoot ? '#ef4444' : '#3b82f6';
      ctx.fill();

      ctx.fillStyle = '#fff';
      ctx.font = 'bold 13px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(note, x, y);
    }
  });
}

export default function App() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement | null>(null);

  const [accidental, setAccidental] = useState<Accidental>('flat');
  const [modeSetting, setModeSetting] = useState<ModeSetting>('scale');
  const [key, setKey] = useState('C');
  const [type, setType] = useState('major');

  const notesList = generateNotes(accidental);

  const typeOptions: readonly string[] =
    modeSetting === 'scale' ? SCALE_TYPES :
    modeSetting === 'mode'  ? MODE_TYPES  :
    CHORD_TYPES;

  function redraw(img: HTMLImageElement, currentKey: string, currentType: string, currentAcc: Accidental, currentMode: ModeSetting) {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);

    if (!currentKey || !currentType) return;

    const notes = generateNotes(currentAcc);
    const fretboardMap = createFretboard(notes);

    let result: string[];
    if (currentMode === 'chord') result = createChord(notes, currentKey, currentType);
    else if (currentMode === 'scale') result = createScale(notes, currentKey, currentType);
    else result = createMode(notes, currentKey, currentType);

    drawNotes(ctx, fretboardMap, result);
  }

  useEffect(() => {
    const img = new Image();
    img.src = '/fretboard.png';
    img.onload = () => {
      imageRef.current = img;
      redraw(img, key, type, accidental, modeSetting);
    };
  }, []);

  useEffect(() => {
    if (imageRef.current) redraw(imageRef.current, key, type, accidental, modeSetting);
  }, [key, type, accidental, modeSetting]);

  function handleModeChange(newMode: ModeSetting) {
    setModeSetting(newMode);
    setType('');
  }

  function handleAccidentalChange(newAcc: Accidental) {
    setAccidental(newAcc);
    setKey('');
  }

  const label =
    key && type
      ? modeSetting === 'chord' ? `${key}${type}` : `${key} ${type}`
      : '';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1 style={{ marginBottom: '8px' }}>Fretboard Visualizer</h1>

      <canvas ref={canvasRef} style={{ maxWidth: '100%', borderRadius: '6px' }} />

      {label && (
        <p style={{ fontSize: '1.2rem', fontWeight: 'bold', margin: '10px 0 0' }}>{label}</p>
      )}

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', alignItems: 'center', marginTop: '14px' }}>
        <label>
          Mode&nbsp;
          <select value={modeSetting} onChange={(e) => handleModeChange(e.target.value as ModeSetting)}>
            <option value="chord">Chord</option>
            <option value="scale">Scale</option>
            <option value="mode">Mode</option>
          </select>
        </label>

        <span>
          Accidental&nbsp;
          <label style={{ marginRight: '6px' }}>
            <input type="radio" name="accidental" value="flat"
              checked={accidental === 'flat'}
              onChange={() => handleAccidentalChange('flat')} /> ♭
          </label>
          <label>
            <input type="radio" name="accidental" value="sharp"
              checked={accidental === 'sharp'}
              onChange={() => handleAccidentalChange('sharp')} /> ♯
          </label>
        </span>

        <label>
          Key&nbsp;
          <select value={key} onChange={(e) => setKey(e.target.value)}>
            <option value="">—</option>
            {notesList.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
        </label>

        <label>
          Type&nbsp;
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="">—</option>
            {typeOptions.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>
      </div>
    </div>
  );
}
