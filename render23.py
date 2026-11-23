"""Front page for Monday 23 November 2026, drawn with Pillow.

A broadsheet-style sheet: black masthead, one lead story, four
half-width stories with small drawn motifs, and an ALSO TODAY strip.
No external assets; the same input always renders the same PNG bytes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 40
W = SIZE - 2 * MARGIN

PAPER = (248, 245, 238)
CARD = (255, 253, 248)
INK = (24, 24, 28)
BODY = (58, 58, 64)
RED = (172, 28, 36)
GREY = (110, 110, 116)
LINE = (24, 24, 28)
BLUE = (28, 70, 130)
GOLD = (196, 138, 20)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FDIR}/{name}", size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, limit):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_motif(draw, kind, x, y, s):
    """Small flat motif, drawn in a s x s box at (x, y)."""
    if kind == "sun":
        draw.ellipse([x + s * 0.2, y + s * 0.08, x + s * 0.8, y + s * 0.68], fill=GOLD)
        draw.rectangle([x, y + s * 0.72, x + s, y + s * 0.78], fill=INK)
    elif kind == "ballot":
        draw.rectangle([x + s * 0.1, y + s * 0.3, x + s * 0.9, y + s * 0.95],
                       outline=BLUE, width=5)
        draw.rectangle([x + s * 0.3, y + s * 0.1, x + s * 0.7, y + s * 0.34],
                       fill=BLUE)
        draw.line([x + s * 0.28, y + s * 0.62, x + s * 0.45, y + s * 0.8,
                   x + s * 0.78, y + s * 0.42], fill=RED, width=6)
    elif kind == "building":
        draw.rectangle([x + s * 0.15, y + s * 0.3, x + s * 0.55, y + s * 0.95],
                       fill=GREY)
        draw.rectangle([x + s * 0.6, y + s * 0.5, x + s * 0.9, y + s * 0.95],
                       fill=(150, 150, 156))
        for wy in (0.42, 0.62, 0.82):
            draw.rectangle([x + s * 0.25, y + s * wy, x + s * 0.45, y + s * wy + 7],
                           fill=PAPER)
        draw.ellipse([x + s * 0.58, y, x + s * 0.88, y + s * 0.3], fill=(175, 175, 180))
    elif kind == "flame":
        pts = [(x + s * 0.5, y), (x + s * 0.78, y + s * 0.45),
               (x + s * 0.95, y + s * 0.75), (x + s * 0.7, y + s * 0.95),
               (x + s * 0.3, y + s * 0.95), (x + s * 0.05, y + s * 0.75),
               (x + s * 0.22, y + s * 0.45)]
        draw.polygon(pts, fill=RED)
        draw.ellipse([x + s * 0.35, y + s * 0.55, x + s * 0.65, y + s * 0.85],
                     fill=GOLD)
    elif kind == "plane":
        # paper plane: two triangles
        draw.polygon([(x, y + s * 0.45), (x + s, y + s * 0.2),
                      (x + s * 0.55, y + s * 0.7)], fill=BLUE)
        draw.polygon([(x, y + s * 0.45), (x + s * 0.55, y + s * 0.7),
                      (x + s * 0.35, y + s * 0.95)], fill=(90, 130, 190))


def story_card(draw, x, y, w, h, kicker, headline, body, motif, head_px=28, body_px=18):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=LINE)
    draw.text((x + 12, y + 5), kicker, font=font(SANS_B, 16), fill=PAPER)
    text_w = w - 28
    if motif:
        draw_motif(draw, motif, x + w - 96, y + 42, 84)
        text_w = w - 96 - 40
    cur = y + 42
    hf = font(SERIF_B, head_px)
    for line in wrap(draw, headline, hf, text_w):
        draw.text((x + 14, cur), line, font=hf, fill=INK)
        cur += head_px + 6
    cur += 4
    bf = font(SANS, body_px)
    for line in wrap(draw, body, bf, w - 28):
        draw.text((x + 14, cur), line, font=bf, fill=BODY)
        cur += body_px + 5
    return cur


def also_item(draw, x, y, w, lead, rest):
    """One ALSO TODAY item, wrapped inside w; returns lines used."""
    fb = font(SANS_B, 15)
    fr = font(SANS, 15)
    lead_txt = "• " + lead + " "
    lw = draw.textlength(lead_txt, font=fb)
    lines = wrap(draw, rest, fr, w - lw)
    draw.text((x, y), lead_txt, font=fb, fill=INK)
    draw.text((x + lw, y), lines[0], font=fr, fill=BODY)
    for i, ln in enumerate(lines[1:]):
        draw.text((x, y + (i + 1) * 20), ln, font=fr, fill=BODY)
    return len(lines)


def also_today(draw, x, y, w, items):
    draw.text((x, y), "ALSO TODAY", font=font(SANS_B, 18), fill=RED)
    draw.line([x + 132, y + 11, x + w, y + 11], fill=LINE, width=2)
    col_w = (w - 2 * 20) // 3
    for i, (lead, rest) in enumerate(items):
        cx = x + (i % 3) * (col_w + 20)
        cy = y + 30 + (i // 3) * 46
        also_item(draw, cx, cy, col_w, lead, rest)


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([MARGIN, 26, SIZE - MARGIN, 108], fill=INK)
    d.text((MARGIN + 18, 36), "THE WORLD IN ONE PAGE",
           font=font(SERIF_B, 46), fill=PAPER)
    d.text((MARGIN, 116), "MONDAY 23 NOVEMBER 2026",
           font=font(SANS_B, 26), fill=RED)
    d.line([MARGIN, 152, SIZE - MARGIN, 152], fill=LINE, width=3)

    # Lead story
    story_card(d, MARGIN, 164, W, 232, "CLIMATE  ·  ANTALYA, TÜRKIYE",
               "COP31 ends with no deal after two days of overtime",
               "Nearly 200 countries left the UN climate summit without an "
               "agreed declaration, after the EU and about 130 nations "
               "rejected a text with no fossil-fuel phase-out. The UN chief "
               "warned there is “no ambiguity in the science”.",
               "sun", head_px=38, body_px=20)

    # Rows of half-width stories
    half = (W - 20) // 2
    story_card(d, MARGIN, 410, half, 216, "UNITED STATES",
               "Democrats clinch a historic House majority",
               "At least 258 seats — the largest House majority since 1992.",
               "ballot", head_px=28, body_px=18)
    story_card(d, MARGIN + half + 20, 410, half, 216, "UKRAINE",
               "Russian strikes kill 11 across the Kyiv region",
               "A drone hit a five-storey block in Dymer; a child was pulled "
               "alive from the rubble.",
               "building", head_px=28, body_px=18)
    story_card(d, MARGIN, 640, half, 216, "INDONESIA  ·  BANTEN",
               "Candy factory fire leaves 3 dead, dozens missing",
               "Rescuers recovered remains in 24 body bags at the plant in "
               "Serang; the search for 34 workers resumes.",
               "flame", head_px=28, body_px=18)
    story_card(d, MARGIN + half + 20, 640, half, 216, "TRAVEL  ·  UNITED STATES",
               "Delta delays pile up before Thanksgiving",
               "An automation-system failure delayed more than 1,000 flights "
               "at the airline's Atlanta hub on Sunday.",
               "plane", head_px=28, body_px=18)

    # Also today strip
    also_today(d, MARGIN, 872, W, [
        ("Seoul:", "S. Korea minister quits in exam-cheating row."),
        ("Washington:", "Trump backs Jensen Huang as Nvidia CEO."),
        ("Tehran:", "Trump warns Iran of strikes if no deal by New Year."),
        ("Pyongyang:", "Kim says North wants security."),
        ("Khartoum:", "drones strike homes and a UN building."),
        ("Space:", "BepiColombo spacecraft reaches Mercury."),
    ])

    d.text((MARGIN, 996), "Summarising the world news of Monday 23 November 2026  ·  AFP / AP / Reuters / Xinhua",
           font=font(SANS, 14), fill=GREY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, optimize=True)


if __name__ == "__main__":
    main()
