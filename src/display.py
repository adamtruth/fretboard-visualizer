import notes
import chords
import scales
import modes
import tkinter as tk

from tkinter import ttk, font as tkf
from PIL import Image, ImageDraw, ImageFont, ImageTk

# pil_image is the working canvas. Notes are drawn onto it directly.
image_path = 'assets/fretboard.png'
pil_image = Image.open(image_path)
draw = ImageDraw.Draw(pil_image)
font = ImageFont.load_default(size=16)
root = tk.Tk()

# Set a larger default font for all Tkinter widgets
tkf.nametofont('TkDefaultFont').configure(size=13)
tkf.nametofont('TkTextFont').configure(size=13)

# SCALE resizes the image for display only
# the underlying coordinates stay the same.
SCALE = 1.5

# circle radius for note markers
r = 15
TEXT_COLOR = '#fff'


class Circle:
    def __init__(self, x, y, r, color="red"):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def drawCircle(self):
        draw.circle(
                (self.x - self.r,
                 self.y - self.r,
                 self.x + self.r,
                 self.y + self.r),
                self.r,
                fill=self.color, outline=None, width=1)


class Text:
    def __init__(self, x, y, text, text_color="#fff"):
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        self.font = font

    def drawText(self):
        draw.text((self.x, self.y), self.text, self.text_color, font=self.font)


def scale_image():
    ''' Returns a scaled copy of pil_image for display. '''
    w = int(pil_image.width * SCALE)
    h = int(pil_image.height * SCALE)
    return pil_image.resize((w, h), Image.LANCZOS)


def reset_image():
    ''' Reloads the blank fretboard image, clearing any drawn notes. '''
    global pil_image, draw
    pil_image = Image.open(image_path)
    draw = ImageDraw.Draw(pil_image)

def show_image(apply=None):
    ''' Display PIL image in Tkinter window.
        apply is called when the user clicks Apply. '''
    root.title('Fretboard Visualizer')

    # Fretboard image
    tk_image = ImageTk.PhotoImage(scale_image())
    image_label = tk.Label(root, image=tk_image)
    image_label.image = tk_image  # keep reference so GC doesn't collect it
    image_label.pack(pady=(10, 0))

    # Selected key + type (e.g. "C major")
    name_label = tk.Label(root, text='', font=('Arial', int(14 * SCALE)))
    name_label.pack(pady=5)
    # TODO: Display the notes in the scale below the name_label

    # Controls row
    controls = tk.Frame(root)
    controls.pack(pady=10)

    # StringVars hold the current selection for each control
    # Chord / Scale / Mode
    mode_setting = tk.StringVar(value='Chord')
    key_var = tk.StringVar()    # root note (e.g. C, F#)
    type_var = tk.StringVar()   # type within the mode (e.g. major, dorian)
    accidental_var = tk.StringVar(value='flat')  # flat or sharp note names

    # Mode selection
    tk.Label(controls, text='Mode').pack(side=tk.LEFT, padx=(0, 4))
    mode_menu = ttk.Combobox(controls, textvariable=mode_setting,
                             values=['Chord', 'Scale', 'Mode'],
                             width=6, state='readonly')
    mode_menu.pack(side=tk.LEFT, padx=(0, 10))

    # Preferred Accidental selection
    tk.Label(controls, text='Accidental').pack(side=tk.LEFT, padx=(0, 4))
    ttk.Radiobutton(controls, text='♭', variable=accidental_var,
                    value='flat').pack(side=tk.LEFT)
    ttk.Radiobutton(controls, text='♯', variable=accidental_var,
                    value='sharp').pack(side=tk.LEFT, padx=(0, 10))

    # Key selection
    tk.Label(controls, text='Key').pack(side=tk.LEFT, padx=(0, 2))
    key_menu = ttk.Combobox(controls, textvariable=key_var,
                            values=notes.Notes('flat').notes,
                            width=4, state='readonly')
    key_menu.pack(side=tk.LEFT, padx=(0, 10))

    # Chord/Scale/Mode Type selection e.g. major, minor, etc.
    # Dependent on the mode selected
    tk.Label(controls, text='Type').pack(side=tk.LEFT, padx=(0, 2))
    type_menu = ttk.Combobox(controls,
                             textvariable=type_var,
                             values=chords.TYPES,
                             width=18, state='readonly')
    type_menu.pack(side=tk.LEFT, padx=(0, 10))

    # Callbacks functions

    def update_keys(*_):
        ''' Refreshes the key dropdown when the accidental changes. '''
        key_menu['values'] = notes.Notes(accidental_var.get())
        key_var.set('')

    def update_type_menu(*_):
        ''' Swaps the Type dropdown options when the Mode changes. '''
        mapping = {'chord': chords.TYPES, 'scale': scales.TYPES, 'mode': modes.TYPES}
        # mode_setting stores 'Chord'/'Scale'/'Mode' (capitalized for display),
        # so .lower() is used to match the mapping keys.
        type_menu['values'] = mapping.get(mode_setting.get().lower(), chords.TYPES)
        type_var.set('')

    def refresh(*_):
        ''' Redraws the fretboard whenever the key or type selection changes.
            Skips if either is empty (e.g. mid-selection). '''
        if not key_var.get() or not type_var.get():
            return
        reset_image()
        if apply:
            apply(key_var.get(), type_var.get(),
                     mode_setting.get().lower(), accidental_var.get())
        new_image = ImageTk.PhotoImage(scale_image())
        image_label.config(image=new_image)
        image_label.image = new_image
        sep = '' if mode_setting.get().lower() == 'chord' else ' '
        name_label.config(text=f'{key_var.get()}{sep}{type_var.get()}')

    accidental_var.trace_add('write', update_keys)
    mode_setting.trace_add('write', update_type_menu)
    key_var.trace_add('write', refresh)
    type_var.trace_add('write', refresh)

    root.mainloop()


def draw_notes(fretboard_map, notes: list) -> None:
    ''' Draws a circle and note text
        for each position of a note on the fretboard.
        The root note is highlighted in red; all others are blue. '''
    idx = 0
    for n in notes:
        notes_lists = fretboard_map.get(n)

        is_root = idx == 0
        idx += 1

        for position in notes_lists:
            x, y = position[0], position[1]

            color = 'red' if is_root else 'blue'
            Circle(x, y, r, color).drawCircle()

            # Offset text position to center it inside the circle
            text = str(n)
            x -= 24 if len(text) == 2 else 20
            y -= 24
            Text(x, y, text, TEXT_COLOR).drawText()


def start(fretboard_map, notes: list, apply=None) -> None:
    ''' Display the notes then opens the UI. '''
    draw_notes(fretboard_map, notes)
    show_image(apply)
