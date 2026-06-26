from PIL import Image, ImageDraw, ImageText

image_path = 'assets/fretboard.png'
image = Image.open(image_path)
draw = ImageDraw.Draw(image)


def show_image():
    image.show()


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

    def drawText(self):
        text = ImageText.Text(self.text)
        draw.text((self.x, self.y), text, self.text_color)
