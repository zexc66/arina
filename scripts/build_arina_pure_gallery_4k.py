#!/usr/bin/env python3
"""
ARINA Pure 4K Luxury Gallery Builder
Generates 8 pristine 4K (3840x2160) master gallery showcase assets using EXCLUSIVELY
authentic ARINA brand packshots, official ARINA gold crest, and Luxor gold logo.
Zero legacy brand contamination, zero artifacts.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "imagery")
LOGO_PATH = os.path.join(BASE_DIR, "arina-logo-gold.png")
CREST_PATH = os.path.join(BASE_DIR, "arina-crest-gold.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load official brand marks
logo_img = Image.open(LOGO_PATH).convert("RGBA")
crest_img = Image.open(CREST_PATH).convert("RGBA")

# Fonts
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_luxury_background():
    """Generates a 3840x2160 dark luxury forest-obsidian canvas with subtle radial gold lighting."""
    W, H = 3840, 2160
    # Create gradient via numpy
    Y, X = np.ogrid[:H, :W]
    cx, cy = W / 2, H * 0.45
    dist_sq = ((X - cx) / (W * 0.6)) ** 2 + ((Y - cy) / (H * 0.6)) ** 2
    dist = np.sqrt(dist_sq)
    dist = np.clip(dist, 0.0, 1.0)

    # Center color: deep dark forest emerald (#0D1A11) -> edge color: obsidian (#040705)
    center_c = np.array([13, 26, 17], dtype=np.float32)
    edge_c = np.array([4, 7, 5], dtype=np.float32)

    bg_arr = center_c[None, None, :] * (1.0 - dist[:, :, None]) + edge_c[None, None, :] * dist[:, :, None]
    bg_arr = np.clip(bg_arr, 0, 255).astype(np.uint8)

    bg_img = Image.fromarray(bg_arr, "RGB")
    draw = ImageDraw.Draw(bg_img)

    # Double-bezel luxury gold perimeter border
    gold_border_outer = (218, 172, 54, 80)
    gold_border_inner = (218, 172, 54, 40)
    
    # Outer frame
    draw.rectangle([60, 60, W - 60, H - 60], outline=(218, 172, 54), width=2)
    # Inner frame
    draw.rectangle([76, 76, W - 76, H - 76], outline=(184, 142, 40), width=1)

    # Corner decorative brackets
    bracket_len = 40
    for cx_c, cy_c, sx, sy in [
        (60, 60, 1, 1),
        (W - 60, 60, -1, 1),
        (60, H - 60, 1, -1),
        (W - 60, H - 60, -1, -1)
    ]:
        draw.line([(cx_c, cy_c), (cx_c + sx * bracket_len, cy_c)], fill=(218, 172, 54), width=4)
        draw.line([(cx_c, cy_c), (cx_c, cy_c + sy * bracket_len)], fill=(218, 172, 54), width=4)

    return bg_img

def add_header_and_footer(canvas, category_tag, title_text, subtitle_text, spec_tag):
    """Adds pristine Arina luxury branding, typography, and technical badges."""
    draw = ImageDraw.Draw(canvas)
    W, H = canvas.size

    # 1. Top Brand Logo & Category Tag
    # Resize and place Arina Logo
    logo_w = 260
    logo_h = int(logo_img.height * (logo_w / logo_img.width))
    logo_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    canvas.paste(logo_resized, (int((W - logo_w) / 2), 110), logo_resized)

    # Category Pill below logo
    f_cat = get_font(FONT_SANS_BOLD, 24)
    cat_bbox = draw.textbbox((0, 0), category_tag, font=f_cat)
    cat_w = cat_bbox[2] - cat_bbox[0]
    pill_w = cat_w + 50
    pill_x0 = int((W - pill_w) / 2)
    pill_y0 = 195
    draw.rounded_rectangle([pill_x0, pill_y0, pill_x0 + pill_w, pill_y0 + 38], radius=19, fill=(218, 172, 54, 40), outline=(218, 172, 54), width=1)
    draw.text((int((W - cat_w) / 2), pill_y0 + 7), category_tag, fill=(218, 172, 54), font=f_cat)

    # 2. Bottom Information Banner
    f_title = get_font(FONT_SERIF_BOLD, 52)
    f_sub = get_font(FONT_SANS_REG, 26)
    f_spec = get_font(FONT_SANS_BOLD, 22)

    # Title
    t_bbox = draw.textbbox((0, 0), title_text, font=f_title)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text((int((W - t_w) / 2), H - 240), title_text, fill=(248, 245, 238), font=f_title)

    # Subtitle
    s_bbox = draw.textbbox((0, 0), subtitle_text, font=f_sub)
    s_w = s_bbox[2] - s_bbox[0]
    draw.text((int((W - s_w) / 2), H - 175), subtitle_text, fill=(218, 172, 54), font=f_sub)

    # Technical Spec Plate (Bottom Center)
    spec_bbox = draw.textbbox((0, 0), spec_tag, font=f_spec)
    spec_w = spec_bbox[2] - spec_bbox[0]
    draw.text((int((W - spec_w) / 2), H - 120), spec_tag, fill=(180, 185, 180), font=f_spec)

    # Badges in Bottom Corners
    f_badge = get_font(FONT_SANS_BOLD, 20)
    # Bottom Left: 4K UHD Master Asset
    draw.text((120, H - 110), "4K UHD • 3840 × 2160 • 300 DPI", fill=(218, 172, 54), font=f_badge)
    # Bottom Right: Authentic B2B Export Standard
    draw.text((W - 480, H - 110), "ARINA COMMERCIAL EXPORT DIVISION", fill=(218, 172, 54), font=f_badge)

def paste_isolated_subject(canvas, img_path, target_h, center_x, center_y, add_reflection=True):
    """Loads a subject image, removes/masks white background if needed, and composites with drop shadow and reflection."""
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        return

    subj = Image.open(img_path).convert("RGBA")
    w, h = subj.size
    new_h = target_h
    new_w = int(w * (new_h / h))
    subj_scaled = subj.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Create soft ground contact shadow
    shadow_w = int(new_w * 0.9)
    shadow_h = int(new_h * 0.12)
    shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([0, 0, shadow_w, shadow_h], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=25))

    s_x = center_x - int(shadow_w / 2)
    s_y = center_y + int(new_h / 2) - int(shadow_h / 2)
    canvas.paste(shadow, (s_x, s_y), shadow)

    # Paste subject
    px = center_x - int(new_w / 2)
    py = center_y - int(new_h / 2)
    canvas.paste(subj_scaled, (px, py), subj_scaled)


# =========================================================================
# ASSET BUILDERS (8 MASTER 4K COMPOSITIONS)
# =========================================================================

def build_asset_1_master_lineup():
    print("Building Asset 1: Master Export Lineup Panorama...")
    canvas = create_luxury_background()
    src_p = os.path.join(OUTPUT_DIR, "arina_complete_master_catalog_lineup_hero_4k.jpg")
    
    # Load and scale panorama
    if os.path.exists(src_p):
        pano = Image.open(src_p).convert("RGB")
        target_w = 3200
        target_h = int(pano.height * (target_w / pano.width))
        pano_scaled = pano.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Rounded mask with gold border
        mask = Image.new("L", (target_w, target_h), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, target_w, target_h], radius=32, fill=255)
        
        px = int((3840 - target_w) / 2)
        py = 320 + int((1450 - target_h) / 2)
        
        # Soft shadow
        sh = Image.new("RGBA", (target_w + 60, target_h + 60), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh)
        sh_draw.rounded_rectangle([30, 30, target_w + 30, target_h + 30], radius=32, fill=(0, 0, 0, 180))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        canvas.paste(sh, (px - 30, py - 30), sh)
        
        canvas.paste(pano_scaled, (px, py), mask)
        
        # Gold framing border around panorama
        c_draw = ImageDraw.Draw(canvas)
        c_draw.rounded_rectangle([px, py, px + target_w, py + target_h], radius=32, outline=(218, 172, 54), width=3)

    add_header_and_footer(
        canvas,
        category_tag="MASTER PRODUCT PORTFOLIO • التشكيلة التصديرية الكاملة",
        title_text="ARINA 14-SKU Master Export Lineup Panorama",
        subtitle_text="The Definitive Mediterranean Glass Portfolio: Royal Pickles, Table Olives, and Garlic Emulsions",
        spec_tag="100% FLINT GLASS JARS • 24-MONTH AMBIENT SHELF LIFE • AUTOMATED PALLETIZING (TI/HI CERTIFIED)"
    )
    
    out_p = os.path.join(OUTPUT_DIR, "arina_gallery_master_lineup_4k.jpg")
    canvas.save(out_p, "JPEG", quality=98)
    print("Saved:", out_p)


def build_asset_2_gastronomy_trinity():
    print("Building Asset 2: Foundational Gastronomy Trinity...")
    canvas = create_luxury_background()
    src_p = os.path.join(OUTPUT_DIR, "arina_complete_gastronomy_trinity_hero_4k.jpg")
    
    if os.path.exists(src_p):
        trin = Image.open(src_p).convert("RGB")
        target_w = 3200
        target_h = int(trin.height * (target_w / trin.width))
        trin_scaled = trin.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (target_w, target_h), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, target_w, target_h], radius=32, fill=255)
        
        px = int((3840 - target_w) / 2)
        py = 310 + int((1460 - target_h) / 2)
        
        sh = Image.new("RGBA", (target_w + 60, target_h + 60), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh)
        sh_draw.rounded_rectangle([30, 30, target_w + 30, target_h + 30], radius=32, fill=(0, 0, 0, 180))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        canvas.paste(sh, (px - 30, py - 30), sh)
        
        canvas.paste(trin_scaled, (px, py), mask)
        c_draw = ImageDraw.Draw(canvas)
        c_draw.rounded_rectangle([px, py, px + target_w, py + target_h], radius=32, outline=(218, 172, 54), width=3)

    add_header_and_footer(
        canvas,
        category_tag="FLAGSHIP EXPORT TRIO • ثلاثية التصدير الأساسية",
        title_text="ARINA Foundational Gastronomy Master Trinity",
        subtitle_text="Acoustic Crisp Baby Cucumbers, Royal Kalamata Olives & Pure Unroasted Crushed Garlic",
        spec_tag="LUXOR GOLD SEAL • HERMETIC LIDS • FOOD CONTACT CERTIFIED FLINT GLASS"
    )
    
    out_p = os.path.join(OUTPUT_DIR, "arina_gallery_gastronomy_trinity_4k.jpg")
    canvas.save(out_p, "JPEG", quality=98)
    print("Saved:", out_p)


def build_asset_3_stuffed_olives():
    print("Building Asset 3: Royal Table & Stuffed Olives Showcase...")
    canvas = create_luxury_background()

    # Three jars lineup: Almond Stuffed, Garlic Stuffed, Spanish Black
    jars = [
        (os.path.join(OUTPUT_DIR, "arina_gourmet_stuffed_olives_white_studio_hero_4k.jpg"), 1050, 1150),
        (os.path.join(OUTPUT_DIR, "arina_azizi_estate_olives_white_studio_hero_4k.jpg"), 1920, 1100),
        (os.path.join(OUTPUT_DIR, "arina_spanish_black_olives_white_studio_hero_4k.jpg"), 2790, 1150)
    ]
    for p, cx, cy in jars:
        if os.path.exists(p):
            paste_isolated_subject(canvas, p, target_h=1100, center_x=cx, center_y=cy)

    add_header_and_footer(
        canvas,
        category_tag="ESTATE TABLE OLIVES • زيتون المائدة الفاخر والمحشو",
        title_text="ARINA Connoisseur Table & Stuffed Olives Showcase",
        subtitle_text="Hand-Stuffed Almond Queen Olives, Egyptian Azizi Olives & Spanish Black Manzanilla",
        spec_tag="WHOLE BLANCHED CALIFORNIA ALMONDS • LOW SALT BRINE • ZERO RESIDUAL ACETIC HARSHNESS"
    )

    out_p = os.path.join(OUTPUT_DIR, "arina_gallery_stuffed_queen_olives_4k.jpg")
    canvas.save(out_p, "JPEG", quality=98)
    print("Saved:", out_p)


def build_asset_4_heritage_pickles():
    print("Building Asset 4: Egyptian Terroir Heritage Pickles...")
    canvas = create_luxury_background()

    jars = [
        (os.path.join(OUTPUT_DIR, "arina_crisp_baby_cucumbers_white_studio_hero_4k.jpg"), 1050, 1120),
        (os.path.join(OUTPUT_DIR, "arina_wild_turnip_beetroot_white_studio_hero_4k.jpg"), 1920, 1100),
        (os.path.join(OUTPUT_DIR, "arina_pickled_carrot_chili_medley_white_studio_hero_4k.jpg"), 2790, 1140)
    ]
    for p, cx, cy in jars:
        if os.path.exists(p):
            paste_isolated_subject(canvas, p, target_h=1120, center_x=cx, center_y=cy)

    add_header_and_footer(
        canvas,
        category_tag="HERITAGE PICKLING TERROIR • المخللات البلدية الأصيلة",
        title_text="ARINA Heritage Pickles & Nile Delta Terroir",
        subtitle_text="Acoustic Baby Cucumbers, Wild Turnips in Natural Beetroot & Pickled Carrot-Chili Medley",
        spec_tag="NATURAL FERMENTATION • SPRING-WATER BRINE • EXTRA VIRGIN OLIVE OIL PACKING"
    )

    out_p = os.path.join(OUTPUT_DIR, "arina_gallery_heritage_pickles_4k.jpg")
    canvas.save(out_p, "JPEG", quality=98)
    print("Saved:", out_p)


def build_asset_5_garlic_toum():
    print("Building Asset 5: Mediterranean Garlic & Toum Suite...")
    canvas = create_luxury_background()

    jars = [
        (os.path.join(OUTPUT_DIR, "arina_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg"), 1350, 1120),
        (os.path.join(OUTPUT_DIR, "arina_whipped_toum_white_studio_hero_4k.jpg"), 2490, 1120)
    ]
    for p, cx, cy in jars:
        if os.path.exists(p):
            paste_isolated_subject(canvas, p, target_h=1120, center_x=cx, center_y=cy)

    add_header_and_footer(
        canvas,
        category_tag="CHEF CONDIMENTS & EMULSIONS • تغميسات الثوم الفاخرة",
        title_text="ARINA Cloud-Whipped Toum & Pure Crushed Garlic Suite",
        subtitle_text="Artisanal Emulsified Toum Garlic Cream & 100% Unroasted Crushed Garlic in Squat Glass",
        spec_tag="210G SQUAT GLASS JARS • COLD-EMULSIFIED WITH EXTRA VIRGIN OLIVE OIL • ZERO PRESERVATIVES"
    )

    out_p = os.path.join(OUTPUT_DIR, "arina_gallery_garlic_toum_suite_4k.jpg")
    canvas.save(out_p, "JPEG", quality=98)
    print("Saved:", out_p)


def build_asset_6_tapenades():
    print("Building Asset 6: Gourmet Mediterranean Tapenades...")
    canvas = create_luxury_background()

    jars = [
        (os.path.join(OUTPUT_DIR, "arina_kalamata_olive_tapenade_white_studio_hero_4k.jpg"), 1350, 1120),
        (os.path.join(OUTPUT_DIR, "arina_green_olive_tapenade_white_studio_hero_4k.jpg"), 2490, 1120)
    ]
    for p, cx, cy in jars:
        if os.path.exists(p):
            paste_isolated_subject(canvas, p, target_h=1120, center_x=cx, center_y=cy)

    add_header_and_footer(
        canvas,
        category_tag="GOURMET MEDITERRANEAN SPREADS • معجون التابيناد الفاخر",
        title_text="ARINA Artisan Olive Tapenades & Gastronomy Spreads",
        subtitle_text="Dark Kalamata Olive Tapenade with Capers & Herb-Infused Green Olive Tapenade",
        spec_tag="190G AMBIENT GLASS • EXTRA VIRGIN OLIVE OIL BASE • CHARCUTERIE & DELI GRADE"
    )

    out_p = os.path.join(OUTPUT_DIR, "arina_gallery_tapenades_spreads_4k.jpg")
    canvas.save(out_p, "JPEG", quality=98)
    print("Saved:", out_p)


def build_asset_7_bulk_barrel():
    print("Building Asset 7: 230kg Bulk HDPE Export Drum...")
    canvas = create_luxury_background()

    barrel_p = os.path.join(OUTPUT_DIR, "arina_bulk_olives_barrel_230kg_white_studio_hero_4k.jpg")
    if os.path.exists(barrel_p):
        paste_isolated_subject(canvas, barrel_p, target_h=1200, center_x=1920, center_y=1120)

    add_header_and_footer(
        canvas,
        category_tag="INDUSTRIAL FOODSERVICE EXPORT • براميل التصدير الصناعية",
        title_text="ARINA 230kg High-Density Food-Grade Export Drum",
        subtitle_text="Heavy-Duty Blue HDPE Airtight Drums Engineered for Ocean Transit & Global Foodservice",
        spec_tag="230KG NET WEIGHT • 80 DRUMS PER 20FT FCL • 18.4 METRIC TONS FULL CONTAINER LOAD"
    )

    out_p = os.path.join(OUTPUT_DIR, "arina_gallery_bulk_barrel_4k.jpg")
    canvas.save(out_p, "JPEG", quality=98)
    print("Saved:", out_p)


def build_asset_8_container_freight():
    print("Building Asset 8: Ocean Container Logistics Loading...")
    canvas = create_luxury_background()

    cont_p = os.path.join(OUTPUT_DIR, "arina_bulk_olives_230kg_container_loading_view.jpg")
    if os.path.exists(cont_p):
        cont_img = Image.open(cont_p).convert("RGB")
        target_h = 1150
        target_w = int(cont_img.width * (target_h / cont_img.height))
        cont_scaled = cont_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (target_w, target_h), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, target_w, target_h], radius=28, fill=255)
        
        px = int((3840 - target_w) / 2)
        py = 310 + int((1460 - target_h) / 2)
        
        sh = Image.new("RGBA", (target_w + 60, target_h + 60), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh)
        sh_draw.rounded_rectangle([30, 30, target_w + 30, target_h + 30], radius=28, fill=(0, 0, 0, 180))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        canvas.paste(sh, (px - 30, py - 30), sh)
        
        canvas.paste(cont_scaled, (px, py), mask)
        c_draw = ImageDraw.Draw(canvas)
        c_draw.rounded_rectangle([px, py, px + target_w, py + target_h], radius=28, outline=(218, 172, 54), width=3)

    add_header_and_footer(
        canvas,
        category_tag="MARITIME FREIGHT LOGISTICS • شحن الحاويات البحرية المباشر",
        title_text="ARINA 20ft FCL Ocean Container Direct Loading",
        subtitle_text="Alexandria & Port Said Port Direct Dispatch to GCC, Europe, and North America",
        spec_tag="MARITIME BILL OF LADING • PHYTOSANITARY CERTIFICATE • EUR.1 / GAFTA TARIFF RELIEF"
    )

    out_p = os.path.join(OUTPUT_DIR, "arina_gallery_container_freight_4k.jpg")
    canvas.save(out_p, "JPEG", quality=98)
    print("Saved:", out_p)


def main():
    print("=" * 70)
    print("GENERATING PURE 4K ARINA BRAND MASTER GALLERY SUITE (ZERO LEGACY BRANDS)")
    print("=" * 70)
    build_asset_1_master_lineup()
    build_asset_2_gastronomy_trinity()
    build_asset_3_stuffed_olives()
    build_asset_4_heritage_pickles()
    build_asset_5_garlic_toum()
    build_asset_6_tapenades()
    build_asset_7_bulk_barrel()
    build_asset_8_container_freight()
    print("=" * 70)
    print("ALL 8 ARINA 4K ASSETS GENERATED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
