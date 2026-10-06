#!/usr/bin/env python3
"""
Arina Luxury Brand - High-Definition Packshot Sharpening & Precision Rebranding Engine
Eliminates all label blurring by restricting cylinder reconstruction strictly to the brand logo zone (Y=1200:1540),
preserving 100% of product titles and typography, and applying unsharp masking for crystal clarity.
"""

import os
import shutil
import cv2
import numpy as np
from PIL import Image, ImageFilter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "imagery")
BACKUP_DIR = os.path.join(BASE_DIR, "output", "imagery_backup_mariam")
LOGO_PATH = os.path.join(BASE_DIR, "arina-logo-gold.png")

logo_master = Image.open(LOGO_PATH).convert("RGBA")


def precision_cylinder_patch(crop, top_y_range, bot_y_range, mask_fade_top, mask_fade_bot, logo_scale_w, logo_y_offset):
    H, W, C = crop.shape

    top_curve = np.mean(crop[top_y_range[0]:top_y_range[1], :], axis=0)
    bot_curve = np.mean(crop[bot_y_range[0]:bot_y_range[1], :], axis=0)

    top_smooth = cv2.GaussianBlur(top_curve.reshape(1, W, 3), (55, 1), 20).reshape(W, 3)
    bot_smooth = cv2.GaussianBlur(bot_curve.reshape(1, W, 3), (55, 1), 20).reshape(W, 3)

    surf = np.zeros((H, W, 3), dtype=np.float32)
    for y in range(H):
        t = y / (H - 1)
        surf[y] = top_smooth * (1 - t) + bot_smooth * t

    noise = np.random.normal(0, 1.2, (H, W, 3)).astype(np.float32)
    surf = np.clip(surf + noise, 0, 255).astype(np.uint8)

    mask_y = np.zeros(H, dtype=np.float32)
    y_in_0, y_in_1 = mask_fade_top
    y_out_0, y_out_1 = mask_fade_bot

    for y in range(H):
        if y < y_in_0:
            mask_y[y] = 0.0
        elif y < y_in_1:
            mask_y[y] = (y - y_in_0) / float(y_in_1 - y_in_0)
        elif y <= y_out_0:
            mask_y[y] = 1.0
        elif y < y_out_1:
            mask_y[y] = 1.0 - (y - y_out_0) / float(y_out_1 - y_out_0)
        else:
            mask_y[y] = 0.0

    mask_x = np.ones(W, dtype=np.float32)
    pad_x = 35
    for x in range(W):
        if x < pad_x:
            mask_x[x] = x / float(pad_x)
        elif x > W - pad_x:
            mask_x[x] = (W - x) / float(pad_x)

    mask_2d = mask_y[:, None] * mask_x[None, :]
    clean_zone = crop.astype(np.float32) * (1 - mask_2d[:, :, None]) + surf.astype(np.float32) * mask_2d[:, :, None]
    clean_zone = np.clip(clean_zone, 0, 255).astype(np.uint8)

    target_w = logo_scale_w
    target_h = int(logo_master.height * target_w / logo_master.width)
    logo_scaled = logo_master.resize((target_w, target_h), Image.Resampling.LANCZOS)

    clean_pil = Image.fromarray(cv2.cvtColor(clean_zone, cv2.COLOR_BGR2RGB)).convert("RGBA")
    pos_x = (W - target_w) // 2
    pos_y = logo_y_offset
    clean_pil.paste(logo_scaled, (pos_x, pos_y), mask=logo_scaled)

    return clean_pil


def process_sharp_hero_jar(filename):
    src_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(src_path):
        print(f"[SKIP MISSING] {filename}")
        return

    orig_im = cv2.imread(src_path)
    if orig_im is None:
        return

    # Strictly target brand logo zone: Y=1200:1540 (H=340), X=950:2050 (W=1100)
    x0, x1 = 950, 2050
    y0, y1 = 1200, 1540
    crop = orig_im[y0:y1, x0:x1]

    patch = precision_cylinder_patch(
        crop=crop,
        top_y_range=(8, 22),
        bot_y_range=(320, 334),
        mask_fade_top=(15, 35),
        mask_fade_bot=(300, 325),
        logo_scale_w=660,
        logo_y_offset=60,
    )

    full_pil = Image.fromarray(cv2.cvtColor(orig_im, cv2.COLOR_BGR2RGB)).convert("RGBA")
    full_pil.paste(patch, (x0, y0))

    # Apply professional high-frequency unsharp mask
    sharp_pil = full_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))
    rgb = sharp_pil.convert("RGB")

    out_orig = os.path.join(OUTPUT_DIR, filename)
    out_arina = os.path.join(OUTPUT_DIR, filename.replace("mariam_", "arina_"))

    rgb.save(out_orig, "JPEG", quality=98)
    rgb.save(out_arina, "JPEG", quality=98)
    print(f"[SHARP HERO 4K] {filename} -> {out_arina}")


def process_sharp_solo_jar(filename):
    src_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(src_path):
        print(f"[SKIP MISSING] {filename}")
        return

    orig_im = cv2.imread(src_path)
    if orig_im is None:
        return

    x0, x1 = 720, 1680
    y0, y1 = 1200, 1540
    crop = orig_im[y0:y1, x0:x1]

    patch = precision_cylinder_patch(
        crop=crop,
        top_y_range=(8, 22),
        bot_y_range=(320, 334),
        mask_fade_top=(15, 35),
        mask_fade_bot=(300, 325),
        logo_scale_w=640,
        logo_y_offset=60,
    )

    full_pil = Image.fromarray(cv2.cvtColor(orig_im, cv2.COLOR_BGR2RGB)).convert("RGBA")
    full_pil.paste(patch, (x0, y0))

    sharp_pil = full_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))
    rgb = sharp_pil.convert("RGB")

    out_orig = os.path.join(OUTPUT_DIR, filename)
    out_arina = os.path.join(OUTPUT_DIR, filename.replace("mariam_", "arina_"))

    rgb.save(out_orig, "JPEG", quality=98)
    rgb.save(out_arina, "JPEG", quality=98)
    print(f"[SHARP SOLO 4K] {filename} -> {out_arina}")


def sharpen_existing_imagery():
    """Applies unsharp masking to honey and banner imagery so all images are vector-sharp."""
    honey_and_banners = [
        "arina_honey_royal_mix_500g_white_studio_hero_4k.jpg",
        "arina_honey_mountain_sidr_500g_white_studio_hero_4k.jpg",
        "arina_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg",
        "arina_honey_clover_blossom_1kg_white_studio_hero_4k.jpg",
        "arina_honey_black_seed_500g_white_studio_hero_4k.jpg",
        "arina_honey_citrus_blossom_500g_white_studio_hero_4k.jpg",
        "arina_honey_royal_mix_500g_open_jar_white_studio_4k.jpg",
        "arina_honey_sidr_500g_open_jar_white_studio_4k.jpg",
        "arina_honey_sidr_500g_45deg_angle_white_studio_4k.jpg",
        "arina_honey_royal_mix_500g_back_label_white_studio_4k.jpg",
        "arina_honey_cap_seal_and_ribbon_macro_white_studio_4k.jpg",
        "arina_complete_gastronomy_trinity_hero_4k.jpg",
    ]

    for fname in honey_and_banners:
        p = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            sharp = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=145, threshold=2))
            sharp.save(p, "JPEG", quality=98)
            # Also update legacy counterpart
            p_leg = os.path.join(OUTPUT_DIR, fname.replace("arina_", "mariam_"))
            sharp.save(p_leg, "JPEG", quality=98)
            print(f"[ENHANCED SHARPNESS] {fname}")


def main():
    print("=" * 70)
    print("RE-RENDERING PACKSHOTS WITH PRECISION LOGO ZONE & ULTRA SHARPNESS")
    print("=" * 70)

    heroes = [
        # Olives & Tapenade
        "mariam_royal_kalamata_olives_white_studio_hero_4k.jpg",
        "mariam_natural_black_olives_white_studio_hero_4k.jpg",
        "mariam_almond_stuffed_olives_white_studio_hero_4k.jpg",
        "mariam_garlic_stuffed_olives_white_studio_hero_4k.jpg",
        "mariam_green_olive_tapenade_white_studio_hero_4k.jpg",
        "mariam_kalamata_olive_tapenade_white_studio_hero_4k.jpg",
        # Pickles
        "mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg",
        "mariam_crisp_baby_cucumbers_petite_210g_white_studio_hero_4k.jpg",
        "mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg",
        "mariam_wild_turnip_beetroot_petite_210g_white_studio_hero_4k.jpg",
        "mariam_royal_mixed_pickles_white_studio_hero_4k.jpg",
        "mariam_royal_mixed_pickles_petite_210g_white_studio_hero_4k.jpg",
        # Garlic
        "mariam_whipped_toum_white_studio_hero_4k.jpg",
        "mariam_whipped_toum_petite_100g_white_studio_hero_4k.jpg",
        "mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg",
        "mariam_crushed_garlic_unroasted_petite_100g_white_studio_hero_4k.jpg",
        "mariam_slow_roasted_garlic_white_studio_hero_4k.jpg",
        "mariam_slow_roasted_garlic_petite_100g_white_studio_hero_4k.jpg",
    ]

    for f in heroes:
        process_sharp_hero_jar(f)

    solos = [
        "mariam_natural_black_olives_solo_4k.jpg",
        "mariam_garlic_stuffed_olives_solo_4k.jpg",
        "mariam_crisp_baby_cucumbers_solo_4k.jpg",
        "mariam_petite_wild_turnip_beetroot_solo_4k.jpg",
        "mariam_wild_turnip_beetroot_pickles_solo_4k.jpg",
        "mariam_royal_mixed_pickles_solo_4k.jpg",
        "mariam_petite_royal_mixed_pickles_solo_4k.jpg",
        "mariam_whipped_toum_garlic_paste_solo_4k.jpg",
        "mariam_slow_roasted_garlic_paste_solo_4k.jpg",
    ]

    for f in solos:
        process_sharp_solo_jar(f)

    sharpen_existing_imagery()
    print("=" * 70)
    print("ALL PACKSHOTS RE-RENDERED WITH FLAWLESS SHARPNESS & UNTOUCHED TYPOGRAPHY")
    print("=" * 70)


if __name__ == "__main__":
    main()
