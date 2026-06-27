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


def create_menu(label, items):
    # To capture selected item into a variable
    selected = tk.StringVar()

    menu_button = ttk.Menubutton(root, text=label)
    menu = tk.Menu(menu_button, tearoff=0)

    for item in items:
        menu.add_radiobutton(
                label=item,
                value=item,
                variable=selected)

    menu_button['menu'] = menu
    menu_button.pack(expand=True)

    return selected


def draw_label(text):
    text_label = tk.Label(root, text=text, font=("Arial", 14))
    text_label.pack(padx=300, pady=300)


def reset_image():
    global pil_image, draw
    pil_image = Image.open(image_path)
    draw = ImageDraw.Draw(pil_image)


def show_image(on_apply=None):
    root.title('Fretboard Visualizer')
    tk_image = ImageTk.PhotoImage(pil_image)
    label = tk.Label(root, image=tk_image)
    label.pack(padx=100, pady=300)
    notes = nt.generate_notes('sharp')
    key_menu = create_menu('Key', notes)
    type_menu = create_menu('Type', ['major', 'minor', '7', 'dim', 'aug'])

    def apply():
        reset_image()
        if on_apply:
            on_apply(key_menu.get(), type_menu.get())
        new_image = ImageTk.PhotoImage(pil_image)
        label.config(image=new_image)

    ttk.Button(root, text='Apply', command=apply).pack()
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
