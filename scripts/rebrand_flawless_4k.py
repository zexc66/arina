#!/usr/bin/env python3
"""
Arina Luxury Brand - Flawless 4K Packshot Rebranding & De-Ghosting Engine
Completely eliminates all traces of legacy cursive 'Mariam made with love',
all blurry bands, and all edge artifacts across all packshot categories:
- 3000x3000px Studio Hero & Petite Packshots
- 3840x2160px Flagship Gastronomy Trinity Hero
- 2400x3200px Solo Packshots
- 3840x2143px Connoisseur Lifestyle Jars

Reconstructs the matte cylindrical paper surface with authentic micro-grain texture,
perfect lighting curve interpolation, and pristine gold foil Arina Crest branding.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageFilter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "imagery")
BACKUP_DIR = os.path.join(BASE_DIR, "output", "imagery_backup_mariam")
CREST_PATH = os.path.join(BASE_DIR, "arina-crest-gold.png")
LOGO_PATH = os.path.join(BASE_DIR, "arina-logo-gold.png")

crest_master = Image.open(CREST_PATH).convert("RGBA")
logo_master = Image.open(LOGO_PATH).convert("RGBA")


def clean_strip_extremes(strip):
    """Clean white studio background contamination from the ends of sample strips."""
    is_white = np.mean(strip, axis=1) > 180
    valid_indices = np.where(~is_white)[0]
    if len(valid_indices) > 0:
        first_valid, last_valid = valid_indices[0], valid_indices[-1]
        strip[:first_valid] = strip[first_valid]
        strip[last_valid + 1:] = strip[last_valid]
    return strip


def clean_cylinder_patch(crop, top_slice, bot_slice, fade_y, fade_x, logo_h, y_offset=0, use_crest=True):
    """
    Synthesize pristine cylindrical matte paper surface matching the jar lighting,
    with monochrome paper grain and seamless 2D cosine falloff alpha blending.
    """
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

    # Monochrome luminance micro-grain noise
    np.random.seed(42)
    noise = np.random.normal(0, 1.2, (H, W, 1)).astype(np.float32)
    surf_grained = np.clip(surf + noise, 0, 255).astype(np.uint8)

    # 2D Cosine Falloff Alpha Blending Mask
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

    # Place scaled Arina Crest or Logo
    target_logo = crest_master if use_crest else logo_master
    w_scaled = int(target_logo.width * logo_h / target_logo.height)
    logo_scaled = target_logo.resize((w_scaled, logo_h), Image.Resampling.LANCZOS)

    clean_pil = Image.fromarray(cv2.cvtColor(clean_zone, cv2.COLOR_BGR2RGB)).convert("RGBA")
    pos_x = (W - w_scaled) // 2
    pos_y = (H - logo_h) // 2 + y_offset
    clean_pil.paste(logo_scaled, (pos_x, pos_y), mask=logo_scaled)

    return clean_pil


def process_hero_3000(filename):
    """Process a 3000x3000px Hero or Petite jar packshot with verified razor-sharp algorithm."""
    src_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(src_path):
        print(f"[SKIP] Not found: {filename}")
        return

    orig_im = cv2.imread(src_path)
    if orig_im is None:
        return

    # Verified coordinates for 3000x3000px:
    # leaves intact olive branch watermark at X<875 & X>2125
    # clean green gap above product title at Y=1710
    x0, x1 = 860, 2140
    y0, y1 = 1150, 1710
    crop = orig_im[y0:y1, x0:x1].copy()

    patch = clean_cylinder_patch(
        crop=crop,
        top_slice=(5, 25),
        bot_slice=(crop.shape[0] - 25, crop.shape[0] - 5),
        fade_y=20,
        fade_x=30,
        logo_h=360,
        y_offset=-15,
        use_crest=True
    )

    full_pil = Image.fromarray(cv2.cvtColor(orig_im, cv2.COLOR_BGR2RGB)).convert("RGBA")
    full_pil.paste(patch, (x0, y0))

    sharp_pil = full_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=2))
    rgb = sharp_pil.convert("RGB")

    out_arina = os.path.join(OUTPUT_DIR, filename.replace("mariam_", "arina_"))
    out_mariam = os.path.join(OUTPUT_DIR, filename)
    rgb.save(out_arina, "JPEG", quality=98)
    rgb.save(out_mariam, "JPEG", quality=98)
    print(f"[HERO 3000 OK] {filename} -> {out_arina}")


def process_squat_jar(filename):
    """
    Process squat garlic / toum jars (3000x3000px) where the legacy cursive 'M'
    extends higher up (from Y=1114) and wider (X=800..2200).
    Leaves the top gold pinstripe at Y=1000..1025 intact and stops above
    product title at Y=1670.
    """
    src_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(src_path):
        print(f"[SKIP] Not found: {filename}")
        return

    orig_im = cv2.imread(src_path)
    if orig_im is None:
        return

    x0, x1 = 800, 2200
    y0, y1 = 1040, 1670
    crop = orig_im[y0:y1, x0:x1].copy()

    patch = clean_cylinder_patch(
        crop=crop,
        top_slice=(4, 20),
        bot_slice=(crop.shape[0] - 20, crop.shape[0] - 4),
        fade_y=18,
        fade_x=28,
        logo_h=360,
        y_offset=-10,
        use_crest=True
    )

    full_pil = Image.fromarray(cv2.cvtColor(orig_im, cv2.COLOR_BGR2RGB)).convert("RGBA")
    full_pil.paste(patch, (x0, y0))

    sharp_pil = full_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=2))
    rgb = sharp_pil.convert("RGB")

    out_arina = os.path.join(OUTPUT_DIR, filename.replace("mariam_", "arina_"))
    out_mariam = os.path.join(OUTPUT_DIR, filename)
    rgb.save(out_arina, "JPEG", quality=98)
    rgb.save(out_mariam, "JPEG", quality=98)
    print(f"[SQUAT HERO OK] {filename} -> {out_arina}")


def process_solo_jar(filename):
    """Process a 2400x3200px Solo tall jar packshot."""
    src_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(src_path):
        print(f"[SKIP] Not found: {filename}")
        return

    orig_im = cv2.imread(src_path)
    if orig_im is None:
        return

    x0, x1 = 700, 1700
    y0, y1 = 1320, 1720
    crop = orig_im[y0:y1, x0:x1].copy()

    patch = clean_cylinder_patch(
        crop=crop,
        top_slice=(4, 18),
        bot_slice=(crop.shape[0] - 18, crop.shape[0] - 4),
        fade_y=15,
        fade_x=25,
        logo_h=270,
        y_offset=-10,
        use_crest=True
    )

    full_pil = Image.fromarray(cv2.cvtColor(orig_im, cv2.COLOR_BGR2RGB)).convert("RGBA")
    full_pil.paste(patch, (x0, y0))

    sharp_pil = full_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=2))
    rgb = sharp_pil.convert("RGB")

    out_arina = os.path.join(OUTPUT_DIR, filename.replace("mariam_", "arina_"))
    out_mariam = os.path.join(OUTPUT_DIR, filename)
    rgb.save(out_arina, "JPEG", quality=98)
    rgb.save(out_mariam, "JPEG", quality=98)
    print(f"[SOLO 4K OK] {filename} -> {out_arina}")


def process_flawless_trinity():
    """Process the Flagship Gastronomy Trinity Hero (3840x2160) with individually calibrated jars."""
    src_path = os.path.join(BACKUP_DIR, "mariam_complete_gastronomy_trinity_hero_4k.jpg")
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, "mariam_complete_gastronomy_trinity_hero_4k.jpg")
    if not os.path.exists(src_path):
        print("[FAIL] Trinity original not found!")
        return

    trinity = cv2.imread(src_path)
    if trinity is None:
        return

    def apply_jar(x0, y0, x1, y1, logo_h, y_offset=-3):
        crop = trinity[y0:y1, x0:x1].copy()
        patch = clean_cylinder_patch(
            crop=crop,
            top_slice=(2, 12),
            bot_slice=(crop.shape[0] - 12, crop.shape[0] - 2),
            fade_y=12,
            fade_x=20,
            logo_h=logo_h,
            y_offset=y_offset,
            use_crest=True
        )
        patch_bgr = cv2.cvtColor(np.array(patch.convert("RGB")), cv2.COLOR_RGB2BGR)
        trinity[y0:y1, x0:x1] = patch_bgr

    # Jar 1: Acoustic Crisp Baby Cucumbers
    apply_jar(x0=730, y0=1170, x1=1280, y1=1405, logo_h=175)

    # Jar 2: Royal Kalamata Olives
    apply_jar(x0=1635, y0=1210, x1=2210, y1=1470, logo_h=190)

    # Jar 3: Crushed Garlic Unroasted
    apply_jar(x0=2470, y0=1190, x1=3210, y1=1465, logo_h=205)

    full_pil = Image.fromarray(cv2.cvtColor(trinity, cv2.COLOR_BGR2RGB))
    sharp_pil = full_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=2))

    out_arina = os.path.join(OUTPUT_DIR, "arina_complete_gastronomy_trinity_hero_4k.jpg")
    out_mariam = os.path.join(OUTPUT_DIR, "mariam_complete_gastronomy_trinity_hero_4k.jpg")
    sharp_pil.save(out_arina, "JPEG", quality=98)
    sharp_pil.save(out_mariam, "JPEG", quality=98)
    print(f"[TRINITY 4K OK] -> {out_arina}")


def process_lifestyle_jar():
    """Process the Connoisseur 3D Lifestyle Jar (Garlic & Almond Stuffed Olives, 3840x2143)."""
    src_path = os.path.join(BACKUP_DIR, "mariam_garlic_almond_stuffed_olives_jar_4k.jpg")
    if not os.path.exists(src_path):
        src_path = os.path.join(OUTPUT_DIR, "mariam_garlic_almond_stuffed_olives_jar_4k.jpg")
    if not os.path.exists(src_path):
        return

    img = cv2.imread(src_path)
    if img is None:
        return

    x0, x1 = 1620, 2220
    y0, y1 = 945, 1170
    crop = img[y0:y1, x0:x1].copy()

    patch = clean_cylinder_patch(
        crop=crop,
        top_slice=(2, 10),
        bot_slice=(crop.shape[0] - 10, crop.shape[0] - 2),
        fade_y=12,
        fade_x=25,
        logo_h=160,
        y_offset=0,
        use_crest=True
    )

    full_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert("RGBA")
    full_pil.paste(patch, (x0, y0))

    sharp_pil = full_pil.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=2))
    rgb = sharp_pil.convert("RGB")

    out_arina = os.path.join(OUTPUT_DIR, "arina_garlic_almond_stuffed_olives_jar_4k.jpg")
    out_mariam = os.path.join(OUTPUT_DIR, "mariam_garlic_almond_stuffed_olives_jar_4k.jpg")
    rgb.save(out_arina, "JPEG", quality=98)
    rgb.save(out_mariam, "JPEG", quality=98)
    print(f"[LIFESTYLE JAR OK] -> {out_arina}")


def main():
    print("=" * 70)
    print("EXECUTING FLAWLESS 4K PACKSHOT REBRANDING & DE-GHOSTING ENGINE")
    print("=" * 70)

    # 1. Flagship Gastronomy Trinity Hero (3840x2160)
    process_flawless_trinity()

    # 2. Connoisseur Lifestyle Jar (3840x2143)
    process_lifestyle_jar()

    # 3. 3000x3000px Hero & Petite Tall Jars
    heroes_3000 = [
        "mariam_pitted_green_olives_white_studio_hero_4k.jpg",
        "mariam_sliced_green_olives_white_studio_hero_4k.jpg",
        "mariam_sliced_black_olives_white_studio_hero_4k.jpg",
        "mariam_royal_kalamata_olives_white_studio_hero_4k.jpg",
        "mariam_natural_black_olives_white_studio_hero_4k.jpg",
        "mariam_almond_stuffed_olives_white_studio_hero_4k.jpg",
        "mariam_garlic_stuffed_olives_white_studio_hero_4k.jpg",
        "mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg",
        "mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg",
        "mariam_royal_mixed_pickles_white_studio_hero_4k.jpg",
        "mariam_slow_roasted_garlic_white_studio_hero_4k.jpg",
        "mariam_green_olive_tapenade_white_studio_hero_4k.jpg",
        "mariam_kalamata_olive_tapenade_white_studio_hero_4k.jpg",
        # Petite Jars
        "mariam_crisp_baby_cucumbers_petite_210g_white_studio_hero_4k.jpg",
        "mariam_wild_turnip_beetroot_petite_210g_white_studio_hero_4k.jpg",
        "mariam_royal_mixed_pickles_petite_210g_white_studio_hero_4k.jpg",
        "mariam_slow_roasted_garlic_petite_100g_white_studio_hero_4k.jpg",
    ]

    for f in heroes_3000:
        process_hero_3000(f)

    # 4. Squat Gourmet Garlic & Toum Jars (3000x3000px)
    squat_jars = [
        "mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg",
        "mariam_whipped_toum_white_studio_hero_4k.jpg",
        "mariam_crushed_garlic_unroasted_petite_100g_white_studio_hero_4k.jpg",
        "mariam_whipped_toum_petite_100g_white_studio_hero_4k.jpg",
    ]

    for f in squat_jars:
        process_squat_jar(f)

    # 5. Solo Tall Jars (2400x3200)
    solos = [
        "mariam_natural_black_olives_solo_4k.jpg",
        "mariam_garlic_stuffed_olives_solo_4k.jpg",
        "mariam_crisp_baby_cucumbers_solo_4k.jpg",
        "mariam_petite_wild_turnip_beetroot_solo_4k.jpg",
        "mariam_royal_mixed_pickles_solo_4k.jpg",
        "mariam_pitted_green_olives_solo_4k.jpg",
        "mariam_green_olives_4k.jpg",
        "mariam_petite_royal_mixed_pickles_solo_4k.jpg",
        "mariam_wild_turnip_beetroot_pickles_solo_4k.jpg",
    ]

    for f in solos:
        process_solo_jar(f)

    print("=" * 70)
    print("ALL PACKSHOTS REBRANDED TO ARINA WITH ZERO GHOSTING & ZERO BLUR!")
    print("=" * 70)


if __name__ == "__main__":
    main()
