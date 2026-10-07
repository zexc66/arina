#!/usr/bin/env python3
"""
Arina Luxury Brand - Pickles Packshots Dual-Size Calibration Engine
Reconstructs distinct, authentic geometry and typography for Turnips and Cucumbers:
1. Standard 720ml (700g) Glass Jar with TO 82mm lid (calibrated to '700g e' in authentic gold foil)
2. Petite 370ml (360g) Glass Jar with TO 63mm lid (extracted from authentic 3D trio render,
   rebranded to Arina Gold Crest, calibrated to '360g e', and scaled proportionally on 3000x3000 pure white studio canvas)
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "imagery")
CREST_PATH = os.path.join(BASE_DIR, "arina-crest-gold.png")
FONT_PATH = os.path.join(BASE_DIR, "fonts", "PlayfairDisplay.ttf")

crest_master = Image.open(CREST_PATH).convert("RGBA")


def clean_strip_extremes(strip):
    is_white = np.mean(strip, axis=1) > 180
    valid_indices = np.where(~is_white)[0]
    if len(valid_indices) > 0:
        first_valid, last_valid = valid_indices[0], valid_indices[-1]
        strip[:first_valid] = strip[first_valid]
        strip[last_valid + 1:] = strip[last_valid]
    return strip


def clean_cylinder_patch(crop, top_slice, bot_slice, fade_y, fade_x, logo_h, y_offset=0, use_crest=True):
    H, W, C = crop.shape

    top_strip = np.median(crop[top_slice[0]:top_slice[1], :], axis=0)
    bot_strip = np.median(crop[bot_slice[0]:bot_slice[1], :], axis=0)

    top_strip = clean_strip_extremes(top_strip)
    bot_strip = clean_strip_extremes(bot_strip)

    top_smooth = cv2.GaussianBlur(top_strip.reshape(1, W, 3), (25, 1), 6).reshape(W, 3)
    bot_smooth = cv2.GaussianBlur(bot_strip.reshape(1, W, 3), (25, 1), 6).reshape(W, 3)

    surf = np.zeros((H, W, 3), dtype=np.float32)
    for y in range(H):
        t = y / float(H - 1)
        surf[y] = top_smooth * (1 - t) + bot_smooth * t

    np.random.seed(42)
    noise = np.random.normal(0, 1.2, (H, W, 1)).astype(np.float32)
    surf_grained = np.clip(surf + noise, 0, 255).astype(np.uint8)

    mask_y = np.ones(H, dtype=np.float32)
    for y in range(fade_y):
        mask_y[y] = 0.5 - 0.5 * np.cos(np.pi * y / fade_y)
        mask_y[H - 1 - y] = 0.5 - 0.5 * np.cos(np.pi * y / fade_y)

    mask_x = np.ones(W, dtype=np.float32)
    for x in range(fade_x):
        mask_x[x] = 0.5 - 0.5 * np.cos(np.pi * x / fade_x)
        mask_x[W - 1 - x] = 0.5 - 0.5 * np.cos(np.pi * x / fade_x)

    mask_2d = mask_y[:, None] * mask_x[None, :]
    clean_zone = crop.astype(np.float32) * (1 - mask_2d[:, :, None]) + surf_grained.astype(np.float32) * mask_2d[:, :, None]
    clean_zone = np.clip(clean_zone, 0, 255).astype(np.uint8)

    w_scaled = int(crest_master.width * logo_h / crest_master.height)
    logo_scaled = crest_master.resize((w_scaled, logo_h), Image.Resampling.LANCZOS)

    clean_pil = Image.fromarray(cv2.cvtColor(clean_zone, cv2.COLOR_BGR2RGB)).convert("RGBA")
    pos_x = (W - w_scaled) // 2
    pos_y = (H - logo_h) // 2 + y_offset
    clean_pil.paste(logo_scaled, (pos_x, pos_y), mask=logo_scaled)

    return clean_pil


def update_large_jar_weight_to_700g(jar_filename):
    """Calibrate large 720ml jar weight typography from '500g e' to '700g e'."""
    jar_path = os.path.join(OUTPUT_DIR, jar_filename)
    img = cv2.imread(jar_path)
    if img is None:
        print(f"[FAIL] Could not load {jar_path}")
        return

    kal_path = os.path.join(OUTPUT_DIR, "arina_royal_kalamata_olives_white_studio_hero_4k.jpg")
    kal_img = cv2.imread(kal_path)
    kal_wt = kal_img[2160:2240, 1380:1620]

    large_wt = img[2160:2240, 1380:1620].copy()
    H_wt, W_wt, _ = large_wt.shape

    # Clean digit 5 at x=10..60
    top_s = np.median(large_wt[1:6, 10:60], axis=0)
    bot_s = np.median(large_wt[H_wt-6:H_wt-1, 10:60], axis=0)
    surf5 = np.zeros((H_wt, 50, 3), dtype=np.float32)
    for y in range(H_wt):
        t = y / float(H_wt - 1)
        surf5[y] = top_s * (1 - t) + bot_s * t
    noise = np.random.normal(0, 1.0, (H_wt, 50, 1)).astype(np.float32)
    surf5 = np.clip(surf5 + noise, 0, 255).astype(np.uint8)

    fade = 5
    for y in range(H_wt):
        for x in range(50):
            ax = 1.0
            if x < fade:
                ax = x / float(fade)
            elif x > 50 - fade:
                ax = (50 - x) / float(fade)
            large_wt[y, 10 + x] = large_wt[y, 10 + x] * (1 - ax) + surf5[y, x] * ax

    # Digit 7 from kalamata (x=55..86)
    d7_crop = kal_wt[:, 55:86].copy()
    d7_w = d7_crop.shape[1]
    d7_mask = (d7_crop[:, :, 2] > 60) & (d7_crop[:, :, 1] > 50)
    d7_mask_f = cv2.GaussianBlur(d7_mask.astype(np.float32), (3, 3), 0.7)

    target = large_wt[:, 21:21+d7_w]
    blended = target * (1 - d7_mask_f[:, :, None]) + d7_crop * d7_mask_f[:, :, None]
    large_wt[:, 21:21+d7_w] = blended.astype(np.uint8)

    img[2160:2240, 1380:1620] = large_wt
    cv2.imwrite(jar_path, img, [cv2.IMWRITE_JPEG_QUALITY, 98])
    print(f"[OK] Calibrated 720ml jar weight to 700g e: {jar_filename}")


def generate_petite_jar_packshot(trio_crop_x, tight_x_range, tight_y_range, target_height_ratio, out_filename):
    """
    Extract, rebrand, and composite authentic 370ml petite jar on 3000x3000px white studio canvas.
    """
    trio_path = os.path.join(OUTPUT_DIR, "mariam_petite_pickles_trio_white_studio_4k.jpg")
    trio = cv2.imread(trio_path)
    if trio is None:
        print(f"[FAIL] Could not load {trio_path}")
        return

    crop = trio[:, trio_crop_x[0]:trio_crop_x[1]].copy()

    # 1. Cursive rebrand to Arina Gold Crest
    x0, x1 = 130, 825
    y0, y1 = 890, 1215
    patch_target = crop[y0:y1, x0:x1].copy()

    patch = clean_cylinder_patch(
        crop=patch_target,
        top_slice=(2, 10),
        bot_slice=(patch_target.shape[0] - 10, patch_target.shape[0] - 2),
        fade_y=12,
        fade_x=22,
        logo_h=190,
        y_offset=-10,
        use_crest=True
    )
    patch_bgr = cv2.cvtColor(np.array(patch.convert("RGB")), cv2.COLOR_RGB2BGR)
    crop[y0:y1, x0:x1] = patch_bgr

    # 2. Weight patch to 360g e
    wy0, wy1 = 1430, 1485
    wx0, wx1 = 380, 570
    wt_crop = crop[wy0:wy1, wx0:wx1].copy()
    h, w, _ = wt_crop.shape

    top_s = np.median(wt_crop[1:4, :], axis=0)
    bot_s = np.median(wt_crop[h-4:h-1, :], axis=0)
    surf = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        t = y / float(h - 1)
        surf[y] = top_s * (1 - t) + bot_s * t

    np.random.seed(42)
    noise = np.random.normal(0, 1.0, (h, w, 1)).astype(np.float32)
    surf = np.clip(surf + noise, 0, 255).astype(np.uint8)

    fade = 5
    mask_y = np.ones(h, dtype=np.float32)
    for y in range(fade):
        mask_y[y] = 0.5 - 0.5 * np.cos(np.pi * y / fade)
        mask_y[h - 1 - y] = 0.5 - 0.5 * np.cos(np.pi * y / fade)
    mask_x = np.ones(w, dtype=np.float32)
    for x in range(fade*2):
        mask_x[x] = 0.5 - 0.5 * np.cos(np.pi * x / (fade*2))
        mask_x[w - 1 - x] = 0.5 - 0.5 * np.cos(np.pi * x / (fade*2))
    m2d = mask_y[:, None] * mask_x[None, :]

    clean_wt = wt_crop.astype(np.float32) * (1 - m2d[:, :, None]) + surf.astype(np.float32) * m2d[:, :, None]
    clean_wt = np.clip(clean_wt, 0, 255).astype(np.uint8)

    pil_wt = Image.fromarray(cv2.cvtColor(clean_wt, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_wt)
    font = ImageFont.truetype(FONT_PATH, 20)
    text = "360g e"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = (h - th) // 2 - 1

    draw.text((tx, ty+1), text, font=font, fill=(10, 20, 15))
    draw.text((tx, ty), text, font=font, fill=(195, 178, 128))

    crop[wy0:wy1, wx0:wx1] = cv2.cvtColor(np.array(pil_wt), cv2.COLOR_RGB2BGR)

    # 3. Tight crop and pure white studio isolation
    tight = crop[tight_y_range[0]:tight_y_range[1], tight_x_range[0]:tight_x_range[1]].copy()
    th_h, th_w, _ = tight.shape

    white_mask = np.all(tight >= 248, axis=2)
    tight[white_mask] = [255, 255, 255]

    # Proportional scaling
    target_h = int(th_h * target_height_ratio)
    target_w = int(th_w * (target_h / float(th_h)))

    resized_petite = cv2.resize(tight, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

    # 4. Canvas assembly
    canvas = np.full((3000, 3000, 3), 255, dtype=np.uint8)
    pos_y = 2820 - int(target_h * 0.96)
    pos_x = (3000 - target_w) // 2

    canvas[pos_y:pos_y+target_h, pos_x:pos_x+target_w] = resized_petite
    canvas[:pos_y, :] = [255, 255, 255]
    canvas[pos_y+target_h:, :] = [255, 255, 255]
    canvas[:, :pos_x] = [255, 255, 255]
    canvas[:, pos_x+target_w:] = [255, 255, 255]

    out_path = os.path.join(OUTPUT_DIR, out_filename)
    cv2.imwrite(out_path, canvas, [cv2.IMWRITE_JPEG_QUALITY, 98])
    print(f"[OK] Generated authentic 370ml petite jar packshot: {out_filename}")


def main():
    print("=" * 70)
    print("EXECUTING ARINA PICKLES DUAL-SIZE CALIBRATION ENGINE")
    print("=" * 70)

    # 1. Turnips 720ml (700g e)
    update_large_jar_weight_to_700g("arina_wild_turnip_beetroot_white_studio_hero_4k.jpg")

    # 2. Turnips Petite 370ml (360g e)
    generate_petite_jar_packshot(
        trio_crop_x=(2460, 3420),
        tight_x_range=(50, 910),
        tight_y_range=(380, 1920),
        target_height_ratio=(1990.0 / 1446.0),
        out_filename="arina_wild_turnip_beetroot_petite_210g_white_studio_hero_4k.jpg"
    )

    # 3. Cucumbers 720ml (700g e)
    update_large_jar_weight_to_700g("arina_crisp_baby_cucumbers_white_studio_hero_4k.jpg")

    # 4. Cucumbers Petite 370ml (360g e)
    generate_petite_jar_packshot(
        trio_crop_x=(450, 1400),
        tight_x_range=(20, 900),
        tight_y_range=(480, 1820),
        target_height_ratio=(1990.0 / 1248.0),
        out_filename="arina_crisp_baby_cucumbers_petite_210g_white_studio_hero_4k.jpg"
    )

    print("=" * 70)
    print("ALL PICKLE PACKSHOTS CALIBRATED WITH DISTINCT GEOMETRY & WEIGHTS!")
    print("=" * 70)


if __name__ == "__main__":
    main()
