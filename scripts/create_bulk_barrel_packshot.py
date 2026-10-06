#!/usr/bin/env python3
"""
Generate 4K Studio Packshot for Arina Bulk 230kg HDPE Export Drum
Composites the isolated 230kg industrial barrel with Arina gold crest,
fine typography, and B2B export specification badge on pure white background.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "imagery")
CREST_PATH = os.path.join(BASE_DIR, "arina-crest-gold.png")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
GEN_SRC = "/home/zexc/.gemini/antigravity/brain/8d5f2167-ea3c-4506-99d9-2d545bea6065/bulk_barrel_packshot_1791317967895.jpg"
TARGET_FILE = os.path.join(OUTPUT_DIR, "arina_bulk_olives_barrel_230kg_white_studio_hero_4k.jpg")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    src = Image.open(GEN_SRC).convert("RGB")
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    # Label geometry
    LW, LH = 870, 740
    label = Image.new("RGBA", (LW, LH), (255, 255, 255, 0))
    draw = ImageDraw.Draw(label)

    # Crisp card with metallic gold border
    draw.rounded_rectangle([(0, 0), (LW - 1, LH - 1)], radius=20, fill=(254, 254, 253, 255), outline=(218, 172, 54, 220), width=3)
    draw.rounded_rectangle([(10, 10), (LW - 11, LH - 11)], radius=14, outline=(218, 172, 54, 110), width=1)

    # Luxury Crest
    crest = Image.open(CREST_PATH).convert("RGBA")
    crest_h = 240
    crest_w = int(crest.width * crest_h / crest.height)
    crest_scaled = crest.resize((crest_w, crest_h), Image.Resampling.LANCZOS)
    label.paste(crest_scaled, ((LW - crest_w) // 2, 25), mask=crest_scaled)

    # Fonts
    font_serif = ImageFont.truetype(os.path.join(FONTS_DIR, "PlayfairDisplay.ttf"), 42)
    font_sans_bold = ImageFont.truetype(os.path.join(FONTS_DIR, "Tajawal-Bold.ttf"), 28)
    font_sans_med = ImageFont.truetype(os.path.join(FONTS_DIR, "Tajawal-Medium.ttf"), 22)
    font_small = ImageFont.truetype(os.path.join(FONTS_DIR, "Tajawal-Regular.ttf"), 18)

    # Brand Title
    text_brand = "ARINA"
    bb_b = draw.textbbox((0, 0), text_brand, font=font_serif)
    bw = bb_b[2] - bb_b[0]
    draw.text(((LW - bw) // 2, 275), text_brand, fill=(180, 135, 30), font=font_serif)

    # Product Title
    title_en = "BULK KALAMATA & TABLE OLIVES"
    bb_te = draw.textbbox((0, 0), title_en, font=font_sans_bold)
    draw.text(((LW - (bb_te[2] - bb_te[0])) // 2, 335), title_en, fill=(20, 30, 20), font=font_sans_bold)

    # Divider line
    draw.line([(60, 385), (LW - 60, 385)], fill=(218, 172, 54, 160), width=2)

    # Technical Specifications
    specs = [
        ("NET DRAINED WEIGHT", "155 KG (الوزن المصفى)"),
        ("GROSS BARREL WEIGHT", "230 KG (الوزن القائم)"),
        ("FOOD-GRADE HDPE DRUM", "220 LITERS (سعة 220 لتر)"),
        ("PRESERVATION MEDIUM", "NATURAL FERMENTED BRINE"),
        ("EXPORT SPECIFICATION", "TIER-1 B2B INDUSTRIAL GRADE"),
    ]

    y_pos = 405
    for label_txt, val_txt in specs:
        draw.text((70, y_pos), label_txt, fill=(90, 95, 90), font=font_small)
        bb_val = draw.textbbox((0, 0), val_txt, font=font_sans_med)
        draw.text((LW - 70 - (bb_val[2] - bb_val[0]), y_pos - 2), val_txt, fill=(20, 25, 20), font=font_sans_med)
        y_pos += 48
        draw.line([(70, y_pos - 8), (LW - 70, y_pos - 8)], fill=(230, 230, 230), width=1)

    # Subtle drop shadow
    shadow = Image.new("RGBA", (LW + 40, LH + 40), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow)
    sh_draw.rounded_rectangle([(20, 20), (LW + 20, LH + 20)], radius=24, fill=(0, 0, 0, 50))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))

    # Composite onto 3K Drum
    pos_x, pos_y = 1065, 1145
    im_rgba = im_3k.convert("RGBA")
    im_rgba.paste(shadow, (pos_x - 20, pos_y - 20), mask=shadow)
    im_rgba.paste(label, (pos_x, pos_y), mask=label)

    out = im_rgba.convert("RGB")
    out.save(TARGET_FILE, quality=95)
    print(f"Generated 4K packshot at {TARGET_FILE} ({out.size})")


if __name__ == "__main__":
    main()
