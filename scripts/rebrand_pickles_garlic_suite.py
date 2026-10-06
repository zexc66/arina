#!/usr/bin/env python3
"""
Arina Luxury Brand - Automated 4K Pickles & Garlic Imagery Rebranding Engine
Applies precision cylinder-surface reconstruction and 2x supersampled compositing
of the authentic Arina gold logo (arina-logo-gold.png) across all pickles and garlic packshots.
"""

import os
import shutil
import cv2
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "imagery")
BACKUP_DIR = os.path.join(BASE_DIR, "output", "imagery_backup_mariam")
LOGO_PATH = os.path.join(BASE_DIR, "arina-logo-gold.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

logo_master = Image.open(LOGO_PATH).convert("RGBA")


def process_cylinder_patch(crop, top_y_range, bot_y_range, mask_fade_top, mask_fade_bot, logo_scale_w, logo_y_offset):
    """
    Reconstructs the curved matte paper cylinder gradient between top and bottom clean lines
    and composites the authentic Arina logo with 2x supersampling.
    """
    H, W, C = crop.shape

    top_curve = np.mean(crop[top_y_range[0]:top_y_range[1], :], axis=0)
    bot_curve = np.mean(crop[bot_y_range[0]:bot_y_range[1], :], axis=0)

    top_smooth = cv2.GaussianBlur(top_curve.reshape(1, W, 3), (55, 1), 20).reshape(W, 3)
    bot_smooth = cv2.GaussianBlur(bot_curve.reshape(1, W, 3), (55, 1), 20).reshape(W, 3)

    surf = np.zeros((H, W, 3), dtype=np.float32)
    for y in range(H):
        t = y / (H - 1)
        surf[y] = top_smooth * (1 - t) + bot_smooth * t

    # Subtle fine paper fiber grain
    noise = np.random.normal(0, 1.2, (H, W, 3)).astype(np.float32)
    surf = np.clip(surf + noise, 0, 255).astype(np.uint8)

    # Vertical transition mask
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

    # Horizontal edge fade (preserves side margins / curved paper lighting)
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

    # 2x supersampled compositing
    target_w = logo_scale_w
    target_h = int(logo_master.height * target_w / logo_master.width)
    logo_2x = logo_master.resize((target_w * 2, target_h * 2), Image.Resampling.LANCZOS)

    clean_pil = Image.fromarray(cv2.cvtColor(clean_zone, cv2.COLOR_BGR2RGB)).convert("RGBA")
    clean_2x = clean_pil.resize((W * 2, H * 2), Image.Resampling.LANCZOS)

    pos_x_2x = (W * 2 - target_w * 2) // 2
    pos_y_2x = logo_y_offset * 2
    clean_2x.paste(logo_2x, (pos_x_2x, pos_y_2x), mask=logo_2x)

    res_pil = clean_2x.resize((W, H), Image.Resampling.LANCZOS)
    return res_pil


def backup_if_needed(filename):
    src = os.path.join(OUTPUT_DIR, filename)
    dst = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f"[BACKED UP] {filename}")


def rebrand_standard_hero(filename):
    """Processes 3000x3000 standard studio jars."""
    backup_if_needed(filename)
    src_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(src_path):
        print(f"[SKIP MISSING] {filename}")
        return

    orig = Image.open(src_path).convert("RGBA")
    im = cv2.imread(src_path)

    x0, x1 = 950, 2050
    y0, y1 = 1200, 1750
    crop = im[y0:y1, x0:x1]

    patch = process_cylinder_patch(
        crop=crop,
        top_y_range=(8, 22),
        bot_y_range=(495, 508),
        mask_fade_top=(15, 35),
        mask_fade_bot=(475, 495),
        logo_scale_w=780,
        logo_y_offset=135,
    )

    orig.paste(patch, (x0, y0))

    out_orig = os.path.join(OUTPUT_DIR, filename)
    out_arina = os.path.join(OUTPUT_DIR, filename.replace("mariam_", "arina_"))

    rgb = orig.convert("RGB")
    rgb.save(out_orig, "JPEG", quality=98)
    rgb.save(out_arina, "JPEG", quality=98)
    print(f"[REBRANDED 4K HERO] {filename} -> {out_arina}")


def rebrand_solo_shot(filename):
    """Processes 2400x3200 vertical solo studio shots."""
    backup_if_needed(filename)
    src_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(src_path):
        print(f"[SKIP MISSING] {filename}")
        return

    orig = Image.open(src_path).convert("RGBA")
    im = cv2.imread(src_path)

    x0, x1 = 720, 1680
    y0, y1 = 1200, 1750
    crop = im[y0:y1, x0:x1]

    patch = process_cylinder_patch(
        crop=crop,
        top_y_range=(8, 22),
        bot_y_range=(495, 508),
        mask_fade_top=(15, 35),
        mask_fade_bot=(475, 495),
        logo_scale_w=750,
        logo_y_offset=135,
    )

    orig.paste(patch, (x0, y0))

    out_orig = os.path.join(OUTPUT_DIR, filename)
    out_arina = os.path.join(OUTPUT_DIR, filename.replace("mariam_", "arina_"))
    rgb = orig.convert("RGB")
    rgb.save(out_orig, "JPEG", quality=98)
    rgb.save(out_arina, "JPEG", quality=98)
    print(f"[REBRANDED 4K SOLO] {filename} -> {out_arina}")


def main():
    print("=" * 70)
    print("REBRANDING PICKLES & GARLIC SUITE TO ARINA LUXURY BRAND")
    print("=" * 70)

    standard_heroes = [
        "mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg",
        "mariam_crisp_baby_cucumbers_petite_210g_white_studio_hero_4k.jpg",
        "mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg",
        "mariam_wild_turnip_beetroot_petite_210g_white_studio_hero_4k.jpg",
        "mariam_royal_mixed_pickles_white_studio_hero_4k.jpg",
        "mariam_royal_mixed_pickles_petite_210g_white_studio_hero_4k.jpg",
        "mariam_whipped_toum_white_studio_hero_4k.jpg",
        "mariam_whipped_toum_petite_100g_white_studio_hero_4k.jpg",
        "mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg",
        "mariam_crushed_garlic_unroasted_petite_100g_white_studio_hero_4k.jpg",
        "mariam_slow_roasted_garlic_white_studio_hero_4k.jpg",
        "mariam_slow_roasted_garlic_petite_100g_white_studio_hero_4k.jpg",
    ]

    for f in standard_heroes:
        rebrand_standard_hero(f)

    solo_shots = [
        "mariam_crisp_baby_cucumbers_solo_4k.jpg",
        "mariam_petite_wild_turnip_beetroot_solo_4k.jpg",
        "mariam_wild_turnip_beetroot_pickles_solo_4k.jpg",
        "mariam_royal_mixed_pickles_solo_4k.jpg",
        "mariam_petite_royal_mixed_pickles_solo_4k.jpg",
        "mariam_whipped_toum_garlic_paste_solo_4k.jpg",
        "mariam_slow_roasted_garlic_paste_solo_4k.jpg",
    ]

    for f in solo_shots:
        rebrand_solo_shot(f)

    print("=" * 70)
    print("PICKLES & GARLIC SUITE REBRANDING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
