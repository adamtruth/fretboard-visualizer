import sys, math

import tkinter as tk
from PIL import Image, ImageTk

window_title = 'Fretboard Visualizer'
image_path = 'assets/fretboard.png'
screen_resolution = (3456, 2090) # current resolution

colors = {
        'red': (1, 0, 0),
        'orange': (0, 0, 0),
        'yellow': (0 , 0, 0),
        'light_green': (0 , 0, 0),
        'green': (0 , 0, 0),
        'aqua': (0 , 0, 0),
        'blue': (0 , 0, 0),
        'purple': (0 , 0, 0),
        'pink': (0 , 0, 0),
        'black': (0 , 0, 0),
        'grey': (0 , 0, 0)
}

root = tk.Tk()

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

def drawCircle():
    circle = draw.ellipse((50, 50, 150, 150), fill="#F00F4F")  # Red circle
    return circle

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

