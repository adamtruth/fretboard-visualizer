import note
import tkinter as tk

from PIL import Image, ImageDraw, ImageText, ImageTk
from tkinter import ttk

# PIL globals
image_path = 'assets/fretboard.png'
pil_image = Image.open(image_path)

draw = ImageDraw.Draw(pil_image)

# font_path = "assets/fonts/Montserrat.ttf"
# font = ImageFont.truetype(font_path, 32)

# Tkinter globals
root = tk.Tk()

# Circle attributes
# Initial starting location (Open low E string)
x_i, y_i = 45, 57
# Distance between frets (x) and STRING_COUNT (y)
x_bar, y_bar = 120, 45
# radius
r = 15
# offset delta string/fret distances
x_offset, y_offset = 10, 10

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


def show_image():
    root.title('Fretboard Visualizer')
    tk_image = ImageTk.PhotoImage(pil_image)
    label = tk.Label(root, image=tk_image)
    label.pack(padx=100, pady=300)
    notes = note.generate_notes('sharp')
    create_menu('Key', notes)
    create_menu('Type', ['major'])
    root.mainloop()


def display(fretboard_map, notes: list) -> None:
    idx = 0
    for n in notes:
        notes_lists = fretboard_map.get(n)  # all lists

        if idx == 0:
            is_root = True
        else:
            is_root = False

        idx += 1

        for position in notes_lists:
            x, y = position[0], position[1]

            # Describe circle attributes for PIL to draw
            if is_root is True:
                color = 'red'
            else:
                color = 'blue'

            circles = Circle(x, y, r, color)
            circles.drawCircle()

            # So we can center the notes with a accidental
            text = str(note)
            if len(text) == 2:
                x -= 20
            else:
                x -= 18

            y -= 20
            text = Text(x, y, text, TEXT_COLOR)
            text.drawText()

    show_image()


def get_offset(fret):
    if fret == 0:
        return 0
    if fret == 1:
        return 46
    if fret == 2:
        return 39
    if fret == 3:
        return 39
    if fret == 4:
        return 36
    if fret == 5:
        return 36
    if fret == 6:
        return 40
    if fret == 7:
        return 50
    if fret == 8:
        return 57
    if fret == 9:
        return 72
    if fret == 10:
        return 85
    if fret == 11:
        return 105
    if fret == 12:
        return 125


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
