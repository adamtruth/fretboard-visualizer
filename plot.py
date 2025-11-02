import cairo
from config import scale_colors  # import from config.py

MARGIN = 40
NOTE_RADIUS = 12

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255 for i in (0,2,4))

def draw_circle(ctx, x, y, radius, color):
    if isinstance(color, str):
        if color.startswith('#'):
            ctx.set_source_rgb(*hex_to_rgb(color))
        else:
            named_colors = {
                'red': (1,0,0),
                'orange': (1,0.5,0),
                'yellow': (1,1,0),
                'green': (0,1,0),
                'blue': (0,0,1),
                'purple': (0.75,0,1),
                'pink': (1,0.75,0.8),
                'black': (0,0,0),
                'white': (1,1,1)
            }
            ctx.set_source_rgb(*named_colors.get(color, (0,0,0)))
    else:
        ctx.set_source_rgb(*color)

    ctx.arc(x, y, radius, 0, 2*3.14159)
    ctx.fill()

def draw_centered_text(ctx, x, y, text, size=10):
    ctx.set_source_rgb(0,0,0)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    extents = ctx.text_extents(text)
    ctx.move_to(x - extents.width/2, y + extents.height/2)
    ctx.show_text(text)

def draw_fretboard(ctx, width, height, fretboard, tuning, num_frets, degree_map, root, scale_type):
    num_strings = len(tuning)
    string_spacing = (height - 2*MARGIN) / (num_strings - 1)
    fret_spacing = (width - 2*MARGIN) / num_frets

    # Background
    ctx.set_source_rgb(1,1,1)
    ctx.paint()

    # Draw strings
    ctx.set_line_width(2)
    ctx.set_source_rgb(0,0,0)
    for s in range(num_strings):
        y = MARGIN + s * string_spacing
        ctx.move_to(MARGIN, y)
        ctx.line_to(width - MARGIN, y)
        ctx.stroke()

    # Draw frets
    ctx.set_line_width(1)
    for f in range(num_frets + 1):
        x = MARGIN + f * fret_spacing
        ctx.move_to(x, MARGIN)
        ctx.line_to(x, height - MARGIN)
        ctx.stroke()

    # Draw notes
    for s, string_notes in enumerate(fretboard):
        y = MARGIN + s * string_spacing
        for f, note in enumerate(string_notes):
            if note not in degree_map:
                continue
            x = MARGIN + f * fret_spacing
            deg = degree_map[note]
            color = scale_colors.get(deg, 'red')  # use config.py colors
            draw_circle(ctx, x, y, NOTE_RADIUS, color)
            draw_centered_text(ctx, x, y, note, size=10)

