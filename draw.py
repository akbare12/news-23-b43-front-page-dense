#!/usr/bin/env python3
"""news-23 b43 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"

BLACK = (17, 17, 17)
WHITE = (255, 255, 255)
PAPER = (250, 248, 240)
GOLD = (201, 162, 39)
GOLD_D = (176, 134, 11)
RED = (178, 34, 34)
RED_B = (192, 57, 43)
NAVY = (11, 42, 74)
NAVY2 = (31, 58, 147)
TEAL = (14, 124, 123)
PURPLE = (125, 60, 152)
GREEN = (39, 174, 96)
CREAM = (253, 245, 220)
GRAY = (93, 109, 126)
LGRAY = (220, 220, 220)

def f_serif(size):
    return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", size)

def f_sans(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def trunc(d, text, font, max_w, ell="..."):
    if d.textlength(text, font=font) <= max_w:
        return text
    while text and d.textlength(text + ell, font=font) > max_w:
        text = text[:-1]
    return text + ell

def chip(d, x, y, label, color):
    ft = f_sans(9, True)
    w = d.textlength(label, font=ft) + 10
    d.rectangle([x, y, x + w, y + 13], fill=color)
    d.text((x + 5, y + 2), label, font=ft, fill=WHITE)
    return w

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 62], fill=BLACK)
d.text((12, 12), "THE WORLD TODAY", font=f_serif(36), fill=WHITE)
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 12 - d.textlength(dt, font=f_sans(20, True)), 20), dt, font=f_sans(20, True), fill=GOLD)

# ---------- kicker ----------
kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
d.text((12, 66), kick, font=f_sans(16, True), fill=RED)

# ---------- number strip: 5 cols x 2 rows ----------
strip = [
    [("-3.3%", "KOSPI", RED_B), ("5.3", "US-CHINA POWER GAP", NAVY2),
     ("11,762", "EBOLA CASES, DRC", (21, 128, 61)), ("10T won", "SEOUL STABILISATION FUND", GOLD_D),
     ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE)],
    [("$450M", "SKUBAL DEAL", PURPLE), ("165", "RUSSIAN MISSILES IN A WEEK", RED_B),
     ("12,000", "CLEARED IN MANCHESTER", NAVY2), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", GOLD_D),
     ("$107.3B", "ANTHROPIC IPO \u2014 LARGEST", PURPLE)],
]
col_w = (W - 24) // 5
for r, row in enumerate(strip):
    y0 = 86 + r * 36
    for c, (num, lab, col) in enumerate(row):
        x = 12 + c * col_w
        d.text((x, y0), num, font=f_sans(23, True), fill=col)
        d.text((x, y0 + 25), lab, font=f_sans(9, True), fill=BLACK)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", TEAL, 290), ("AMERICAS 8", NAVY2, 290),
           ("MIDDLE EAST 6", GOLD_D, 190), ("EUROPE 5", PURPLE, 116),
           ("AFRICA 3", RED_B, 62), ("WORLD 2", GRAY, 60)]
x = 8
for name, col, w in regions:
    d.rectangle([x, 160, x + w, 176], fill=col)
    tw = d.textlength(name, font=f_sans(10, True))
    d.text((x + (w - tw) / 2, 163), name, font=f_sans(10, True), fill=WHITE)
    x += w

# ---------- UTC strip ----------
d.rectangle([0, 178, W, 194], fill=NAVY)
d.text((8, 181), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles   ~18:00 IPO $97.17",
       font=f_sans(10), fill=WHITE)
d.text((W - 8 - d.textlength("~ APPROX", font=f_sans(10)), 181), "~ APPROX", font=f_sans(10), fill=(180, 200, 220))

# ---------- hero scenes ----------
HX0, HY0, HW, GAP = 8, 196, 330, 8
SCENE_H = 140

# --- scene 1: Kospi chart ---
sx = HX0
d.rectangle([sx, HY0, sx + HW, HY0 + SCENE_H], fill=(10, 30, 60))
d.text((sx + 8, HY0 + 6), "-3.3%", font=f_sans(30, True), fill=(255, 90, 70))
# skyline
import random
random.seed(43)
bx = sx + 8
while bx < sx + HW - 14:
    bw = random.randint(16, 30)
    bh = random.randint(28, 62)
    d.rectangle([bx, HY0 + SCENE_H - bh, bx + bw, HY0 + SCENE_H], fill=(24, 52, 92))
    for wy in range(HY0 + SCENE_H - bh + 5, HY0 + SCENE_H - 4, 9):
        for wx in range(bx + 4, bx + bw - 3, 8):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
    bx += bw + 3
# chart line
pts = [(sx + 10, HY0 + 52), (sx + 60, HY0 + 62), (sx + 110, HY0 + 55), (sx + 165, HY0 + 72),
       (sx + 215, HY0 + 66), (sx + 265, HY0 + 82), (sx + 315, HY0 + 78)]
d.line(pts, fill=(255, 90, 70), width=3)
for p in pts:
    d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(255, 214, 90), outline=(255, 90, 70))

# --- scene 2: Guterres ---
sx = HX0 + HW + GAP
d.rectangle([sx, HY0, sx + HW, HY0 + SCENE_H], fill=TEAL)
d.text((sx + 10, HY0 + 8), "150 DELEGATES", font=f_sans(30, True), fill=(255, 214, 90))
d.text((sx + 10, HY0 + 44), "BACK A RISK", font=f_sans(30, True), fill=WHITE)
d.text((sx + 10, HY0 + 80), "FRAMEWORK", font=f_sans(30, True), fill=WHITE)
# globe bottom-right
gx, gy, gr = sx + HW - 34, HY0 + SCENE_H - 26, 17
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(180, 220, 210), outline=WHITE, width=2)
d.ellipse([gx - 8, gy - gr + 2, gx + 8, gy + gr - 2], outline=(90, 140, 130), width=1)
d.line([gx - gr + 2, gy, gx + gr - 2, gy], fill=(90, 140, 130), width=1)

# --- scene 3: power bars ---
sx = HX0 + 2 * (HW + GAP)
d.rectangle([sx, HY0, sx + HW, HY0 + SCENE_H], fill=CREAM)
d.text((sx + 10, HY0 + 6), "NARROWEST SINCE 2018", font=f_sans(11, True), fill=BLACK)
d.text((sx + HW - 10 - d.textlength("GAP 5.3", font=f_sans(11, True)), HY0 + 6), "GAP 5.3", font=f_sans(11, True), fill=GOLD_D)
bars = [("78.9", "US", NAVY, 100), ("73.6", "CHINA", RED_B, 94), ("40.5", "INDIA", GOLD_D, 52)]
base = HY0 + SCENE_H - 6
bx = sx + 22
for val, lab, col, bh in bars:
    d.rectangle([bx, base - bh, bx + 74, base], fill=col)
    d.text((bx + 37 - d.textlength(val, font=f_sans(15, True)) / 2, base - bh + 8), val, font=f_sans(15, True), fill=WHITE)
    d.text((bx + 37 - d.textlength(lab, font=f_sans(11, True)) / 2, base - 20), lab, font=f_sans(11, True), fill=WHITE)
    bx += 96

# hero black bars + headlines + bodies + source/chip
heroes = [
    ("KOSPI 4,708.54  \u00b7  -161 PTS", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.",
     "KOREA EXCHANGE", True),
    ("UN  \u00b7  BRIDGETOWN", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS", True),
    ("ASIA POWER INDEX 2026", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", True),
]
hy_bar = HY0 + SCENE_H
for i, (bar, head, body, src, rep) in enumerate(heroes):
    sx = HX0 + i * (HW + GAP)
    d.rectangle([sx, hy_bar, sx + HW, hy_bar + 16], fill=BLACK)
    d.text((sx + 6, hy_bar + 3), bar, font=f_sans(10, True), fill=WHITE)
    lines = wrap(d, head, f_sans(16, True), HW)
    ly = hy_bar + 20
    for ln in lines[:2]:
        d.text((sx, ly), ln, font=f_sans(16, True), fill=BLACK)
        ly += 19
    blines = wrap(d, body, f_sans(11), HW)
    by = hy_bar + 60
    for ln in blines[:2]:
        d.text((sx, by), ln, font=f_sans(11), fill=BLACK)
        by += 13
    sy = hy_bar + 88
    d.text((sx, sy + 1), src, font=f_sans(9), fill=GRAY)
    chip(d, sx + HW - 62, sy, "REPORTED", NAVY)

# ---------- MORE OF THE DAY ----------
d.rectangle([0, 436, W, 452], fill=BLACK)
d.text((8, 439), "MORE OF THE DAY  \u2014  10 STORIES", font=f_sans(12, True), fill=WHITE)

# ---------- 10 cards: 5 cols x 2 rows ----------
cards = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", True),
    ("FBI", PURPLE, "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", True),
    ("WHITE HOUSE", GOLD_D, "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", True),
    ("MARKETS", GREEN, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", True),
    ("SPORT", RED_B, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", True),
    ("SPORT", RED_B, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", True),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", True),
    ("TECH", NAVY2, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", True),
    ("EUROPE", GOLD_D, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", False),
    ("SPACE", GRAY, "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite may carry a nuke.", "Reuters", False),
]
CW = 200
for idx, (tag, tcol, head, body, src, rep) in enumerate(cards):
    r, c = divmod(idx, 5)
    cx = 8 + c * (CW + 4)
    cy = 456 + r * 100
    d.rectangle([cx, cy, cx + CW, cy + 14], fill=tcol)
    d.text((cx + 4, cy + 2), tag, font=f_sans(10, True), fill=WHITE)
    num = str(idx + 1)
    d.text((cx + CW - 4 - d.textlength(num, font=f_sans(10, True)), cy + 2), num, font=f_sans(10, True), fill=WHITE)
    hlines = wrap(d, head, f_sans(12, True), CW)
    hy = cy + 17
    for ln in hlines[:2]:
        d.text((cx, hy), ln, font=f_sans(12, True), fill=BLACK)
        hy += 14
    by = cy + 48
    d.text((cx, by), trunc(d, body, f_sans(10), CW), font=f_sans(10), fill=BLACK)
    sy = cy + 66
    d.text((cx, sy + 1), src, font=f_sans(9), fill=GRAY)
    chip(d, cx + CW - 62, sy, "REPORTED" if rep else "CLAIM", NAVY if rep else RED_B)

# ---------- map + ALSO header ----------
d.rectangle([0, 656, W, 672], fill=BLACK)
d.text((8, 659), "WHERE IT HAPPENED", font=f_sans(12, True), fill=WHITE)
d.text((340, 659), "ALSO ON MONDAY", font=f_sans(12, True), fill=WHITE)

# ---------- map ----------
mx0, my0, mx1, my1 = 8, 676, 330, 848
d.rectangle([mx0, my0, mx1, my1], fill=(214, 234, 248))
for gx in range(mx0, mx1, 16):
    d.line([gx, my0, gx, my1], fill=(190, 212, 232), width=1)
for gy in range(my0, my1, 16):
    d.line([mx0, gy, mx1, gy], fill=(190, 212, 232), width=1)
# simplified continents
d.ellipse([mx0 + 18, my0 + 18, mx0 + 130, my0 + 118], fill=(139, 195, 122))
d.ellipse([mx0 + 118, my0 + 8, mx0 + 250, my0 + 108], fill=(139, 195, 122))
d.ellipse([mx0 + 240, my0 + 30, mx0 + 312, my0 + 96], fill=(139, 195, 122))
d.ellipse([mx0 + 60, my0 + 118, mx0 + 150, my0 + 164], fill=(139, 195, 122))
d.ellipse([mx0 + 235, my0 + 122, mx0 + 300, my0 + 162], fill=(139, 195, 122))
pins = {
    1: (60, 48), 2: (118, 108), 3: (272, 40), 4: (88, 78), 5: (112, 62),
    6: (205, 72), 7: (80, 96), 8: (48, 92), 9: (68, 112), 10: (96, 118),
    11: (168, 52), 12: (188, 44), 13: (228, 36),
}
for n, (px, py) in pins.items():
    ax, ay = mx0 + px, my0 + py
    d.ellipse([ax - 8, ay - 8, ax + 8, ay + 8], fill=RED_B, outline=WHITE, width=2)
    d.text((ax - 3, ay - 6), str(n), font=f_sans(9, True), fill=WHITE)
leg = ["Pins: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington",
       "5 New York \u00b7 6 Tehran \u00b7 7 Chicago \u00b7 8 San Francisco",
       "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow"]
ly = my1 - 38
for ln in leg:
    d.text((mx0 + 4, ly), ln, font=f_sans(9), fill=BLACK)
    ly += 12

# ---------- ALSO list ----------
also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
    "23. Lebanon seizes 264 kg explosives", "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones", "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns", "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools", "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col = 0 if i < 9 else 1
    row = i if i < 9 else i - 9
    ax = 340 + col * 340
    ay = 678 + row * 19
    d.text((ax, ay), item, font=f_sans(11), fill=BLACK)

# ---------- DATE CHECK ----------
d.rectangle([8, 854, 1016, 928], outline=RED_B, width=3)
d.text((14, 859), "DATE CHECK", font=f_sans(14, True), fill=RED_B)
rt = "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY"
d.text((1010 - d.textlength(rt, font=f_sans(9, True)), 861), rt, font=f_sans(9, True), fill=RED_B)
lo = "LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro captured (22 Nov) \u00b7 EU-Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)"
lol = wrap(d, lo, f_sans(11), 1000)
ly = 880
for ln in lol:
    d.text((14, ly), ln, font=f_sans(11), fill=BLACK)
    ly += 14
d.text((14, ly + 2), "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
       font=f_sans(11), fill=BLACK)

# ---------- footer ----------
d.text((8, 934), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=f_sans(9), fill=GRAY)
d.text((8, 948), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing",
       font=f_sans(9), fill=GRAY)
d.text((8, 962), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=f_sans(9), fill=GRAY)

# ---------- bottom bar ----------
d.rectangle([0, 994, W, 1024], fill=BLACK)
bt = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - d.textlength(bt, font=f_sans(14, True))) / 2, 1003), bt, font=f_sans(14, True), fill=GOLD)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
