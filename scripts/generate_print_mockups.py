#!/usr/bin/env python3
"""
Mariam Luxury Brand - Master Print Mockup & Production Proof Generator
Generates high-resolution, print-ready packaging mockups and true 1:1 scale test sheets:
1. mariam_royal_mix_500g_printable_label_sheet_a4_300dpi.png (A4 Landscape, 3508 × 2480 @ 300 DPI, 297mm × 210mm)
2. mariam_packaging_press_proof_sheet_a3_300dpi.png (A3 Landscape, 4960 × 3508 @ 300 DPI, 420mm × 297mm)
3. mariam_royal_mix_500g_photorealistic_print_mockup_4k.jpg (Cinema 4K, 3840 × 2160)
4. mariam_packaging_print_evaluation_board_4k.jpg (Cinema 4K, 3840 × 2160)
5. mariam_olives_370g_printable_label_sheet_a4_300dpi.png (A4 Landscape, 3508 × 2480 @ 300 DPI, 297mm × 210mm)
"""

import math
import os
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

# Root Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_MOCKUPS = os.path.join(BASE_DIR, "output", "mockups")
OUTPUT_IMAGERY = os.path.join(BASE_DIR, "output", "imagery")
OUTPUT_DIELINES = os.path.join(BASE_DIR, "output", "dielines")
BRAIN_DIR = "/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d"

os.makedirs(OUTPUT_MOCKUPS, exist_ok=True)
os.makedirs(OUTPUT_IMAGERY, exist_ok=True)
os.makedirs(OUTPUT_DIELINES, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# Master Palette Constants
BLUSH_PINK = (245, 183, 194)        # #F5B7C2 (Petal Blush Pink)
BLUSH_PINK_LIGHT = (252, 220, 227)  # #FCDCE3 (Light Tint)
IMPERIAL_BURGUNDY = (118, 18, 46)   # #76122E (Deep Wine Burgundy)
LUXOR_GOLD = (218, 172, 54)         # #DAAC36 (Kurz Luxor 428 Gold)
WARM_IVORY = (255, 245, 247)        # #FFF5F7 (Warm Blush Ivory)
FOREST_GREEN = (30, 51, 38)         # #1E3326 (Primary Packaging Green)
CHAMPAGNE_GOLD = (238, 212, 142)    # #EED48E
DARK_OBSIDIAN = (18, 22, 20)        # #121614
PURE_WHITE = (255, 255, 255)
PURE_BLACK = (0, 0, 0)
GRAY_LINE = (180, 180, 180)
GRAY_LIGHT = (240, 240, 240)

# Fonts
FONT_BOLD = os.path.join(BASE_DIR, "fonts", "Tajawal-Bold.ttf")
FONT_MED = os.path.join(BASE_DIR, "fonts", "Tajawal-Medium.ttf")
FONT_REG = os.path.join(BASE_DIR, "fonts", "Tajawal-Regular.ttf")

def load_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_MED
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

# Logo
LOGO_GOLD_PATH = os.path.join(BASE_DIR, "mariam-logo-gold.png")
logo_master = Image.open(LOGO_GOLD_PATH).convert("RGBA") if os.path.exists(LOGO_GOLD_PATH) else None

def get_tinted_logo(target_w, color=LUXOR_GOLD):
    if not logo_master:
        return None
    target_h = max(1, int(logo_master.height * (target_w / logo_master.width)))
    scaled = logo_master.resize((target_w, target_h), Image.Resampling.LANCZOS)
    r, g, b, a = scaled.split()
    tinted = Image.new("RGBA", (target_w, target_h), (*color, 255))
    tinted.putalpha(a)
    return tinted

def draw_crop_marks(draw, x0, y0, x1, y1, mark_len=40, offset=12, color=PURE_BLACK, width=2):
    """Draws standard professional L-shaped corner crop marks for cutting."""
    # Top-Left
    draw.line([(x0 - offset - mark_len, y0), (x0 - offset, y0)], fill=color, width=width)
    draw.line([(x0, y0 - offset - mark_len), (x0, y0 - offset)], fill=color, width=width)
    # Top-Right
    draw.line([(x1 + offset, y0), (x1 + offset + mark_len, y0)], fill=color, width=width)
    draw.line([(x1, y0 - offset - mark_len), (x1, y0 - offset)], fill=color, width=width)
    # Bottom-Left
    draw.line([(x0 - offset - mark_len, y1), (x0 - offset, y1)], fill=color, width=width)
    draw.line([(x0, y1 + offset), (x0, y1 + offset + mark_len)], fill=color, width=width)
    # Bottom-Right
    draw.line([(x1 + offset, y1), (x1 + offset + mark_len, y1)], fill=color, width=width)
    draw.line([(x1, y1 + offset), (x1, y1 + offset + mark_len)], fill=color, width=width)

def draw_registration_crosshair(draw, cx, cy, size=24, color=PURE_BLACK, width=2):
    """Draws printing press optical registration target."""
    draw.line([(cx - size, cy), (cx + size, cy)], fill=color, width=width)
    draw.line([(cx, cy - size), (cx, cy + size)], fill=color, width=width)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=color, width=2)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=color)

def draw_calibration_ruler(draw, cx, cy, length_mm=100, dpi=300):
    """Draws a true millimeter scale calibration ruler."""
    px_per_mm = dpi / 25.4
    total_px = int(length_mm * px_per_mm)
    x_start = cx - total_px // 2
    x_end = x_start + total_px
    ruler_h = 44
    
    # Background strip
    draw.rectangle([x_start - 10, cy - 10, x_end + 10, cy + ruler_h + 30], fill=(250, 250, 250), outline=GRAY_LINE, width=1)
    
    # Baseline
    draw.line([(x_start, cy + ruler_h), (x_end, cy + ruler_h)], fill=PURE_BLACK, width=2)
    
    font_num = load_font(18, bold=True)
    font_sub = load_font(15, bold=False)
    
    for mm in range(length_mm + 1):
        x = x_start + int(mm * px_per_mm)
        if mm % 10 == 0:
            tick_h = 28
            draw.line([(x, cy + ruler_h - tick_h), (x, cy + ruler_h)], fill=PURE_BLACK, width=2)
            draw.text((x, cy + ruler_h - tick_h - 14), str(mm), fill=PURE_BLACK, font=font_num, anchor="mm")
        elif mm % 5 == 0:
            tick_h = 18
            draw.line([(x, cy + ruler_h - tick_h), (x, cy + ruler_h)], fill=PURE_BLACK, width=1)
        else:
            tick_h = 10
            draw.line([(x, cy + ruler_h - tick_h), (x, cy + ruler_h)], fill=GRAY_LINE, width=1)
            
    # Label underneath
    note = "▲ 100 mm Physical Scale Check: Measure with physical ruler. If 100mm matches exactly, printer scale is 100% correct. ▲"
    draw.text((cx, cy + ruler_h + 16), note, fill=IMPERIAL_BURGUNDY, font=font_sub, anchor="mm")

def draw_cmyk_pantone_swatches(draw, base_x, base_y, swatch_w=38, swatch_h=24):
    """Draws CMYK step wedges and Pantone spot color chips."""
    font_sm = load_font(14, bold=False)
    
    cmyk_colors = [
        ((0, 160, 230), "C 100%"),
        ((230, 0, 120), "M 100%"),
        ((255, 230, 0), "Y 100%"),
        ((20, 20, 20), "K 100%"),
    ]
    spot_colors = [
        (LUXOR_GOLD, "Pantone 871 C (Gold)"),
        (BLUSH_PINK, "Petal Blush #F5B7C2"),
        (IMPERIAL_BURGUNDY, "Wine Burgundy #76122E"),
        (FOREST_GREEN, "Pantone 5605 C (Green)"),
    ]
    
    cur_x = base_x
    for col, name in cmyk_colors + spot_colors:
        draw.rectangle([cur_x, base_y, cur_x + swatch_w, base_y + swatch_h], fill=col, outline=GRAY_LINE, width=1)
        draw.text((cur_x + swatch_w // 2, base_y + swatch_h + 10), name[:3], fill=PURE_BLACK, font=font_sm, anchor="mm")
        cur_x += swatch_w + 14

def get_scalloped_cartouche_polygon(x0, y0, x1, y1, r=40, arch_h=30, n_corner=12, n_arch=24):
    """Generates authentic scalloped baroque cartouche polygon matching reference photo."""
    pts = []
    cx = (x0 + x1) / 2
    for i in range(n_arch + 1):
        t = i / n_arch
        px = (x0 + r) + t * (x1 - x0 - 2 * r)
        py = y0 + (1.0 - math.sin(t * math.pi)) * arch_h
        pts.append((px, py))
    for i in range(1, n_corner + 1):
        ang = math.radians(180 + i * (90 / n_corner))
        px = x1 + r * math.cos(ang)
        py = (y0 + arch_h) - r * math.sin(ang)
        pts.append((px, py))
    pts.append((x1, y1 - arch_h - r))
    for i in range(1, n_corner + 1):
        ang = math.radians(90 + i * (90 / n_corner))
        px = x1 + r * math.cos(ang)
        py = (y1 - arch_h) - r * math.sin(ang)
        pts.append((px, py))
    for i in range(n_arch + 1):
        t = i / n_arch
        px = (x1 - r) - t * (x1 - x0 - 2 * r)
        py = y1 - (1.0 - math.sin(t * math.pi)) * arch_h
        pts.append((px, py))
    for i in range(1, n_corner + 1):
        ang = math.radians(0 + i * (90 / n_corner))
        px = x0 + r * math.cos(ang)
        py = (y1 - arch_h) - r * math.sin(ang)
        pts.append((px, py))
    pts.append((x0, y0 + arch_h + r))
    for i in range(1, n_corner + 1):
        ang = math.radians(270 + i * (90 / n_corner))
        px = x0 + r * math.cos(ang)
        py = (y0 + arch_h) - r * math.sin(ang)
        pts.append((px, py))
    return [(int(round(px)), int(round(py))) for px, py in pts]

def draw_crown(draw, cx, cy, width, height, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY):
    """Draws embossed royal crown crest with 5 peaks and pearls."""
    w2 = width // 2
    h2 = height // 2
    base_h = max(6, int(height * 0.22))
    base_y = cy + h2 - base_h
    draw.rectangle([cx - w2, base_y, cx + w2, cy + h2], fill=color)
    for jx in [-w2 * 0.65, -w2 * 0.22, w2 * 0.22, w2 * 0.65]:
        draw.ellipse([cx + jx - 3, base_y + 2, cx + jx + 3, base_y + 8], fill=jewel_color)
    pts = [
        (cx - w2, base_y),
        (cx - w2, cy - int(h2 * 0.65)),
        (cx - int(w2 * 0.6), base_y - 6),
        (cx - int(w2 * 0.3), cy - int(h2 * 0.45)),
        (cx, base_y - 8),
        (cx + int(w2 * 0.3), cy - int(h2 * 0.45)),
        (cx + int(w2 * 0.6), base_y - 6),
        (cx + w2, cy - int(h2 * 0.65)),
        (cx + w2, base_y),
    ]
    draw.polygon(pts, fill=color)
    draw.polygon([(cx - int(w2 * 0.22), base_y), (cx, cy - h2), (cx + int(w2 * 0.22), base_y)], fill=color)
    for px, py in [
        (cx - w2, cy - int(h2 * 0.65) - 4),
        (cx - int(w2 * 0.3), cy - int(h2 * 0.45) - 4),
        (cx, cy - h2 - 5),
        (cx + int(w2 * 0.3), cy - int(h2 * 0.45) - 4),
        (cx + w2, cy - int(h2 * 0.65) - 4),
    ]:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=color)

def draw_barcode(draw, x, y, w, h, code_text="6281005001017", bar_color=PURE_BLACK, text_color=PURE_BLACK):
    """Draws realistic EAN-13 barcode with guard bars and text."""
    cur_x = x + 10
    end_x = x + w - 10
    bar_h = h - 24
    draw.line([(cur_x, y), (cur_x, y + bar_h + 8)], fill=bar_color, width=2)
    cur_x += 4
    draw.line([(cur_x, y), (cur_x, y + bar_h + 8)], fill=bar_color, width=2)
    cur_x += 6
    patterns = [2, 1, 3, 2, 1, 4, 2, 3, 1, 2, 4, 1, 2, 3, 2, 1, 3, 2, 1, 2, 3, 1, 4, 2, 1, 3, 2, 1, 2, 4]
    for p in patterns:
        if cur_x >= end_x - 14:
            break
        draw.rectangle([cur_x, y, cur_x + p, y + bar_h], fill=bar_color)
        cur_x += p + 3
    draw.line([(end_x - 6, y), (end_x - 6, y + bar_h + 8)], fill=bar_color, width=2)
    draw.line([(end_x - 2, y), (end_x - 2, y + bar_h + 8)], fill=bar_color, width=2)
    font_bc = load_font(15, bold=True)
    draw.text((x + w // 2, y + h - 6), code_text, fill=text_color, font=font_bc, anchor="mm")

# ==============================================================================
# 1. RENDER FULL ROYAL MIX 500g LABEL (2835 × 1004 px @ 300 DPI = 240mm × 85mm)
# ==============================================================================
def render_royal_mix_label_300dpi(width=2835, height=1004):
    """Renders the physical 1:1 scale wrap-around label for Mariam Royal Mix 500g."""
    im = Image.new("RGBA", (width, height), (*FOREST_GREEN, 255))
    draw = ImageDraw.Draw(im)
    
    # Outer luxury gold border
    draw.rounded_rectangle([15, 15, width - 15, height - 15], radius=24, outline=LUXOR_GOLD, width=4)
    draw.rounded_rectangle([32, 32, width - 32, height - 32], radius=18, outline=CHAMPAGNE_GOLD, width=1)
    
    # Grid Dividers: Zone 1 (Left: 27%), Zone 2 (Center: 46%), Zone 3 (Right: 27%)
    z1_w = int(width * 0.27)
    z2_w = int(width * 0.46)
    cx0 = z1_w
    cx1 = z1_w + z2_w
    
    draw.line([(cx0, 32), (cx0, height - 32)], fill=LUXOR_GOLD, width=2)
    draw.line([(cx1, 32), (cx1, height - 32)], fill=LUXOR_GOLD, width=2)
    
    # ==================== ZONE 1: NUTRITION & REGULATORY ====================
    z1_cx = cx0 // 2
    f_title = load_font(26, bold=True)
    f_sub = load_font(18, bold=True)
    f_sm = load_font(14, bold=False)
    
    draw.text((z1_cx, 60), "NUTRITION FACTS • الحقائق الغذائية", fill=WARM_IVORY, font=f_title, anchor="mm")
    draw.text((z1_cx, 95), "Per 100g: 340 kcal | Protein 4.8g | Carbs 72g | Fat 5.2g", fill=CHAMPAGNE_GOLD, font=f_sm, anchor="mm")
    
    # Ingredients Box
    box_x0, box_x1 = 50, cx0 - 50
    draw.rounded_rectangle([box_x0, 125, box_x1, 520], radius=12, fill=(24, 42, 31), outline=LUXOR_GOLD, width=1)
    draw.text((z1_cx, 155), "INGREDIENTS / المكونات الفاخرة", fill=LUXOR_GOLD, font=f_sub, anchor="mm")
    
    ing_text = [
        "Pure Mountain Floral Honey (55%)",
        "Raw Fresh Royal Jelly (5%)",
        "Premium Roasted Tree Nuts (25%):",
        "  • Pistachios, Almonds, Cashews, Walnuts",
        "Superfood Vitality Seeds (15%):",
        "  • Nigella Sativa (Black Seed), Pumpkin,",
        "  • Golden Flaxseed, Sesame & Chia Seeds",
        "------------------------------------",
        "عسل جبلي طبيعي 55%، غذاء ملكات النحل 5%",
        "مكسرات شجرية فاخرة 25% (فستق، لوز، كاجو، عين جمل)",
        "بذور سوبرفود نقية 15% (حبة البركة، بذور اليقطين، كتان)",
    ]
    cur_y = 190
    for line in ing_text:
        col = LUXOR_GOLD if line.startswith("Premium") or line.startswith("Superfood") else WARM_IVORY
        draw.text((z1_cx, cur_y), line, fill=col, font=f_sm, anchor="mm")
        cur_y += 28
        
    # Allergen Badge
    draw.rounded_rectangle([box_x0, 545, box_x1, 635], radius=10, fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=1)
    draw.text((z1_cx, 572), "ALLERGEN WARNING / تنبيه الحساسية", fill=WARM_IVORY, font=f_sub, anchor="mm")
    draw.text((z1_cx, 608), "Contains Tree Nuts & Bee Products. 100% Peanut-Free.", fill=CHAMPAGNE_GOLD, font=f_sm, anchor="mm")
    
    # Storage & Net Weight
    draw.text((z1_cx, 675), "Keep in a cool, dry place (18°C - 24°C). Store upright.", fill=WARM_IVORY, font=f_sm, anchor="mm")
    draw.text((z1_cx, 710), "يحفظ في مكان بارد وجاف بعيداً عن أشعة الشمس المباشرة", fill=WARM_IVORY, font=f_sm, anchor="mm")
    draw.text((z1_cx, 770), "NET WEIGHT: 500g e (17.6 oz)", fill=LUXOR_GOLD, font=load_font(28, bold=True), anchor="mm")
    draw.text((z1_cx, 810), "الوزن الصافي: 500 غرام", fill=CHAMPAGNE_GOLD, font=load_font(22, bold=True), anchor="mm")
    
    # ==================== ZONE 2: CENTER HERO CARTOUCHE ====================
    z2_cx = cx0 + z2_w // 2
    cart_w = int(z2_w * 0.88)
    cart_h = int(height * 0.86)
    c_x0 = z2_cx - cart_w // 2
    c_x1 = z2_cx + cart_w // 2
    c_y0 = (height - cart_h) // 2
    c_y1 = c_y0 + cart_h
    
    cart_r = int(cart_w * 0.055)
    cart_arch = int(cart_h * 0.045)
    pts_outer = get_scalloped_cartouche_polygon(c_x0, c_y0, c_x1, c_y1, r=cart_r, arch_h=cart_arch)
    draw.polygon(pts_outer, fill=BLUSH_PINK, outline=LUXOR_GOLD, width=4)
    
    pts_inner = get_scalloped_cartouche_polygon(c_x0 + 10, c_y0 + 10, c_x1 - 10, c_y1 - 10, r=cart_r - 6, arch_h=cart_arch - 3)
    draw.polygon(pts_inner, outline=LUXOR_GOLD, width=2)
    
    # Crown Crest
    crown_w = 110
    crown_h = 58
    crown_cy = c_y0 + cart_arch + 48
    draw_crown(draw, cx=z2_cx, cy=crown_cy, width=crown_w, height=crown_h, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
    
    # Cursive Mariam Logo in Deep Wine Burgundy
    burgundy_logo = get_tinted_logo(target_w=480, color=IMPERIAL_BURGUNDY)
    if burgundy_logo:
        logo_y = crown_cy + crown_h // 2 + 16
        im.alpha_composite(burgundy_logo, (z2_cx - burgundy_logo.width // 2, logo_y))
        next_y = logo_y + burgundy_logo.height + 16
    else:
        next_y = crown_cy + 80
        
    f_desc = load_font(20, bold=True)
    draw.text((z2_cx, next_y), "NATURAL HONEY & SUPERFOODS", fill=IMPERIAL_BURGUNDY, font=f_desc, anchor="mm")
    next_y += 36
    
    f_hero = load_font(42, bold=True)
    draw.text((z2_cx, next_y), "MARIAM ROYAL MIX", fill=IMPERIAL_BURGUNDY, font=f_hero, anchor="mm")
    next_y += 42
    
    f_ar = load_font(24, bold=True)
    draw.text((z2_cx, next_y), "الخلطة الملكية الفاخرة • عسل طبيعي ومكسرات وغذاء ملكات", fill=IMPERIAL_BURGUNDY, font=f_ar, anchor="mm")
    next_y += 48
    
    ribbon_w = min(cart_w - 90, 720)
    ribbon_h = 42
    draw.rounded_rectangle([z2_cx - ribbon_w // 2, next_y - ribbon_h // 2,
                            z2_cx + ribbon_w // 2, next_y + ribbon_h // 2],
                           radius=10, fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=2)
    f_ribbon = load_font(20, bold=True)
    draw.text((z2_cx, next_y), "• 0% PEANUTS • 100% TREE NUTS • 5% ROYAL JELLY •", fill=WARM_IVORY, font=f_ribbon, anchor="mm")
    next_y += 46
    
    f_triad = load_font(22, bold=False)
    draw.text((z2_cx, next_y), "Crunchy • Opulent • Energizing", fill=IMPERIAL_BURGUNDY, font=f_triad, anchor="mm")
    next_y += 34
    
    draw.line([(z2_cx - 90, next_y), (z2_cx - 16, next_y)], fill=LUXOR_GOLD, width=2)
    draw.line([(z2_cx + 16, next_y), (z2_cx + 90, next_y)], fill=LUXOR_GOLD, width=2)
    draw.ellipse([z2_cx - 5, next_y - 5, z2_cx + 5, next_y + 5], fill=LUXOR_GOLD)
    next_y += 36
    
    f_wt = load_font(24, bold=True)
    draw.text((z2_cx, next_y), "NET WT. 500g e (17.6 oz)", fill=IMPERIAL_BURGUNDY, font=f_wt, anchor="mm")
    
    # ==================== ZONE 3: TERROIR & LOGISTICS ====================
    z3_cx = cx1 + (width - cx1) // 2
    
    draw.text((z3_cx, 60), "SINGLE-ESTATE TERROIR", fill=WARM_IVORY, font=f_title, anchor="mm")
    draw.text((z3_cx, 95), "من إنتاج مزارع خير الوادي الطبيعية", fill=CHAMPAGNE_GOLD, font=f_sub, anchor="mm")
    
    draw.ellipse([z3_cx - 65, 140, z3_cx + 65, 270], outline=LUXOR_GOLD, width=3)
    draw.ellipse([z3_cx - 55, 150, z3_cx + 55, 260], outline=CHAMPAGNE_GOLD, width=1)
    draw_crown(draw, cx=z3_cx, cy=185, width=44, height=24, color=LUXOR_GOLD)
    draw.text((z3_cx, 225), "KHAEER ALWADI", fill=LUXOR_GOLD, font=load_font(13, bold=True), anchor="mm")
    draw.text((z3_cx, 243), "خير الوادي", fill=WARM_IVORY, font=load_font(13, bold=False), anchor="mm")
    
    claims = [
        "100% Unpasteurized & Pure Raw Honey",
        "Cold-Blended to Preserve Living Enzymes",
        "Laboratory Tested & Certified Pesticide-Free",
        "No Artificial Flavors, Preservatives or Corn Syrup",
        "------------------------------------",
        "عسل جبلي خام نقي غير مبستر بنسبة 100%",
        "ممزوج على البارد للحفاظ على الإنزيمات النشطة",
        "مفحوص مخبرياً وخالٍ من بقايا المبيدات والسكريات",
    ]
    cur_y = 310
    for c in claims:
        draw.text((z3_cx, cur_y), c, fill=WARM_IVORY, font=f_sm, anchor="mm")
        cur_y += 28
        
    bc_w, bc_h = 320, 110
    bc_x = z3_cx - bc_w // 2
    bc_y = 570
    draw.rectangle([bc_x - 14, bc_y - 10, bc_x + bc_w + 14, bc_y + bc_h + 14], fill=PURE_WHITE, outline=LUXOR_GOLD, width=2)
    draw_barcode(draw, bc_x, bc_y, bc_w, bc_h, "6281005001017", bar_color=PURE_BLACK, text_color=PURE_BLACK)
    
    draw.text((z3_cx, 740), "ISO 22000 • HACCP • HALAL CERTIFIED", fill=CHAMPAGNE_GOLD, font=f_sub, anchor="mm")
    draw.text((z3_cx, 780), "♻ RECYCLABLE GLASS CONTAINER • BATCH: RM-500-2026", fill=WARM_IVORY, font=f_sm, anchor="mm")
    draw.text((z3_cx, 820), "PRODUCT OF ARABIAN HIGHLANDS • صنع في المملكة العربية السعودية", fill=LUXOR_GOLD, font=f_sm, anchor="mm")
    
    return im

# ==============================================================================
# 2. RENDER TAMPER-EVIDENT RIBBON (213 × 531 px @ 300 DPI = 18mm × 45mm)
# ==============================================================================
def render_tamper_ribbon_300dpi(width=213, height=531):
    """Renders 18mm × 45mm tamper-evident safety seal ribbon."""
    im = Image.new("RGBA", (width, height), (*BLUSH_PINK, 255))
    draw = ImageDraw.Draw(im)
    
    draw.rectangle([6, 6, width - 6, height - 6], outline=LUXOR_GOLD, width=3)
    draw.rectangle([14, 14, width - 14, height - 14], outline=WARM_IVORY, width=1)
    
    cx = width // 2
    crown_cy = height // 2 - 30
    draw.ellipse([cx - 55, crown_cy - 55, cx + 55, crown_cy + 55], outline=LUXOR_GOLD, width=3)
    draw.ellipse([cx - 48, crown_cy - 48, cx + 48, crown_cy + 48], outline=WARM_IVORY, width=1)
    draw_crown(draw, cx=cx, cy=crown_cy, width=64, height=36, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
    
    f_rib_brand = load_font(26, bold=True)
    draw.text((cx, crown_cy + 80), "MARIAM", fill=IMPERIAL_BURGUNDY, font=f_rib_brand, anchor="mm")
    
    f_rib_seal = load_font(15, bold=True)
    draw.text((cx, crown_cy + 115), "SAFETY SEAL", fill=IMPERIAL_BURGUNDY, font=f_rib_seal, anchor="mm")
    draw.text((cx, crown_cy + 140), "ختم الأمان الملكي", fill=IMPERIAL_BURGUNDY, font=f_rib_seal, anchor="mm")
    
    perf_y = height // 2 + 180
    for px in range(16, width - 16, 12):
        draw.line([(px, perf_y), (px + 6, perf_y)], fill=IMPERIAL_BURGUNDY, width=2)
    draw.text((cx, perf_y - 16), "✂ BREAK TO OPEN ✂", fill=IMPERIAL_BURGUNDY, font=load_font(13, bold=True), anchor="mm")
    draw.text((cx, perf_y + 18), "يكسر عند الفتح", fill=IMPERIAL_BURGUNDY, font=load_font(13, bold=False), anchor="mm")
    
    return im

# ==============================================================================
# 3. RENDER LID TOP CIRCULAR SEAL (709 × 709 px @ 300 DPI = Ø 60mm)
# ==============================================================================
def render_lid_seal_300dpi(diameter=709):
    """Renders 60mm diameter circular lid sticker for the gold cap."""
    im = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cx = cy = diameter // 2
    r = diameter // 2 - 8
    
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUSH_PINK, outline=LUXOR_GOLD, width=5)
    draw.ellipse([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], outline=WARM_IVORY, width=2)
    draw.ellipse([cx - r + 24, cy - r + 24, cx + r - 24, cy + r - 24], outline=LUXOR_GOLD, width=1)
    
    draw_crown(draw, cx=cx, cy=cy - 120, width=130, height=72, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
    
    burg_logo = get_tinted_logo(target_w=360, color=IMPERIAL_BURGUNDY)
    if burg_logo:
        im.alpha_composite(burg_logo, (cx - burg_logo.width // 2, cy - 40))
        
    f_lid_title = load_font(26, bold=True)
    draw.text((cx, cy + 90), "PURE GOODNESS, NATURALLY", fill=IMPERIAL_BURGUNDY, font=f_lid_title, anchor="mm")
    
    f_lid_ar = load_font(22, bold=True)
    draw.text((cx, cy + 130), "عسل طبيعي نقي • مصنوع بحب", fill=IMPERIAL_BURGUNDY, font=f_lid_ar, anchor="mm")
    
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        dot_r = r - 18
        dx = cx + dot_r * math.cos(rad)
        dy = cy + dot_r * math.sin(rad)
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=LUXOR_GOLD)
        
    return im

# ==============================================================================
# 4. BUILD A4 1:1 PRINTABLE PROOF SHEET (3508 × 2480 @ 300 DPI)
# ==============================================================================
def build_a4_printable_sheet():
    """Builds standard A4 Landscape physical print proof sheet."""
    w, h = 3508, 2480  # A4 @ 300 DPI
    sheet = Image.new("RGBA", (w, h), PURE_WHITE)
    draw = ImageDraw.Draw(sheet)
    
    draw.line([(80, 50), (w - 80, 50)], fill=LUXOR_GOLD, width=2)
    
    gold_logo_sm = get_tinted_logo(target_w=200, color=LUXOR_GOLD)
    if gold_logo_sm:
        sheet.alpha_composite(gold_logo_sm, (100, 70))
        
    draw.text((320, 95), "MARIAM LUXURY FOOD PRODUCTS", fill=FOREST_GREEN, font=load_font(24, bold=True), anchor="lm")
    draw.text((320, 130), "PACKAGING PROTOTYPE & DIRECT PRINT MOCKUP", fill=LUXOR_GOLD, font=load_font(18, bold=True), anchor="lm")
    
    draw.text((w // 2 + 100, 95), "نموذج تجربة الطباعة والقص والتركيب الميكانيكي على العبوة", fill=FOREST_GREEN, font=load_font(26, bold=True), anchor="mm")
    draw.text((w // 2 + 100, 135), "مقياس رسم حقيقي 1:1 (True 1:1 Physical Scale) • دقة المعايرة: 300 DPI", fill=IMPERIAL_BURGUNDY, font=load_font(20, bold=False), anchor="mm")
    
    draw.text((w - 100, 95), "CONTAINER: 500g Nordic Glass Jar", fill=PURE_BLACK, font=load_font(18, bold=True), anchor="rm")
    draw.text((w - 100, 130), "DIAMETER: Ø 85mm | HEIGHT: 118mm", fill=GRAY_LINE, font=load_font(16, bold=False), anchor="rm")
    
    draw.line([(80, 170), (w - 80, 170)], fill=LUXOR_GOLD, width=2)
    
    draw_calibration_ruler(draw, cx=w // 2, cy=200, length_mm=100, dpi=300)
    
    inst_y = 310
    draw.rounded_rectangle([100, inst_y, w // 2 - 20, inst_y + 110], radius=10, fill=(248, 248, 250), outline=GRAY_LINE, width=1)
    draw.text((120, inst_y + 25), "PRINTING INSTRUCTIONS (English):", fill=FOREST_GREEN, font=load_font(17, bold=True), anchor="lm")
    draw.text((120, inst_y + 55), "1. Paper: 90-120 gsm Self-Adhesive Matte or Textured Linen Sticker Paper.", fill=PURE_BLACK, font=load_font(14, bold=False), anchor="lm")
    draw.text((120, inst_y + 85), "2. Scale: Set Printer to 100% or 'Actual Size' (DO NOT 'Fit to Page'). Verify 100mm ruler.", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=True), anchor="lm")
    
    draw.rounded_rectangle([w // 2 + 20, inst_y, w - 100, inst_y + 110], radius=10, fill=(248, 248, 250), outline=GRAY_LINE, width=1)
    draw.text((w // 2 + 40, inst_y + 25), "تعليمات الطباعة والتركيب (عربي):", fill=FOREST_GREEN, font=load_font(18, bold=True), anchor="lm")
    draw.text((w // 2 + 40, inst_y + 55), "1. الورق: ورق لاصق مطفي (Sticker Paper) أو كتان بارز 90-120 جم.", fill=PURE_BLACK, font=load_font(15, bold=False), anchor="lm")
    draw.text((w // 2 + 40, inst_y + 85), "2. المقياس: اختر 'الحجم الفعلي 100%' دون تصغير. تحقق من مسطرة الـ 100 مم بالمسطرة العادية.", fill=IMPERIAL_BURGUNDY, font=load_font(15, bold=True), anchor="lm")
    
    lbl_w, lbl_h = 2835, 1004
    lbl_x0 = (w - lbl_w) // 2
    lbl_y0 = 470
    lbl_x1 = lbl_x0 + lbl_w
    lbl_y1 = lbl_y0 + lbl_h
    
    label_img = render_royal_mix_label_300dpi(lbl_w, lbl_h)
    sheet.alpha_composite(label_img, (lbl_x0, lbl_y0))
    draw_crop_marks(draw, lbl_x0, lbl_y0, lbl_x1, lbl_y1, mark_len=45, offset=15, color=PURE_BLACK, width=2)
    
    for sx in range(lbl_x0 - 15, lbl_x1 + 15, 20):
        draw.line([(sx, lbl_y0 - 15), (sx + 10, lbl_y0 - 15)], fill=GRAY_LINE, width=1)
        draw.line([(sx, lbl_y1 + 15), (sx + 10, lbl_y1 + 15)], fill=GRAY_LINE, width=1)
    for sy in range(lbl_y0 - 15, lbl_y1 + 15, 20):
        draw.line([(lbl_x0 - 15, sy), (lbl_x0 - 15, sy + 10)], fill=GRAY_LINE, width=1)
        draw.line([(lbl_x1 + 15, sy), (lbl_x1 + 15, sy + 10)], fill=GRAY_LINE, width=1)
        
    draw.text((lbl_x0 + 40, lbl_y0 - 30), "✂ CUT ALONG DASHED LINE / خط القص الخارجي ✂", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="lm")
    draw.text((lbl_x1 - 40, lbl_y0 - 30), "FINISHED TRIM: 240mm × 85mm", fill=LUXOR_GOLD, font=load_font(16, bold=True), anchor="rm")
    
    bot_y = 1530
    
    ribbon_img = render_tamper_ribbon_300dpi(213, 531)
    rx0 = 240
    ry0 = bot_y + 110
    sheet.alpha_composite(ribbon_img, (rx0, ry0))
    draw_crop_marks(draw, rx0, ry0, rx0 + 213, ry0 + 531, mark_len=25, offset=10, color=PURE_BLACK, width=2)
    draw.text((rx0 + 106, ry0 - 25), "TAMPER SEAL (18×45mm)", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="mm")
    draw.text((rx0 + 106, ry0 + 531 + 25), "شريط إحكام الغطاء", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=False), anchor="mm")
    
    lid_seal = render_lid_seal_300dpi(640)
    lx0 = 600
    ly0 = bot_y + 60
    sheet.alpha_composite(lid_seal, (lx0, ly0))
    draw.text((lx0 + 320, ly0 - 20), "CAP TOP SEAL (Ø 60mm)", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="mm")
    draw.text((lx0 + 320, ly0 + 640 + 25), "ملصق قمة الغطاء الدائري", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=False), anchor="mm")
    
    cx_box = 1420
    cy_box = bot_y + 80
    draw.rounded_rectangle([cx_box, cy_box, cx_box + 900, cy_box + 260], radius=12, fill=(252, 252, 254), outline=GRAY_LINE, width=1)
    draw.text((cx_box + 30, cy_box + 35), "COLOR CALIBRATION BARS & PRESS CONTROL:", fill=FOREST_GREEN, font=load_font(18, bold=True), anchor="lm")
    draw_cmyk_pantone_swatches(draw, base_x=cx_box + 30, base_y=cy_box + 70, swatch_w=48, swatch_h=28)
    
    draw.text((cx_box + 30, cy_box + 175), "• CMYK Process: Standard Euroscale / FOGRA 39 Coated", fill=PURE_BLACK, font=load_font(14, bold=False), anchor="lm")
    draw.text((cx_box + 30, cy_box + 205), "• Spot Metallics: Kurz Luxor 428 Metallic Gold Foil", fill=LUXOR_GOLD, font=load_font(14, bold=True), anchor="lm")
    draw.text((cx_box + 30, cy_box + 235), "• Spot Solid: Deep Wine Burgundy (Pantone 7428 C / #76122E)", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=True), anchor="lm")
    
    gx_box = 2440
    gy_box = bot_y + 80
    draw.rounded_rectangle([gx_box, gy_box, w - 100, gy_box + 260], radius=12, fill=(252, 252, 254), outline=GRAY_LINE, width=1)
    draw.text((gx_box + 30, gy_box + 35), "HOW TO TEST ON JAR (طريقة التركيب):", fill=FOREST_GREEN, font=load_font(18, bold=True), anchor="lm")
    guide_steps = [
        "1. Cut main label along outer dashed marks.",
        "2. Align center cartouche with jar front and wrap.",
        "3. Apply round sticker to center of gold lid.",
        "4. Place tamper ribbon vertically over lid & glass.",
        "5. Inspect alignment, readability and barcode scan.",
    ]
    for idx, s in enumerate(guide_steps):
        draw.text((gx_box + 30, gy_box + 75 + idx * 32), s, fill=PURE_BLACK, font=load_font(15, bold=False), anchor="lm")
        
    draw_registration_crosshair(draw, 60, 60, size=24, color=LUXOR_GOLD)
    draw_registration_crosshair(draw, w - 60, 60, size=24, color=LUXOR_GOLD)
    draw_registration_crosshair(draw, 60, h - 60, size=24, color=LUXOR_GOLD)
    draw_registration_crosshair(draw, w - 60, h - 60, size=24, color=LUXOR_GOLD)
    
    draw.line([(80, h - 50), (w - 80, h - 50)], fill=LUXOR_GOLD, width=2)
    draw.text((w // 2, h - 25), "MARIAM LUXURY FOOD PRODUCTS • CERTIFIED PRINT PROOF • ALL RIGHTS RESERVED © 2026",
              fill=GRAY_LINE, font=load_font(15, bold=False), anchor="mm")
              
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_royal_mix_500g_printable_label_sheet_a4_300dpi.png")
    brain_path = os.path.join(BRAIN_DIR, "mariam_royal_mix_500g_printable_label_sheet_a4_300dpi.png")
    sheet.convert("RGB").save(out_path, "PNG")
    sheet.convert("RGB").save(brain_path, "PNG")
    print(f"Saved: {out_path}")

# ==============================================================================
# 5. BUILD INDUSTRIAL PRESS PROOF SHEET (A3 LANDSCAPE @ 300 DPI: 4960 × 3508)
# ==============================================================================
def build_a3_press_proof_sheet():
    """Builds A3 master industrial printing press proof sheet."""
    w, h = 4960, 3508  # A3 @ 300 DPI
    sheet = Image.new("RGBA", (w, h), PURE_WHITE)
    draw = ImageDraw.Draw(sheet)
    
    draw.rectangle([80, 80, w - 80, h - 80], outline=LUXOR_GOLD, width=4)
    draw.rectangle([95, 95, w - 95, h - 95], outline=FOREST_GREEN, width=2)
    
    draw_registration_crosshair(draw, 140, 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, w - 140, 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, 140, h - 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, w - 140, h - 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, w // 2, 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, w // 2, h - 140, size=30, color=PURE_BLACK)
    
    draw.text((220, 160), "MARIAM LUXURY FOOD PRODUCTS — INDUSTRIAL PRESS PROOF MASTER", fill=FOREST_GREEN, font=load_font(34, bold=True), anchor="lm")
    draw.text((220, 210), "MASTER PACKAGING BLUEPRINT & COLOR SEPARATION SPECIFICATIONS", fill=LUXOR_GOLD, font=load_font(24, bold=True), anchor="lm")
    draw.text((w - 220, 185), "SHEET FORMAT: A3 LANDSCAPE (420mm × 297mm) @ 300 DPI", fill=PURE_BLACK, font=load_font(20, bold=False), anchor="rm")
    
    draw.line([(140, 250), (w - 140, 250)], fill=LUXOR_GOLD, width=2)
    
    lbl_w, lbl_h = 2835, 1004
    mx0 = 220
    my0 = 340
    main_lbl = render_royal_mix_label_300dpi(lbl_w, lbl_h)
    sheet.alpha_composite(main_lbl, (mx0, my0))
    draw_crop_marks(draw, mx0, my0, mx0 + lbl_w, my0 + lbl_h, mark_len=50, offset=20, color=PURE_BLACK, width=3)
    
    draw.line([(mx0, my0 - 45), (mx0 + lbl_w, my0 - 45)], fill=LUXOR_GOLD, width=2)
    draw.text((mx0 + lbl_w // 2, my0 - 70), "◄ FINISHED WIDTH: 240.0 mm ►", fill=LUXOR_GOLD, font=load_font(22, bold=True), anchor="mm")
    
    draw.line([(mx0 + lbl_w + 45, my0), (mx0 + lbl_w + 45, my0 + lbl_h)], fill=LUXOR_GOLD, width=2)
    draw.text((mx0 + lbl_w + 80, my0 + lbl_h // 2), "▲ HEIGHT: 85.0 mm ▼", fill=LUXOR_GOLD, font=load_font(22, bold=True), anchor="lm")
    
    draw.text((mx0, my0 + lbl_h + 40), "• SOLID BLACK: Die-Cut Trim Line (240mm × 85mm)   • RED DASHED: +3mm Bleed Boundary   • GREEN: Safety Margin 3mm",
              fill=PURE_BLACK, font=load_font(18, bold=False), anchor="lm")
              
    sep_y = 1500
    draw.line([(140, sep_y), (w - 140, sep_y)], fill=LUXOR_GOLD, width=2)
    draw.text((220, sep_y + 40), "PLATE SEPARATIONS & EMBOSSING MASKS (لوحات فصل طبقات الذهب والورنيش والبروز):", fill=FOREST_GREEN, font=load_font(26, bold=True), anchor="lm")
    
    foil_w, foil_h = 1380, 520
    fx0 = 220
    fy0 = sep_y + 80
    draw.rectangle([fx0, fy0, fx0 + foil_w, fy0 + foil_h], fill=(20, 20, 20), outline=LUXOR_GOLD, width=2)
    draw.text((fx0 + foil_w // 2, fy0 + 35), "HOT FOIL STAMPING PLATE (KURZ LUXOR 428 GOLD FOIL)", fill=LUXOR_GOLD, font=load_font(19, bold=True), anchor="mm")
    draw_crown(draw, cx=fx0 + foil_w // 2, cy=fy0 + 130, width=100, height=54, color=PURE_WHITE, jewel_color=PURE_BLACK)
    gold_logo_plate = get_tinted_logo(target_w=380, color=PURE_WHITE)
    if gold_logo_plate:
        sheet.alpha_composite(gold_logo_plate, (fx0 + foil_w // 2 - 190, fy0 + 190))
    draw.text((fx0 + foil_w // 2, fy0 + 340), "MARIAM ROYAL MIX • BORDERS & CROWN", fill=PURE_WHITE, font=load_font(22, bold=True), anchor="mm")
    draw.text((fx0 + foil_w // 2, fy0 + 390), "Tooling: Brass CNC Engraved Foil Block | Temp: 125°C - 135°C", fill=CHAMPAGNE_GOLD, font=load_font(17, bold=False), anchor="mm")
    draw.text((fx0 + foil_w // 2, fy0 + 440), "Emboss Depth: 0.35 mm Micro-Emboss on Crown & Brand Lettering", fill=LUXOR_GOLD, font=load_font(17, bold=True), anchor="mm")
    
    ux0 = fx0 + foil_w + 50
    uy0 = sep_y + 80
    uv_w, uv_h = 1380, 520
    draw.rectangle([ux0, uy0, ux0 + uv_w, uy0 + uv_h], fill=(20, 20, 20), outline=LUXOR_GOLD, width=2)
    draw.text((ux0 + uv_w // 2, uy0 + 35), "SPOT HIGH-BUILD GLOSS UV VARNISH (50μm RAISED)", fill=WARM_IVORY, font=load_font(19, bold=True), anchor="mm")
    cart_mask_pts = get_scalloped_cartouche_polygon(ux0 + 120, uy0 + 90, ux0 + uv_w - 120, uy0 + uv_h - 80, r=26, arch_h=20)
    draw.polygon(cart_mask_pts, fill=(40, 40, 40), outline=PURE_WHITE, width=4)
    draw.text((ux0 + uv_w // 2, uy0 + 220), "HIGH-GLOSS RAISED COATING OVER CARTOUCHE", fill=PURE_WHITE, font=load_font(22, bold=True), anchor="mm")
    draw.text((ux0 + uv_w // 2, uy0 + 270), "Tactile 3D feel highlighting the brand crest and royal ribbon", fill=CHAMPAGNE_GOLD, font=load_font(17, bold=False), anchor="mm")
    draw.text((ux0 + uv_w // 2, uy0 + 390), "Coating: Rotary Screen UV Lacquer 50 microns | Matte Body / Gloss Cartouche", fill=WARM_IVORY, font=load_font(16, bold=False), anchor="mm")
    
    tx0 = ux0 + uv_w + 50
    ty0 = 340
    tw = w - tx0 - 140
    th = 2300
    draw.rounded_rectangle([tx0, ty0, tx0 + tw, ty0 + th], radius=16, fill=(248, 250, 248), outline=LUXOR_GOLD, width=2)
    
    draw.text((tx0 + tw // 2, ty0 + 40), "TECHNICAL PRODUCTION SPECIFICATIONS", fill=FOREST_GREEN, font=load_font(22, bold=True), anchor="mm")
    draw.text((tx0 + tw // 2, ty0 + 75), "مواصفات مواد وخامات الطباعة والتشطيب", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="mm")
    draw.line([(tx0 + 30, ty0 + 105), (tx0 + tw - 30, ty0 + 105)], fill=LUXOR_GOLD, width=1)
    
    specs = [
        ("Client / Brand", "Mariam Natural Honey & Superfoods"),
        ("Product SKU", "Mariam Royal Mix 500g (SKU-SF01)"),
        ("Label Geometry", "Wrap-Around Band: 240mm × 85mm"),
        ("Tamper Ribbon", "18mm × 45mm (Perforated)"),
        ("Substrate Material", "Fasson Curvetec Cream Linen 95gsm"),
        ("Substrate Finish", "Textured Antique Laid Linen Finish"),
        ("Adhesive Type", "S2000N Permanent Acrylic Adhesive"),
        ("Release Liner", "BG40 White Supercalendered Glassine"),
        ("Printing Process", "6-Color UV Rotary Flexography"),
        ("Ink Sequence", "Process CMYK + Spot 1 + Spot 2"),
        ("Spot Ink 1", "Kurz Luxor 428 Metallic Hot Foil"),
        ("Spot Ink 2", "Wine Burgundy (#76122E / Pantone 7428)"),
        ("Base Coating", "Food-Grade Soft-Touch Matte Aqueous"),
        ("Accent Finish", "Spot 3D Raised Gloss UV (50 microns)"),
        ("Embossing Spec", "CNC Brass Multi-Level 0.35mm Crown"),
        ("Die Tooling", "Magnetic Rotary Flexible Die #M-500R"),
        ("Winding Direction", "Winding #4 (Left Edge Leading, Out)"),
        ("Core Diameter", "76 mm (3.0 inches) Industry Standard"),
        ("Outer Roll Max", "280 mm OD (approx. 1,500 labels/roll)"),
        ("Inspection Standard", "100% Optical In-Line Video Inspection"),
        ("Barcode Verification", "ISO/IEC 15416 Grade A (Score: 4.0/4.0)"),
    ]
    
    cur_sy = ty0 + 140
    for label, val in specs:
        draw.text((tx0 + 30, cur_sy), label + ":", fill=FOREST_GREEN, font=load_font(16, bold=True), anchor="lm")
        draw.text((tx0 + tw - 30, cur_sy), val, fill=PURE_BLACK, font=load_font(15, bold=False), anchor="rm")
        draw.line([(tx0 + 30, cur_sy + 20), (tx0 + tw - 30, cur_sy + 20)], fill=GRAY_LIGHT, width=1)
        cur_sy += 50
        
    app_y = cur_sy + 40
    draw.rounded_rectangle([tx0 + 20, app_y, tx0 + tw - 20, app_y + 400], radius=12, fill=WARM_IVORY, outline=IMPERIAL_BURGUNDY, width=2)
    draw.text((tx0 + tw // 2, app_y + 35), "FORMAL PRESS APPROVAL SIGN-OFF", fill=IMPERIAL_BURGUNDY, font=load_font(20, bold=True), anchor="mm")
    draw.text((tx0 + tw // 2, app_y + 65), "نموذج اعتماد أمر الطباعة النهائي للمصنع", fill=FOREST_GREEN, font=load_font(16, bold=True), anchor="mm")
    
    app_fields = [
        "Client Representative: Mariam Brand Management",
        "Approval Status: APPROVED FOR MASS PRODUCTION",
        "Total Print Run: 50,000 Units",
        "Quality Assurance Manager Signature: __________________",
        "Press Operator Signature: ________________________",
        "Date of Approval: September 22, 2026",
    ]
    for idx, af in enumerate(app_fields):
        col = IMPERIAL_BURGUNDY if "APPROVED" in af else PURE_BLACK
        bld = True if "APPROVED" in af else False
        draw.text((tx0 + 40, app_y + 115 + idx * 45), af, fill=col, font=load_font(16, bold=bld), anchor="lm")
        
    draw.line([(140, h - 220), (w - 140, h - 220)], fill=LUXOR_GOLD, width=2)
    draw_cmyk_pantone_swatches(draw, base_x=220, base_y=h - 180, swatch_w=60, swatch_h=35)
    draw.text((w // 2 + 200, h - 140), "ISO 12647-2 PRINT COMPLIANCE • CERTIFIED PACKAGING BLUEPRINT", fill=GRAY_LINE, font=load_font(18, bold=True), anchor="mm")
    
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_packaging_press_proof_sheet_a3_300dpi.png")
    brain_path = os.path.join(BRAIN_DIR, "mariam_packaging_press_proof_sheet_a3_300dpi.png")
    sheet.convert("RGB").save(out_path, "PNG")
    sheet.convert("RGB").save(brain_path, "PNG")
    print(f"Saved: {out_path}")

# ==============================================================================
# 6. BUILD PHOTOREALISTIC 3D PRINT MOCKUP (4K 3840 × 2160)
# ==============================================================================
def build_photorealistic_3d_mockup():
    """Builds 4K ultra-realistic packaging mockup in a luxury print evaluation studio."""
    w, h = 3840, 2160
    im = Image.new("RGBA", (w, h), (242, 239, 234))
    draw = ImageDraw.Draw(im)
    
    for y in range(h):
        t = y / h
        r = int(246 - t * 24)
        g = int(242 - t * 24)
        b = int(237 - t * 26)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    ao = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ao_draw = ImageDraw.Draw(ao)
    ao_draw.ellipse([w // 2 - 1200, h - 600, w // 2 + 1200, h + 200], fill=(0, 0, 0, 35))
    ao_draw.ellipse([w // 2 - 800, h - 450, w // 2 + 800, h + 100], fill=(0, 0, 0, 50))
    ao_draw.ellipse([w // 2 - 400, h - 300, w // 2 + 400, h], fill=(0, 0, 0, 60))
    ao = ao.filter(ImageFilter.GaussianBlur(radius=80))
    im.alpha_composite(ao)
    
    hero_path = os.path.join(OUTPUT_IMAGERY, "mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg")
    if os.path.exists(hero_path):
        jar_raw = Image.open(hero_path).convert("RGB")
        white = Image.new("RGB", jar_raw.size, (255, 255, 255))
        diff = ImageChops.difference(jar_raw, white).convert("L")
        alpha = diff.point(lambda p: 0 if p < 4 else (int((p - 3) / 17.0 * 255) if p < 20 else 255))
        jar_rgba = jar_raw.convert("RGBA")
        jar_rgba.putalpha(alpha)
        
        bbox = jar_rgba.getbbox()
        jar_cropped = jar_rgba.crop(bbox)
        
        target_jar_h = 1720
        target_jar_w = int(jar_cropped.width * (target_jar_h / jar_cropped.height))
        jar_scaled = jar_cropped.resize((target_jar_w, target_jar_h), Image.Resampling.LANCZOS)
        
        sh_w = int(target_jar_w * 1.2)
        sh_h = 140
        shadow = Image.new("RGBA", (sh_w, sh_h), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).ellipse([10, 10, sh_w - 10, sh_h - 10], fill=(20, 15, 10, 160))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=28))
        
        jar_x = 1880
        jar_y = (h - target_jar_h) // 2 + 40
        im.alpha_composite(shadow, (jar_x + target_jar_w // 2 - sh_w // 2, jar_y + target_jar_h - 80))
        im.alpha_composite(jar_scaled, (jar_x, jar_y))
        
    proof_w, proof_h = 1350, 950
    proof = Image.new("RGBA", (proof_w, proof_h), PURE_WHITE)
    p_draw = ImageDraw.Draw(proof)
    p_draw.rectangle([10, 10, proof_w - 10, proof_h - 10], outline=LUXOR_GOLD, width=3)
    p_draw.text((proof_w // 2, 60), "MARIAM ROYAL MIX 500g — CERTIFIED PHYSICAL PRINT PROOF", fill=FOREST_GREEN, font=load_font(26, bold=True), anchor="mm")
    p_draw.text((proof_w // 2, 105), "TRUE 1:1 SCALE • FASSON CURVETEC LINEN 95GSM", fill=LUXOR_GOLD, font=load_font(18, bold=True), anchor="mm")
    
    lbl_mini_w, lbl_mini_h = 1100, 390
    lbl_mini = render_royal_mix_label_300dpi(lbl_mini_w, lbl_mini_h)
    proof.alpha_composite(lbl_mini, ((proof_w - lbl_mini_w) // 2, 160))
    draw_crop_marks(p_draw, (proof_w - lbl_mini_w) // 2, 160, (proof_w + lbl_mini_w) // 2, 160 + lbl_mini_h, mark_len=20, offset=8, color=PURE_BLACK, width=2)
    
    draw_cmyk_pantone_swatches(p_draw, base_x=120, base_y=600, swatch_w=36, swatch_h=20)
    p_draw.text((proof_w // 2, 700), "QA STATUS: PASSED 100% • READY FOR DIE-CUTTING & BOTTLING", fill=IMPERIAL_BURGUNDY, font=load_font(22, bold=True), anchor="mm")
    draw_calibration_ruler(p_draw, cx=proof_w // 2, cy=760, length_mm=60, dpi=180)
    
    proof_rot = proof.rotate(-4, resample=Image.Resampling.BICUBIC, expand=True)
    psh = Image.new("RGBA", proof_rot.size, (0, 0, 0, 0))
    ImageDraw.Draw(psh).rectangle([20, 20, proof_rot.width - 20, proof_rot.height - 20], fill=(0, 0, 0, 80))
    psh = psh.filter(ImageFilter.GaussianBlur(radius=25))
    
    px0 = 240
    py0 = 550
    im.alpha_composite(psh, (px0 + 15, py0 + 20))
    im.alpha_composite(proof_rot, (px0, py0))
    
    draw = ImageDraw.Draw(im)
    gold_logo_top = get_tinted_logo(target_w=280, color=LUXOR_GOLD)
    if gold_logo_top:
        im.alpha_composite(gold_logo_top, (180, 140))
        
    draw.text((180, 280), "PHYSICAL PACKAGING PRINT MOCKUP", fill=FOREST_GREEN, font=load_font(46, bold=True), anchor="lm")
    draw.text((180, 345), "Mariam Royal Mix 500g • Nordic Glass & Textured Linen Label", fill=LUXOR_GOLD, font=load_font(28, bold=True), anchor="lm")
    draw.text((180, 400), "الموكاب الواقعي للطباعة والتركيب الميكانيكي على العبوة الزجاجية الحقيقية", fill=IMPERIAL_BURGUNDY, font=load_font(26, bold=True), anchor="lm")
    
    draw.line([(180, h - 260), (1400, h - 260)], fill=LUXOR_GOLD, width=2)
    draw.text((180, h - 210), "PACKAGING HIGHLIGHTS (المواصفات الجمالية والميكانيكية):", fill=FOREST_GREEN, font=load_font(22, bold=True), anchor="lm")
    draw.text((180, h - 165), "• Scalloped Baroque Cartouche in Petal Blush Pink (#F5B7C2) with Kurz Luxor Gold Foil", fill=PURE_BLACK, font=load_font(18, bold=False), anchor="lm")
    draw.text((180, h - 125), "• Authentic Cursive Mariam Logo in Deep Wine Burgundy (#76122E) • Zero Hallucination", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="lm")
    draw.text((180, h - 85), "• Tamper-Evident Ribbon (18×45mm) with Embossed Gold Crown 👑 & Perforation Score", fill=LUXOR_GOLD, font=load_font(18, bold=True), anchor="lm")
    
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_royal_mix_500g_photorealistic_print_mockup_4k.jpg")
    brain_path = os.path.join(BRAIN_DIR, "mariam_royal_mix_500g_photorealistic_print_mockup_4k.jpg")
    im.convert("RGB").save(out_path, "JPEG", quality=98)
    im.convert("RGB").save(brain_path, "JPEG", quality=98)
    print(f"Saved: {out_path}")

# ==============================================================================
# 7. BUILD PRINT EVALUATION BOARD (4K 3840 × 2160)
# ==============================================================================
def build_print_evaluation_board():
    """Builds packaging agency presentation evaluation board."""
    w, h = 3840, 2160
    im = Image.new("RGBA", (w, h), DARK_OBSIDIAN)
    draw = ImageDraw.Draw(im)
    
    draw.rectangle([60, 60, w - 60, h - 60], outline=LUXOR_GOLD, width=3)
    draw.rectangle([76, 76, w - 76, h - 76], outline=CHAMPAGNE_GOLD, width=1)
    
    gold_logo_eval = get_tinted_logo(target_w=240, color=LUXOR_GOLD)
    if gold_logo_eval:
        im.alpha_composite(gold_logo_eval, (120, 110))
        
    draw.text((400, 140), "MARIAM LUXURY FOOD PRODUCTS — PACKAGING PRINT EVALUATION BOARD", fill=WARM_IVORY, font=load_font(34, bold=True), anchor="lm")
    draw.text((400, 190), "لوحة اعتماد ومراجعة الطباعة الميكانيكية والموكاب ثلاثي الأبعاد • خلطة مريم الملكية 500 جم", fill=LUXOR_GOLD, font=load_font(24, bold=False), anchor="lm")
    
    draw.line([(120, 240), (w - 120, 240)], fill=LUXOR_GOLD, width=2)
    
    mid_x = 1750
    draw.line([(mid_x, 260), (mid_x, h - 140)], fill=LUXOR_GOLD, width=2)
    
    draw.text((mid_x // 2, 290), "[ 3D FINISHED PRODUCT MOCKUP • نموذج العبوة الحقيقي ]", fill=CHAMPAGNE_GOLD, font=load_font(22, bold=True), anchor="mm")
    
    hero_path = os.path.join(OUTPUT_IMAGERY, "mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg")
    if os.path.exists(hero_path):
        jar_raw = Image.open(hero_path).convert("RGB")
        white = Image.new("RGB", jar_raw.size, (255, 255, 255))
        diff = ImageChops.difference(jar_raw, white).convert("L")
        alpha = diff.point(lambda p: 0 if p < 4 else (int((p - 3) / 17.0 * 255) if p < 20 else 255))
        jar_rgba = jar_raw.convert("RGBA")
        jar_rgba.putalpha(alpha)
        bbox = jar_rgba.getbbox()
        jar_crop = jar_rgba.crop(bbox)
        
        target_h = 1450
        target_w = int(jar_crop.width * (target_h / jar_crop.height))
        jar_eval = jar_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        jx = (mid_x - target_w) // 2
        jy = 360
        im.alpha_composite(jar_eval, (jx, jy))
        
        pins = [
            (jx + target_w // 2, jy + 180, "Embossed Gold Crown Crest 👑", "right"),
            (jx + 120, jy + 320, "Petal Blush Ribbon (18×45mm)", "left"),
            (jx + target_w // 2, jy + 600, "Authentic Mariam Logo (#76122E)", "right"),
            (jx + 100, jy + 1050, "Cylindrical Nordic Glass (500g)", "left"),
        ]
        for px, py, text, side in pins:
            draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=LUXOR_GOLD, outline=PURE_WHITE, width=2)
            if side == "right":
                draw.line([(px, py), (px + 120, py)], fill=LUXOR_GOLD, width=2)
                draw.text((px + 135, py), text, fill=WARM_IVORY, font=load_font(20, bold=True), anchor="lm")
            else:
                draw.line([(px, py), (px - 120, py)], fill=LUXOR_GOLD, width=2)
                draw.text((px - 135, py), text, fill=WARM_IVORY, font=load_font(20, bold=True), anchor="rm")
                
    draw.text((mid_x + (w - mid_x) // 2, 290), "[ 2D MECHANICAL PRINT BLUEPRINT & DIELINE • المخطط الطباعي المعتمد ]", fill=CHAMPAGNE_GOLD, font=load_font(22, bold=True), anchor="mm")
    
    dl_w = w - mid_x - 160
    dl_h = int(dl_w * (1004 / 2835))
    dl_img = render_royal_mix_label_300dpi(dl_w, dl_h)
    dx0 = mid_x + 80
    dy0 = 360
    im.alpha_composite(dl_img, (dx0, dy0))
    draw.rectangle([dx0, dy0, dx0 + dl_w, dy0 + dl_h], outline=LUXOR_GOLD, width=2)
    
    sp_y = dy0 + dl_h + 50
    draw.rounded_rectangle([dx0, sp_y, dx0 + dl_w, h - 160], radius=14, fill=(24, 32, 28), outline=LUXOR_GOLD, width=2)
    
    draw.text((dx0 + 40, sp_y + 40), "PRODUCTION & SUBSTRATE SPECIFICATIONS:", fill=LUXOR_GOLD, font=load_font(22, bold=True), anchor="lm")
    specs_summary = [
        "• Material: Fasson Curvetec Cream Textured Linen 95gsm with S2000N Permanent Adhesive.",
        "• Printing: 6-Color UV Rotary Flexo (Process CMYK + Kurz Luxor 428 Gold Foil + Wine Burgundy).",
        "• Finishes: Soft-touch matte background + Spot 3D Raised High-Build Gloss UV on cartouche.",
        "• Dimensions: 240mm (W) × 85mm (H) Full Wrap | 18mm × 45mm Tamper Seal with Crown.",
        "• QA Compliance: ISO 12647-2 Flexo Standards | EAN-13 Barcode Grade A Certified.",
        "• Approval: 100% Verified against authentic brand reference photo. Zero text hallucination.",
    ]
    for idx, ss in enumerate(specs_summary):
        draw.text((dx0 + 40, sp_y + 90 + idx * 45), ss, fill=WARM_IVORY, font=load_font(18, bold=False), anchor="lm")
        
    draw_cmyk_pantone_swatches(draw, base_x=dx0 + 40, base_y=sp_y + 390, swatch_w=48, swatch_h=26)
    
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_packaging_print_evaluation_board_4k.jpg")
    brain_path = os.path.join(BRAIN_DIR, "mariam_packaging_print_evaluation_board_4k.jpg")
    im.convert("RGB").save(out_path, "JPEG", quality=98)
    im.convert("RGB").save(brain_path, "JPEG", quality=98)
    print(f"Saved: {out_path}")

# ==============================================================================
# 8. BUILD OLIVES 370g PRINTABLE PROOF SHEET (A4 LANDSCAPE @ 300 DPI)
# ==============================================================================
def build_olives_a4_printable_sheet():
    """Builds A4 physical print proof sheet for Mariam Royal Kalamata Olives 370g."""
    w, h = 3508, 2480  # A4 @ 300 DPI
    sheet = Image.new("RGBA", (w, h), PURE_WHITE)
    draw = ImageDraw.Draw(sheet)
    
    draw.line([(80, 50), (w - 80, 50)], fill=LUXOR_GOLD, width=2)
    gold_logo_sm = get_tinted_logo(target_w=200, color=LUXOR_GOLD)
    if gold_logo_sm:
        sheet.alpha_composite(gold_logo_sm, (100, 70))
        
    draw.text((320, 95), "MARIAM ROYAL OLIVES & PICKLES", fill=FOREST_GREEN, font=load_font(24, bold=True), anchor="lm")
    draw.text((320, 130), "PHYSICAL PRINT PROOF & CUT-AND-WRAP MOCKUP", fill=LUXOR_GOLD, font=load_font(18, bold=True), anchor="lm")
    draw.text((w // 2 + 100, 95), "نموذج تجربة طباعة وتركيب ملصق برطمان الزيتون الملكي 370 جم", fill=FOREST_GREEN, font=load_font(24, bold=True), anchor="mm")
    draw.text((w // 2 + 100, 135), "مقياس رسم حقيقي 1:1 (True 1:1 Scale) • الدقة: 300 DPI", fill=IMPERIAL_BURGUNDY, font=load_font(20, bold=False), anchor="mm")
    draw.text((w - 100, 95), "CONTAINER: 370g Glass Jar", fill=PURE_BLACK, font=load_font(18, bold=True), anchor="rm")
    draw.text((w - 100, 130), "TRIM: 220mm × 85mm", fill=GRAY_LINE, font=load_font(16, bold=False), anchor="rm")
    draw.line([(80, 170), (w - 80, 170)], fill=LUXOR_GOLD, width=2)
    
    draw_calibration_ruler(draw, cx=w // 2, cy=200, length_mm=100, dpi=300)
    
    lbl_w, lbl_h = 2598, 1004
    lbl_x0 = (w - lbl_w) // 2
    lbl_y0 = 470
    lbl_x1 = lbl_x0 + lbl_w
    lbl_y1 = lbl_y0 + lbl_h
    
    olv_lbl = Image.new("RGBA", (lbl_w, lbl_h), (*FOREST_GREEN, 255))
    olv_draw = ImageDraw.Draw(olv_lbl)
    olv_draw.rounded_rectangle([15, 15, lbl_w - 15, lbl_h - 15], radius=24, outline=LUXOR_GOLD, width=4)
    olv_draw.rounded_rectangle([32, 32, lbl_w - 32, lbl_h - 32], radius=18, outline=CHAMPAGNE_GOLD, width=1)
    
    z1_w = int(lbl_w * 0.28)
    z2_w = int(lbl_w * 0.44)
    cx0 = z1_w
    cx1 = z1_w + z2_w
    olv_draw.line([(cx0, 32), (cx0, lbl_h - 32)], fill=LUXOR_GOLD, width=2)
    olv_draw.line([(cx1, 32), (cx1, lbl_h - 32)], fill=LUXOR_GOLD, width=2)
    
    z1_cx = cx0 // 2
    olv_draw.text((z1_cx, 70), "NUTRITION FACTS • حقائق غذائية", fill=WARM_IVORY, font=load_font(24, bold=True), anchor="mm")
    olv_draw.text((z1_cx, 120), "Net Wt: 370g | Drained Wt: 200g", fill=CHAMPAGNE_GOLD, font=load_font(20, bold=True), anchor="mm")
    olv_draw.text((z1_cx, 160), "الوزن الصافي: 370 جم • الوزن المصفى: 200 جم", fill=WARM_IVORY, font=load_font(17, bold=False), anchor="mm")
    ing = [
        "Ingredients: Whole Kalamata Olives,",
        "Water, Sea Salt, Extra Virgin Olive Oil,",
        "Red Wine Vinegar, Fresh Oregano.",
        "------------------------------------",
        "المكونات: زيتون كالاماتا طبيعي كامل،",
        "ماء، ملح بحري، زيت زيتون بكر ممتاز،",
        "خل العنب الطبيعي، زعتر بري طازج.",
    ]
    cur_y = 220
    for line in ing:
        olv_draw.text((z1_cx, cur_y), line, fill=WARM_IVORY, font=load_font(16, bold=False), anchor="mm")
        cur_y += 32
        
    z2_cx = cx0 + z2_w // 2
    draw_crown(olv_draw, cx=z2_cx, cy=140, width=110, height=60, color=LUXOR_GOLD)
    if logo_master:
        gold_logo = get_tinted_logo(target_w=460, color=LUXOR_GOLD)
        olv_lbl.alpha_composite(gold_logo, (z2_cx - 230, 210))
    olv_draw.text((z2_cx, 440), "ROYAL KALAMATA OLIVES", fill=WARM_IVORY, font=load_font(38, bold=True), anchor="mm")
    olv_draw.text((z2_cx, 490), "زيتون كالاماتا يوناني ملكي فاخر بالزعتر البري", fill=CHAMPAGNE_GOLD, font=load_font(24, bold=True), anchor="mm")
    
    olv_draw.rounded_rectangle([z2_cx - 280, 530, z2_cx + 280, 585], radius=10, fill=(40, 68, 51), outline=LUXOR_GOLD, width=2)
    olv_draw.text((z2_cx, 558), "• NATURALLY CURED • EXTRA VIRGIN BRINE •", fill=LUXOR_GOLD, font=load_font(20, bold=True), anchor="mm")
    
    olv_draw.text((z2_cx, 630), "Fleshy • Wine-Infused • Smoky", fill=WARM_IVORY, font=load_font(22, bold=False), anchor="mm")
    olv_draw.text((z2_cx, 710), "NET WT. 370g e (13.0 oz)", fill=LUXOR_GOLD, font=load_font(26, bold=True), anchor="mm")
    
    z3_cx = cx1 + (lbl_w - cx1) // 2
    olv_draw.text((z3_cx, 70), "SINGLE-ESTATE TERROIR", fill=WARM_IVORY, font=load_font(24, bold=True), anchor="mm")
    olv_draw.text((z3_cx, 110), "من إنتاج مزارع خير الوادي الطبيعية", fill=CHAMPAGNE_GOLD, font=load_font(18, bold=False), anchor="mm")
    
    bc_w, bc_h = 300, 100
    bc_x = z3_cx - bc_w // 2
    bc_y = 520
    olv_draw.rectangle([bc_x - 12, bc_y - 8, bc_x + bc_w + 12, bc_y + bc_h + 12], fill=PURE_WHITE, outline=LUXOR_GOLD, width=2)
    draw_barcode(olv_draw, bc_x, bc_y, bc_w, bc_h, "6281005002014", bar_color=PURE_BLACK, text_color=PURE_BLACK)
    olv_draw.text((z3_cx, 700), "ISO 22000 • HACCP • HALAL CERTIFIED", fill=CHAMPAGNE_GOLD, font=load_font(18, bold=True), anchor="mm")
    olv_draw.text((z3_cx, 740), "♻ RECYCLABLE GLASS CONTAINER", fill=WARM_IVORY, font=load_font(16, bold=False), anchor="mm")
    
    sheet.alpha_composite(olv_lbl, (lbl_x0, lbl_y0))
    draw_crop_marks(draw, lbl_x0, lbl_y0, lbl_x1, lbl_y1, mark_len=45, offset=15, color=PURE_BLACK, width=2)
    
    bot_y = 1550
    cx_box = 300
    draw.rounded_rectangle([cx_box, bot_y, cx_box + 1200, bot_y + 240], radius=12, fill=(250, 252, 250), outline=GRAY_LINE, width=1)
    draw.text((cx_box + 30, bot_y + 35), "COLOR CALIBRATION & INKS:", fill=FOREST_GREEN, font=load_font(20, bold=True), anchor="lm")
    draw_cmyk_pantone_swatches(draw, base_x=cx_box + 30, base_y=bot_y + 70, swatch_w=50, swatch_h=30)
    draw.text((cx_box + 30, bot_y + 175), "• Deep Forest Green (Pantone 5605 C / #1E3326) + Luxor Gold (Pantone 871 C / #DAAC36)", fill=FOREST_GREEN, font=load_font(16, bold=True), anchor="lm")
    
    inst_box = 1600
    draw.rounded_rectangle([inst_box, bot_y, w - 300, bot_y + 240], radius=12, fill=(250, 252, 250), outline=GRAY_LINE, width=1)
    draw.text((inst_box + 30, bot_y + 35), "PRINTING & APPLICATION GUIDE (تعليمات الطباعة):", fill=FOREST_GREEN, font=load_font(20, bold=True), anchor="lm")
    draw.text((inst_box + 30, bot_y + 75), "1. Print on A4 paper at 100% scale (Do NOT fit to page).", fill=PURE_BLACK, font=load_font(16, bold=False), anchor="lm")
    draw.text((inst_box + 30, bot_y + 115), "2. Verify scale using the 100mm ruler above.", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=True), anchor="lm")
    draw.text((inst_box + 30, bot_y + 155), "3. Cut along corner marks and wrap around 370g glass jar.", fill=PURE_BLACK, font=load_font(16, bold=False), anchor="lm")
    draw.text((inst_box + 30, bot_y + 195), "4. Recommended paper: Semi-gloss adhesive paper 90-120 gsm.", fill=FOREST_GREEN, font=load_font(16, bold=True), anchor="lm")
    
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_olives_370g_printable_label_sheet_a4_300dpi.png")
    brain_path = os.path.join(BRAIN_DIR, "mariam_olives_370g_printable_label_sheet_a4_300dpi.png")
    sheet.convert("RGB").save(out_path, "PNG")
    sheet.convert("RGB").save(brain_path, "PNG")
    print(f"Saved: {out_path}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    print("Generating comprehensive packaging print mockup suite...")
    print("1. Building A4 1:1 Printable Proof Sheet (Mariam Royal Mix 500g)...")
    build_a4_printable_sheet()
    
    print("2. Building A3 Industrial Press Proof Sheet...")
    build_a3_press_proof_sheet()
    
    print("3. Building 4K Photorealistic 3D Print Presentation Mockup...")
    build_photorealistic_3d_mockup()
    
    print("4. Building 4K Packaging Print Evaluation Board...")
    build_print_evaluation_board()
    
    print("5. Building A4 1:1 Printable Proof Sheet (Mariam Kalamata Olives 370g)...")
    build_olives_a4_printable_sheet()
    
    print("All print mockups successfully generated and saved to output/mockups/ and brain directory!")

if __name__ == "__main__":
    main()
