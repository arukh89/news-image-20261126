#!/usr/bin/env python3
"""Draw the front page for Thursday 26 November 2026.

Build-time only: reads no clock, makes no network request, and writes the
same PNG bytes on every run. Story facts come from the official make.fun
edition for 2026-11-26, reworded here; garbled edition headlines were
corrected against the edition's own article hooks before drawing.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (179, 35, 42)
NAVY = (29, 58, 95)
TEAL = (18, 110, 108)
MUSTARD = (196, 138, 20)
GREY = (92, 88, 80)
RULE = (60, 56, 50)
SKY = (214, 230, 240)
SEA = (168, 205, 224)
DOT = (120, 130, 140)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, width, fill, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def badge(draw, cx, cy, num, fill):
    r = 10
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(255, 255, 255), width=2)
    fnt = font(SANS_B, 11)
    label = str(num)
    tw = draw.textlength(label, font=fnt)
    draw.text((cx - tw / 2, cy - 7), label, font=fnt, fill=(255, 255, 255))


LEADS = [
    {
        "n": 1, "place": "NEW YORK", "color": RED,
        "head": "Macy's 100th parade postponed to Saturday",
        "body": "A nor'easter with 60 mph gusts forced the first postponement in 100 years. The parade moves to Sat 28 Nov, 8:30 a.m.; safety first, Macy's said.",
        "src": "AP · REPORTED",
    },
    {
        "n": 2, "place": "MUMBAI", "color": NAVY,
        "head": "India marks 18 years since 26/11 attacks",
        "body": "Tributes for the 166 killed and 300+ injured in 2008's 60-hour siege. India also marked 77 years of its Constitution.",
        "src": "PTI · REPORTED",
    },
    {
        "n": 3, "place": "GENEVA", "color": TEAL,
        "head": "Gukesh-Sindarov Game 3: match level 1-1",
        "body": "Game 2 drew in 20 moves by threefold repetition. Sindarov has White in Game 3 today.",
        "src": "FIDE · REPORTED",
    },
]

CARDS = [
    (4, "RAS TANURA", "Houthis say they hit Saudi refinery",
     "Houthis claim fires; the coalition says it intercepted 4 drones.", "Reuters · CLAIM"),
    (5, "HORMUZ", "Two tankers hit naval mines",
     "Iran says two oil tankers struck naval mines and caught fire in the strait.", "Reuters · REPORTED"),
    (6, "GAZA", "Israeli strike kills Hamas security chief",
     "Col. Mohammed Abu al-Ouf, his wife and two daughters died in Al-Shati camp; 12 wounded.", "AP · REPORTED"),
    (7, "UKRAINE", "Ukraine says laser downed jet drone",
     "Adviser: the Blysk combat laser downed a jet-powered Geran drone. Testing continues.", "Euronews · CLAIM"),
    (8, "UKRAINE", "Russian strikes cut power in 5 regions",
     "At least 5 killed. Zaporizhzhia plant on diesel, 17th loss this year.", "Reuters · REPORTED"),
    (9, "WASHINGTON", "US proposes tariffs on 14 partners",
     "New Section 301 rates include 20% on China. Greer: unlikely to bite for months.", "Reuters · PROPOSED"),
    (10, "DHAKA", "Garment wage up 36% to Tk17,000",
     "Minimum raised from Tk12,500 after protests. New pay from January.", "AP · REPORTED"),
    (11, "MOSCOW", "Leaked data list 490,334 war dead",
     "BBC/Mediazona analysed 11m records; deaths may approach 700,000.", "BBC · REPORTED"),
    (12, "HONIARA", "Solomons sign pact with Australia",
     "Australia named primary security partner, A$740m over a decade; no foreign base.", "AP · REPORTED"),
    (13, "TIANGONG", "Shenzhou-24 docks; first Pakistani",
     "Zeeshan Ali, 40, docked in ~3.5 hours; a week of experiments.", "Xinhua · REPORTED"),
]

BRIEFS = [
    (14, "US jobless claims ease to 187,000", "Reuters"),
    (15, "Nvidia -4%; Nasdaq -0.6%, S&P -0.3%, Dow +0.3%", "Reuters"),
    (16, "EU imposes visa rules, quotas on Chinese cars", "Reuters"),
    (17, "Cartagena: police free 20 hostages after 17h; 1 gunman dead", "AP"),
    (18, "Sudan: RSF drones kill at least 19 in Blue Nile", "Reuters"),
    (19, "Iraq jails Saudi national for 45 years", "Reuters"),
    (20, "Cairo Ring Road tanker fire kills at least 31, injures 21", "AP"),
    (21, "Plane crashes into Gulf of Mexico; six aboard", "AP"),
    (22, "PIA shifts UK flights to its own 777 fleet", "Reuters"),
    (23, "Sooryavanshi, 15, hits 204 off 53 balls, 28 sixes", "Cricinfo"),
    (24, "IITs add 6,000 seats in robotics, AI and space", "Govt of India"),
    (25, "Shanghai party chief Chen Jining under probe", "Reuters"),
    (26, "ESA's Hera images DART crater on Dimorphos", "ESA"),
    (27, "Brazil: mosquitoes cut virus infections 68%", "Study"),
    (28, "Malaysia sues Google RM600m over YouTube content", "Reuters"),
    (29, "Cameroon: elephant kills Swiss tourist on Mt Cameroon", "AP"),
    (30, "Iowa: Army blows up 5 tonnes of explosives", "AP"),
    (31, "Coalition action at Hodeidah after Houthi attacks", "Reuters"),
    (32, "UN: Gaza staff sacked on unfounded claim", "The Guardian"),
]

PINS = {
    1: (-69.0, 45.0), 2: (72.9, 19.1), 3: (6.1, 46.2), 4: (50.2, 26.7),
    5: (56.5, 26.6), 6: (34.4, 31.4), 7: (28.5, 52.0), 8: (35.5, 47.5),
    9: (-81.0, 33.0), 10: (90.4, 23.8), 11: (37.6, 55.8),
    12: (160.0, -9.4), 13: (105.0, 34.0),
}


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-78, 58), (-65, 50), (-60, 46), (-70, 42), (-74, 40),
     (-76, 35), (-81, 31), (-81, 26), (-84, 30), (-89, 30), (-94, 29),
     (-97, 26), (-97, 22), (-94, 18), (-90, 21), (-87, 21), (-83, 9),
     (-79, 9), (-83, 15), (-92, 15), (-97, 16), (-105, 20), (-110, 24),
     (-114, 29), (-117, 33), (-122, 37), (-124, 46), (-130, 54),
     (-140, 60), (-155, 60), (-165, 60)],
    [(-79, 9), (-72, 12), (-64, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-40, -20), (-48, -26), (-52, -32),
     (-58, -38), (-65, -41), (-67, -46), (-69, -52), (-71, -54),
     (-74, -50), (-73, -44), (-72, -37), (-70, -30), (-70, -20),
     (-75, -15), (-79, -8), (-80, -4), (-80, 1), (-77, 4)],
    [(-9, 37), (-9, 43), (-2, 44), (0, 46), (-5, 48), (0, 49), (5, 50),
     (8, 54), (10, 57), (18, 56), (21, 59), (24, 60), (30, 60), (28, 66),
     (40, 66), (50, 69), (70, 72), (90, 75), (110, 74), (130, 72),
     (150, 70), (170, 67), (178, 65), (170, 60), (162, 56), (156, 51),
     (142, 52), (140, 45), (135, 38), (129, 33), (122, 30), (120, 25),
     (110, 20), (108, 12), (105, 5), (100, 6), (98, 10), (95, 16),
     (92, 20), (88, 22), (86, 20), (80, 13), (77, 8), (72, 20), (66, 25),
     (61, 25), (57, 27), (52, 26), (50, 29), (48, 30), (43, 12),
     (38, 20), (35, 28), (36, 36), (30, 36), (27, 37), (23, 36),
     (19, 40), (15, 38), (16, 40), (12, 44), (8, 44), (3, 43), (0, 39),
     (-2, 37)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (35, 28), (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (48, 5),
     (42, -2), (40, -10), (36, -18), (33, -26), (28, -33), (20, -35),
     (17, -32), (14, -22), (12, -15), (13, -5), (9, 0), (8, 4), (2, 6),
     (-5, 5), (-12, 8), (-16, 12), (-17, 15), (-16, 21), (-13, 27),
     (-9, 31)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -36), (140, -38),
     (145, -38), (147, -38), (150, -37), (153, -32), (153, -27),
     (151, -24), (146, -19), (142, -11), (142, -14), (141, -17),
     (136, -15), (135, -12), (132, -11), (126, -14), (122, -17),
     (118, -20)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9),
     (142, -8), (137, -7), (132, -4)],
    [(167, -45), (172, -43), (174, -41), (176, -38), (178, -37),
     (175, -36), (173, -39), (169, -43)],
]


def inside(lon, lat, poly):
    hit = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > lat) != (y2 > lat):
            x = x1 + (lat - y1) * (x2 - x1) / (y2 - y1)
            if lon < x:
                hit = not hit
    return hit


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 244, 248), outline=RULE, width=1)

    def proj(lon, lat):
        x = x0 + (lon + 180) / 360 * (x1 - x0)
        y = y0 + (82 - lat) / 140 * (y1 - y0)
        return x, y

    step = 5
    gy = y0 + 4
    while gy < y1 - 3:
        gx = x0 + 4
        while gx < x1 - 3:
            lon = (gx - x0) / (x1 - x0) * 360 - 180
            lat = 82 - (gy - y0) / (y1 - y0) * 140
            if any(inside(lon, lat, poly) for poly in CONTINENTS):
                draw.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=DOT)
            gx += step
        gy += step
    for num, (lon, lat) in PINS.items():
        cx, cy = proj(lon, lat)
        if num == 13:
            draw.ellipse([cx - 16, cy - 6, cx + 16, cy + 6], outline=TEAL, width=2)
        badge(draw, cx, cy, num, RED if num <= 3 else NAVY)
    draw.rectangle([x0 + 4, y1 - 22, x0 + 330, y1 - 4], fill=(238, 244, 248))
    draw.text((x0 + 8, y1 - 20), "Pins 1-13 match the stories above and below. 13 is in orbit.",
              font=font(SANS, 11), fill=GREY)


def scene_parade(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    for i, h in enumerate([38, 55, 30, 62, 44, 34]):
        bx = x0 + 8 + i * 52
        draw.rectangle([bx, y1 - h, bx + 36, y1], fill=(90, 100, 115))
    draw.ellipse([x0 + 150, y0 + 8, x0 + 205, y0 + 58], fill=RED)
    draw.polygon([(x0 + 172, y0 + 56), (x0 + 183, y0 + 56), (x0 + 177, y0 + 68)], fill=RED)
    draw.line([x0 + 177, y0 + 68, x0 + 177, y0 + 82], fill=INK, width=2)
    for dy in (18, 34, 50):
        draw.arc([x0 + 210, y0 + dy, x0 + 300, y0 + dy + 22], 300, 80, fill=NAVY, width=3)


def scene_memorial(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(30, 42, 66))
    draw.rectangle([x0, y1 - 26, x1, y1], fill=SEA)
    for i in range(5):
        cx = x0 + 55 + i * 55
        draw.rectangle([cx - 5, y1 - 52, cx + 5, y1 - 26], fill=(240, 235, 220))
        draw.ellipse([cx - 4, y1 - 64, cx + 4, y1 - 50], fill=(250, 180, 60))
    draw.arc([x0 + 120, y0 + 6, x0 + 200, y0 + 66], 180, 360, fill=(240, 235, 220), width=5)


def scene_chess(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 230, 214))
    cell = 22
    ox, oy = x0 + 95, y0 + 8
    for r in range(4):
        for c in range(4):
            fill = (90, 64, 40) if (r + c) % 2 else (245, 240, 225)
            draw.rectangle([ox + c * cell, oy + r * cell,
                            ox + (c + 1) * cell, oy + (r + 1) * cell], fill=fill)
    draw.text((x0 + 18, y0 + 30), "1-1", font=font(SERIF_B, 34), fill=INK)
    draw.text((x0 + 215, y0 + 38), "GAME 3", font=font(SANS_B, 16), fill=TEAL)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 24
    right = W - margin

    d.text((margin, 10), "THE WORLD TODAY", font=font(SERIF_B, 30), fill=INK)
    tag = "32 STORIES · 7 REGIONS"
    tw = d.textlength(tag, font=font(SANS_B, 16))
    d.text((right - tw, 18), tag, font=font(SANS_B, 16), fill=RED)
    d.text((margin, 46), "THURSDAY 26 NOVEMBER 2026", font=font(SERIF_B, 47), fill=INK)
    d.line([margin, 108, right, 108], fill=INK, width=3)
    d.line([margin, 114, right, 114], fill=INK, width=1)

    d.text((margin, 122), "THE DAY IN NUMBERS", font=font(SANS_B, 14), fill=RED)
    nums = "60 mph gusts, New York   ·   166 killed in 2008, 18 years on   ·   1-1 in the chess title match   ·   490,334 war dead listed   ·   Tk17,000 garment wage   ·   204 off 53 balls"
    text_block(d, (margin, 142), nums, font(SANS, 13), right - margin, INK, 16)
    d.line([margin, 176, right, 176], fill=RULE, width=1)

    scenes = [scene_parade, scene_memorial, scene_chess]
    col_w = (right - margin - 24) // 3
    for i, lead in enumerate(LEADS):
        x = margin + i * (col_w + 12)
        scenes[i](d, (x, 186, x + col_w, 282))
        place_w = d.textlength(lead["place"], font=font(SANS_B, 13))
        d.rectangle([x + 2, 188, x + 34 + place_w, 212], fill=PAPER)
        badge(d, x + 14, 200, lead["n"], lead["color"])
        d.text((x + 30, 192), lead["place"], font=font(SANS_B, 13), fill=lead["color"])
        y = text_block(d, (x, 290), lead["head"], font(SERIF_B, 20), col_w, INK, 24)
        y = text_block(d, (x, y + 2), lead["body"], font(SANS, 14), col_w, INK, 18)
        d.text((x, y + 2), lead["src"], font=font(SANS_B, 11), fill=GREY)

    d.line([margin, 438, right, 438], fill=RULE, width=1)
    draw_map(d, (margin, 446, 660, 600))

    bx0, by0, bx1, by1 = 676, 446, right, 600
    d.rectangle([bx0, by0, bx1, by1], outline=RED, width=2)
    d.text((bx0 + 10, by0 + 7), "DATE CHECK", font=font(SANS_B, 15), fill=RED)
    check = ("Every story here happened, or was first reported, on Thu 26 Nov "
             "2026 in some time zone. Claims are labelled, not shown as facts.")
    text_block(d, (bx0 + 10, by0 + 29), check, font(SANS, 12), bx1 - bx0 - 20, INK, 15)
    d.text((bx0 + 10, by0 + 84), "HOW TO READ IT", font=font(SANS_B, 13), fill=NAVY)
    legend = "REPORTED = named outlet. CLAIM = one side says it. PROPOSED = not yet in force."
    text_block(d, (bx0 + 10, by0 + 100), legend, font(SANS, 11), bx1 - bx0 - 20, INK, 14)
    regions = "Americas 8, Asia 8, Europe 5, Middle East 4, Africa 4, World 2, Oceania 1"
    text_block(d, (bx0 + 10, by0 + 131), regions, font(SANS, 9), bx1 - bx0 - 20, GREY, 11)

    card_w = (right - margin - 32) // 5
    for i, (num, place, head, body, src) in enumerate(CARDS):
        row, col = divmod(i, 5)
        x = margin + col * (card_w + 8)
        y = 612 + row * 118
        badge(d, x + 10, y + 10, num, NAVY)
        d.text((x + 24, y + 3), place, font=font(SANS_B, 11), fill=NAVY)
        yy = text_block(d, (x, y + 22), head, font(SERIF_B, 13), card_w, INK, 16)
        yy = text_block(d, (x, yy + 1), body, font(SANS, 11), card_w, INK, 13)
        d.text((x, yy + 1), src, font=font(SANS_B, 9), fill=GREY)

    d.line([margin, 848, right, 848], fill=RULE, width=1)
    d.text((margin, 854), "ALSO TODAY", font=font(SANS_B, 14), fill=RED)
    half = (len(BRIEFS) + 1) // 2
    colw = (right - margin - 16) // 2
    for i, (num, text, src) in enumerate(BRIEFS):
        col = 0 if i < half else 1
        row = i if col == 0 else i - half
        x = margin + col * (colw + 16)
        y = 876 + row * 13
        d.text((x, y), "%d." % num, font=font(SANS_B, 11), fill=NAVY)
        line = text + " — " + src
        d.text((x + 26, y), line, font=font(SANS, 11), fill=INK)

    d.line([margin, 1006, right, 1006], fill=INK, width=2)
    foot = "One day, one page: Thursday 26 November 2026 · every story carries its source · 32 stories, 7 regions"
    d.text((margin, 1010), foot, font=font(SANS, 11), fill=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
