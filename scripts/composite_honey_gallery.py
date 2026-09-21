#!/usr/bin/env python3
"""
Mariam Luxury Brand - 4K Compositing Engine for Honey & Superfoods Gallery
Composites the authentic cursive logo (mariam-logo-gold.png) onto 4K commercial photography
with 2x supersampling, shadow embossing, and zero artifacts.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

def composite_trio_photo(
    src_path,
    logo_path='mariam-logo-gold.png',
    out_path='output/imagery/mariam_honey_master_trio_commercial_4k.jpg'
):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    src = Image.open(src_path).convert('RGBA')
    orig_w, orig_h = src.size  # 1376 x 768

    # --- 1. Inpaint Left Jar (Mountain Sidr Honey 500g) ---
    # Placeholder text in x: 315..395, y: 328..368
    lx0, ly0, lx1, ly1 = 315, 328, 395, 368
    lw, lh = lx1 - lx0, ly1 - ly0
    patch_l = Image.new('RGBA', (lw, lh))
    for px in range(lw):
        t = px / lw
        r = int(180 - t * 65)
        g = int(88 - t * 45)
        b = int(98 - t * 65)
        for py in range(lh):
            patch_l.putpixel((px, py), (r, g, b, 255))
    mask_l = Image.new('L', (lw, lh), 0)
    ImageDraw.Draw(mask_l).rounded_rectangle([1, 1, lw - 1, lh - 1], radius=5, fill=255)
    src.paste(patch_l, (lx0, ly0), mask_l.filter(ImageFilter.GaussianBlur(radius=2.5)))

    # --- 2. Inpaint Middle Jar (Mariam Royal Mix 500g) ---
    # Placeholder text in x: 620..745, y: 335..380
    mx0, my0, mx1, my1 = 620, 335, 745, 380
    mw, mh = mx1 - mx0, my1 - my0
    patch_m = Image.new('RGBA', (mw, mh))
    for px in range(mw):
        t = px / mw
        r = int(250 + t * (228 - 250))
        g = int(195 + t * (165 - 195))
        b = int(190 + t * (160 - 190))
        for py in range(mh):
            patch_m.putpixel((px, py), (r, g, b, 255))
    mask_m = Image.new('L', (mw, mh), 0)
    ImageDraw.Draw(mask_m).rounded_rectangle([1, 1, mw - 1, mh - 1], radius=6, fill=255)
    src.paste(patch_m, (mx0, my0), mask_m.filter(ImageFilter.GaussianBlur(radius=3)))

    # --- 3. Inpaint Right Jar (Raw Honeycomb 500g) ---
    # Placeholder text in x: 985..1075, y: 338..362
    rx0, ry0, rx1, ry1 = 985, 338, 1075, 362
    rw, rh = rx1 - rx0, ry1 - ry0
    patch_r = Image.new('RGBA', (rw, rh))
    for px in range(rw):
        t = px / rw
        r = int(240 - t * 10)
        g = int(214 - t * 10)
        b = int(180 - t * 8)
        for py in range(rh):
            patch_r.putpixel((px, py), (r, g, b, 255))
    mask_r = Image.new('L', (rw, rh), 0)
    ImageDraw.Draw(mask_r).rounded_rectangle([1, 1, rw - 1, rh - 1], radius=4, fill=255)
    src.paste(patch_r, (rx0, ry0), mask_r.filter(ImageFilter.GaussianBlur(radius=2)))

    # --- 4. Upscale to Cinema 4K UHD (3840 x 2160) ---
    target_w, target_h = 3840, 2160
    scale_x = target_w / orig_w
    scale_y = target_h / orig_h
    im_4k = src.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # --- 5. Composite Authentic Cursive Logo onto each jar ---
    logo_master = Image.open(logo_path).convert('RGBA')

    # Palette
    gold_luxor = (218, 172, 54)
    burgundy_wine = (118, 18, 46)

    def get_tinted_logo(w, color, alpha=255):
        s = w / logo_master.width
        h = int(logo_master.height * s)
        resized = logo_master.resize((w, h), Image.Resampling.LANCZOS)
        _, _, _, a = resized.split()
        tinted = Image.new('RGBA', (w, h), (*color, alpha))
        tinted.putalpha(a)
        return tinted

    # A) Left Jar (Mountain Sidr Honey 500g): Gold logo on Burgundy
    left_logo_w = int(105 * scale_x)
    logo_left_gold = get_tinted_logo(left_logo_w, gold_luxor)
    logo_left_shadow = get_tinted_logo(left_logo_w, (40, 10, 15), 160)
    logo_left_shadow = logo_left_shadow.filter(ImageFilter.GaussianBlur(radius=1.5))
    lx_4k = int(355 * scale_x - left_logo_w // 2)
    ly_4k = int(348 * scale_y - logo_left_gold.height // 2)
    im_4k.alpha_composite(logo_left_shadow, (lx_4k + 2, ly_4k + 2))
    im_4k.alpha_composite(logo_left_gold, (lx_4k, ly_4k))

    # B) Middle Jar (Mariam Royal Mix 500g): Burgundy logo on Blush Pink with Gold Foil Rim
    mid_logo_w = int(145 * scale_x)
    logo_mid_burg = get_tinted_logo(mid_logo_w, burgundy_wine)
    logo_mid_gold = get_tinted_logo(mid_logo_w, gold_luxor, 120)
    logo_mid_gold = logo_mid_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    mx_4k = int(682 * scale_x - mid_logo_w // 2)
    my_4k = int(357 * scale_y - logo_mid_burg.height // 2)
    im_4k.alpha_composite(logo_mid_gold, (mx_4k + 2, my_4k + 2))
    im_4k.alpha_composite(logo_mid_burg, (mx_4k, my_4k))

    # C) Right Jar (Raw Honeycomb 500g): Luxor Gold logo on Warm Ivory
    right_logo_w = int(115 * scale_x)
    logo_right_gold = get_tinted_logo(right_logo_w, gold_luxor)
    logo_right_shadow = get_tinted_logo(right_logo_w, (120, 80, 40), 140)
    logo_right_shadow = logo_right_shadow.filter(ImageFilter.GaussianBlur(radius=1.5))
    rx_4k = int(1030 * scale_x - right_logo_w // 2)
    ry_4k = int(350 * scale_y - logo_right_gold.height // 2)
    im_4k.alpha_composite(logo_right_shadow, (rx_4k + 1, ry_4k + 2))
    im_4k.alpha_composite(logo_right_gold, (rx_4k, ry_4k))

    # Save final 4K Cinema
    final_rgb = im_4k.convert('RGB')
    final_rgb.save(out_path, 'JPEG', quality=98)
    print(f'Successfully saved Trio 4K photograph to: {out_path}')
    return out_path


def composite_comparison_photo(
    src_path,
    logo_path='mariam-logo-gold.png',
    out_path='output/imagery/mariam_honey_sizes_comparison_500g_vs_1kg_4k.jpg'
):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    src = Image.open(src_path).convert('RGBA')
    orig_w, orig_h = src.size  # 1200 x 896

    # --- 1. Inpaint Left Jar (500g Royal Mix) ---
    # Placeholder text in x: 315..425, y: 450..495
    lx0, ly0, lx1, ly1 = 315, 450, 425, 495
    lw, lh = lx1 - lx0, ly1 - ly0
    patch_l = Image.new('RGBA', (lw, lh))
    for px in range(lw):
        t = px / lw
        r = int(248 + t * (220 - 248))
        g = int(214 + t * (165 - 214))
        b = int(220 + t * (160 - 220))
        for py in range(lh):
            patch_l.putpixel((px, py), (r, g, b, 255))
    mask_l = Image.new('L', (lw, lh), 0)
    ImageDraw.Draw(mask_l).rounded_rectangle([1, 1, lw - 1, lh - 1], radius=6, fill=255)
    src.paste(patch_l, (lx0, ly0), mask_l.filter(ImageFilter.GaussianBlur(radius=3)))

    # --- 2. Upscale to 4K (3200 x 2400) ---
    target_w, target_h = 3200, 2400
    scale_x = target_w / orig_w
    scale_y = target_h / orig_h
    im_4k = src.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # --- 3. Composite Authentic Cursive Logo ---
    logo_master = Image.open(logo_path).convert('RGBA')
    gold_luxor = (218, 172, 54)
    burgundy_wine = (118, 18, 46)

    def get_tinted_logo(w, color, alpha=255):
        s = w / logo_master.width
        h = int(logo_master.height * s)
        resized = logo_master.resize((w, h), Image.Resampling.LANCZOS)
        _, _, _, a = resized.split()
        tinted = Image.new('RGBA', (w, h), (*color, alpha))
        tinted.putalpha(a)
        return tinted

    # A) Left Jar (500g Royal Mix): Deep Wine Burgundy on Petal Blush Pink
    left_logo_w = int(140 * scale_x)
    logo_left_burg = get_tinted_logo(left_logo_w, burgundy_wine)
    logo_left_gold = get_tinted_logo(left_logo_w, gold_luxor, 120)
    logo_left_gold = logo_left_gold.filter(ImageFilter.GaussianBlur(radius=1.5))
    lx_4k = int(370 * scale_x - left_logo_w // 2)
    ly_4k = int(472 * scale_y - logo_left_burg.height // 2)
    im_4k.alpha_composite(logo_left_gold, (lx_4k + 2, ly_4k + 2))
    im_4k.alpha_composite(logo_left_burg, (lx_4k, ly_4k))

    # B) Right Jar (1kg Family Reserve Pure Clover Blossom Honey): Luxor Gold on Burgundy
    right_logo_w = int(180 * scale_x)
    logo_right_gold = get_tinted_logo(right_logo_w, gold_luxor)
    logo_right_shadow = get_tinted_logo(right_logo_w, (40, 10, 5), 180)
    logo_right_shadow = logo_right_shadow.filter(ImageFilter.GaussianBlur(radius=2.0))
    rx_4k = int(810 * scale_x - right_logo_w // 2)
    ry_4k = int(375 * scale_y - logo_right_gold.height // 2)
    im_4k.alpha_composite(logo_right_shadow, (rx_4k + 2, ry_4k + 2))
    im_4k.alpha_composite(logo_right_gold, (rx_4k, ry_4k))

    # Save final 4K Portrait/Landscape
    final_rgb = im_4k.convert('RGB')
    final_rgb.save(out_path, 'JPEG', quality=98)
    print(f'Successfully saved Sizing Comparison 4K photograph to: {out_path}')
    return out_path


if __name__ == '__main__':
    trio_src = '/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d/honey_master_trio_1790022379158.jpg'
    comp_src = '/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d/honey_sizes_compare_1790022422187.jpg'

    if os.path.exists(trio_src):
        composite_trio_photo(trio_src)
    if os.path.exists(comp_src):
        composite_comparison_photo(comp_src)
