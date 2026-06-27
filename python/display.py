import notes as nt
import tkinter as tk

from tkinter import ttk
from PIL import Image, ImageDraw, ImageText, ImageTk

# PIL globals
image_path = 'assets/fretboard.png'
pil_image = Image.open(image_path)

draw = ImageDraw.Draw(pil_image)

# font_path = "assets/fonts/Montserrat.ttf"
# font = ImageFont.truetype(font_path, 32)

# Tkinter globals
root = tk.Tk()

r = 15
TEXT_COLOR = '#fff'


def reset_image():
    global pil_image, draw
    pil_image = Image.open(image_path)
    draw = ImageDraw.Draw(pil_image)


def show_image(on_apply=None):
    root.title('Fretboard Visualizer')

    CHORD_TYPES = ['major', 'minor', '7', 'dim', 'aug']
    SCALE_TYPES = ['major', 'minor', 'major pentatonic', 'minor pentatonic']

    # Image
    tk_image = ImageTk.PhotoImage(pil_image)
    image_label = tk.Label(root, image=tk_image)
    image_label.image = tk_image
    image_label.pack(pady=(10, 0))

    # Name label below image
    name_label = tk.Label(root, text='', font=('Arial', 14))
    name_label.pack(pady=5)

    # Inline controls row
    controls = tk.Frame(root)
    controls.pack(pady=10)

    # Select scales or chords
    toggle_btn = ttk.Button(controls, text='Scales')
    toggle_btn.pack(side=tk.LEFT, padx=(10, 10))
    mode = tk.StringVar(value='chord')
    key_var = tk.StringVar()
    type_var = tk.StringVar()
    accidental_var = tk.StringVar(value='flat')

    # Select accidental
    tk.Label(controls, text='Accidental').pack(side=tk.LEFT, padx=(0, 4))
    ttk.Radiobutton(controls, text='♭', variable=accidental_var,
                    value='flat').pack(side=tk.LEFT)

    ttk.Radiobutton(controls, text='♯', variable=accidental_var,
                    value='sharp').pack(side=tk.LEFT, padx=(0, 10))

    tk.Label(controls, text='Key').pack(side=tk.LEFT, padx=(0, 2))
    key_menu = ttk.Combobox(controls, textvariable=key_var,
                            values=nt.generate_notes('flat'),
                            width=4, state='readonly')
    key_menu.pack(side=tk.LEFT, padx=(0, 10))

    # Select Chord or Scale type
    tk.Label(controls, text='Type').pack(side=tk.LEFT, padx=(0, 2))
    type_menu = ttk.Combobox(controls,
                             textvariable=type_var,
                             values=CHORD_TYPES,
                             width=18, state='readonly')
    type_menu.pack(side=tk.LEFT, padx=(0, 10))

    apply_btn = ttk.Button(controls, text='Apply')
    apply_btn.pack(side=tk.LEFT, padx=(0, 10))

    def update_keys(*_):
        key_menu['values'] = nt.generate_notes(accidental_var.get())
        key_var.set('')

    accidental_var.trace_add('write', update_keys)

    def toggle_mode():
        if mode.get() == 'chord':
            mode.set('scale')
            type_menu['values'] = SCALE_TYPES
            toggle_btn.config(text='Chords')
        else:
            mode.set('chord')
            type_menu['values'] = CHORD_TYPES
            toggle_btn.config(text='Scales')
        type_var.set('')

    def apply():
        reset_image()
        if on_apply:
            on_apply(key_var.get(), type_var.get(), mode.get(), accidental_var.get())
        new_image = ImageTk.PhotoImage(pil_image)
        image_label.config(image=new_image)
        image_label.image = new_image
        name_label.config(text=f'{key_var.get()} {type_var.get()}')

    toggle_btn.config(command=toggle_mode)
    apply_btn.config(command=apply)

    root.mainloop()


def draw_notes(fretboard_map, notes: list) -> None:
    idx = 0
    for n in notes:
        notes_lists = fretboard_map.get(n)

        is_root = idx == 0
        idx += 1

        for position in notes_lists:
            x, y = position[0], position[1]

            color = 'red' if is_root else 'blue'
            Circle(x, y, r, color).drawCircle()

            text = str(n)
            x -= 20 if len(text) == 2 else 18
            y -= 20
            Text(x, y, text, TEXT_COLOR).drawText()


def display(fretboard_map, notes: list, on_apply=None) -> None:
    draw_notes(fretboard_map, notes)
    show_image(on_apply)


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
        # self.font = font

    def drawText(self):
        text = ImageText.Text(self.text)
        draw.text((self.x, self.y), text, self.text_color)
