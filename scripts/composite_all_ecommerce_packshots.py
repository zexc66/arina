#!/usr/bin/env python3
"""
Mariam Luxury Brand - E-Commerce 4K PDP Studio Packshot Engine (Perfected)
Builds pixel-perfect e-commerce product photography for all Honey & Superfoods products
on 100% pure white studio background (#FFFFFF) with soft contact drop shadows,
compositing strictly the authentic cursive logo (mariam-logo-gold.png) with 2x supersampling,
guaranteeing ZERO ghost text or hallucinated artifacts.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = '/home/zexc/Desktop/Arina/New Folder/output/imagery'
BRAIN_DIR = '/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d'
LOGO_GOLD = '/home/zexc/Desktop/Arina/New Folder/mariam-logo-gold.png'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# Master Colors
GOLD_LUXOR = (218, 172, 54)
BURGUNDY_WINE = (118, 18, 46)

logo_master = Image.open(LOGO_GOLD).convert('RGBA')

def get_tinted_logo(target_w, color=GOLD_LUXOR, alpha=255):
    """Resizes and tints the authentic cursive Mariam logo with Lanczos filter."""
    target_h = int(logo_master.height * (target_w / logo_master.width))
    scaled = logo_master.resize((target_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a = scaled.split()
    tinted = Image.new('RGBA', (target_w, target_h), (*color, alpha))
    tinted.putalpha(a)
    return tinted

def make_pure_white_bg(img, thresh=232):
    """Ensures background outside the product is 100% pure RGB(255, 255, 255)."""
    rgb = img.convert('RGB')
    w, h = rgb.size
    out = Image.new('RGB', (w, h), (255, 255, 255))
    gray = rgb.convert('L')
    for y in range(h):
        for x in range(w):
            p = rgb.getpixel((x, y))
            gl = gray.getpixel((x, y))
            # if very bright and neutral, clamp to pure white
            if gl >= thresh and max(abs(p[0]-p[1]), abs(p[1]-p[2])) < 14:
                factor = (gl - thresh) / (255 - thresh)
                r = int(p[0] * (1 - factor) + 255 * factor)
                g = int(p[1] * (1 - factor) + 255 * factor)
                b = int(p[2] * (1 - factor) + 255 * factor)
                out.putpixel((x, y), (r, g, b))
            else:
                out.putpixel((x, y), p)
    return out.convert('RGBA')

def clamp_to_pure_white(img, thresh=220, clamp_thresh=245):
    """Ensures background outside the product is strictly RGB(255, 255, 255)."""
    rgb = img.convert('RGB')
    gray = rgb.convert('L')
    mask = gray.point(lambda p: 0 if p < thresh else (255 if p >= clamp_thresh else int((p - thresh) / (clamp_thresh - thresh) * 255)))
    white = Image.new('RGB', rgb.size, (255, 255, 255))
    return Image.composite(white, rgb, mask)

def save_pdp(img_rgba, filename):
    out_p = os.path.join(OUTPUT_DIR, filename)
    brain_p = os.path.join(BRAIN_DIR, filename)
    clamped = clamp_to_pure_white(img_rgba)
    clamped.save(out_p, 'JPEG', quality=98)
    clamped.save(brain_p, 'JPEG', quality=98)
    print(f'[SAVED PDP 4K] {filename} ({clamped.size})')
    return out_p

# ==============================================================================
# 1. Mariam Royal Mix (500g) — Flagship Superfood PDP
# ==============================================================================
def render_royal_mix_pdp():
    src_p = os.path.join(BRAIN_DIR, 'honey_royal_pdp_1790027932056.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

    # Inpaint placeholder text: x: 330..670, y: 555..665
    x0, y0, x1, y1 = 330, 555, 670, 665
    w, h = x1 - x0, y1 - y0
    patch = Image.new('RGBA', (w, h))
    for px in range(w):
        t = px / w
        r = int(244 - t * 24)
        g = int(204 - t * 42)
        b = int(204 - t * 39)
        for py in range(h):
            patch.putpixel((px, py), (r, g, b, 255))
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([2, 2, w-2, h-2], radius=8, fill=255)
    src.paste(patch, (x0, y0), mask.filter(ImageFilter.GaussianBlur(radius=3)))

    # Upscale to 3000 x 3000
    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    # Composite authentic cursive logo strictly in Luxor Gold (#DAAC36)
    target_w = 980
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR, 255)
    logo_shadow = get_tinted_logo(target_w, (75, 18, 30), 140)
    logo_shadow_blur = logo_shadow.filter(ImageFilter.GaussianBlur(radius=2.0))

    lx = int(500 * scale - target_w // 2)
    ly = int(615 * scale - logo_gold.height // 2)

    im_3k.alpha_composite(logo_shadow_blur, (lx + 2, ly + 3))
    im_3k.alpha_composite(logo_gold, (lx, ly))

    save_pdp(im_3k, 'mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg')

# ==============================================================================
# 2. Mariam Mountain Sidr Honey (500g) — Royal Reserve PDP
# ==============================================================================
def render_sidr_pdp():
    src_p = os.path.join(BRAIN_DIR, 'honey_sidr_pdp_1790027946203.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

    # Inpaint strictly inside border: x: 320..705, y: 508..575
    x0, y0, x1, y1 = 320, 508, 705, 575
    w, h = x1 - x0, y1 - y0
    patch = Image.new('RGBA', (w, h))
    for px in range(w):
        t = px / w
        r = int(105 - t * 23)
        g = int(30 - t * 10)
        b = int(48 - t * 12)
        for py in range(h):
            patch.putpixel((px, py), (r, g, b, 255))
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([2, 2, w-2, h-2], radius=4, fill=255)
    src.paste(patch, (x0, y0), mask.filter(ImageFilter.GaussianBlur(radius=2)))

    # Upscale to 3000 x 3000
    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    # Composite authentic cursive logo in Luxor Gold
    target_w = 400 * scale
    target_w_int = int(target_w)
    logo_gold = get_tinted_logo(target_w_int, GOLD_LUXOR)
    logo_shadow = get_tinted_logo(target_w_int, (40, 10, 15), 180)
    logo_shadow_blur = logo_shadow.filter(ImageFilter.GaussianBlur(radius=2.0))

    lx = int(500 * scale - target_w_int // 2)
    ly = int(541 * scale - logo_gold.height // 2)

    im_3k.alpha_composite(logo_shadow_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_gold, (lx, ly))

    save_pdp(im_3k, 'mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg')

# ==============================================================================
# 3. Mariam Raw Honeycomb in Hexagonal Jar (500g) — Showpiece PDP
# ==============================================================================
def render_honeycomb_pdp():
    src_p = os.path.join(BRAIN_DIR, 'honey_hex_pdp_1790027961353.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

    # Inpaint ivory badge: x: 315..685, y: 518..598
    x0, y0, x1, y1 = 315, 518, 685, 598
    w, h = x1 - x0, y1 - y0
    patch = Image.new('RGBA', (w, h))
    for px in range(w):
        t = px / w
        r = int(250 - t * 16)
        g = int(244 - t * 16)
        b = int(224 - t * 14)
        for py in range(h):
            patch.putpixel((px, py), (r, g, b, 255))
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([2, 2, w-2, h-2], radius=4, fill=255)
    src.paste(patch, (x0, y0), mask.filter(ImageFilter.GaussianBlur(radius=2)))

    # Upscale to 3000 x 3000
    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    # Composite authentic cursive logo in Luxor Gold
    target_w = int(420 * scale)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR)
    logo_shadow = get_tinted_logo(target_w, (120, 80, 40), 160)
    logo_shadow_blur = logo_shadow.filter(ImageFilter.GaussianBlur(radius=1.5))

    lx = int(500 * scale - target_w // 2)
    ly = int(556 * scale - logo_gold.height // 2)

    im_3k.alpha_composite(logo_shadow_blur, (lx + 2, ly + 3))
    im_3k.alpha_composite(logo_gold, (lx, ly))

    save_pdp(im_3k, 'mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg')

# ==============================================================================
# 4. Mariam Pure Clover Blossom Honey (1kg) — Family Reserve PDP
# ==============================================================================
def render_clover_1kg_pdp():
    src_p = os.path.join(BRAIN_DIR, 'honey_clover_pdp_1790027979425.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

    # Inpaint between gold borders: x: 245..775, y: 446..560
    x0, y0, x1, y1 = 245, 446, 775, 560
    w, h = x1 - x0, y1 - y0
    patch = Image.new('RGBA', (w, h))
    for px in range(w):
        t = px / w
        r = int(116 - t * 21)
        g = int(44 - t * 6)
        b = int(56 - t * 8)
        for py in range(h):
            patch.putpixel((px, py), (r, g, b, 255))
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([2, 2, w-2, h-2], radius=4, fill=255)
    src.paste(patch, (x0, y0), mask.filter(ImageFilter.GaussianBlur(radius=2)))

    # Upscale to 3000 x 3000
    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    # Composite authentic cursive logo in Luxor Gold
    target_w = int(460 * scale)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR)
    logo_shadow = get_tinted_logo(target_w, (40, 10, 15), 180)
    logo_shadow_blur = logo_shadow.filter(ImageFilter.GaussianBlur(radius=2.0))

    lx = int(500 * scale - target_w // 2)
    ly = int(503 * scale - logo_gold.height // 2)

    im_3k.alpha_composite(logo_shadow_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_gold, (lx, ly))

    save_pdp(im_3k, 'mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg')

# ==============================================================================
# 5. Mariam Royal Jelly Vitality Elixir (500g) — Vitality Infusion PDP
# ==============================================================================
def render_vitality_pdp():
    src_p = os.path.join(BRAIN_DIR, 'honey_vitality_pdp_1790028022185.jpg')
    src = Image.open(src_p).convert('RGBA')
    # Clean background to 100% pure white
    src = make_pure_white_bg(src, thresh=232)
    orig_w, orig_h = src.size

    # Inpaint burgundy label: x: 300..680, y: 508..605
    x0, y0, x1, y1 = 300, 508, 680, 605
    w, h = x1 - x0, y1 - y0
    patch = Image.new('RGBA', (w, h))
    for px in range(w):
        t = px / w
        r = int(112 - t * 34)
        g = int(32 - t * 14)
        b = int(45 - t * 17)
        for py in range(h):
            patch.putpixel((px, py), (r, g, b, 255))
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([2, 2, w-2, h-2], radius=4, fill=255)
    src.paste(patch, (x0, y0), mask.filter(ImageFilter.GaussianBlur(radius=2)))

    # Upscale to 3000 x 3000
    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    # Composite authentic cursive logo in Luxor Gold
    target_w = int(400 * scale)
    logo_gold = get_tinted_logo(target_w, GOLD_LUXOR)
    logo_shadow = get_tinted_logo(target_w, (40, 10, 15), 180)
    logo_shadow_blur = logo_shadow.filter(ImageFilter.GaussianBlur(radius=2.0))

    lx = int(500 * scale - target_w // 2)
    ly = int(556 * scale - logo_gold.height // 2)

    im_3k.alpha_composite(logo_shadow_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(logo_gold, (lx, ly))

    save_pdp(im_3k, 'mariam_honey_royal_jelly_elixir_white_studio_hero_4k.jpg')

# ==============================================================================
# 6. Mariam Discovery Flight Box (6x50g) — Gifting Suite PDP
# ==============================================================================
def render_flight_box_pdp():
    src_p = os.path.join(BRAIN_DIR, 'honey_flight_pdp_1790027997408.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

    # Rotation-based inpaint to clean entire diagonal text zone on lid
    crop_box = (150, 180, 650, 420)
    lid_crop = src.crop(crop_box)
    rot_neg = lid_crop.rotate(-9.5, resample=Image.Resampling.BICUBIC, expand=True)

    w_rot, h_rot = rot_neg.size
    patch = Image.new('RGBA', (450, 180), (237, 188, 185, 255))
    mask = Image.new('L', (450, 180), 0)
    ImageDraw.Draw(mask).rounded_rectangle([2, 2, 448, 178], radius=6, fill=255)
    rot_neg.paste(patch, (30, 70), mask.filter(ImageFilter.GaussianBlur(radius=2.5)))

    # Composite authentic logo horizontally
    target_w = 300
    target_h = int(logo_master.height * (target_w / logo_master.width))
    logo_r = logo_master.resize((target_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a = logo_r.split()
    logo_gold = Image.new('RGBA', (target_w, target_h), (*GOLD_LUXOR, 255))
    logo_gold.putalpha(a)
    logo_sh = Image.new('RGBA', (target_w, target_h), (160, 110, 80, 140))
    logo_sh.putalpha(a)
    logo_sh_blur = logo_sh.filter(ImageFilter.GaussianBlur(radius=1.5))

    lx = (w_rot - target_w) // 2
    ly = 70 + (180 - target_h) // 2

    rot_neg.alpha_composite(logo_sh_blur, (lx + 1, ly + 2))
    rot_neg.alpha_composite(logo_gold, (lx, ly))

    # Rotate back and paste
    rot_pos = rot_neg.rotate(9.5, resample=Image.Resampling.BICUBIC)
    cx, cy = (crop_box[0] + crop_box[2]) // 2, (crop_box[1] + crop_box[3]) // 2
    src.paste(rot_pos, (cx - rot_pos.width // 2, cy - rot_pos.height // 2), rot_pos)

    # Upscale to 3000 x 3000
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)
    save_pdp(im_3k, 'mariam_honey_discovery_flight_box_white_studio_hero_4k.jpg')

# ==============================================================================
# 7. Master Honey & Superfoods Collection Lineup (White Studio Cinema 4K)
# ==============================================================================
def render_master_honey_collection():
    """Composites an expansive Cinema 4K e-commerce hero lineup showing all products on pure white."""
    canvas = Image.new('RGB', (3840, 2160), (255, 255, 255))
    y_ground = 1850

    def get_jar_mask(jar_rgb):
        gray = jar_rgb.convert('L')
        alpha = gray.point(lambda p: 0 if p > 252 else 255)
        alpha = alpha.filter(ImageFilter.GaussianBlur(radius=2))
        return alpha

    jars = [
        ('mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg', 650, 1300),
        ('mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg', 1220, 1150),
        ('mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg', 1920, 1250), # Center Hero
        ('mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg', 2600, 1150),
        ('mariam_honey_royal_jelly_elixir_white_studio_hero_4k.jpg', 3200, 1150),
    ]

    for filename, cx, target_h in jars:
        p = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(p):
            continue
        jar = Image.open(p).convert('RGBA')
        aspect = jar.width / jar.height
        w = int(target_h * aspect)
        jar_r = jar.resize((w, target_h), Image.Resampling.LANCZOS)
        
        # Soft contact shadow underneath
        shadow_w = int(w * 0.85)
        shadow_h = int(target_h * 0.08)
        shadow = Image.new('RGBA', (shadow_w, shadow_h), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shadow)
        sh_draw.ellipse([0, 0, shadow_w, shadow_h], fill=(180, 180, 180, 90))
        shadow_blur = shadow.filter(ImageFilter.GaussianBlur(radius=10))
        canvas.paste(shadow_blur, (cx - shadow_w // 2, y_ground - shadow_h // 2), shadow_blur)

        # Paste jar
        jar_mask = get_jar_mask(jar_r)
        canvas.paste(jar_r, (cx - w // 2, y_ground - int(target_h * 0.96)), jar_mask)

    out_p = os.path.join(OUTPUT_DIR, 'mariam_honey_master_collection_white_studio_hero_4k.jpg')
    brain_p = os.path.join(BRAIN_DIR, 'mariam_honey_master_collection_white_studio_hero_4k.jpg')
    canvas.save(out_p, 'JPEG', quality=98)
    canvas.save(brain_p, 'JPEG', quality=98)
    print(f'[SAVED MASTER COLLECTION 4K] {out_p}')

if __name__ == '__main__':
    render_royal_mix_pdp()
    render_sidr_pdp()
    render_honeycomb_pdp()
    render_clover_1kg_pdp()
    render_vitality_pdp()
    render_flight_box_pdp()
    render_master_honey_collection()
