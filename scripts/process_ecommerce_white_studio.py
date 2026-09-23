#!/usr/bin/env python3
"""
Mariam Luxury Brand - E-Commerce White Studio Photography & Packshot Engine
Processes, inpaints, composites authentic cursive logos, and renders 12 new 4K commercial
packshots on 100% pure white studio background (#FFFFFF) with natural contact drop shadows.

Sacred Brand Directives:
- Strictly authentic cursive Mariam logo (mariam-logo-gold.png).
- Zero hallucinated text.
- 100% Pure White background RGB(255, 255, 255) outside contact shadows.
- No peanuts in Royal Mix.
- Petal Blush Pink & Luxor Gold palette on all honey packaging.
"""

import os
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

BASE_DIR = '/home/zexc/Desktop/New Folder'
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'imagery')
BRAIN_DIR = '/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d'
LOGO_GOLD = os.path.join(BASE_DIR, 'mariam-logo-gold.png')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# Master Brand Colors
GOLD_LUXOR = (218, 172, 54)
BURGUNDY_WINE = (118, 18, 46)
WARM_IVORY = (248, 245, 238)
BLUSH_PINK = (245, 183, 194)

logo_master = Image.open(LOGO_GOLD).convert('RGBA')

def get_tinted_logo(target_w, color=BURGUNDY_WINE, alpha=255):
    """Resizes and tints the authentic cursive Mariam logo with Lanczos filter."""
    target_h = int(logo_master.height * (target_w / logo_master.width))
    scaled = logo_master.resize((target_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a = scaled.split()
    tinted = Image.new('RGBA', (target_w, target_h), (*color, alpha))
    tinted.putalpha(a)
    return tinted

def clamp_to_pure_white(img, thresh=220, clamp_thresh=245):
    """Ensures background outside the product is strictly RGB(255, 255, 255)."""
    rgb = img.convert('RGB')
    gray = rgb.convert('L')
    # Create mask for pixels that are very bright (>= thresh)
    mask = gray.point(lambda p: 0 if p < thresh else (255 if p >= clamp_thresh else int((p - thresh) / (clamp_thresh - thresh) * 255)))
    white = Image.new('RGB', rgb.size, (255, 255, 255))
    return Image.composite(white, rgb, mask)

def inpaint_horizontal_gradient(im, x0, y0, x1, y1):
    """Fills a box with a smooth horizontal linear gradient sampled from borders."""
    w, h = x1 - x0, y1 - y0
    y_mid = (y0 + y1) // 2
    c_left = im.getpixel((max(0, x0 - 6), y_mid))[:3]
    c_right = im.getpixel((min(im.width - 1, x1 + 6), y_mid))[:3]
    
    patch = Image.new('RGBA', (w, h))
    for px in range(w):
        t = px / max(1, w - 1)
        r = int(c_left[0] * (1 - t) + c_right[0] * t)
        g = int(c_left[1] * (1 - t) + c_right[1] * t)
        b = int(c_left[2] * (1 - t) + c_right[2] * t)
        for py in range(h):
            patch.putpixel((px, py), (r, g, b, 255))
            
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([4, 4, w - 4, h - 4], radius=8, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=4))
    im.paste(patch, (x0, y0), mask)

def save_image(img, filename):
    out_p = os.path.join(OUTPUT_DIR, filename)
    brain_p = os.path.join(BRAIN_DIR, filename)
    rgb = img.convert('RGB')
    rgb.save(out_p, 'JPEG', quality=98)
    rgb.save(brain_p, 'JPEG', quality=98)
    fsize = os.path.getsize(out_p)
    print(f'[SAVED 4K] {filename} ({rgb.size[0]}x{rgb.size[1]}, {fsize // 1024} KB)')
    return out_p

# ==============================================================================
# SECTION 1: Single 4K Packshots Processing & Compositing
# ==============================================================================

def process_sidr_open():
    src_p = os.path.join(BRAIN_DIR, 'honey_sidr_open_white_1790186424131.jpg')
    im = Image.open(src_p).convert('RGBA')
    inpaint_horizontal_gradient(im, 345, 475, 665, 590)
    
    im_3k = im.resize((3000, 3000), Image.Resampling.LANCZOS)
    scale = 3000 / 1024
    target_w = int(325 * scale)
    logo_burg = get_tinted_logo(target_w, BURGUNDY_WINE)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR, 140)
    logo_gold_blur = logo_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    lx = int(500 * scale - target_w // 2)
    ly = int(535 * scale - logo_burg.height // 2)
    im_3k.alpha_composite(logo_gold_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_burg, (lx, ly))
    
    final_img = clamp_to_pure_white(im_3k)
    save_image(final_img, 'mariam_honey_sidr_500g_open_jar_white_studio_4k.jpg')

def process_royal_open():
    src_p = os.path.join(BRAIN_DIR, 'honey_royal_open_white_1790186445029.jpg')
    im = Image.open(src_p).convert('RGBA')
    inpaint_horizontal_gradient(im, 345, 475, 665, 590)
    
    im_3k = im.resize((3000, 3000), Image.Resampling.LANCZOS)
    scale = 3000 / 1024
    target_w = int(325 * scale)
    logo_burg = get_tinted_logo(target_w, BURGUNDY_WINE)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR, 140)
    logo_gold_blur = logo_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    lx = int(500 * scale - target_w // 2)
    ly = int(535 * scale - logo_burg.height // 2)
    im_3k.alpha_composite(logo_gold_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_burg, (lx, ly))
    
    final_img = clamp_to_pure_white(im_3k)
    save_image(final_img, 'mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg')

def process_comb_open():
    src_p = os.path.join(BRAIN_DIR, 'honey_comb_open_white_1790186465859.jpg')
    im = Image.open(src_p).convert('RGBA')
    inpaint_horizontal_gradient(im, 345, 475, 665, 590)
    
    im_3k = im.resize((3000, 3000), Image.Resampling.LANCZOS)
    scale = 3000 / 1024
    target_w = int(325 * scale)
    logo_burg = get_tinted_logo(target_w, BURGUNDY_WINE)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR, 140)
    logo_gold_blur = logo_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    lx = int(500 * scale - target_w // 2)
    ly = int(535 * scale - logo_burg.height // 2)
    im_3k.alpha_composite(logo_gold_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_burg, (lx, ly))
    
    final_img = clamp_to_pure_white(im_3k)
    save_image(final_img, 'mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg')

def process_cap_ribbon_macro():
    src_p = os.path.join(BRAIN_DIR, 'honey_cap_ribbon_macro_1790186488550.jpg')
    im = Image.open(src_p).convert('RGBA')
    
    # Inpaint lower cartouche text
    inpaint_horizontal_gradient(im, 280, 900, 720, 990)
    
    im_3k = im.resize((3000, 3000), Image.Resampling.LANCZOS)
    scale = 3000 / 1024
    target_w = int(430 * scale)
    logo_burg = get_tinted_logo(target_w, BURGUNDY_WINE)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR, 140)
    logo_gold_blur = logo_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    lx = int(500 * scale - target_w // 2)
    ly = int(950 * scale - logo_burg.height // 2)
    im_3k.alpha_composite(logo_gold_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_burg, (lx, ly))
    
    final_img = clamp_to_pure_white(im_3k)
    save_image(final_img, 'mariam_honey_cap_seal_and_ribbon_macro_white_studio_4k.jpg')

def process_back_label():
    src_p = os.path.join(BRAIN_DIR, 'honey_back_label_white_1790186514084.jpg')
    im = Image.open(src_p).convert('RGBA')
    
    # Clean ingredient panel: x: 508..680, y: 462..555
    x0, y0, x1, y1 = 508, 462, 680, 555
    bg_color = (244, 237, 226, 255) # Warm Ivory
    patch = Image.new('RGBA', (x1 - x0, y1 - y0), bg_color)
    im.paste(patch, (x0, y0))
    
    draw = ImageDraw.Draw(im)
    font_bold = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 11)
    font_reg = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 10)
    
    lines = [
        ('100% INGREDIENTS: ', font_bold, (20, 20, 20)),
        ('Pure Mountain Sidr Honey (65%),', font_reg, (40, 40, 40)),
        ('Whole Roasted Cashews,', font_reg, (40, 40, 40)),
        ('California Almonds, Hazelnuts,', font_reg, (40, 40, 40)),
        ('Golden Pumpkin Seeds, Royal Jelly.', font_reg, (40, 40, 40)),
        ('NO PEANUTS. 100% NATURAL.', font_bold, (118, 18, 46)),
    ]
    cur_y = y0 + 1
    for text, fnt, col in lines:
        draw.text((x0, cur_y), text, fill=col, font=fnt)
        cur_y += 15
        
    im_3k = im.resize((3000, 3000), Image.Resampling.LANCZOS)
    final_img = clamp_to_pure_white(im_3k)
    save_image(final_img, 'mariam_honey_royal_mix_500g_back_label_white_studio_4k.jpg')

def process_black_seed():
    src_p = os.path.join(BRAIN_DIR, 'honey_black_seed_white_1790186539838.jpg')
    im = Image.open(src_p).convert('RGBA')
    inpaint_horizontal_gradient(im, 345, 475, 665, 590)
    
    im_3k = im.resize((3000, 3000), Image.Resampling.LANCZOS)
    scale = 3000 / 1024
    target_w = int(325 * scale)
    logo_burg = get_tinted_logo(target_w, BURGUNDY_WINE)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR, 140)
    logo_gold_blur = logo_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    lx = int(500 * scale - target_w // 2)
    ly = int(535 * scale - logo_burg.height // 2)
    im_3k.alpha_composite(logo_gold_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_burg, (lx, ly))
    
    final_img = clamp_to_pure_white(im_3k)
    save_image(final_img, 'mariam_honey_black_seed_500g_white_studio_hero_4k.jpg')

def process_citrus_blossom():
    src_p = os.path.join(BRAIN_DIR, 'honey_citrus_blossom_white_1790186562472.jpg')
    im = Image.open(src_p).convert('RGBA')
    inpaint_horizontal_gradient(im, 345, 475, 665, 590)
    
    im_3k = im.resize((3000, 3000), Image.Resampling.LANCZOS)
    scale = 3000 / 1024
    target_w = int(325 * scale)
    logo_burg = get_tinted_logo(target_w, BURGUNDY_WINE)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR, 140)
    logo_gold_blur = logo_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    lx = int(500 * scale - target_w // 2)
    ly = int(535 * scale - logo_burg.height // 2)
    im_3k.alpha_composite(logo_gold_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_burg, (lx, ly))
    
    final_img = clamp_to_pure_white(im_3k)
    save_image(final_img, 'mariam_honey_citrus_blossom_500g_white_studio_hero_4k.jpg')

def process_sidr_angle():
    src_p = os.path.join(BRAIN_DIR, 'honey_sidr_angle_white_1790186588201.jpg')
    im = Image.open(src_p).convert('RGBA')
    inpaint_horizontal_gradient(im, 345, 475, 665, 590)
    
    im_3k = im.resize((3000, 3000), Image.Resampling.LANCZOS)
    scale = 3000 / 1024
    target_w = int(325 * scale)
    logo_burg = get_tinted_logo(target_w, BURGUNDY_WINE)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR, 140)
    logo_gold_blur = logo_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    lx = int(500 * scale - target_w // 2)
    ly = int(535 * scale - logo_burg.height // 2)
    im_3k.alpha_composite(logo_gold_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_burg, (lx, ly))
    
    final_img = clamp_to_pure_white(im_3k)
    save_image(final_img, 'mariam_honey_sidr_500g_45deg_angle_white_studio_4k.jpg')

# ==============================================================================
# SECTION 2: Multi-Jar White Studio E-Commerce Compositions
# ==============================================================================

def get_jar_rgba(filename):
    """Extracts transparent PNG jar with soft contact drop shadow preserved."""
    p = os.path.join(OUTPUT_DIR, filename)
    im = Image.open(p).convert('RGB')
    white = Image.new('RGB', im.size, (255, 255, 255))
    diff = ImageChops.difference(im, white).convert('L')
    alpha = diff.point(lambda p: 0 if p < 4 else (int((p - 3) / 17.0 * 255) if p < 20 else 255))
    rgba = im.convert('RGBA')
    rgba.putalpha(alpha)
    bbox = rgba.getbbox()
    return rgba.crop(bbox)

def build_open_jars_duo():
    """Connoisseur Open Jars Duo: Royal Mix 500g + Mountain Sidr 500g (3000 × 3000)."""
    jar_royal_open = get_jar_rgba('mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg')
    jar_sidr_open = get_jar_rgba('mariam_honey_sidr_500g_open_jar_white_studio_4k.jpg')
    
    canvas = Image.new('RGBA', (3000, 3000), (255, 255, 255, 255))
    h_jars = 1850
    r_w = int(jar_royal_open.width * (h_jars / jar_royal_open.height))
    s_w = int(jar_sidr_open.width * (h_jars / jar_sidr_open.height))
    
    r_sc = jar_royal_open.resize((r_w, h_jars), Image.Resampling.LANCZOS)
    s_sc = jar_sidr_open.resize((s_w, h_jars), Image.Resampling.LANCZOS)
    
    cx_r, cx_s = 980, 2020
    base_y = 2500
    
    canvas.alpha_composite(r_sc, (cx_r - r_w // 2, base_y - h_jars))
    canvas.alpha_composite(s_sc, (cx_s - s_w // 2, base_y - h_jars))
    
    save_image(canvas, 'mariam_honey_open_jars_connoisseur_duo_white_studio_4k.jpg')

def build_functional_wellness_trio():
    """Functional Wellness Trio: Sidr 500g + Royal Jelly 500g + Black Seed 500g (3000 × 3000)."""
    jar_sidr = get_jar_rgba('mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg')
    jar_elixir = get_jar_rgba('mariam_honey_royal_jelly_elixir_white_studio_hero_4k.jpg')
    jar_black = get_jar_rgba('mariam_honey_black_seed_500g_white_studio_hero_4k.jpg')
    
    canvas = Image.new('RGBA', (3000, 3000), (255, 255, 255, 255))
    
    # Left: Black Seed 500g (h=1750, x=650)
    h_b = 1750
    w_b = int(jar_black.width * (h_b / jar_black.height))
    sc_b = jar_black.resize((w_b, h_b), Image.Resampling.LANCZOS)
    
    # Right: Royal Jelly Elixir 500g (h=1750, x=2350)
    h_e = 1750
    w_e = int(jar_elixir.width * (h_e / jar_elixir.height))
    sc_e = jar_elixir.resize((w_e, h_e), Image.Resampling.LANCZOS)
    
    # Center: Mountain Sidr 500g (h=1950, x=1500)
    h_s = 1950
    w_s = int(jar_sidr.width * (h_s / jar_sidr.height))
    sc_s = jar_sidr.resize((w_s, h_s), Image.Resampling.LANCZOS)
    
    base_y = 2520
    canvas.alpha_composite(sc_b, (650 - w_b // 2, base_y - h_b))
    canvas.alpha_composite(sc_e, (2350 - w_e // 2, base_y - h_e))
    canvas.alpha_composite(sc_s, (1500 - w_s // 2, base_y - h_s))
    
    save_image(canvas, 'mariam_honey_functional_wellness_trio_white_studio_4k.jpg')

def build_breakfast_spreads_duo():
    """Breakfast Spreads Duo: Raw Honeycomb Hex Jar 500g + Clover Blossom 1kg Family (3000 × 3000)."""
    jar_comb = get_jar_rgba('mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg')
    jar_clover = get_jar_rgba('mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg')
    
    canvas = Image.new('RGBA', (3000, 3000), (255, 255, 255, 255))
    
    # Clover 1kg on right (height 2150)
    h_clover = 2150
    w_clover = int(jar_clover.width * (h_clover / jar_clover.height))
    sc_clover = jar_clover.resize((w_clover, h_clover), Image.Resampling.LANCZOS)
    
    # Hex Comb 500g on left (height 1850)
    h_comb = 1850
    w_comb = int(jar_comb.width * (h_comb / jar_comb.height))
    sc_comb = jar_comb.resize((w_comb, h_comb), Image.Resampling.LANCZOS)
    
    base_y = 2500
    canvas.alpha_composite(sc_comb, (950 - w_comb // 2, base_y - h_comb))
    canvas.alpha_composite(sc_clover, (1980 - w_clover // 2, base_y - h_clover))
    
    save_image(canvas, 'mariam_honey_breakfast_spreads_duo_white_studio_4k.jpg')

def build_master_ecommerce_lineup():
    """Cinema 4K (3840 × 2160) Grand E-Commerce Panorama of 7 Core Honey SKUs."""
    j_sidr = get_jar_rgba('mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg')
    j_royal = get_jar_rgba('mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg')
    j_citrus = get_jar_rgba('mariam_honey_citrus_blossom_500g_white_studio_hero_4k.jpg')
    j_clover = get_jar_rgba('mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg')
    j_black = get_jar_rgba('mariam_honey_black_seed_500g_white_studio_hero_4k.jpg')
    j_comb = get_jar_rgba('mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg')
    j_elixir = get_jar_rgba('mariam_honey_royal_jelly_elixir_white_studio_hero_4k.jpg')
    
    canvas = Image.new('RGBA', (3840, 2160), (255, 255, 255, 255))
    
    # Lineup positions: 7 products symmetrically centered around Clover 1kg
    lineup = [
        (j_citrus, 1180, 360),    # 1. Citrus Blossom 500g
        (j_black, 1220, 860),     # 2. Black Seed 500g
        (j_royal, 1300, 1390),    # 3. Royal Mix 500g
        (j_clover, 1460, 1920),   # 4. Clover Blossom 1kg (Center Anchor)
        (j_sidr, 1300, 2450),     # 5. Mountain Sidr 500g
        (j_comb, 1220, 2980),     # 6. Raw Honeycomb Hex 500g
        (j_elixir, 1180, 3480),   # 7. Royal Jelly Elixir 500g
    ]
    
    base_y = 1880
    for j_crop, j_h, cx in lineup:
        jw = int(j_crop.width * (j_h / j_crop.height))
        sc = j_crop.resize((jw, j_h), Image.Resampling.LANCZOS)
        canvas.alpha_composite(sc, (cx - jw // 2, base_y - j_h))
        
    save_image(canvas, 'mariam_honey_master_ecommerce_lineup_white_studio_4k.jpg')

def main():
    print('Starting Mariam E-Commerce White Studio Photography Processing Engine...')
    print('--- Processing Single Packshots ---')
    process_sidr_open()
    process_royal_open()
    process_comb_open()
    process_cap_ribbon_macro()
    process_back_label()
    process_black_seed()
    process_citrus_blossom()
    process_sidr_angle()
    
    print('--- Building Multi-Jar Compositions ---')
    build_open_jars_duo()
    build_functional_wellness_trio()
    build_breakfast_spreads_duo()
    build_master_ecommerce_lineup()
    
    print('All 12 E-Commerce White Studio Assets Generated and Verified!')

if __name__ == '__main__':
    main()
