# Source - https://stackoverflow.com/a/26189022
# Posted by zeronineseven, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-13, License - CC BY-SA 3.0
import math
from tkinter import Tk, Label
from PIL import Image, ImageTk
from cairo import ImageSurface, Context, FORMAT_ARGB32

colors = {
        'red': (1, 0, 0),
        'orange': (0, 0, 0),
        'yellow': (0, 0, 0),
        'light_green': (0, 0, 0),
        'green': (0, 1, 0),
        'aqua': (0, 0, 0),
        'blue': (0, 0, 1),
        'purple': (0, 0, 0),
        'pink': (0, 0, 0),
        'black': (0, 0, 0),
        'grey': (0.7, 0.7, 0.7)
}

class ExampleGui(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        w, h = 400, 1920
        color = colors['red']

        self.geometry("{}x{}".format(w, h))

        self.surface = ImageSurface(FORMAT_ARGB32, w, h)
        self.context = Context(self.surface)

        # Draw something
        cx, cy = w/2, h/2
        r = 60
        self.context.arc(cx, cy, r, 0, 2  * math.pi)
        self.context.set_source_rgb(color[0], color[1], color[2])
        self.context.fill_preserve()

        #  For outlines
        #  self.context.set_line_width(10)
        #  self.context.set_source_rgb(0, 0, 0)
        #  self.context.stroke()

        self._image_ref = ImageTk.PhotoImage(
                Image.frombuffer("RGBA",
                                 (w, h),
                                 self.surface.get_data(),
                                 "raw",
                                 "BGRA", 0, 1))

        self.label = Label(self, image=self._image_ref)
        self.label.pack(expand=True, fill="both")

        self.mainloop()


if __name__ == "__main__":
    ExampleGui()

