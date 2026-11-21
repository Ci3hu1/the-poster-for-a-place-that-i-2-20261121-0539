#!/usr/bin/env python3
"""VITRAEL — The Glass Desert. Build-time renderer for the travel poster.

Renders entry.png (1024x1024) for make.fun's "The Poster for a Place
That Isn't There". Procedural Pillow illustration: a glass desert at
golden hour — one glass spire, rippled glass dunes, a lone traveller,
and the place name set in large letterspaced type.

Build-time only: the graded program (main.py) is pure stdlib and just
copies the bundled entry.png. Run: python3 render_poster.py
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SS = 2            # supersample
W, H = 1024, 1024
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def S(v):
    return int(round(v * SS))


def font(path, size):
    return ImageFont.truetype(path, S(size))


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vgrad(img, box, stops):
    """Vertical multi-stop gradient. stops: [(y_frac, (r,g,b)), ...]."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    h = y1 - y0
    for y in range(y0, y1):
        f = (y - y0) / max(1, h)
        for i in range(len(stops) - 1):
            f0, c0 = stops[i]
            f1, c1 = stops[i + 1]
            if f0 <= f <= f1:
                t = 0 if f1 == f0 else (f - f0) / (f1 - f0)
                col = lerp(c0, c1, t)
                break
        else:
            col = stops[-1][1]
        d.line([(x0, y), (x1, y)], fill=col)


def dune_points(cx, base_y, amp, wavelength, phase, y_bottom):
    """Irregular ripple ridge: two sines so the crest is not a scallop."""
    pts = []
    for x in range(0, W + 9, 8):
        y = (base_y
             + amp * math.sin((x / wavelength) * 2 * math.pi + phase)
             + amp * 0.45 * math.sin((x / (wavelength * 0.37)) * 2 * math.pi
                                     + phase * 2.7))
        pts.append((x, y))
    pts.append((W, y_bottom))
    pts.append((0, y_bottom))
    return pts


def draw_spaced(d, cx, y_top, text, fnt, spacing, fill):
    """Draw letterspaced text centred on cx; returns total width."""
    widths = [fnt.getlength(ch) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y_top), ch, font=fnt, fill=fill)
        x += w + spacing
    return total


def main():
    img = Image.new("RGB", (S(W), S(H)))
    d = ImageDraw.Draw(img)

    # --- sky: deep indigo -> violet -> amber horizon -------------------
    vgrad(img, (0, 0, S(W), S(660)), [
        (0.00, (16, 16, 44)),
        (0.35, (58, 38, 94)),
        (0.62, (122, 62, 96)),
        (0.85, (214, 122, 74)),
        (1.00, (238, 164, 92)),
    ])

    # --- faint stars in the upper sky ----------------------------------
    stars = [(90, 70), (210, 45), (330, 110), (470, 60), (600, 90),
             (760, 55), (880, 120), (940, 70), (150, 180), (420, 150),
             (820, 200), (60, 300), (960, 260), (260, 230), (700, 160)]
    for sx, sy in stars:
        r = S(2)
        d.ellipse([S(sx) - r, S(sy) - r, S(sx) + r, S(sy) + r],
                  fill=(255, 240, 210))

    # --- sun + halo (low, right, clear of the subtitle) -------------------
    glow = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([S(770 - 150), S(430 - 150), S(770 + 150), S(430 + 150)],
               fill=(255, 170, 80, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(S(50)))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    d = ImageDraw.Draw(img)
    d.ellipse([S(770 - 62), S(430 - 62), S(770 + 62), S(430 + 62)],
              fill=(255, 233, 184, 255))
    d.ellipse([S(770 - 50), S(430 - 50), S(770 + 50), S(430 + 50)],
              fill=(255, 247, 222, 255))

    # --- distant spire (right, hazy) -------------------------------------
    far = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
    fd = ImageDraw.Draw(far)
    fd.polygon([(S(690), S(500)), (S(655), S(700)), (S(725), S(700))],
               fill=(150, 110, 160, 110))
    far = far.filter(ImageFilter.GaussianBlur(S(3)))
    img = Image.alpha_composite(img, far)
    d = ImageDraw.Draw(img)

    # --- secondary spire (left, shorter) ---------------------------------
    left = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(left)
    ld.polygon([(S(352), S(430)), (S(300), S(700)), (S(352), S(700))],
               fill=(96, 84, 150, 170))
    ld.polygon([(S(352), S(430)), (S(352), S(700)), (S(404), S(700))],
               fill=(216, 130, 70, 180))
    ld.line([(S(352), S(430)), (S(352), S(700))],
            fill=(255, 230, 180, 230), width=S(2))
    img = Image.alpha_composite(img, left)
    d = ImageDraw.Draw(img)

    # --- main glass spire (centre) ---------------------------------------
    spire = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spire)
    # left face: cool violet glass
    sd.polygon([(S(512), S(268)), (S(428), S(700)), (S(512), S(700))],
               fill=(122, 108, 208, 205))
    # right face: sunlit amber glass
    sd.polygon([(S(512), S(268)), (S(512), S(700)), (S(602), S(700))],
               fill=(242, 165, 65, 215))
    # facet lines
    sd.line([(S(512), S(268)), (S(470), S(700))],
            fill=(255, 240, 210, 150), width=S(2))
    sd.line([(S(512), S(268)), (S(556), S(700))],
            fill=(255, 220, 160, 170), width=S(2))
    # bright centre rib
    sd.line([(S(512), S(268)), (S(512), S(700))],
            fill=(255, 246, 224, 255), width=S(3))
    # base edge
    sd.line([(S(428), S(700)), (S(602), S(700))],
            fill=(255, 220, 160, 200), width=S(2))
    spire = spire.filter(ImageFilter.GaussianBlur(S(1)))
    img = Image.alpha_composite(img, spire)
    d = ImageDraw.Draw(img)

    # --- refraction beams from the spire tip ------------------------------
    beams = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beams)
    bd.polygon([(S(512), S(280)), (S(300), S(640)), (S(340), S(640))],
               fill=(255, 220, 150, 55))
    bd.polygon([(S(512), S(280)), (S(760), S(660)), (S(790), S(660))],
               fill=(255, 210, 130, 45))
    beams = beams.filter(ImageFilter.GaussianBlur(S(6)))
    img = Image.alpha_composite(img, beams)
    d = ImageDraw.Draw(img)

    # --- glass dunes (four ridges, near to far) --------------------------
    # each dune: vertical gradient (light crest -> dark base) clipped to
    # its ridge polygon, plus a thin crest highlight.
    dunes = [
        # (base_y, amp, wavelength, phase, crest_col, base_col, crest_line)
        (640, 14, 420, 0.6, (232, 150, 92), (140, 82, 52), (255, 214, 150)),
        (730, 18, 360, 2.1, (196, 112, 72), (104, 54, 44), (255, 196, 130)),
        (830, 22, 300, 4.0, (140, 66, 76), (62, 30, 46), (232, 160, 110)),
        (930, 26, 260, 1.2, (72, 40, 66), (30, 18, 36), (200, 130, 100)),
    ]
    for base_y, amp, wl, ph, crest_col, base_col, crest in dunes:
        pts = dune_points(0, base_y, amp, wl, ph, H)
        mask = Image.new("L", (S(W), S(H)), 0)
        md = ImageDraw.Draw(mask)
        md.polygon([(S(x), S(y)) for x, y in pts], fill=255)
        top_y = int(min(y for _, y in pts))
        grad = Image.new("RGB", (S(W), S(H)))
        vgrad(grad, (0, top_y, S(W), S(H)), [
            (0.0, crest_col), (0.45, lerp(crest_col, base_col, 0.45)),
            (1.0, base_col)])
        layer = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
        layer.paste(grad.convert("RGBA"), (0, 0), mask)
        ld = ImageDraw.Draw(layer)
        crest_pts = [(x, y) for x, y in pts[: len(pts) - 2]]
        ld.line([(S(x), S(y)) for x, y in crest_pts],
                fill=crest + (170,), width=S(2), joint="curve")
        img = Image.alpha_composite(img, layer)
    d = ImageDraw.Draw(img)

    # --- caustic light patches on the dunes -------------------------------
    ca = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
    cd = ImageDraw.Draw(ca)
    for cx, cy, rx, ry in [(640, 760, 90, 16), (300, 860, 120, 20),
                           (780, 880, 100, 18), (180, 740, 70, 12)]:
        cd.ellipse([S(cx - rx), S(cy - ry), S(cx + rx), S(cy + ry)],
                   fill=(255, 200, 120, 70))
    ca = ca.filter(ImageFilter.GaussianBlur(S(10)))
    img = Image.alpha_composite(img, ca)
    d = ImageDraw.Draw(img)

    # --- lone traveller on the third ridge + long shadow -------------------
    # feet sit on the third ridge's crest at x=430 (same ridge function)
    crest_y = (830 + 22 * math.sin((430 / 300) * 2 * math.pi + 4.0)
               + 22 * 0.45 * math.sin((430 / 111) * 2 * math.pi + 4.0 * 2.7))
    tx, ty = 430, int(round(crest_y)) + 2
    sh = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
    shd = ImageDraw.Draw(sh)
    shd.polygon([(S(tx), S(ty)), (S(tx - 110), S(ty + 16)),
                 (S(tx - 110), S(ty + 21)), (S(tx), S(ty + 5))],
                fill=(30, 16, 34, 160))
    img = Image.alpha_composite(img, sh)
    d = ImageDraw.Draw(img)
    d.ellipse([S(tx - 6), S(ty - 46), S(tx + 6), S(ty - 34)],
              fill=(30, 16, 34, 255))                       # head
    d.polygon([(S(tx - 7), S(ty - 34)), (S(tx + 7), S(ty - 34)),
               (S(tx + 6), S(ty - 10)), (S(tx - 6), S(ty - 10))],
              fill=(30, 16, 34, 255))                       # body
    d.line([(S(tx - 4), S(ty - 10)), (S(tx - 7), S(ty))],
           fill=(30, 16, 34, 255), width=S(3))              # legs
    d.line([(S(tx + 4), S(ty - 10)), (S(tx + 8), S(ty))],
           fill=(30, 16, 34, 255), width=S(3))
    # warm rim light on the sun side
    d.line([(S(tx + 6), S(ty - 44)), (S(tx + 7), S(ty - 12))],
           fill=(255, 200, 120, 220), width=S(2))

    # --- type: VITRAEL + subtitle (warm shadow, then cream) ---------------
    name = "VITRAEL"
    f_name = font(SERIF_BOLD, 150)
    spacing = 18
    total = sum(f_name.getlength(ch) for ch in name) + spacing * (len(name) - 1)
    while total > 880:  # keep inside the frame
        f_name = font(SERIF_BOLD, int(f_name.size / SS) - 4)
        spacing = max(6, spacing - 2)
        total = sum(f_name.getlength(ch) for ch in name) + spacing * (len(name) - 1)
    # soft warm shadow copy
    sh_txt = Image.new("RGBA", (S(W), S(H)), (0, 0, 0, 0))
    std = ImageDraw.Draw(sh_txt)
    draw_spaced(std, S(512) + S(4), S(104), name, f_name, S(spacing),
                (120, 50, 30, 160))
    sh_txt = sh_txt.filter(ImageFilter.GaussianBlur(S(4)))
    img = Image.alpha_composite(img, sh_txt)
    d = ImageDraw.Draw(img)
    draw_spaced(d, S(512), S(100), name, f_name, S(spacing), (255, 246, 224, 255))

    sub = "THE GLASS DESERT"
    f_sub = font(SANS, 30)
    sub_spacing = 10
    y_sub = 296
    draw_spaced(d, S(512), S(y_sub), sub, f_sub, S(sub_spacing),
                (255, 246, 224, 255))

    # --- poster frame -------------------------------------------------------
    d.rectangle([S(26), S(26), S(W - 26), S(H - 26)],
                outline=(255, 246, 224, 220), width=S(3))
    d.rectangle([S(36), S(36), S(W - 36), S(H - 36)],
                outline=(255, 246, 224, 110), width=S(1))

    out = img.convert("RGB").resize((W, H), Image.LANCZOS)
    out.save("entry.png", optimize=True)
    import os
    print("wrote entry.png (%d bytes, %s)" % (os.path.getsize("entry.png"), out.size))


if __name__ == "__main__":
    main()
