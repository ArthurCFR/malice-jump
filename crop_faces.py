"""Detourage : decoupe les visages en bulles circulaires PNG transparentes."""
from PIL import Image, ImageDraw, ImageFilter
import os

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "assets")
os.makedirs(OUT, exist_ok=True)

# (fichier, centre_x, centre_y, rayon, sortie)
CROPS = [
    ("malice.jpeg", 600, 690, 270, "malice.png"),
    ("Azelie.jpeg", 640, 660, 380, "azelie.png"),
    ("ALicia.jpeg", 475, 555, 250, "alicia.png"),
    ("Artus.jpeg", 640, 390, 320, "artus.png"),
]

SIZE = 256  # taille finale de la bulle

for src, cx, cy, r, out in CROPS:
    im = Image.open(os.path.join(DIR, src)).convert("RGBA")
    box = (cx - r, cy - r, cx + r, cy + r)
    crop = im.crop(box).resize((SIZE, SIZE), Image.LANCZOS)

    # masque circulaire avec bord adouci
    mask = Image.new("L", (SIZE * 4, SIZE * 4), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((8, 8, SIZE * 4 - 8, SIZE * 4 - 8), fill=255)
    mask = mask.resize((SIZE, SIZE), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5))

    crop.putalpha(mask)
    crop.save(os.path.join(OUT, out))
    print("OK", out)
