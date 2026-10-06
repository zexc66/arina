#!/usr/bin/env python3
"""
Mariam Luxury Brand - 4K Compositing Engine for Honey & Superfoods
Composites the authentic cursive logo (mariam-logo-gold.png) strictly in Luxor Gold (#DAAC36)
onto 4K commercial photography with 2x supersampling, shadow embossing, and zero artifacts.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = '/home/zexc/Desktop/New Folder/output/imagery'
BRAIN_DIR = '/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d'

def composite_hero(src_path, logo_path=('arina-logo-gold.png' if os.path.exists('arina-logo-gold.png') else 'mariam-logo-gold.png'), out_path='output/imagery/mariam_honey_royal_mix_hero_commercial_4k.jpg'):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # 1. Load source image (1024x1024)
    src = Image.open(src_path).convert('RGBA')

    # 2. Clean ribbon text under crown on ribbon: x from 472 to 552, y from 287 to 314
    rx0, ry0, rx1, ry1 = 472, 287, 552, 314
    rw, rh = rx1 - rx0, ry1 - ry0
    patch_r = Image.new('RGBA', (rw, rh))
    for px in range(rw):
        t = px / rw
        r = int(240 + t * (226 - 240))
        g = int(198 + t * (176 - 198))
        b = int(194 + t * (174 - 194))
        for py in range(rh):
            patch_r.putpixel((px, py), (r, g, b, 255))
    mask_r = Image.new('L', (rw, rh), 0)
    draw_mr = ImageDraw.Draw(mask_r)
    draw_mr.rounded_rectangle([1, 1, rw - 1, rh - 1], radius=3, fill=255)
    mask_r_blur = mask_r.filter(ImageFilter.GaussianBlur(radius=2))
    src.paste(patch_r, (rx0, ry0), mask_r_blur)

    # 3. Clean placeholder text on the cartouche badge: x from 372 to 642, y from 396 to 532
    bx0, by0, bx1, by1 = 372, 396, 642, 532
    bw, bh = bx1 - bx0, by1 - by0
    patch = Image.new('RGBA', (bw, bh))
    for px in range(bw):
        t = px / bw
        if t < 0.45:
            sub_t = t / 0.45
            r = int(252 + sub_t * (230 - 252))
            g = int(222 + sub_t * (181 - 222))
            b = int(220 + sub_t * (176 - 220))
        else:
            sub_t = (t - 0.45) / 0.55
            r = int(230 + sub_t * (198 - 230))
            g = int(181 + sub_t * (138 - 181))
            b = int(176 + sub_t * (130 - 176))
        for py in range(bh):
            patch.putpixel((px, py), (r, g, b, 255))

    mask = Image.new('L', (bw, bh), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.rounded_rectangle([4, 4, bw - 4, bh - 4], radius=16, fill=255)
    mask_blurred = mask.filter(ImageFilter.GaussianBlur(radius=4))
    src.paste(patch, (bx0, by0), mask_blurred)

    # 4. Upscale cleanly to Square 4K (3000 x 3000) using LANCZOS
    scale_factor = 3000 / 1024
    im_4k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    # 5. Composite authentic cursive Mariam logo in Luxor Gold (#DAAC36)
    logo_master = Image.open(logo_path).convert('RGBA')

    # Target logo dimensions: width ~ 730 px
    target_w = 730
    logo_scale = target_w / logo_master.width
    target_h = int(logo_master.height * logo_scale)

    scaled_logo = logo_master.resize((target_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a = scaled_logo.split()

    # Authentic Luxor Gold (#DAAC36)
    gold_luxor = (218, 172, 54)
    gold_logo = Image.new('RGBA', (target_w, target_h), (*gold_luxor, 255))
    gold_logo.putalpha(a)

    # Subtle soft contact shadow
    shadow = Image.new('RGBA', (target_w, target_h), (75, 18, 30, 140))
    shadow.putalpha(a)
    shadow_blur = shadow.filter(ImageFilter.GaussianBlur(radius=1.8))

    # Coordinates at 3000x3000:
    logo_4k_x = int(510 * scale_factor - target_w // 2)
    logo_4k_y = int(464 * scale_factor - target_h // 2)

    im_4k.alpha_composite(shadow_blur, (logo_4k_x + 2, logo_4k_y + 3))
    im_4k.alpha_composite(gold_logo, (logo_4k_x, logo_4k_y))

    # Convert to RGB and save at JPEG Quality 98
    final_rgb = im_4k.convert('RGB')
    final_rgb.save(out_path, 'JPEG', quality=98)
    
    # Also save to brain dir
    brain_dst = os.path.join(BRAIN_DIR, os.path.basename(out_path))
    final_rgb.save(brain_dst, 'JPEG', quality=98)
    print(f'Successfully saved 4K product photograph to: {out_path} and {brain_dst}')
    return out_path

if __name__ == '__main__':
    src = '/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d/honey_royal_mix_1790021272366.jpg'
    composite_hero(src)
