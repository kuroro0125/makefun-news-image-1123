"""Draw the front page for Monday, November 23, 2026.

Run locally:  python3 render23.py
Writes entry.png (1024 x 1024) next to this file.

Only Pillow is needed, and only at authoring time: the submitted
entrypoint (main.py) simply copies the finished image into place,
so the graded program itself needs nothing but the standard library.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 253, 248)
INK = (17, 17, 17)
NAVY = (15, 42, 74)
NAVY_DARK = (10, 30, 54)
RED = (164, 31, 31)
GOLD = (198, 158, 62)
GRAY = (92, 92, 88)
LIGHT = (236, 236, 230)
SKY = (26, 60, 98)
EARTH_BLUE = (52, 110, 168)
EARTH_GREEN = (96, 148, 92)
DUSK = (214, 158, 96)
SMOKE = (150, 150, 146)
FLAME = (224, 110, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Split text into lines that fit inside width pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, gap=6):
    """Draw a wrapped paragraph; return the y below it."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def headline(draw, x, y, text, width, size=54, fill=INK):
    """Draw a headline, shrinking it until it fits the column."""
    while size > 28:
        fnt = font(SERIF_BOLD, size)
        if draw.textlength(text, font=fnt) <= width:
            break
        size -= 2
    fnt = font(SERIF_BOLD, size)
    return para(draw, x, y, text, fnt, width, fill=fill, gap=2)


def kicker(draw, x, y, text):
    fnt = font(SANS_BOLD, 19)
    draw.text((x, y), text.upper(), font=fnt, fill=RED)
    return y + 26


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def globe_panel(draw, x0, y0, x1, y1):
    """A night sky with the Earth, a rising sun and stars."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    for sx, sy, r in [(x0 + 40, y0 + 36, 3), (x0 + 120, y0 + 22, 2),
                      (x0 + 300, y0 + 44, 3), (x0 + 360, y0 + 20, 2),
                      (x0 + 70, y0 + 90, 2), (x0 + 330, y0 + 96, 2)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(240, 240, 230))
    # rising sun, top right
    cx, cy = x1 - 78, y0 + 74
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(232, 178, 74))
    for k in range(12):
        import math
        a = k * math.pi / 6
        x_a, y_a = cx + int(42 * math.cos(a)), cy + int(42 * math.sin(a))
        x_b, y_b = cx + int(56 * math.cos(a)), cy + int(56 * math.sin(a))
        draw.line([(x_a, y_a), (x_b, y_b)], fill=(232, 178, 74), width=4)
    # the Earth
    ex, ey, er = x0 + 190, y0 + 196, 100
    draw.ellipse([ex - er, ey - er, ex + er, ey + er], fill=EARTH_BLUE)
    draw.ellipse([ex - 78, ey - 62, ex - 6, ey + 6], fill=EARTH_GREEN)
    draw.ellipse([ex + 22, ey + 28, ex + 92, ey + 92], fill=EARTH_GREEN)
    draw.ellipse([ex + 34, ey - 84, ex + 82, ey - 30], fill=EARTH_GREEN)
    draw.arc([ex - er, ey - er, ex + er, ey + er], 200, 330, fill=(210, 225, 235), width=5)
    draw.arc([ex - er, ey - er, ex + er, ey + er], 20, 140, fill=(210, 225, 235), width=5)


def kyiv_panel(draw, x0, y0, x1, y1):
    """Dusk skyline: a damaged apartment block, smoke rising."""
    draw.rectangle([x0, y0, x1, y1], fill=DUSK)
    draw.rectangle([x0, y1 - 22, x1, y1], fill=(52, 44, 40))
    # far buildings
    draw.rectangle([x0 + 8, y1 - 84, x0 + 44, y1 - 22], fill=(74, 62, 54))
    draw.rectangle([x1 - 44, y1 - 96, x1 - 8, y1 - 22], fill=(74, 62, 54))
    # the struck block, centre
    bx0, bx1 = x0 + 52, x1 - 52
    draw.rectangle([bx0, y0 + 52, bx1, y1 - 22], fill=(44, 40, 38))
    # broken top corner
    draw.polygon([(bx0 + 34, y0 + 52), (bx1, y0 + 52), (bx1, y0 + 76),
                  (bx0 + 52, y0 + 76)], fill=DUSK)
    # lit windows
    for wy in range(y0 + 70, y1 - 34, 24):
        for wx in [bx0 + 10, bx0 + 34]:
            draw.rectangle([wx, wy, wx + 13, wy + 11], fill=(232, 196, 110))
    # smoke
    for sx, sy, r in [(bx0 + 44, y0 + 40, 12), (bx0 + 56, y0 + 24, 15),
                      (bx0 + 72, y0 + 10, 18)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SMOKE)


def factory_panel(draw, x0, y0, x1, y1):
    """A factory block with flames on the roof and smoke."""
    draw.rectangle([x0, y0, x1, y1], fill=(58, 62, 66))
    roof = y0 + 84
    # chimney, right side
    draw.rectangle([x1 - 34, y0 + 22, x1 - 14, roof], fill=(88, 84, 80))
    # flames above the roof
    for fx, fh in [(x0 + 18, 34), (x0 + 66, 46), (x0 + 112, 30)]:
        draw.polygon([(fx, roof), (fx + 14, roof - fh),
                      (fx + 28, roof)], fill=FLAME)
        draw.polygon([(fx + 6, roof), (fx + 14, roof - fh + 14),
                      (fx + 22, roof)], fill=(240, 200, 90))
    # the factory block
    draw.rectangle([x0, roof, x1, y1], fill=(34, 36, 40))
    draw.rectangle([x0 + 14, roof + 26, x0 + 46, roof + 58], fill=(232, 196, 110))
    draw.rectangle([x0 + 62, roof + 26, x0 + 94, roof + 58], fill=(232, 196, 110))
    draw.rectangle([x0 + 110, roof + 26, x0 + 142, roof + 58], fill=(232, 196, 110))
    # smoke from the chimney
    for sx, sy, r in [(x1 - 24, y0 + 10, 11), (x1 - 34, y0 - 2, 14)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SMOKE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # side margin

    # ---- masthead ----
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 116], fill=GOLD)
    title = font(SERIF_BOLD, 66)
    name = "THE WORLD TODAY"
    tw = d.textlength(name, font=title)
    d.text(((W - tw) / 2, 16), name, font=title, fill=(250, 248, 240))
    sub = font(SANS, 20)
    tag = "THE DAY'S NEWS  •  IN ONE PAGE"
    tw2 = d.textlength(tag, font=sub)
    d.text(((W - tw2) / 2, 84), tag, font=sub, fill=(198, 178, 120))

    # ---- dateline ----
    rule(d, m, W - m, 138)
    dl = font(SANS_BOLD, 22)
    d.text((m, 146), "MONDAY, NOVEMBER 23, 2026", font=dl, fill=INK)
    right = "ANTALYA  •  KYIV  •  SERANG  •  KHARTOUM"
    rw = d.textlength(right, font=font(SANS, 20))
    d.text((W - m - rw, 147), right, font=font(SANS, 20), fill=GRAY)
    rule(d, m, W - m, 182)

    # ---- lead story: COP31 ----
    y = 200
    y = kicker(d, m, y, "Climate — COP31, Antalya")
    y = headline(d, m, y, "CLIMATE TALKS END", W - m - 430, size=58)
    y = headline(d, m, y, "WITHOUT A DEAL", W - m - 430, size=58)
    y += 8
    y = para(d, m, y,
             "Nearly 200 countries closed two days of overtime talks "
             "in Türkiye on Sunday with no overarching agreement.",
             font(SERIF, 24), 500, gap=4)
    y += 6
    y = para(d, m, y,
             "The European Union and about 130 nations rejected a final "
             "text with no language on phasing out fossil fuels, leaving "
             "the summit without a climate declaration.",
             font(SANS, 20), 500, fill=(52, 52, 50), gap=4)
    globe_panel(d, 580, 196, W - m, 500)
    cap = font(SANS, 17)
    d.text((580, 508), "The summit ran almost 48 hours past schedule.",
           font=cap, fill=GRAY)
    d.text((580, 530), "No cover decision was agreed.",
           font=cap, fill=GRAY)

    rule(d, m, W - m, 566)

    # ---- second row: two stories, text beside a small panel ----
    y = 584
    col_w = 452
    text_w = 300
    panel_w = 138
    panel_h = 150
    # left: Kyiv
    yy = kicker(d, m, y, "Ukraine")
    yy = headline(d, m, yy, "DRONE STRIKE HITS", col_w, size=34)
    yy = headline(d, m, yy, "KYIV FLAT BLOCK", col_w, size=34)
    yy += 6
    para(d, m, yy,
         "At least five people were killed when a Russian drone "
         "destroyed part of a five-storey apartment building in "
         "Dymer, north of Kyiv, on Sunday. The region declared "
         "23 November a day of mourning.",
         font(SANS, 18), text_w, fill=(52, 52, 50), gap=3)
    kyiv_panel(d, m + text_w + 14, yy, m + col_w, yy + panel_h)

    # right: Indonesia factory fire
    x2 = W - m - col_w
    yy2 = kicker(d, x2, y, "Indonesia")
    yy2 = headline(d, x2, yy2, "FACTORY FIRE KILLS", col_w, size=34)
    yy2 = headline(d, x2, yy2, "DOZENS; MANY MISSING", col_w, size=34)
    yy2 += 6
    para(d, x2, yy2,
         "A fire at a candy factory in Serang, Banten, has left "
         "at least 24 people dead, with about 30 still "
         "unaccounted for. The blaze was still burning on "
         "Sunday evening.",
         font(SANS, 18), text_w, fill=(52, 52, 50), gap=3)
    factory_panel(d, x2 + text_w + 14, yy2, x2 + col_w, yy2 + panel_h)

    rule(d, m, W - m, 856)

    # ---- also today: four briefs ----
    y = 874
    d.text((m, y), "ALSO TODAY", font=font(SANS_BOLD, 20), fill=RED)
    y += 34
    briefs = [
        ("SPACE", "BepiColombo enters orbit around Mercury after "
         "eight years in flight."),
        ("SOUTH KOREA", "The education minister resigns over an "
         "exam-cheating scandal."),
        ("SUDAN", "Drones strike homes and a United Nations building "
         "in Khartoum."),
        ("SPORT", "Carlos Alcaraz beats Alexander Zverev to win his "
         "first ATP Finals title."),
    ]
    bw = 218
    gapx = 14
    for i, (tag, text) in enumerate(briefs):
        bx = m + i * (bw + gapx)
        d.text((bx, y), tag, font=font(SANS_BOLD, 18), fill=NAVY)
        para(d, bx, y + 26, text, font(SANS, 17), bw,
             fill=(52, 52, 50), gap=2)
        if i < 3:
            d.line([(bx + bw + 7, y), (bx + bw + 7, y + 82)],
                   fill=LIGHT, width=2)

    # ---- footer ----
    rule(d, m, W - m, 994)
    foot = font(SANS, 16)
    d.text((m, 1002), "Compiled from wire reports  •  Monday, November 23, 2026",
           font=foot, fill=GRAY)
    pg = "PAGE 1"
    pw = d.textlength(pg, font=foot)
    d.text((W - m - pw, 1002), pg, font=foot, fill=GRAY)

    img.save("entry.png", "PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
