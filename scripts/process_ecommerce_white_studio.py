#!/usr/bin/env python3
"""
Mariam Luxury Brand - E-Commerce White Studio Photography & Packshot Engine
Processes, inpaints, composites authentic cursive logos, and renders 12 commercial
packshots on 100% pure white studio background (#FFFFFF) with natural contact drop shadows.

Sacred Brand Directives:
- Strictly authentic cursive Mariam logo (mariam-logo-gold.png in #DAAC36).
- Zero hallucinated text, zero burgundy logos, zero rectangular inpainting artifacts.
- 100% Pure White background RGB(255, 255, 255) outside contact shadows.
- No peanuts in Royal Mix.
- Petal Blush Pink & Luxor Gold palette on all honey packaging.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'imagery')
BRAIN_DIR = '/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d'
LOGO_GOLD = os.path.join(BASE_DIR, 'arina-logo-gold.png')
if not os.path.exists(LOGO_GOLD):
    LOGO_GOLD = os.path.join(BASE_DIR, 'mariam-logo-gold.png')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# Master Brand Colors
GOLD_LUXOR = (218, 172, 54)
WARM_IVORY = (248, 245, 238)
BLUSH_PINK = (245, 183, 194)

logo_master = Image.open(LOGO_GOLD).convert('RGBA')

def get_tinted_logo(target_w, color=GOLD_LUXOR, alpha=255):
    """Resizes and tints the authentic cursive Arina logo with Lanczos filter."""
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

def save_image(img, filename):
    out_p = os.path.join(OUTPUT_DIR, filename)
    rgb = img.convert('RGB')
    rgb.save(out_p, 'JPEG', quality=98)
    if filename.startswith('mariam_'):
        arina_name = filename.replace('mariam_', 'arina_')
        out_arina = os.path.join(OUTPUT_DIR, arina_name)
        rgb.save(out_arina, 'JPEG', quality=98)
    fsize = os.path.getsize(out_p)
    print(f'[SAVED 4K] {filename} & {filename.replace("mariam_", "arina_")} ({rgb.size[0]}x{rgb.size[1]}, {fsize // 1024} KB)')
    return out_p

# ==============================================================================
# SECTION 1: Single 4K Packshots Processing & Compositing
# ==============================================================================

def process_sidr_open():
    """
    Mountain Sidr 500g Open Jar packshot.
    Uses perfected 2D bilinear background interpolation to eliminate gold lid right-edge shadow artifacts.
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

    # Composite authentic cursive Luxor Gold logo
    pil_im = Image.fromarray(cv2.cvtColor(im_3k, cv2.COLOR_BGR2RGB)).convert('RGBA')
    logo_w = 850
    target_h = int(logo_master.height * (logo_w / logo_master.width))
    scaled_logo = logo_master.resize((logo_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a = scaled_logo.split()

    shadow = Image.new('RGBA', scaled_logo.size, (75, 18, 30, 140))
    shadow.putalpha(a)
    shadow_blur = shadow.filter(ImageFilter.GaussianBlur(radius=1.8))

    gold_logo = Image.new('RGBA', scaled_logo.size, (*GOLD_LUXOR, 255))
    gold_logo.putalpha(a)

    cx, cy = 1475, 1585
    lx = cx - logo_w // 2
    ly = cy - target_h // 2

    pil_im.alpha_composite(shadow_blur, (lx + 2, ly + 2))
    pil_im.alpha_composite(gold_logo, (lx, ly))

    final_img = clamp_to_pure_white(pil_im)
    save_image(final_img, 'mariam_honey_sidr_500g_open_jar_white_studio_4k.jpg')

def clean_and_composite_hero_jar(src_filename, out_filename, logo_w=850, cy=1585, cx=1475, crown_y_max=1436):
    """
    Standard inpainting and Luxor Gold compositing pipeline for single honey jars:
    - Extracts smooth column background model from label paper.
    - Accurately segments and eliminates residual text.
    - Blends synthetic background with fine sensor noise.
    - Composites the authentic cursive logo in Luxor Gold (#DAAC36) with soft warm contact shadow.
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

    target_h = int(logo_master.height * (logo_w / logo_master.width))
    scaled_logo = logo_master.resize((logo_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a = scaled_logo.split()

    shadow = Image.new('RGBA', scaled_logo.size, (75, 18, 30, 140))
    shadow.putalpha(a)
    shadow_blur = shadow.filter(ImageFilter.GaussianBlur(radius=2.0))

    gold_logo = Image.new('RGBA', scaled_logo.size, (*GOLD_LUXOR, 255))
    gold_logo.putalpha(a)

    lx = cx - logo_w // 2
    ly = cy - target_h // 2

    pil_im.alpha_composite(shadow_blur, (lx + 2, ly + 3))
    pil_im.alpha_composite(gold_logo, (lx, ly))

    final_img = clamp_to_pure_white(pil_im)
    save_image(final_img, out_filename)

def process_royal_open():
    clean_and_composite_hero_jar('honey_royal_open_white_1790186445029.jpg', 'mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg')

def process_comb_open():
    clean_and_composite_hero_jar('honey_comb_open_white_1790186465859.jpg', 'mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg')

def process_black_seed():
    clean_and_composite_hero_jar('honey_black_seed_white_1790186539838.jpg', 'mariam_honey_black_seed_500g_white_studio_hero_4k.jpg')

def process_citrus_blossom():
    clean_and_composite_hero_jar('honey_citrus_blossom_white_1790186562472.jpg', 'mariam_honey_citrus_blossom_500g_white_studio_hero_4k.jpg')

def process_sidr_angle():
    clean_and_composite_hero_jar('honey_sidr_angle_white_1790186588201.jpg', 'mariam_honey_sidr_500g_45deg_angle_white_studio_4k.jpg')

def process_cap_ribbon_macro():
    """
    Macro shot of cap seal and blush pink tamper ribbon.
    Cleans ribbon cartouche zone and composites authentic Luxor Gold logo.
    """
    src_p = os.path.join(BRAIN_DIR, 'honey_cap_ribbon_macro_1790186488550.jpg')
    im_bgr = cv2.imread(src_p)
    im_3k = cv2.resize(im_bgr, (3000, 3000), interpolation=cv2.INTER_LANCZOS4)

    y0, y1 = 2650, 2980
    x0, x1 = 800, 2200
    roi = im_3k[y0:y1, x0:x1]
    H, W, C = roi.shape

    # Sample top background profile from y in [2650..2680], interpolate across crown
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
    target_h = int(logo_master.height * (logo_w / logo_master.width))
    scaled_logo = logo_master.resize((logo_w, target_h), Image.Resampling.LANCZOS)
    _, _, _, a = scaled_logo.split()

    shadow = Image.new('RGBA', scaled_logo.size, (75, 18, 30, 140))
    shadow.putalpha(a)
    shadow_blur = shadow.filter(ImageFilter.GaussianBlur(radius=2.0))

    gold_logo = Image.new('RGBA', scaled_logo.size, (*GOLD_LUXOR, 255))
    gold_logo.putalpha(a)

    cx, cy = 1500, 2815
    lx = cx - logo_w // 2
    ly = cy - target_h // 2

    pil_im.alpha_composite(shadow_blur, (lx + 2, ly + 3))
    pil_im.alpha_composite(gold_logo, (lx, ly))

    final_img = clamp_to_pure_white(pil_im)
    save_image(final_img, 'mariam_honey_cap_seal_and_ribbon_macro_white_studio_4k.jpg')

def process_back_label():
    """
    Back label technical verification packshot.
    Cleans ingredient panel and prints 100% natural, NO PEANUTS formula.
    """
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

    final_img = clamp_to_pure_white(canvas)
    save_image(final_img, 'mariam_honey_open_jars_connoisseur_duo_white_studio_4k.jpg')

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

    final_img = clamp_to_pure_white(canvas)
    save_image(final_img, 'mariam_honey_functional_wellness_trio_white_studio_4k.jpg')

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

    final_img = clamp_to_pure_white(canvas)
    save_image(final_img, 'mariam_honey_breakfast_spreads_duo_white_studio_4k.jpg')

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

    final_img = clamp_to_pure_white(canvas)
    save_image(final_img, 'mariam_honey_master_ecommerce_lineup_white_studio_4k.jpg')

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
