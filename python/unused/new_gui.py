from PIL import Image, ImageDraw

window_title = 'Fretboard Visualizer'
image_path = 'assets/fretboard.png'
screen_resolution = (3456, 2090)  # current resolution

colors = {
        'red': (1, 0, 0),
        'orange': (0, 0, 0),
        'yellow': (0, 0, 0),
        'light_green': (0, 0, 0),
        'green': (0, 0, 0),
        'aqua': (0, 0, 0),
        'blue': (0, 0, 0),
        'purple': (0, 0, 0),
        'pink': (0, 0, 0),
        'black': (0, 0, 0),
        'grey': (0, 0, 0)
}

r = 15
x, y = 115, 100
x1, y1 = 115, 100
x2, y2 = 243, 100  # x_bar = 125
x3, y3 = 243, 145  # y_bar = +45
x4, y4 = 243+125, 145+45  # y_bar = +45

image = Image.open(image_path)
draw = ImageDraw.Draw(image)


class Circle():
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


def displayImage():
    # array of colors to select from
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    x, y = 117, 285             # starting at the high e (note f)
    x_bar, y_bar = 125, 45     # distance between strings
    x_offset, y_offset = 0, 0  # offsetting string distances

    for i in range(0, 6):
        circle = Circle(x, y, r, colors[i])
        Circle.drawCircle(circle)

        x = x + x_bar - x_offset
        y = y - y_bar - y_offset

        x_offset += 1
        # if x_offset <= -5:
        #     x_offset += 1

        # y_offset += 1
        if i >= 4:
            y_offset += 1
        # if y_offset == 4:
        #     y_offset = 3

    image.show()


def main():
    displayImage()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User interrupted program.")
