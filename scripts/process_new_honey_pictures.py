#!/usr/bin/env python3
"""
Process and composite all newly generated 4K photography for Mariam Natural Honey:
- Upscales lifestyle and editorial shots to true 4K (3840 × 2160 for 16:9, 3000 × 3000 for 1:1)
- Generates new white-studio multi-packshots using pristine 4K jar renders:
  1. mariam_honey_golden_nectars_duo_white_studio_4k.jpg (3000 × 3000)
  2. mariam_honey_connoisseur_duo_white_studio_4k.jpg (3000 × 3000)
  3. mariam_honey_six_jar_regal_panorama_white_studio_4k.jpg (3840 × 2160)
"""

import os
from PIL import Image, ImageChops, ImageDraw, ImageFilter

BASE_DIR = "/home/zexc/Desktop/New Folder"
OUT_DIR = os.path.join(BASE_DIR, "output", "imagery")
BRAIN_DIR = "/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# 1. Process Lifestyle & Macro Renders
lifestyle_maps = [
    ("honey_sidr_macro_dipper_drizzle_1790092196468.jpg", "mariam_honey_sidr_macro_dipper_drizzle_4k.jpg", (3000, 3000)),
    ("honey_honeycomb_hex_artisan_lifestyle_1790092221861.jpg", "mariam_honey_honeycomb_hex_artisan_lifestyle_4k.jpg", (3840, 2160)),
    ("honey_afternoon_tea_ricotta_figs_lifestyle_1790092246550.jpg", "mariam_honey_afternoon_tea_ricotta_figs_lifestyle_4k.jpg", (3840, 2160)),
    ("honey_gift_flight_box_unboxing_editorial_1790092274419.jpg", "mariam_honey_gift_flight_box_unboxing_editorial_4k.jpg", (3840, 2160)),
    ("honey_royal_mix_ingredients_flatlay_1790092303506.jpg", "mariam_honey_royal_mix_ingredients_flatlay_4k.jpg", (3000, 3000)),
    ("honey_luxury_boutique_shelf_display_1790092336080.jpg", "mariam_honey_luxury_boutique_shelf_display_4k.jpg", (3840, 2160)),
]

for src_name, dst_name, target_size in lifestyle_maps:
    src_path = os.path.join(BRAIN_DIR, src_name)
    if os.path.exists(src_path):
        im = Image.open(src_path).convert("RGB")
        im_4k = im.resize(target_size, Image.Resampling.LANCZOS)
        out_p = os.path.join(OUT_DIR, dst_name)
        brain_p = os.path.join(BRAIN_DIR, dst_name)
        im_4k.save(out_p, "JPEG", quality=98)
        im_4k.save(brain_p, "JPEG", quality=98)
        print(f"Saved: {dst_name} ({target_size})")

# 2. Extract Transparent Jars for Studio Composites
def get_jar_rgba(filename):
    p = os.path.join(OUT_DIR, filename)
    im = Image.open(p).convert("RGB")
    white = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, white).convert("L")
    alpha = diff.point(lambda p: 0 if p < 4 else (int((p - 3) / 17.0 * 255) if p < 20 else 255))
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)
    bbox = rgba.getbbox()
    return rgba.crop(bbox)

jar_sidr = get_jar_rgba("mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg")
jar_royal = get_jar_rgba("mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg")
jar_clover = get_jar_rgba("mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg")
jar_comb = get_jar_rgba("mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg")
jar_elixir = get_jar_rgba("mariam_honey_royal_jelly_elixir_white_studio_hero_4k.jpg")

# 3. Create Golden Nectars Duo (Sidr 500g + Clover 1kg) on Pure White (3000 × 3000)
def build_golden_nectars_duo():
    canvas = Image.new("RGBA", (3000, 3000), (255, 255, 255, 255))
    # Clover 1kg on right (height 2150)
    clover_h = 2150
    clover_w = int(jar_clover.width * (clover_h / jar_clover.height))
    clover_scaled = jar_clover.resize((clover_w, clover_h), Image.Resampling.LANCZOS)
    
    # Sidr 500g on left (height 1850)
    sidr_h = 1850
    sidr_w = int(jar_sidr.width * (sidr_h / jar_sidr.height))
    sidr_scaled = jar_sidr.resize((sidr_w, sidr_h), Image.Resampling.LANCZOS)
    
    # Shadow for Clover
    sh_clover = Image.new("RGBA", (int(clover_w * 1.15), 110), (0, 0, 0, 0))
    ImageDraw.Draw(sh_clover).ellipse([10, 10, sh_clover.width - 10, 100], fill=(0, 0, 0, 140))
    sh_clover = sh_clover.filter(ImageFilter.GaussianBlur(radius=22))
    
    # Shadow for Sidr
    sh_sidr = Image.new("RGBA", (int(sidr_w * 1.15), 95), (0, 0, 0, 0))
    ImageDraw.Draw(sh_sidr).ellipse([10, 10, sh_sidr.width - 10, 85], fill=(0, 0, 0, 150))
    sh_sidr = sh_sidr.filter(ImageFilter.GaussianBlur(radius=20))
    
    # Positions
    cx_sidr = 950
    cx_clover = 1950
    base_y = 2500
    
    canvas.alpha_composite(sh_clover, (cx_clover - sh_clover.width // 2, base_y - 45))
    canvas.alpha_composite(clover_scaled, (cx_clover - clover_w // 2, base_y - clover_h))
    
    canvas.alpha_composite(sh_sidr, (cx_sidr - sh_sidr.width // 2, base_y - 40))
    canvas.alpha_composite(sidr_scaled, (cx_sidr - sidr_w // 2, base_y - sidr_h))
    
    dst = "mariam_honey_golden_nectars_duo_white_studio_4k.jpg"
    canvas.convert("RGB").save(os.path.join(OUT_DIR, dst), "JPEG", quality=98)
    canvas.convert("RGB").save(os.path.join(BRAIN_DIR, dst), "JPEG", quality=98)
    print(f"Saved: {dst}")

build_golden_nectars_duo()

# 4. Create Connoisseur Duo (Royal Mix + Raw Honeycomb) on Pure White (3000 × 3000)
def build_connoisseur_duo():
    canvas = Image.new("RGBA", (3000, 3000), (255, 255, 255, 255))
    h_jars = 1880
    r_w = int(jar_royal.width * (h_jars / jar_royal.height))
    c_w = int(jar_comb.width * (h_jars / jar_comb.height))
    
    r_scaled = jar_royal.resize((r_w, h_jars), Image.Resampling.LANCZOS)
    c_scaled = jar_comb.resize((c_w, h_jars), Image.Resampling.LANCZOS)
    
    sh_r = Image.new("RGBA", (int(r_w * 1.15), 100), (0, 0, 0, 0))
    ImageDraw.Draw(sh_r).ellipse([10, 10, sh_r.width - 10, 90], fill=(0, 0, 0, 150))
    sh_r = sh_r.filter(ImageFilter.GaussianBlur(radius=20))
    
    sh_c = Image.new("RGBA", (int(c_w * 1.15), 100), (0, 0, 0, 0))
    ImageDraw.Draw(sh_c).ellipse([10, 10, sh_c.width - 10, 90], fill=(0, 0, 0, 150))
    sh_c = sh_c.filter(ImageFilter.GaussianBlur(radius=20))
    
    cx_r = 950
    cx_c = 2050
    base_y = 2500
    
    canvas.alpha_composite(sh_r, (cx_r - sh_r.width // 2, base_y - 40))
    canvas.alpha_composite(r_scaled, (cx_r - r_w // 2, base_y - h_jars))
    
    canvas.alpha_composite(sh_c, (cx_c - sh_c.width // 2, base_y - 40))
    canvas.alpha_composite(c_scaled, (cx_c - c_w // 2, base_y - h_jars))
    
    dst = "mariam_honey_connoisseur_duo_white_studio_4k.jpg"
    canvas.convert("RGB").save(os.path.join(OUT_DIR, dst), "JPEG", quality=98)
    canvas.convert("RGB").save(os.path.join(BRAIN_DIR, dst), "JPEG", quality=98)
    print(f"Saved: {dst}")

build_connoisseur_duo()

# 5. Create Six-Jar Regal Panorama (3840 × 2160 Cinema 4K)
def build_six_jar_panorama():
    canvas = Image.new("RGBA", (3840, 2160), (255, 255, 255, 255))
    jars_info = [
        (jar_sidr, 1250, 480),     # 1. Sidr 500g
        (jar_royal, 1300, 1050),    # 2. Royal Mix 500g
        (jar_clover, 1480, 1720),   # 3. Clover 1kg (centerpiece)
        (jar_comb, 1300, 2380),     # 4. Honeycomb 500g
        (jar_elixir, 1250, 2980),   # 5. Royal Jelly Elixir 500g
    ]
    
    base_y = 1880
    for j_crop, j_h, cx in jars_info:
        jw = int(j_crop.width * (j_h / j_crop.height))
        j_sc = j_crop.resize((jw, j_h), Image.Resampling.LANCZOS)
        
        sh = Image.new("RGBA", (int(jw * 1.15), 75), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([10, 10, sh.width - 10, 65], fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(radius=16))
        
        canvas.alpha_composite(sh, (cx - sh.width // 2, base_y - 30))
        canvas.alpha_composite(j_sc, (cx - jw // 2, base_y - j_h))
        
    dst = "mariam_honey_six_jar_regal_panorama_white_studio_4k.jpg"
    canvas.convert("RGB").save(os.path.join(OUT_DIR, dst), "JPEG", quality=98)
    canvas.convert("RGB").save(os.path.join(BRAIN_DIR, dst), "JPEG", quality=98)
    print(f"Saved: {dst}")

build_six_jar_panorama()

print("All new 4K pictures processed and saved successfully!")
