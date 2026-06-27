from PIL import Image, ImageDraw, ImageText


image_path = 'assets/fretboard.png'
# font_path = "assets/fonts/Montserrat.ttf"
image = Image.open(image_path)
draw = ImageDraw.Draw(image)
# font = ImageFont.truetype(font_path, 32)


def show_image():
    image.show()


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
