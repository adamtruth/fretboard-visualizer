import sys, math

import cairo
import tkinter as tk
from PIL import Image, ImageTk

window_title = 'Fretboard Visualizer'
image_path = 'assets/fretboard.png'
screen_resolution = (3456, 2090) # current resolution

colors = {
        'red': (1, 0, 0),
        'orange': (0, 0, 0),
        'yellow': (0 , 0, 0),
        'light_green': (0 , 0, 0)
        'green': (0 , 0, 0),
        'aqua': (0 , 0, 0),
        'blue': (0 , 0, 0),
        'purple': (0 , 0, 0),
        'pink': (0 , 0, 0),
        'black': (0 , 0, 0),
        'grey': (0 , 0, 0)
}

root = tk.Tk()

# Unused class
class Resolution:
    def __init__(self, path, x, y):
        path = self.path
        x = self.x
        y = self.y

def getImageDimensions(path) -> tuple:
    img = Image.open(path) # from PIL (pillow)
    width, height = img.size
    return (width, height)

def setImagePosition(screen_resolution: tuple,
                     image_resolution: tuple) -> tuple:

    pos_x = (screen_resolution[0] // image_resolution[0]) * 100
    pos_y = (screen_resolution[1] // image_resolution[1]) * 100
    image_position = [pos_x, pos_y]

    return image_position

def setupImage(position):
    root.title(window_title)

    imageObject = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(imageObject)

    label = tk.Label(root, image=tk_image)
    label.image = tk_image
    label.pack(padx=position[0], pady=position[1])

def drawCirclePNG(width, height):
    # Initialize the surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    # Clear background
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()

    cx, cy = width/2, height/2
    r = 60

    ctx.arc(cx, cy, r, 0, 2  * math.pi)
    ctx.set_source_rgb(0.2, 0.6, 0.8)
    ctx.fill_preserve()
    ctx.set_line_width(6)
    ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()

    buf = io.BytesIO()
    surface.write_to_png(buf)
    buf.seek(0)
    return buf

def main():
    image_resolution = getImageDimensions(image_path)
    image_position = setImagePosition(screen_resolution, image_resolution)

    setupImage(image_position)

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User interrupted program.")
        sys.exit(1)

