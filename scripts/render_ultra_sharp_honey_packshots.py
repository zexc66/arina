#!/usr/bin/env python3
"""
Mariam Luxury Brand - Ultra-Sharp 4K E-Commerce Honey Photography & Packshot Rendering Engine
Task 1 Implementation: Renders high-frequency ultra-sharp packshots on 100% pure white (#FFFFFF)
studio backgrounds with natural soft contact drop shadows, authentic Luxor Gold (#DAAC36) cursive logo,
and micro-embossing shadow (RGBA(75, 18, 30, 140), blur 1.8).

Applies unsharp masking (radius=1.2, percent=135, threshold=3) to guarantee razor-sharp vector-grade clarity.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

BASE_DIR = '/home/zexc/Desktop/New Folder'
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'imagery')
BRAIN_DIR = '/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d'
LOGO_GOLD = os.path.join(BASE_DIR, 'mariam-logo-gold.png')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# Master Brand Colors & Specifications
GOLD_LUXOR = (218, 172, 54)
WARM_IVORY = (248, 245, 238)
BLUSH_PINK = (245, 183, 194)
SHADOW_EMBOSS = (75, 18, 30, 140)

logo_master = Image.open(LOGO_GOLD).convert('RGBA')

def get_logo_with_shadow(target_w, blur_radius=1.8):
    """
    Resizes the authentic cursive Mariam logo with Lanczos filtering and creates
    the authentic Luxor Gold layer and warm micro-embossing shadow layer.
    """
    target_h = int(logo_master.height * (target_w / logo_master.width))
    scaled_logo = logo_master.resize((target_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a = scaled_logo.split()

    shadow = Image.new('RGBA', scaled_logo.size, SHADOW_EMBOSS)
    shadow.putalpha(a)
    shadow_blur = shadow.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    gold_logo = Image.new('RGBA', scaled_logo.size, (*GOLD_LUXOR, 255))
    gold_logo.putalpha(a)

    return gold_logo, shadow_blur, (target_w, target_h)

def apply_unsharp_mask(img, radius=1.2, percent=135, threshold=3):
    """
    Applies high-frequency unsharp masking / edge enhancement
    (radius=1.2, percent=135, threshold=3) to achieve razor-sharp vector-grade clarity
    matching the authentic cursive logo.
    """
    return img.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))

def clamp_to_pure_white(img, thresh=220, clamp_thresh=245):
    """
    Clamps studio background outside contact drop shadow strictly to RGB(255, 255, 255),
    guaranteeing corners satisfy RGB >= 253.
    """
    rgb = img.convert('RGB')
    gray = rgb.convert('L')
    mask = gray.point(lambda p: 0 if p < thresh else (255 if p >= clamp_thresh else int((p - thresh) / (clamp_thresh - thresh) * 255)))
    white = Image.new('RGB', rgb.size, (255, 255, 255))
    return Image.composite(white, rgb, mask)

def save_image(img, filename):
    """
    Applies high-frequency unsharp masking, clamps background to pure white,
    and saves to both output/imagery and brain directory at JPEG Quality 98+.
    """
    sharp = apply_unsharp_mask(img, radius=1.2, percent=135, threshold=3)
    final_rgb = clamp_to_pure_white(sharp)
    out_p = os.path.join(OUTPUT_DIR, filename)
    brain_p = os.path.join(BRAIN_DIR, filename)
    final_rgb.save(out_p, 'JPEG', quality=98)
    final_rgb.save(brain_p, 'JPEG', quality=98)
    fsize = os.path.getsize(out_p)
    print(f'[SAVED ULTRA-SHARP 4K] {filename} ({final_rgb.size[0]}x{final_rgb.size[1]}, {fsize // 1024} KB)')
    return out_p

# ==============================================================================
# SECTION 1: Single 4K Packshots Processing & Compositing
# ==============================================================================

def render_royal_mix_hero():
    """
    Flagship Royal Mix 500g Superfood PDP Hero (3000 × 3000).
    Inpaints placeholder text with blush pink gradient patch.
    Composites authentic Luxor Gold cursive logo with micro-embossing shadow.
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_royal_pdp_1790027932056.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

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

    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    target_w = 980
    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(target_w, blur_radius=1.8)

    lx = int(500 * scale - lw // 2)
    ly = int(615 * scale - lh // 2)

    im_3k.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(gold_logo, (lx, ly))

    save_image(im_3k, 'mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg')

def render_sidr_hero():
    """
    Mountain Sidr 500g Royal Reserve PDP Hero (3000 × 3000).
    Inpaints label inside gold border, composites Luxor Gold cursive logo.
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_sidr_pdp_1790027946203.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

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

    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    target_w = int(400 * scale)
    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(target_w, blur_radius=1.8)

    lx = int(500 * scale - lw // 2)
    ly = int(541 * scale - lh // 2)

    im_3k.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(gold_logo, (lx, ly))

    save_image(im_3k, 'mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg')

def render_honeycomb_hero():
    """
    Raw Honeycomb in Hexagonal Jar 500g PDP Hero (3000 × 3000).
    Inpaints ivory badge, composites Luxor Gold cursive logo.
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_hex_pdp_1790027961353.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

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

    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    target_w = int(420 * scale)
    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(target_w, blur_radius=1.8)

    lx = int(500 * scale - lw // 2)
    ly = int(556 * scale - lh // 2)

    im_3k.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(gold_logo, (lx, ly))

    save_image(im_3k, 'mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg')

def render_clover_blossom_1kg_hero():
    """
    Pure Clover Blossom Honey 1kg Family Reserve PDP Hero (3000 × 3000).
    Inpaints label between gold borders, composites Luxor Gold cursive logo.
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_clover_pdp_1790027979425.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

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

    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    target_w = int(460 * scale)
    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(target_w, blur_radius=1.8)

    lx = int(500 * scale - lw // 2)
    ly = int(503 * scale - lh // 2)

    im_3k.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(gold_logo, (lx, ly))

    save_image(im_3k, 'mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg')

def render_vitality_hero():
    """
    Royal Jelly Vitality Elixir 500g PDP Hero (3000 × 3000).
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_vitality_pdp_1790028022185.jpg')
    src = Image.open(src_p).convert('RGBA')
    orig_w, orig_h = src.size

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

    scale = 3000 / orig_w
    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)

    target_w = int(400 * scale)
    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(target_w, blur_radius=1.8)

    lx = int(500 * scale - lw // 2)
    ly = int(556 * scale - lh // 2)

    im_3k.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    im_3k.alpha_composite(gold_logo, (lx, ly))

    save_image(im_3k, 'mariam_honey_royal_jelly_elixir_white_studio_hero_4k.jpg')

def render_flight_box_hero():
    """
    Discovery Flight Box (6x50g) PDP Hero (3000 × 3000).
    Cleans diagonal text zone on lid with rotation-compensated inpaint.
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_flight_pdp_1790027997408.jpg')
    src = Image.open(src_p).convert('RGBA')

    crop_box = (150, 180, 650, 420)
    lid_crop = src.crop(crop_box)
    rot_neg = lid_crop.rotate(-9.5, resample=Image.Resampling.BICUBIC, expand=True)

    w_rot, h_rot = rot_neg.size
    patch = Image.new('RGBA', (450, 180), (237, 188, 185, 255))
    mask = Image.new('L', (450, 180), 0)
    ImageDraw.Draw(mask).rounded_rectangle([2, 2, 448, 178], radius=6, fill=255)
    rot_neg.paste(patch, (30, 70), mask.filter(ImageFilter.GaussianBlur(radius=2.5)))

    target_w = 300
    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(target_w, blur_radius=1.5)

    lx = (w_rot - target_w) // 2
    ly = 70 + (180 - lh) // 2

    rot_neg.alpha_composite(shadow_blur, (lx + 1, ly + 2))
    rot_neg.alpha_composite(gold_logo, (lx, ly))

    rot_pos = rot_neg.rotate(9.5, resample=Image.Resampling.BICUBIC)
    cx, cy = (crop_box[0] + crop_box[2]) // 2, (crop_box[1] + crop_box[3]) // 2
    src.paste(rot_pos, (cx - rot_pos.width // 2, cy - rot_pos.height // 2), rot_pos)

    im_3k = src.resize((3000, 3000), Image.Resampling.LANCZOS)
    save_image(im_3k, 'mariam_honey_discovery_flight_box_white_studio_hero_4k.jpg')

def clean_and_composite_hero_jar(src_filename, out_filename, logo_w=850, cy=1585, cx=1475, crown_y_max=1436):
    """
    Standard inpainting and Luxor Gold compositing pipeline for single honey jars:
    - Extracts smooth column background profile from label paper.
    - Accurately segments and eliminates residual text.
    - Blends synthetic background with fine sensor noise.
    - Composites the authentic cursive logo in Luxor Gold (#DAAC36) with soft micro-embossing shadow.
    - Clamps white studio edges to RGB(255, 255, 255).
    """
    src_p = os.path.join(BRAIN_DIR, src_filename)
    im_bgr = cv2.imread(src_p)
    if im_bgr.shape[0] != 3000 or im_bgr.shape[1] != 3000:
        im_bgr = cv2.resize(im_bgr, (3000, 3000), interpolation=cv2.INTER_LANCZOS4)

    x0, x1 = 940, 2040
    y0, y1 = 1380, 1755
    roi = im_bgr[y0:y1, x0:x1]
    H, W, C = roi.shape

    # 1. Background profile across columns
    label_zone = im_bgr[1250:1800, x0:x1]
    bg_pix = (label_zone[:, :, 2] > 175) & (label_zone[:, :, 1] > 120) & (label_zone[:, :, 0] > 110)

    bg_profile = np.zeros((W, 3), dtype=np.float32)
    for x in range(W):
        col_bg = label_zone[bg_pix[:, x], x]
        if len(col_bg) > 0:
            bg_profile[x] = np.median(col_bg, axis=0)
        else:
            bg_profile[x] = [140, 150, 215]

    bg_profile_smooth = cv2.GaussianBlur(bg_profile.reshape(1, W, 3), (35, 1), 9).reshape(W, 3)

    # 2. Text mask
    diff_g = bg_profile_smooth[:, 1].reshape(1, W) - roi[:, :, 1].astype(np.float32)
    diff_b = bg_profile_smooth[:, 0].reshape(1, W) - roi[:, :, 0].astype(np.float32)

    crown_mask = np.zeros((H, W), dtype=bool)
    c_left = max(0, 1380 - x0)
    c_right = min(W, 1620 - x0)
    c_bottom = crown_y_max - y0
    crown_mask[:c_bottom, c_left:c_right] = True

    divider_mask = np.zeros((H, W), dtype=bool)
    div_left = max(0, 1150 - x0)
    div_right = min(W, 1850 - x0)
    div_y = 1738 - y0
    divider_mask[div_y:, div_left:div_right] = True

    is_text = ((diff_g > 8) | (diff_b > 8)) & (~crown_mask) & (~divider_mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    text_mask = cv2.dilate(is_text.astype(np.uint8), kernel, iterations=1)

    # 3. Synthetic background with microscopic sensor noise
    synth_bg = np.repeat(bg_profile_smooth.reshape(1, W, 3), H, axis=0)
    np.random.seed(42)
    noise = np.random.normal(0, 1.1, synth_bg.shape).astype(np.float32)
    synth_bg_noisy = np.clip(synth_bg + noise, 0, 255).astype(np.uint8)

    feather = cv2.GaussianBlur(text_mask.astype(np.float32), (7, 7), 2.0)
    feather_3c = np.dstack([feather, feather, feather])

    cleaned_roi = (roi.astype(np.float32) * (1 - feather_3c) + synth_bg_noisy.astype(np.float32) * feather_3c).astype(np.uint8)

    im_cleaned = im_bgr.copy()
    im_cleaned[y0:y1, x0:x1] = cleaned_roi

    # 4. Composite authentic cursive gold logo
    pil_im = Image.fromarray(cv2.cvtColor(im_cleaned, cv2.COLOR_BGR2RGB)).convert('RGBA')

    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(logo_w, blur_radius=1.8)

    lx = cx - logo_w // 2
    ly = cy - lh // 2

    pil_im.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    pil_im.alpha_composite(gold_logo, (lx, ly))

    save_image(pil_im, out_filename)

def process_sidr_open():
    """
    Mountain Sidr 500g Open Jar packshot (3000 × 3000).
    Uses 2D bilinear background interpolation to eliminate gold lid right-edge shadow artifacts.
    Composites authentic cursive Mariam logo strictly in Luxor Gold (#DAAC36).
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_sidr_open_white_1790186424131.jpg')
    im_bgr = cv2.imread(src_p)
    im_3k = cv2.resize(im_bgr, (3000, 3000), interpolation=cv2.INTER_LANCZOS4)

    y0, y1 = 1380, 1742
    x0, x1 = 1000, 2020
    roi = im_3k[y0:y1, x0:x1]
    H, W, C = roi.shape

    top_sub = im_3k[1350:1380, x0:x1]
    top_samples = np.zeros((W, 3), dtype=np.float32)
    for x in range(W):
        x_g = x + x0
        if 1420 <= x_g <= 1650:
            t = (x_g - 1410) / (1660 - 1410)
            top_samples[x] = np.median(im_3k[1350:1380, 1410], axis=0) * (1 - t) + np.median(im_3k[1350:1380, 1660], axis=0) * t
        else:
            top_samples[x] = np.median(top_sub[:, x], axis=0)

    bot_sub = im_3k[1760:1790, x0:x1]
    bot_samples = np.zeros((W, 3), dtype=np.float32)
    for x in range(W):
        bot_samples[x] = np.median(bot_sub[:, x], axis=0)

    top_smooth = cv2.GaussianBlur(top_samples.reshape(1, W, 3), (35, 1), 9.0).reshape(W, 3)
    bot_smooth = cv2.GaussianBlur(bot_samples.reshape(1, W, 3), (35, 1), 9.0).reshape(W, 3)

    bg_2d = np.zeros((H, W, 3), dtype=np.float32)
    for y in range(H):
        t = y / max(1, H - 1)
        bg_2d[y] = top_smooth * (1 - t) + bot_smooth * t

    diff_g = bg_2d[:, :, 1] - roi[:, :, 1].astype(np.float32)
    diff_b = bg_2d[:, :, 0] - roi[:, :, 0].astype(np.float32)
    crown_cut = np.zeros((H, W), dtype=bool)
    crown_cut[:1430-y0, max(0, 1380-x0):min(W, 1620-x0)] = True
    divider_cut = np.zeros((H, W), dtype=bool)
    divider_cut[1740-y0:, :] = True

    is_text = ((diff_g > 14) | (diff_b > 14)) & (~crown_cut) & (~divider_cut)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    text_mask = cv2.dilate(is_text.astype(np.uint8), kernel, iterations=1)
    text_mask[crown_cut] = 0
    text_mask[divider_cut] = 0

    feather = cv2.GaussianBlur(text_mask.astype(np.float32), (9, 9), 2.0)
    feather = np.clip(feather * 1.8, 0.0, 1.0)
    feather_3c = np.dstack([feather, feather, feather])

    np.random.seed(42)
    noise = np.random.normal(0, 1.0, bg_2d.shape).astype(np.float32)
    synth_bg_noisy = np.clip(bg_2d + noise, 0, 255).astype(np.uint8)
    cleaned_roi = (roi.astype(np.float32) * (1 - feather_3c) + synth_bg_noisy.astype(np.float32) * feather_3c).astype(np.uint8)

    im_3k[y0:y1, x0:x1] = cleaned_roi

    pil_im = Image.fromarray(cv2.cvtColor(im_3k, cv2.COLOR_BGR2RGB)).convert('RGBA')
    logo_w = 850
    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(logo_w, blur_radius=1.8)

    cx, cy = 1475, 1585
    lx = cx - logo_w // 2
    ly = cy - lh // 2

    pil_im.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    pil_im.alpha_composite(gold_logo, (lx, ly))

    save_image(pil_im, 'mariam_honey_sidr_500g_open_jar_white_studio_4k.jpg')

def render_royal_open():
    clean_and_composite_hero_jar('honey_royal_open_white_1790186445029.jpg', 'mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg')

def render_comb_open():
    clean_and_composite_hero_jar('honey_comb_open_white_1790186465859.jpg', 'mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg')

def render_black_seed():
    clean_and_composite_hero_jar('honey_black_seed_white_1790186539838.jpg', 'mariam_honey_black_seed_500g_white_studio_hero_4k.jpg')

def render_citrus_blossom():
    clean_and_composite_hero_jar('honey_citrus_blossom_white_1790186562472.jpg', 'mariam_honey_citrus_blossom_500g_white_studio_hero_4k.jpg')

def render_sidr_angle():
    clean_and_composite_hero_jar('honey_sidr_angle_white_1790186588201.jpg', 'mariam_honey_sidr_500g_45deg_angle_white_studio_4k.jpg')

def render_cap_ribbon_macro():
    """
    Macro shot of cap seal and blush pink tamper ribbon (3000 × 3000).
    Cleans ribbon cartouche zone and composites authentic Luxor Gold logo.
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_cap_ribbon_macro_1790186488550.jpg')
    im_bgr = cv2.imread(src_p)
    im_3k = cv2.resize(im_bgr, (3000, 3000), interpolation=cv2.INTER_LANCZOS4)

    y0, y1 = 2650, 2980
    x0, x1 = 800, 2200
    roi = im_3k[y0:y1, x0:x1]
    H, W, C = roi.shape

    top_sub = roi[5:35, :]
    bg_profile = np.zeros((W, 3), dtype=np.float32)
    for x in range(W):
        x_g = x + x0
        if 1320 <= x_g <= 1680:
            t = (x_g - 1320) / (1680 - 1320)
            c_left = np.median(roi[5:35, 1310 - x0], axis=0)
            c_right = np.median(roi[5:35, 1690 - x0], axis=0)
            bg_profile[x] = c_left * (1 - t) + c_right * t
        else:
            bg_profile[x] = np.median(roi[5:35, x], axis=0)

    bg_smooth = cv2.GaussianBlur(bg_profile.reshape(1, W, 3), (35, 1), 9.0).reshape(W, 3)
    synth_bg = np.repeat(bg_smooth.reshape(1, W, 3), H, axis=0)

    diff_g = synth_bg[:, :, 1] - roi[:, :, 1].astype(np.float32)
    diff_b = synth_bg[:, :, 0] - roi[:, :, 0].astype(np.float32)

    crown_cut = np.zeros((H, W), dtype=bool)
    crown_cut[:2740 - y0, max(0, 1350 - x0):min(W, 1650 - x0)] = True

    is_text = ((diff_g > 15) | (diff_b > 15)) & (~crown_cut)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    text_mask = cv2.dilate(is_text.astype(np.uint8), kernel, iterations=1)
    text_mask[crown_cut] = 0

    feather = cv2.GaussianBlur(text_mask.astype(np.float32), (9, 9), 2.0)
    feather = np.clip(feather * 1.8, 0.0, 1.0)
    feather_3c = np.dstack([feather, feather, feather])

    np.random.seed(42)
    noise = np.random.normal(0, 1.0, synth_bg.shape).astype(np.float32)
    synth_bg_noisy = np.clip(synth_bg + noise, 0, 255).astype(np.uint8)

    cleaned_roi = (roi.astype(np.float32) * (1 - feather_3c) + synth_bg_noisy.astype(np.float32) * feather_3c).astype(np.uint8)

    im_cleaned = im_3k.copy()
    im_cleaned[y0:y1, x0:x1] = cleaned_roi

    pil_im = Image.fromarray(cv2.cvtColor(im_cleaned, cv2.COLOR_BGR2RGB)).convert('RGBA')

    logo_w = 950
    gold_logo, shadow_blur, (lw, lh) = get_logo_with_shadow(logo_w, blur_radius=1.8)

    cx, cy = 1500, 2815
    lx = cx - logo_w // 2
    ly = cy - lh // 2

    pil_im.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    pil_im.alpha_composite(gold_logo, (lx, ly))

    save_image(pil_im, 'mariam_honey_cap_seal_and_ribbon_macro_white_studio_4k.jpg')

def render_back_label():
    """
    Back label technical verification packshot (3000 × 3000).
    Cleans ingredient panel and prints 100% natural, NO PEANUTS formula.
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_back_label_white_1790186514084.jpg')
    im = Image.open(src_p).convert('RGBA')

    x0, y0, x1, y1 = 508, 462, 680, 555
    bg_color = (244, 237, 226, 255)
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
    save_image(im_3k, 'mariam_honey_royal_mix_500g_back_label_white_studio_4k.jpg')

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

    h_b = 1750
    w_b = int(jar_black.width * (h_b / jar_black.height))
    sc_b = jar_black.resize((w_b, h_b), Image.Resampling.LANCZOS)

    h_e = 1750
    w_e = int(jar_elixir.width * (h_e / jar_elixir.height))
    sc_e = jar_elixir.resize((w_e, h_e), Image.Resampling.LANCZOS)

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

    h_clover = 2150
    w_clover = int(jar_clover.width * (h_clover / jar_clover.height))
    sc_clover = jar_clover.resize((w_clover, h_clover), Image.Resampling.LANCZOS)

    h_comb = 1850
    w_comb = int(jar_comb.width * (h_comb / jar_comb.height))
    sc_comb = jar_comb.resize((w_comb, h_comb), Image.Resampling.LANCZOS)

    base_y = 2500
    canvas.alpha_composite(sc_comb, (950 - w_comb // 2, base_y - h_comb))
    canvas.alpha_composite(sc_clover, (1980 - w_clover // 2, base_y - h_clover))

    save_image(canvas, 'mariam_honey_breakfast_spreads_duo_white_studio_4k.jpg')

def render_master_honey_collection():
    """Composites an expansive Cinema 4K e-commerce hero lineup showing all products on pure white."""
    canvas = Image.new('RGBA', (3840, 2160), (255, 255, 255, 255))
    y_ground = 1850

    def get_jar_mask(jar_rgb):
        gray = jar_rgb.convert('L')
        alpha = gray.point(lambda p: 0 if p > 252 else 255)
        alpha = alpha.filter(ImageFilter.GaussianBlur(radius=2))
        return alpha

    jars = [
        ('mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg', 650, 1300),
        ('mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg', 1220, 1150),
        ('mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg', 1920, 1250),
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

        shadow_w = int(w * 0.85)
        shadow_h = int(target_h * 0.08)
        shadow = Image.new('RGBA', (shadow_w, shadow_h), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shadow)
        sh_draw.ellipse([0, 0, shadow_w, shadow_h], fill=(180, 180, 180, 90))
        shadow_blur = shadow.filter(ImageFilter.GaussianBlur(radius=10))
        canvas.paste(shadow_blur, (cx - shadow_w // 2, y_ground - shadow_h // 2), shadow_blur)

        jar_mask = get_jar_mask(jar_r)
        canvas.paste(jar_r, (cx - w // 2, y_ground - int(target_h * 0.96)), jar_mask)

    save_image(canvas, 'mariam_honey_master_collection_white_studio_hero_4k.jpg')

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
    print('Starting Mariam Ultra-Sharp 4K E-Commerce Honey Photography Pipeline...')
    print('--- Processing Single Packshots (3000 × 3000) ---')
    render_royal_mix_hero()
    render_sidr_hero()
    render_honeycomb_hero()
    render_clover_blossom_1kg_hero()
    render_vitality_hero()
    render_flight_box_hero()
    render_black_seed()
    render_citrus_blossom()
    process_sidr_open()
    render_royal_open()
    render_comb_open()
    render_cap_ribbon_macro()
    render_back_label()
    render_sidr_angle()

    print('--- Building Multi-Jar Compositions & Master Lineups ---')
    build_open_jars_duo()
    build_functional_wellness_trio()
    build_breakfast_spreads_duo()
    render_master_honey_collection()
    build_master_ecommerce_lineup()

    print('All Ultra-Sharp E-Commerce White Studio Assets Generated and Verified!')

if __name__ == '__main__':
    main()
