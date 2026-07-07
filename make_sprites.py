"""Recentre les images detourees et ajoute un contour type sticker."""
from PIL import Image, ImageFilter
import os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# (source, sortie, couleur contour)
JOBS = [
    ("MaliceDetour.png", "sprite_malice.png", (255, 184, 77, 255)),
    ("azelie.png",       "sprite_azelie.png", (255, 122, 184, 255)),
    ("alicia.png",       "sprite_alicia.png", (122, 214, 255, 255)),
]

SIZE = 320       # canevas final (carre)
OUTLINE = 10     # epaisseur du contour en px (sur le canevas final)

for src, out, color in JOBS:
    im = Image.open(os.path.join(DIR, src)).convert("RGBA")

    # 1. recadrage sur le sujet (bbox alpha)
    bbox = im.getchannel("A").getbbox()
    im = im.crop(bbox)

    # 2. redimensionner pour tenir dans le canevas en laissant la place du contour
    inner = SIZE - 2 * (OUTLINE + 6)
    ratio = min(inner / im.width, inner / im.height)
    im = im.resize((max(1, round(im.width * ratio)), max(1, round(im.height * ratio))), Image.LANCZOS)

    # 3. centrer sur canevas carre transparent
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.paste(im, ((SIZE - im.width) // 2, (SIZE - im.height) // 2), im)

    # 4. contour sticker : dilatation du masque alpha
    a = canvas.getchannel("A")
    dil = a.filter(ImageFilter.MaxFilter(OUTLINE * 2 + 1)).filter(ImageFilter.GaussianBlur(1))
    outline_layer = Image.new("RGBA", (SIZE, SIZE), color)
    outline_layer.putalpha(dil.point(lambda v: 255 if v > 40 else 0))
    outline_layer = outline_layer.filter(ImageFilter.GaussianBlur(0.6))

    final = Image.alpha_composite(outline_layer, canvas)
    final.save(os.path.join(DIR, out))
    print("OK", out, final.size)
