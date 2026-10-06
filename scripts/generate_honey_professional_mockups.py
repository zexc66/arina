#!/usr/bin/env python3
"""
Mariam Luxury Brand - Professional Honey Print Mockup & Production Proof Suite
Generates world-class, agency-level packaging print mockups and 1:1 physical test sheets
specifically dedicated to Mariam Natural Honey (Mountain Sidr 500g, Royal Mix 500g, Clover Blossom 1kg).

Outputs:
1. mariam_honey_sidr_500g_printable_label_sheet_a4_300dpi.png (A4 Landscape, 3508 × 2480 @ 300 DPI)
2. mariam_honey_royal_mix_500g_printable_label_sheet_a4_300dpi.png (A4 Landscape, 3508 × 2480 @ 300 DPI)
3. mariam_honey_clover_1kg_printable_label_sheet_a4_300dpi.png (A4 Landscape, 3508 × 2480 @ 300 DPI)
4. mariam_honey_master_press_proof_sheet_a3_300dpi.png (A3 Landscape, 4960 × 3508 @ 300 DPI)
5. mariam_honey_sidr_500g_photorealistic_print_mockup_4k.jpg (Cinema 4K, 3840 × 2160)
6. mariam_honey_royal_mix_500g_photorealistic_print_mockup_4k.jpg (Cinema 4K, 3840 × 2160)
7. mariam_honey_packaging_evaluation_board_4k.jpg (Cinema 4K, 3840 × 2160)
"""

import math
import os
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_MOCKUPS = os.path.join(BASE_DIR, "output", "mockups")
OUTPUT_IMAGERY = os.path.join(BASE_DIR, "output", "imagery")
BRAIN_DIR = "/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d"

os.makedirs(OUTPUT_MOCKUPS, exist_ok=True)
os.makedirs(OUTPUT_IMAGERY, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

# Master Brand Palette Constants - Calibrated to Authentic Reference
BLUSH_PINK = (245, 183, 194)        # #F5B7C2 (Petal Blush Pink)
BLUSH_PINK_LIGHT = (252, 222, 228)  # #FCDCE4 (Tinted Blush)
IMPERIAL_BURGUNDY = (118, 18, 46)   # #76122E (Deep Wine Burgundy)
LUXOR_GOLD = (218, 172, 54)         # #DAAC36 (Kurz Luxor 428 Gold)
WARM_IVORY = (255, 245, 247)        # #FFF5F7 (Warm Blush Ivory)
HONEY_AMBER = (226, 149, 39)        # #E29527 (Golden Honey Amber)
CHAMPAGNE_GOLD = (238, 212, 142)    # #EED48E (Champagne Foil)
DARK_BURGUNDY = (75, 12, 32)        # #4B0C20
DARK_OBSIDIAN = (18, 22, 20)        # #121614
PURE_WHITE = (255, 255, 255)
PURE_BLACK = (0, 0, 0)
GRAY_LINE = (180, 180, 180)
GRAY_LIGHT = (240, 240, 240)

# Fonts
FONT_BOLD = os.path.join(BASE_DIR, "fonts", "Tajawal-Bold.ttf")
FONT_MED = os.path.join(BASE_DIR, "fonts", "Tajawal-Medium.ttf")

def load_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_MED
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

# Logo
LOGO_GOLD_PATH = os.path.join(BASE_DIR, ("arina-logo-gold.png" if os.path.exists("arina-logo-gold.png") else "mariam-logo-gold.png"))
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
    draw.line([(x0 - offset - mark_len, y0), (x0 - offset, y0)], fill=color, width=width)
    draw.line([(x0, y0 - offset - mark_len), (x0, y0 - offset)], fill=color, width=width)
    draw.line([(x1 + offset, y0), (x1 + offset + mark_len, y0)], fill=color, width=width)
    draw.line([(x1, y0 - offset - mark_len), (x1, y0 - offset)], fill=color, width=width)
    draw.line([(x0 - offset - mark_len, y1), (x0 - offset, y1)], fill=color, width=width)
    draw.line([(x0, y1 + offset), (x0, y1 + offset + mark_len)], fill=color, width=width)
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
    draw.rectangle([x_start - 10, cy - 10, x_end + 10, cy + ruler_h + 30], fill=(252, 252, 254), outline=GRAY_LINE, width=1)
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
    note = "▲ 100 mm Physical Scale Check: Measure with physical ruler. If 100mm matches exactly, printer scale is 100% accurate. ▲"
    draw.text((cx, cy + ruler_h + 16), note, fill=IMPERIAL_BURGUNDY, font=font_sub, anchor="mm")

def draw_cmyk_pantone_swatches(draw, base_x, base_y, swatch_w=38, swatch_h=24):
    """Draws CMYK step wedges and Pantone spot color chips for honey."""
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
        (HONEY_AMBER, "Honey Amber #E29527"),
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

def draw_barcode(draw, x, y, w, h, code_text="6281005001031", bar_color=PURE_BLACK, text_color=PURE_BLACK):
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
# 1. RENDER AUTHENTIC MOUNTAIN SIDR HONEY LABEL (220mm × 85mm @ 300 DPI: 2598 × 1004)
# ==============================================================================
def render_mountain_sidr_label_300dpi(width=2598, height=1004):
    """Renders authentic Petal Blush Pink label for Mountain Sidr Honey 500g."""
    im = Image.new("RGBA", (width, height), (*BLUSH_PINK, 255))
    draw = ImageDraw.Draw(im)
    
    # Outer luxury gold border
    draw.rounded_rectangle([15, 15, width - 15, height - 15], radius=24, outline=LUXOR_GOLD, width=4)
    draw.rounded_rectangle([30, 30, width - 30, height - 30], radius=18, outline=IMPERIAL_BURGUNDY, width=1)
    
    # Zone Dividers (Left 28%, Center 44%, Right 28%)
    z1_w = int(width * 0.28)
    z2_w = int(width * 0.44)
    cx0 = z1_w
    cx1 = z1_w + z2_w
    draw.line([(cx0, 30), (cx0, height - 30)], fill=LUXOR_GOLD, width=2)
    draw.line([(cx1, 30), (cx1, height - 30)], fill=LUXOR_GOLD, width=2)
    
    # ==================== ZONE 1: NUTRITION & PURITY ====================
    z1_cx = cx0 // 2
    f_title = load_font(24, bold=True)
    f_sub = load_font(18, bold=True)
    f_sm = load_font(14, bold=False)
    
    draw.text((z1_cx, 60), "NUTRITION FACTS • الحقائق الغذائية", fill=IMPERIAL_BURGUNDY, font=f_title, anchor="mm")
    draw.text((z1_cx, 95), "100% Pure Raw Mountain Honey (Per 100g)", fill=DARK_BURGUNDY, font=f_sm, anchor="mm")
    
    box_x0, box_x1 = 45, cx0 - 45
    draw.rounded_rectangle([box_x0, 125, box_x1, 510], radius=12, fill=(255, 235, 240), outline=LUXOR_GOLD, width=1)
    draw.text((z1_cx, 155), "100% PURE INGREDIENTS / المكونات", fill=IMPERIAL_BURGUNDY, font=f_sub, anchor="mm")
    
    ing_lines = [
        "100% Raw Unpasteurized Mountain Sidr Honey",
        "Single-Floral Origin from Wild Ziziphus Spina-Christi",
        "Naturally Rich in Active Bio-Enzymes & Minerals",
        "Free from Added Sugar, Glucose, or Antibiotics",
        "------------------------------------",
        "عسل سدر جبلي بري خام نقي 100%",
        "أحادي المصدر الزهري من أشجار السدر الجبلية",
        "غني طبيعياً بالإنزيمات الحية ومضادات الأكسدة",
        "خالٍ تماماً من السكر المضاف أو البسترة الحرارية",
    ]
    cur_y = 195
    for l in ing_lines:
        col = IMPERIAL_BURGUNDY if not l.startswith("-") else LUXOR_GOLD
        draw.text((z1_cx, cur_y), l, fill=col, font=f_sm, anchor="mm")
        cur_y += 32
        
    # Purity Guarantee Badge
    draw.rounded_rectangle([box_x0, 535, box_x1, 625], radius=10, fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=1)
    draw.text((z1_cx, 560), "LAB TESTED PURITY GUARANTEE", fill=WARM_IVORY, font=load_font(17, bold=True), anchor="mm")
    draw.text((z1_cx, 595), "مفحوص مخبرياً • ضمان النقاوة المطلقة 100%", fill=CHAMPAGNE_GOLD, font=load_font(15, bold=False), anchor="mm")
    
    # Net Weight
    draw.text((z1_cx, 680), "Store at 18°C - 24°C • Do not refrigerate", fill=IMPERIAL_BURGUNDY, font=f_sm, anchor="mm")
    draw.text((z1_cx, 715), "يحفظ في درجة حرارة الغرفة ولا يوضع بالثلاجة", fill=IMPERIAL_BURGUNDY, font=f_sm, anchor="mm")
    draw.text((z1_cx, 775), "NET WEIGHT: 500g e (17.6 oz)", fill=IMPERIAL_BURGUNDY, font=load_font(28, bold=True), anchor="mm")
    draw.text((z1_cx, 815), "الوزن الصافي: 500 غرام", fill=IMPERIAL_BURGUNDY, font=load_font(22, bold=True), anchor="mm")
    
    # ==================== ZONE 2: CENTER HERO BRANDING ====================
    z2_cx = cx0 + z2_w // 2
    
    # Central Embossed Frame
    frame_w = int(z2_w * 0.88)
    frame_h = int(height * 0.86)
    fx0 = z2_cx - frame_w // 2
    fy0 = (height - frame_h) // 2
    fx1 = fx0 + frame_w
    fy1 = fy0 + frame_h
    
    pts_cart = get_scalloped_cartouche_polygon(fx0, fy0, fx1, fy1, r=int(frame_w * 0.055), arch_h=int(frame_h * 0.045))
    draw.polygon(pts_cart, fill=BLUSH_PINK, outline=LUXOR_GOLD, width=4)
    pts_inner = get_scalloped_cartouche_polygon(fx0 + 8, fy0 + 8, fx1 - 8, fy1 - 8, r=int(frame_w * 0.055) - 5, arch_h=int(frame_h * 0.045) - 3)
    draw.polygon(pts_inner, outline=LUXOR_GOLD, width=1)
    
    # 1. Crown Crest
    crown_w = 110
    crown_h = 58
    crown_cy = fy0 + 60
    draw_crown(draw, cx=z2_cx, cy=crown_cy, width=crown_w, height=crown_h, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
    
    # 2. Authentic Mariam Logo in Wine Burgundy
    burg_logo = get_tinted_logo(target_w=460, color=IMPERIAL_BURGUNDY)
    if burg_logo:
        logo_y = crown_cy + crown_h // 2 + 16
        im.alpha_composite(burg_logo, (z2_cx - burg_logo.width // 2, logo_y))
        next_y = logo_y + burg_logo.height + 16
    else:
        next_y = crown_cy + 80
        
    # 3. Descriptor
    draw.text((z2_cx, next_y), "NATURAL HONEY & SUPERFOODS", fill=IMPERIAL_BURGUNDY, font=load_font(20, bold=True), anchor="mm")
    next_y += 36
    
    # 4. Hero Title
    draw.text((z2_cx, next_y), "MOUNTAIN SIDR HONEY", fill=IMPERIAL_BURGUNDY, font=load_font(42, bold=True), anchor="mm")
    next_y += 42
    
    # 5. Arabic Subtitle
    draw.text((z2_cx, next_y), "عسل السدر الجبلي الملكي النقي • أحادي المصدر الزهري", fill=IMPERIAL_BURGUNDY, font=load_font(24, bold=True), anchor="mm")
    next_y += 48
    
    # 6. Distinction Ribbon
    rib_w = min(frame_w - 80, 680)
    rib_h = 42
    draw.rounded_rectangle([z2_cx - rib_w // 2, next_y - rib_h // 2, z2_cx + rib_w // 2, next_y + rib_h // 2],
                           radius=10, fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=2)
    draw.text((z2_cx, next_y), "• 100% RAW & UNFILTERED • SINGLE-ESTATE • HIGH ENZYMATIC •", fill=WARM_IVORY, font=load_font(18, bold=True), anchor="mm")
    next_y += 46
    
    # 7. Sensory Triad
    draw.text((z2_cx, next_y), "Rich • Velvety • Butterscotch Caramel", fill=IMPERIAL_BURGUNDY, font=load_font(22, bold=False), anchor="mm")
    next_y += 34
    
    # 8. Filigree Divider
    draw.line([(z2_cx - 90, next_y), (z2_cx - 16, next_y)], fill=LUXOR_GOLD, width=2)
    draw.line([(z2_cx + 16, next_y), (z2_cx + 90, next_y)], fill=LUXOR_GOLD, width=2)
    draw.ellipse([z2_cx - 5, next_y - 5, z2_cx + 5, next_y + 5], fill=LUXOR_GOLD)
    next_y += 36
    
    # 9. Net Weight
    draw.text((z2_cx, next_y), "NET WT. 500g e (17.6 oz)", fill=IMPERIAL_BURGUNDY, font=load_font(24, bold=True), anchor="mm")
    
    # ==================== ZONE 3: TERROIR & LOGISTICS ====================
    z3_cx = cx1 + (width - cx1) // 2
    
    draw.text((z3_cx, 60), "SINGLE-ESTATE TERROIR", fill=IMPERIAL_BURGUNDY, font=f_title, anchor="mm")
    draw.text((z3_cx, 95), "من إنتاج مزارع خير الوادي الطبيعية", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=False), anchor="mm")
    
    # Producer Crest
    draw.ellipse([z3_cx - 65, 140, z3_cx + 65, 270], outline=LUXOR_GOLD, width=3)
    draw.ellipse([z3_cx - 55, 150, z3_cx + 55, 260], outline=IMPERIAL_BURGUNDY, width=1)
    draw_crown(draw, cx=z3_cx, cy=185, width=44, height=24, color=LUXOR_GOLD)
    draw.text((z3_cx, 225), "KHAEER ALWADI", fill=IMPERIAL_BURGUNDY, font=load_font(13, bold=True), anchor="mm")
    draw.text((z3_cx, 243), "خير الوادي", fill=IMPERIAL_BURGUNDY, font=load_font(13, bold=False), anchor="mm")
    
    claims = [
        "Harvested at 2,200m Altitude in Mountain Valleys",
        "Cold-Extracted to Preserve Raw Honey Enzymes",
        "Natural Golden Amber Hue with Silky Texture",
        "Crystallization is Natural Proof of Pure Raw Honey",
        "------------------------------------",
        "جني من أعالي الجبال على ارتفاع 2,200 متر",
        "مستخلص على البارد للحفاظ على الإنزيمات الحيوية",
        "لون عنبري ذهبي فاخر وقوام حريري ناعم",
        "التبلور الطبيعي دليل قطعي على نقاوة العسل الخام",
    ]
    cur_y = 310
    for c in claims:
        draw.text((z3_cx, cur_y), c, fill=IMPERIAL_BURGUNDY, font=f_sm, anchor="mm")
        cur_y += 28
        
    # Barcode
    bc_w, bc_h = 320, 110
    bc_x = z3_cx - bc_w // 2
    bc_y = 570
    draw.rectangle([bc_x - 14, bc_y - 10, bc_x + bc_w + 14, bc_y + bc_h + 14], fill=PURE_WHITE, outline=LUXOR_GOLD, width=2)
    draw_barcode(draw, bc_x, bc_y, bc_w, bc_h, "6281005001031", bar_color=PURE_BLACK, text_color=PURE_BLACK)
    
    draw.text((z3_cx, 740), "ISO 22000 • HACCP • HALAL CERTIFIED", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="mm")
    draw.text((z3_cx, 780), "♻ RECYCLABLE GLASS CONTAINER • BATCH: SD-500-2026", fill=IMPERIAL_BURGUNDY, font=f_sm, anchor="mm")
    draw.text((z3_cx, 820), "PRODUCT OF ARABIAN HIGHLANDS • عسل طبيعي فاخر", fill=LUXOR_GOLD, font=load_font(16, bold=True), anchor="mm")
    
    return im

# ==============================================================================
# 2. BUILD A4 PRINTABLE SHEET FOR MOUNTAIN SIDR HONEY (3508 × 2480 @ 300 DPI)
# ==============================================================================
def build_sidr_honey_a4_printable_sheet():
    """Builds true 1:1 scale A4 printable sheet for Mountain Sidr Honey 500g."""
    w, h = 3508, 2480  # A4 Landscape @ 300 DPI
    sheet = Image.new("RGBA", (w, h), PURE_WHITE)
    draw = ImageDraw.Draw(sheet)
    
    # Top Border & Header
    draw.line([(80, 50), (w - 80, 50)], fill=LUXOR_GOLD, width=2)
    
    gold_logo_sm = get_tinted_logo(target_w=200, color=LUXOR_GOLD)
    if gold_logo_sm:
        sheet.alpha_composite(gold_logo_sm, (100, 70))
        
    draw.text((320, 95), "MARIAM NATURAL HONEY & SUPERFOODS", fill=IMPERIAL_BURGUNDY, font=load_font(24, bold=True), anchor="lm")
    draw.text((320, 130), "PROFESSIONAL PACKAGING PRINT PROOF (TRUE 1:1 SCALE)", fill=LUXOR_GOLD, font=load_font(18, bold=True), anchor="lm")
    
    draw.text((w // 2 + 100, 95), "نموذج تجربة طباعة وتركيب ملصق عسل السدر الجبلي الملكي 500 جم", fill=IMPERIAL_BURGUNDY, font=load_font(26, bold=True), anchor="mm")
    draw.text((w // 2 + 100, 135), "مقياس رسم حقيقي 1:1 (True 1:1 Scale) • الدقة: 300 DPI • مطابقة تامة للمرجع", fill=LUXOR_GOLD, font=load_font(20, bold=False), anchor="mm")
    
    draw.text((w - 100, 95), "CONTAINER: 500g Nordic Glass Jar", fill=PURE_BLACK, font=load_font(18, bold=True), anchor="rm")
    draw.text((w - 100, 130), "TRIM: 220mm × 85mm | Ø 85mm", fill=GRAY_LINE, font=load_font(16, bold=False), anchor="rm")
    draw.line([(80, 170), (w - 80, 170)], fill=LUXOR_GOLD, width=2)
    
    # 100mm Scale Calibration Check Ruler
    draw_calibration_ruler(draw, cx=w // 2, cy=200, length_mm=100, dpi=300)
    
    # Instructions Box
    inst_y = 310
    draw.rounded_rectangle([100, inst_y, w // 2 - 20, inst_y + 110], radius=10, fill=(255, 248, 250), outline=GRAY_LINE, width=1)
    draw.text((120, inst_y + 25), "PRINTING & CUTTING INSTRUCTIONS (English):", fill=IMPERIAL_BURGUNDY, font=load_font(17, bold=True), anchor="lm")
    draw.text((120, inst_y + 55), "1. Paper: 90-120 gsm Self-Adhesive Textured Linen Sticker Paper (Fasson Linen).", fill=PURE_BLACK, font=load_font(14, bold=False), anchor="lm")
    draw.text((120, inst_y + 85), "2. Printer Scale: 100% / Actual Size (DO NOT Fit to Page). Check 100mm ruler with desk ruler.", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=True), anchor="lm")
    
    draw.rounded_rectangle([w // 2 + 20, inst_y, w - 100, inst_y + 110], radius=10, fill=(255, 248, 250), outline=GRAY_LINE, width=1)
    draw.text((w // 2 + 40, inst_y + 25), "تعليمات الطباعة والتركيب (عربي):", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="lm")
    draw.text((w // 2 + 40, inst_y + 55), "1. خامة الورق: ورق لاصق مطفي كتان بارز (Linen Sticker Paper) 90-120 جم.", fill=PURE_BLACK, font=load_font(15, bold=False), anchor="lm")
    draw.text((w // 2 + 40, inst_y + 85), "2. المقياس: اطبع بنسبة 100% دون تصغير. تأكد من تطابق مسطرة الـ 100 مم مع المسطرة العادية.", fill=IMPERIAL_BURGUNDY, font=load_font(15, bold=True), anchor="lm")
    
    # Main Label Artwork (220mm × 85mm @ 300 DPI = 2598 × 1004 px)
    lbl_w, lbl_h = 2598, 1004
    lbl_x0 = (w - lbl_w) // 2
    lbl_y0 = 470
    lbl_x1 = lbl_x0 + lbl_w
    lbl_y1 = lbl_y0 + lbl_h
    
    sidr_lbl = render_mountain_sidr_label_300dpi(lbl_w, lbl_h)
    sheet.alpha_composite(sidr_lbl, (lbl_x0, lbl_y0))
    draw_crop_marks(draw, lbl_x0, lbl_y0, lbl_x1, lbl_y1, mark_len=45, offset=15, color=PURE_BLACK, width=2)
    
    # Cut Line Dashed Guides
    for sx in range(lbl_x0 - 15, lbl_x1 + 15, 20):
        draw.line([(sx, lbl_y0 - 15), (sx + 10, lbl_y0 - 15)], fill=GRAY_LINE, width=1)
        draw.line([(sx, lbl_y1 + 15), (sx + 10, lbl_y1 + 15)], fill=GRAY_LINE, width=1)
    for sy in range(lbl_y0 - 15, lbl_y1 + 15, 20):
        draw.line([(lbl_x0 - 15, sy), (lbl_x0 - 15, sy + 10)], fill=GRAY_LINE, width=1)
        draw.line([(lbl_x1 + 15, sy), (lbl_x1 + 15, sy + 10)], fill=GRAY_LINE, width=1)
        
    draw.text((lbl_x0 + 40, lbl_y0 - 30), "✂ CUT ALONG DASHED LINE / خط القص الخارجي ✂", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="lm")
    draw.text((lbl_x1 - 40, lbl_y0 - 30), "FINISHED TRIM: 220mm × 85mm", fill=LUXOR_GOLD, font=load_font(16, bold=True), anchor="rm")
    
    # Bottom Row: Tamper Ribbon + Cap Seal + Swatches + Instructions
    bot_y = 1530
    
    # 1. Tamper Ribbon (18mm × 45mm = 213 × 531 px)
    from generate_print_mockups import render_tamper_ribbon_300dpi, render_lid_seal_300dpi
    ribbon_img = render_tamper_ribbon_300dpi(213, 531)
    rx0 = 240
    ry0 = bot_y + 110
    sheet.alpha_composite(ribbon_img, (rx0, ry0))
    draw_crop_marks(draw, rx0, ry0, rx0 + 213, ry0 + 531, mark_len=25, offset=10, color=PURE_BLACK, width=2)
    draw.text((rx0 + 106, ry0 - 25), "TAMPER SEAL (18×45mm)", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="mm")
    draw.text((rx0 + 106, ry0 + 531 + 25), "شريط إحكام الغطاء بالتاج", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=False), anchor="mm")
    
    # 2. Circular Lid Seal (Ø 60mm)
    lid_seal = render_lid_seal_300dpi(640)
    lx0 = 600
    ly0 = bot_y + 60
    sheet.alpha_composite(lid_seal, (lx0, ly0))
    draw.text((lx0 + 320, ly0 - 20), "CAP TOP SEAL (Ø 60mm)", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="mm")
    draw.text((lx0 + 320, ly0 + 640 + 25), "ملصق قمة الغطاء الذهبي", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=False), anchor="mm")
    
    # 3. Color Swatches
    cx_box = 1420
    cy_box = bot_y + 80
    draw.rounded_rectangle([cx_box, cy_box, cx_box + 900, cy_box + 260], radius=12, fill=(255, 252, 254), outline=GRAY_LINE, width=1)
    draw.text((cx_box + 30, cy_box + 35), "HONEY LINE MASTER COLOR PALETTE & PRESS CONTROL:", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="lm")
    draw_cmyk_pantone_swatches(draw, base_x=cx_box + 30, base_y=cy_box + 70, swatch_w=48, swatch_h=28)
    draw.text((cx_box + 30, cy_box + 175), "• Substrate Shade: Petal Blush Pink (#F5B7C2 / Pantone 496 C)", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=True), anchor="lm")
    draw.text((cx_box + 30, cy_box + 205), "• Typography Color: Deep Wine Burgundy (#76122E / Pantone 7428 C)", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=True), anchor="lm")
    draw.text((cx_box + 30, cy_box + 235), "• Metallic Embellishment: Kurz Luxor 428 Metallic Gold Foil", fill=LUXOR_GOLD, font=load_font(14, bold=True), anchor="lm")
    
    # 4. Assembly & Inspection Guide
    gx_box = 2440
    gy_box = bot_y + 80
    draw.rounded_rectangle([gx_box, gy_box, w - 100, gy_box + 260], radius=12, fill=(255, 252, 254), outline=GRAY_LINE, width=1)
    draw.text((gx_box + 30, gy_box + 35), "APPLICATION ON HONEY JAR (طريقة التركيب):", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="lm")
    guide_steps = [
        "1. Cut main label along crop lines (220mm × 85mm).",
        "2. Center the Mountain Sidr Cartouche on jar front.",
        "3. Wrap tightly around standard 500g glass jar.",
        "4. Place round seal on polished gold lid center.",
        "5. Adhere tamper ribbon vertically over lid and glass.",
    ]
    for idx, s in enumerate(guide_steps):
        draw.text((gx_box + 30, gy_box + 75 + idx * 32), s, fill=PURE_BLACK, font=load_font(15, bold=False), anchor="lm")
        
    draw_registration_crosshair(draw, 60, 60, size=24, color=LUXOR_GOLD)
    draw_registration_crosshair(draw, w - 60, 60, size=24, color=LUXOR_GOLD)
    draw_registration_crosshair(draw, 60, h - 60, size=24, color=LUXOR_GOLD)
    draw_registration_crosshair(draw, w - 60, h - 60, size=24, color=LUXOR_GOLD)
    
    draw.line([(80, h - 50), (w - 80, h - 50)], fill=LUXOR_GOLD, width=2)
    draw.text((w // 2, h - 25), "MARIAM NATURAL HONEY & SUPERFOODS • PROFESSIONAL PRINT PROOF • ALL RIGHTS RESERVED © 2026",
              fill=GRAY_LINE, font=load_font(15, bold=False), anchor="mm")
              
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_honey_sidr_500g_printable_label_sheet_a4_300dpi.png")
    brain_path = os.path.join(BRAIN_DIR, "mariam_honey_sidr_500g_printable_label_sheet_a4_300dpi.png")
    sheet.convert("RGB").save(out_path, "PNG")
    sheet.convert("RGB").save(brain_path, "PNG")
    print(f"Saved: {out_path}")

# ==============================================================================
# 3. BUILD AUTHENTIC ROYAL MIX 500g PRINTABLE SHEET (SOLID PINK / NO GREEN)
# ==============================================================================
def build_royal_mix_pink_a4_printable_sheet():
    """Builds authentic 100% Petal Blush Pink A4 printable sheet for Royal Mix 500g."""
    w, h = 3508, 2480  # A4 @ 300 DPI
    sheet = Image.new("RGBA", (w, h), PURE_WHITE)
    draw = ImageDraw.Draw(sheet)
    
    draw.line([(80, 50), (w - 80, 50)], fill=LUXOR_GOLD, width=2)
    
    gold_logo_sm = get_tinted_logo(target_w=200, color=LUXOR_GOLD)
    if gold_logo_sm:
        sheet.alpha_composite(gold_logo_sm, (100, 70))
        
    draw.text((320, 95), "MARIAM NATURAL HONEY & SUPERFOODS", fill=IMPERIAL_BURGUNDY, font=load_font(24, bold=True), anchor="lm")
    draw.text((320, 130), "FLAGSHIP SUPERFOOD PRINT PROOF (TRUE 1:1 SCALE)", fill=LUXOR_GOLD, font=load_font(18, bold=True), anchor="lm")
    
    draw.text((w // 2 + 100, 95), "نموذج تجربة طباعة وتركيب ملصق خلطة مريم الملكية 500 جم الفاخرة", fill=IMPERIAL_BURGUNDY, font=load_font(26, bold=True), anchor="mm")
    draw.text((w // 2 + 100, 135), "البصمة اللونية الأصلية (Petal Blush Pink #F5B7C2) • الدقة: 300 DPI", fill=LUXOR_GOLD, font=load_font(20, bold=False), anchor="mm")
    
    draw.text((w - 100, 95), "CONTAINER: 500g Wide Nordic Jar", fill=PURE_BLACK, font=load_font(18, bold=True), anchor="rm")
    draw.text((w - 100, 130), "TRIM: 240mm × 85mm", fill=GRAY_LINE, font=load_font(16, bold=False), anchor="rm")
    draw.line([(80, 170), (w - 80, 170)], fill=LUXOR_GOLD, width=2)
    
    draw_calibration_ruler(draw, cx=w // 2, cy=200, length_mm=100, dpi=300)
    
    inst_y = 310
    draw.rounded_rectangle([100, inst_y, w // 2 - 20, inst_y + 110], radius=10, fill=(255, 248, 250), outline=GRAY_LINE, width=1)
    draw.text((120, inst_y + 25), "PRINTING & APPLICATION INSTRUCTIONS:", fill=IMPERIAL_BURGUNDY, font=load_font(17, bold=True), anchor="lm")
    draw.text((120, inst_y + 55), "1. Paper: Fasson Curvetec Cream Textured Linen Sticker Paper 90-120 gsm.", fill=PURE_BLACK, font=load_font(14, bold=False), anchor="lm")
    draw.text((120, inst_y + 85), "2. Scale: 100% / Actual Size. Verify with 100mm ruler before cutting.", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=True), anchor="lm")
    
    draw.rounded_rectangle([w // 2 + 20, inst_y, w - 100, inst_y + 110], radius=10, fill=(255, 248, 250), outline=GRAY_LINE, width=1)
    draw.text((w // 2 + 40, inst_y + 25), "تعليمات الطباعة والتركيب (عربي):", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="lm")
    draw.text((w // 2 + 40, inst_y + 55), "1. خامة الورق: ورق لاصق بملمس الكتان البارز بلون الوردي البتلي الناعم.", fill=PURE_BLACK, font=load_font(15, bold=False), anchor="lm")
    draw.text((w // 2 + 40, inst_y + 85), "2. المقياس: اطبع بنسبة 100% دون تصغير لمطابقة أبعاد البرطمان بدقة تامة.", fill=IMPERIAL_BURGUNDY, font=load_font(15, bold=True), anchor="lm")
    
    # Render Royal Mix in pure Petal Blush Pink background (#F5B7C2) - ZERO GREEN!
    lbl_w, lbl_h = 2835, 1004
    lbl_x0 = (w - lbl_w) // 2
    lbl_y0 = 470
    lbl_x1 = lbl_x0 + lbl_w
    lbl_y1 = lbl_y0 + lbl_h
    
    royal_lbl = Image.new("RGBA", (lbl_w, lbl_h), (*BLUSH_PINK, 255))
    r_draw = ImageDraw.Draw(royal_lbl)
    
    # Outer luxury gold border
    r_draw.rounded_rectangle([15, 15, lbl_w - 15, lbl_h - 15], radius=24, outline=LUXOR_GOLD, width=4)
    r_draw.rounded_rectangle([30, 30, lbl_w - 30, lbl_h - 30], radius=18, outline=IMPERIAL_BURGUNDY, width=1)
    
    z1_w = int(lbl_w * 0.27)
    z2_w = int(lbl_w * 0.46)
    cx0 = z1_w
    cx1 = z1_w + z2_w
    r_draw.line([(cx0, 30), (cx0, lbl_h - 30)], fill=LUXOR_GOLD, width=2)
    r_draw.line([(cx1, 30), (cx1, lbl_h - 30)], fill=LUXOR_GOLD, width=2)
    
    # Zone 1
    z1_cx = cx0 // 2
    r_draw.text((z1_cx, 60), "NUTRITION FACTS • الحقائق الغذائية", fill=IMPERIAL_BURGUNDY, font=load_font(26, bold=True), anchor="mm")
    r_draw.text((z1_cx, 95), "Per 100g: 340 kcal | Protein 4.8g | Carbs 72g", fill=DARK_BURGUNDY, font=load_font(14, bold=False), anchor="mm")
    
    box_x0, box_x1 = 50, cx0 - 50
    r_draw.rounded_rectangle([box_x0, 125, box_x1, 520], radius=12, fill=(255, 235, 240), outline=LUXOR_GOLD, width=1)
    r_draw.text((z1_cx, 155), "INGREDIENTS / المكونات الفاخرة", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="mm")
    
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
        col = LUXOR_GOLD if line.startswith("Premium") or line.startswith("Superfood") else IMPERIAL_BURGUNDY
        r_draw.text((z1_cx, cur_y), line, fill=col, font=load_font(14, bold=False), anchor="mm")
        cur_y += 28
        
    r_draw.rounded_rectangle([box_x0, 545, box_x1, 635], radius=10, fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=1)
    r_draw.text((z1_cx, 572), "ALLERGEN WARNING / تنبيه الحساسية", fill=WARM_IVORY, font=load_font(18, bold=True), anchor="mm")
    r_draw.text((z1_cx, 608), "Contains Tree Nuts & Bee Products. 100% Peanut-Free.", fill=CHAMPAGNE_GOLD, font=load_font(14, bold=False), anchor="mm")
    
    r_draw.text((z1_cx, 675), "Keep in a cool, dry place (18°C - 24°C). Store upright.", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=False), anchor="mm")
    r_draw.text((z1_cx, 710), "يحفظ في مكان بارد وجاف بعيداً عن أشعة الشمس المباشرة", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=False), anchor="mm")
    r_draw.text((z1_cx, 770), "NET WEIGHT: 500g e (17.6 oz)", fill=IMPERIAL_BURGUNDY, font=load_font(28, bold=True), anchor="mm")
    r_draw.text((z1_cx, 810), "الوزن الصافي: 500 غرام", fill=IMPERIAL_BURGUNDY, font=load_font(22, bold=True), anchor="mm")
    
    # Zone 2 (Center Hero Cartouche)
    z2_cx = cx0 + z2_w // 2
    cart_w = int(z2_w * 0.88)
    cart_h = int(lbl_h * 0.86)
    c_x0 = z2_cx - cart_w // 2
    c_x1 = z2_cx + cart_w // 2
    c_y0 = (lbl_h - cart_h) // 2
    c_y1 = c_y0 + cart_h
    
    pts_outer = get_scalloped_cartouche_polygon(c_x0, c_y0, c_x1, c_y1, r=int(cart_w * 0.055), arch_h=int(cart_h * 0.045))
    r_draw.polygon(pts_outer, fill=BLUSH_PINK, outline=LUXOR_GOLD, width=4)
    pts_inner = get_scalloped_cartouche_polygon(c_x0 + 10, c_y0 + 10, c_x1 - 10, c_y1 - 10, r=int(cart_w * 0.055) - 6, arch_h=int(cart_h * 0.045) - 3)
    r_draw.polygon(pts_inner, outline=LUXOR_GOLD, width=2)
    
    crown_w = 110
    crown_h = 58
    crown_cy = c_y0 + int(cart_h * 0.045) + 48
    draw_crown(r_draw, cx=z2_cx, cy=crown_cy, width=crown_w, height=crown_h, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
    
    burgundy_logo = get_tinted_logo(target_w=480, color=IMPERIAL_BURGUNDY)
    if burgundy_logo:
        logo_y = crown_cy + crown_h // 2 + 16
        royal_lbl.alpha_composite(burgundy_logo, (z2_cx - burgundy_logo.width // 2, logo_y))
        next_y = logo_y + burgundy_logo.height + 16
    else:
        next_y = crown_cy + 80
        
    r_draw.text((z2_cx, next_y), "NATURAL HONEY & SUPERFOODS", fill=IMPERIAL_BURGUNDY, font=load_font(20, bold=True), anchor="mm")
    next_y += 36
    r_draw.text((z2_cx, next_y), "MARIAM ROYAL MIX", fill=IMPERIAL_BURGUNDY, font=load_font(42, bold=True), anchor="mm")
    next_y += 42
    r_draw.text((z2_cx, next_y), "الخلطة الملكية الفاخرة • عسل طبيعي ومكسرات وغذاء ملكات", fill=IMPERIAL_BURGUNDY, font=load_font(24, bold=True), anchor="mm")
    next_y += 48
    
    ribbon_w = min(cart_w - 90, 720)
    ribbon_h = 42
    r_draw.rounded_rectangle([z2_cx - ribbon_w // 2, next_y - ribbon_h // 2, z2_cx + ribbon_w // 2, next_y + ribbon_h // 2],
                             radius=10, fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=2)
    r_draw.text((z2_cx, next_y), "• 0% PEANUTS • 100% TREE NUTS • 5% ROYAL JELLY •", fill=WARM_IVORY, font=load_font(20, bold=True), anchor="mm")
    next_y += 46
    
    r_draw.text((z2_cx, next_y), "Crunchy • Opulent • Energizing", fill=IMPERIAL_BURGUNDY, font=load_font(22, bold=False), anchor="mm")
    next_y += 34
    
    r_draw.line([(z2_cx - 90, next_y), (z2_cx - 16, next_y)], fill=LUXOR_GOLD, width=2)
    r_draw.line([(z2_cx + 16, next_y), (z2_cx + 90, next_y)], fill=LUXOR_GOLD, width=2)
    r_draw.ellipse([z2_cx - 5, next_y - 5, z2_cx + 5, next_y + 5], fill=LUXOR_GOLD)
    next_y += 36
    
    r_draw.text((z2_cx, next_y), "NET WT. 500g e (17.6 oz)", fill=IMPERIAL_BURGUNDY, font=load_font(24, bold=True), anchor="mm")
    
    # Zone 3
    z3_cx = cx1 + (lbl_w - cx1) // 2
    r_draw.text((z3_cx, 60), "SINGLE-ESTATE TERROIR", fill=IMPERIAL_BURGUNDY, font=load_font(24, bold=True), anchor="mm")
    r_draw.text((z3_cx, 95), "من إنتاج مزارع خير الوادي الطبيعية", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=False), anchor="mm")
    
    r_draw.ellipse([z3_cx - 65, 140, z3_cx + 65, 270], outline=LUXOR_GOLD, width=3)
    r_draw.ellipse([z3_cx - 55, 150, z3_cx + 55, 260], outline=IMPERIAL_BURGUNDY, width=1)
    draw_crown(r_draw, cx=z3_cx, cy=185, width=44, height=24, color=LUXOR_GOLD)
    r_draw.text((z3_cx, 225), "KHAEER ALWADI", fill=IMPERIAL_BURGUNDY, font=load_font(13, bold=True), anchor="mm")
    r_draw.text((z3_cx, 243), "خير الوادي", fill=IMPERIAL_BURGUNDY, font=load_font(13, bold=False), anchor="mm")
    
    claims_r = [
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
    for c in claims_r:
        r_draw.text((z3_cx, cur_y), c, fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=False), anchor="mm")
        cur_y += 28
        
    bc_w, bc_h = 320, 110
    bc_x = z3_cx - bc_w // 2
    bc_y = 570
    r_draw.rectangle([bc_x - 14, bc_y - 10, bc_x + bc_w + 14, bc_y + bc_h + 14], fill=PURE_WHITE, outline=LUXOR_GOLD, width=2)
    draw_barcode(r_draw, bc_x, bc_y, bc_w, bc_h, "6281005001017", bar_color=PURE_BLACK, text_color=PURE_BLACK)
    
    r_draw.text((z3_cx, 740), "ISO 22000 • HACCP • HALAL CERTIFIED", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="mm")
    r_draw.text((z3_cx, 780), "♻ RECYCLABLE GLASS CONTAINER • BATCH: RM-500-2026", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=False), anchor="mm")
    r_draw.text((z3_cx, 820), "PRODUCT OF ARABIAN HIGHLANDS • صنع في المملكة العربية السعودية", fill=LUXOR_GOLD, font=load_font(16, bold=True), anchor="mm")
    
    sheet.alpha_composite(royal_lbl, (lbl_x0, lbl_y0))
    draw_crop_marks(draw, lbl_x0, lbl_y0, lbl_x1, lbl_y1, mark_len=45, offset=15, color=PURE_BLACK, width=2)
    
    for sx in range(lbl_x0 - 15, lbl_x1 + 15, 20):
        draw.line([(sx, lbl_y0 - 15), (sx + 10, lbl_y0 - 15)], fill=GRAY_LINE, width=1)
        draw.line([(sx, lbl_y1 + 15), (sx + 10, lbl_y1 + 15)], fill=GRAY_LINE, width=1)
    for sy in range(lbl_y0 - 15, lbl_y1 + 15, 20):
        draw.line([(lbl_x0 - 15, sy), (lbl_x0 - 15, sy + 10)], fill=GRAY_LINE, width=1)
        draw.line([(lbl_x1 + 15, sy), (lbl_x1 + 15, sy + 10)], fill=GRAY_LINE, width=1)
        
    draw.text((lbl_x0 + 40, lbl_y0 - 30), "✂ CUT ALONG DASHED LINE / خط القص الخارجي ✂", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="lm")
    draw.text((lbl_x1 - 40, lbl_y0 - 30), "FINISHED TRIM: 240mm × 85mm", fill=LUXOR_GOLD, font=load_font(16, bold=True), anchor="rm")
    
    # Bottom Row
    bot_y = 1530
    from generate_print_mockups import render_tamper_ribbon_300dpi, render_lid_seal_300dpi
    ribbon_img = render_tamper_ribbon_300dpi(213, 531)
    rx0 = 240
    ry0 = bot_y + 110
    sheet.alpha_composite(ribbon_img, (rx0, ry0))
    draw_crop_marks(draw, rx0, ry0, rx0 + 213, ry0 + 531, mark_len=25, offset=10, color=PURE_BLACK, width=2)
    draw.text((rx0 + 106, ry0 - 25), "TAMPER SEAL (18×45mm)", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="mm")
    draw.text((rx0 + 106, ry0 + 531 + 25), "شريط إحكام الغطاء بالتاج", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=False), anchor="mm")
    
    lid_seal = render_lid_seal_300dpi(640)
    lx0 = 600
    ly0 = bot_y + 60
    sheet.alpha_composite(lid_seal, (lx0, ly0))
    draw.text((lx0 + 320, ly0 - 20), "CAP TOP SEAL (Ø 60mm)", fill=PURE_BLACK, font=load_font(16, bold=True), anchor="mm")
    draw.text((lx0 + 320, ly0 + 640 + 25), "ملصق قمة الغطاء الذهبي", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=False), anchor="mm")
    
    cx_box = 1420
    cy_box = bot_y + 80
    draw.rounded_rectangle([cx_box, cy_box, cx_box + 900, cy_box + 260], radius=12, fill=(255, 252, 254), outline=GRAY_LINE, width=1)
    draw.text((cx_box + 30, cy_box + 35), "COLOR CALIBRATION BARS & PRESS CONTROL:", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="lm")
    draw_cmyk_pantone_swatches(draw, base_x=cx_box + 30, base_y=cy_box + 70, swatch_w=48, swatch_h=28)
    draw.text((cx_box + 30, cy_box + 175), "• Substrate: Petal Blush Pink (#F5B7C2 / Pantone 496 C) on Textured Linen", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=True), anchor="lm")
    draw.text((cx_box + 30, cy_box + 205), "• Hot Stamping: Kurz Luxor 428 Metallic Gold Foil", fill=LUXOR_GOLD, font=load_font(14, bold=True), anchor="lm")
    draw.text((cx_box + 30, cy_box + 235), "• Solid Spot: Deep Wine Burgundy (#76122E / Pantone 7428 C)", fill=IMPERIAL_BURGUNDY, font=load_font(14, bold=True), anchor="lm")
    
    gx_box = 2440
    gy_box = bot_y + 80
    draw.rounded_rectangle([gx_box, gy_box, w - 100, gy_box + 260], radius=12, fill=(255, 252, 254), outline=GRAY_LINE, width=1)
    draw.text((gx_box + 30, gy_box + 35), "HOW TO TEST ON JAR (طريقة التركيب):", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="lm")
    guide_steps = [
        "1. Cut main label along outer crop marks.",
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
              
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_honey_royal_mix_500g_printable_label_sheet_a4_300dpi.png")
    brain_path = os.path.join(BRAIN_DIR, "mariam_honey_royal_mix_500g_printable_label_sheet_a4_300dpi.png")
    sheet.convert("RGB").save(out_path, "PNG")
    sheet.convert("RGB").save(brain_path, "PNG")
    print(f"Saved: {out_path}")

# ==============================================================================
# 4. BUILD 4K PHOTOREALISTIC 3D MOCKUP FOR MOUNTAIN SIDR HONEY
# ==============================================================================
def build_sidr_honey_photorealistic_4k_mockup():
    """Builds 4K ultra-realistic packaging mockup for pure Mountain Sidr Honey."""
    w, h = 3840, 2160
    im = Image.new("RGBA", (w, h), (242, 239, 234))
    draw = ImageDraw.Draw(im)
    
    # Warm luxury travertine gradient
    for y in range(h):
        t = y / h
        r = int(248 - t * 20)
        g = int(244 - t * 22)
        b = int(239 - t * 24)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    ao = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ao_draw = ImageDraw.Draw(ao)
    ao_draw.ellipse([w // 2 - 1200, h - 600, w // 2 + 1200, h + 200], fill=(0, 0, 0, 35))
    ao_draw.ellipse([w // 2 - 800, h - 450, w // 2 + 800, h + 100], fill=(0, 0, 0, 50))
    ao_draw.ellipse([w // 2 - 400, h - 300, w // 2 + 400, h], fill=(0, 0, 0, 60))
    ao = ao.filter(ImageFilter.GaussianBlur(radius=80))
    im.alpha_composite(ao)
    
    # Load 4K Mountain Sidr Jar
    sidr_path = os.path.join(OUTPUT_IMAGERY, "mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg")
    if os.path.exists(sidr_path):
        jar_raw = Image.open(sidr_path).convert("RGB")
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
        
    # Left Side: Flat Proof Sheet lying on table
    proof_w, proof_h = 1350, 950
    proof = Image.new("RGBA", (proof_w, proof_h), PURE_WHITE)
    p_draw = ImageDraw.Draw(proof)
    p_draw.rectangle([10, 10, proof_w - 10, proof_h - 10], outline=LUXOR_GOLD, width=3)
    p_draw.text((proof_w // 2, 60), "MARIAM MOUNTAIN SIDR HONEY 500g — PHYSICAL PRINT PROOF", fill=IMPERIAL_BURGUNDY, font=load_font(26, bold=True), anchor="mm")
    p_draw.text((proof_w // 2, 105), "TRUE 1:1 SCALE • FASSON CURVETEC TEXTURED LINEN 95GSM", fill=LUXOR_GOLD, font=load_font(18, bold=True), anchor="mm")
    
    lbl_mini_w, lbl_mini_h = 1080, 415
    lbl_mini = render_mountain_sidr_label_300dpi(lbl_mini_w, lbl_mini_h)
    proof.alpha_composite(lbl_mini, ((proof_w - lbl_mini_w) // 2, 160))
    draw_crop_marks(p_draw, (proof_w - lbl_mini_w) // 2, 160, (proof_w + lbl_mini_w) // 2, 160 + lbl_mini_h, mark_len=20, offset=8, color=PURE_BLACK, width=2)
    
    draw_cmyk_pantone_swatches(p_draw, base_x=120, base_y=620, swatch_w=36, swatch_h=20)
    p_draw.text((proof_w // 2, 710), "QA STATUS: APPROVED FOR BOTTLING & LABELING • 100% RAW SIDR", fill=IMPERIAL_BURGUNDY, font=load_font(22, bold=True), anchor="mm")
    draw_calibration_ruler(p_draw, cx=proof_w // 2, cy=770, length_mm=60, dpi=180)
    
    proof_rot = proof.rotate(-4, resample=Image.Resampling.BICUBIC, expand=True)
    psh = Image.new("RGBA", proof_rot.size, (0, 0, 0, 0))
    ImageDraw.Draw(psh).rectangle([20, 20, proof_rot.width - 20, proof_rot.height - 20], fill=(0, 0, 0, 80))
    psh = psh.filter(ImageFilter.GaussianBlur(radius=25))
    
    px0 = 240
    py0 = 550
    im.alpha_composite(psh, (px0 + 15, py0 + 20))
    im.alpha_composite(proof_rot, (px0, py0))
    
    # Top Left Typography
    draw = ImageDraw.Draw(im)
    gold_logo_top = get_tinted_logo(target_w=280, color=LUXOR_GOLD)
    if gold_logo_top:
        im.alpha_composite(gold_logo_top, (180, 140))
        
    draw.text((180, 280), "PURE NATURAL HONEY PRINT MOCKUP", fill=IMPERIAL_BURGUNDY, font=load_font(46, bold=True), anchor="lm")
    draw.text((180, 345), "Mariam Mountain Sidr Honey 500g • Nordic Glass & Textured Linen Label", fill=LUXOR_GOLD, font=load_font(28, bold=True), anchor="lm")
    draw.text((180, 400), "الموكاب الاحترافي الواقعي لطباعة وتغليف عسل السدر الجبلي الملكي النقي", fill=IMPERIAL_BURGUNDY, font=load_font(26, bold=True), anchor="lm")
    
    draw.line([(180, h - 260), (1400, h - 260)], fill=LUXOR_GOLD, width=2)
    draw.text((180, h - 210), "HONEY PACKAGING SPECIFICATIONS (المواصفات الفنية المعتمدة):", fill=IMPERIAL_BURGUNDY, font=load_font(22, bold=True), anchor="lm")
    draw.text((180, h - 165), "• Authentic Petal Blush Pink (#F5B7C2) with Kurz Luxor Gold Foil & Wine Burgundy Lettering", fill=PURE_BLACK, font=load_font(18, bold=False), anchor="lm")
    draw.text((180, h - 125), "• 100% Reference Fidelity • Authentic Cursive Logo • Zero AI Hallucination", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="lm")
    draw.text((180, h - 85), "• Tamper-Evident Ribbon (18×45mm) with Embossed Gold Crown Crest 👑 & Perforation Score", fill=LUXOR_GOLD, font=load_font(18, bold=True), anchor="lm")
    
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_honey_sidr_500g_photorealistic_print_mockup_4k.jpg")
    brain_path = os.path.join(BRAIN_DIR, "mariam_honey_sidr_500g_photorealistic_print_mockup_4k.jpg")
    im.convert("RGB").save(out_path, "JPEG", quality=98)
    im.convert("RGB").save(brain_path, "JPEG", quality=98)
    print(f"Saved: {out_path}")

# ==============================================================================
# 5. BUILD MASTER A3 INDUSTRIAL PRESS PROOF SHEET (HONEY SUITE)
# ==============================================================================
def build_honey_master_a3_press_proof():
    """Builds A3 master industrial printing press proof sheet for Mariam Honey."""
    w, h = 4960, 3508  # A3 @ 300 DPI
    sheet = Image.new("RGBA", (w, h), PURE_WHITE)
    draw = ImageDraw.Draw(sheet)
    
    draw.rectangle([80, 80, w - 80, h - 80], outline=LUXOR_GOLD, width=4)
    draw.rectangle([95, 95, w - 95, h - 95], outline=IMPERIAL_BURGUNDY, width=2)
    
    draw_registration_crosshair(draw, 140, 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, w - 140, 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, 140, h - 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, w - 140, h - 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, w // 2, 140, size=30, color=PURE_BLACK)
    draw_registration_crosshair(draw, w // 2, h - 140, size=30, color=PURE_BLACK)
    
    draw.text((220, 160), "MARIAM NATURAL HONEY & SUPERFOODS — MASTER PACKAGING PRESS PROOF", fill=IMPERIAL_BURGUNDY, font=load_font(34, bold=True), anchor="lm")
    draw.text((220, 210), "INDUSTRIAL COLOR SEPARATION, HOT FOIL MASK & MECHANICAL DIELINE SPECIFICATIONS", fill=LUXOR_GOLD, font=load_font(24, bold=True), anchor="lm")
    draw.text((w - 220, 185), "FORMAT: A3 LANDSCAPE (420mm × 297mm) @ 300 DPI", fill=PURE_BLACK, font=load_font(20, bold=False), anchor="rm")
    
    draw.line([(140, 250), (w - 140, 250)], fill=LUXOR_GOLD, width=2)
    
    # Main Mechanical Artwork (Sidr Honey 220mm × 85mm)
    lbl_w, lbl_h = 2598, 1004
    mx0 = 220
    my0 = 340
    main_lbl = render_mountain_sidr_label_300dpi(lbl_w, lbl_h)
    sheet.alpha_composite(main_lbl, (mx0, my0))
    draw_crop_marks(draw, mx0, my0, mx0 + lbl_w, my0 + lbl_h, mark_len=50, offset=20, color=PURE_BLACK, width=3)
    
    draw.line([(mx0, my0 - 45), (mx0 + lbl_w, my0 - 45)], fill=LUXOR_GOLD, width=2)
    draw.text((mx0 + lbl_w // 2, my0 - 70), "◄ FINISHED TRIM WIDTH: 220.0 mm ►", fill=LUXOR_GOLD, font=load_font(22, bold=True), anchor="mm")
    
    draw.line([(mx0 + lbl_w + 45, my0), (mx0 + lbl_w + 45, my0 + lbl_h)], fill=LUXOR_GOLD, width=2)
    draw.text((mx0 + lbl_w + 80, my0 + lbl_h // 2), "▲ HEIGHT: 85.0 mm ▼", fill=LUXOR_GOLD, font=load_font(22, bold=True), anchor="lm")
    
    draw.text((mx0, my0 + lbl_h + 40), "• SOLID BLACK: Die-Cut Trim Line (220mm × 85mm)   • RED DASHED: +3mm Bleed Margin   • GREEN: Safety Line 3mm",
              fill=PURE_BLACK, font=load_font(18, bold=False), anchor="lm")
              
    # Separation Plates
    sep_y = 1500
    draw.line([(140, sep_y), (w - 140, sep_y)], fill=LUXOR_GOLD, width=2)
    draw.text((220, sep_y + 40), "HONEY LINE PRINT SEPARATIONS & EMBOSSING PLATES (لوحات فصل طبقات الذهب والورنيش والبروز):", fill=IMPERIAL_BURGUNDY, font=load_font(26, bold=True), anchor="lm")
    
    # 1. Gold Foil Plate
    foil_w, foil_h = 1380, 520
    fx0 = 220
    fy0 = sep_y + 80
    draw.rectangle([fx0, fy0, fx0 + foil_w, fy0 + foil_h], fill=(20, 20, 20), outline=LUXOR_GOLD, width=2)
    draw.text((fx0 + foil_w // 2, fy0 + 35), "HOT FOIL STAMPING PLATE (KURZ LUXOR 428 GOLD)", fill=LUXOR_GOLD, font=load_font(19, bold=True), anchor="mm")
    draw_crown(draw, cx=fx0 + foil_w // 2, cy=fy0 + 130, width=100, height=54, color=PURE_WHITE, jewel_color=PURE_BLACK)
    gold_logo_plate = get_tinted_logo(target_w=380, color=PURE_WHITE)
    if gold_logo_plate:
        sheet.alpha_composite(gold_logo_plate, (fx0 + foil_w // 2 - 190, fy0 + 190))
    draw.text((fx0 + foil_w // 2, fy0 + 340), "MOUNTAIN SIDR HONEY • BORDERS & CROWN", fill=PURE_WHITE, font=load_font(22, bold=True), anchor="mm")
    draw.text((fx0 + foil_w // 2, fy0 + 390), "Tooling: Brass CNC Engraved Foil Block | Temp: 125°C - 135°C", fill=CHAMPAGNE_GOLD, font=load_font(17, bold=False), anchor="mm")
    draw.text((fx0 + foil_w // 2, fy0 + 440), "Emboss Depth: 0.35 mm Micro-Emboss on Crown & Brand Lettering", fill=LUXOR_GOLD, font=load_font(17, bold=True), anchor="mm")
    
    # 2. Spot UV Plate
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
    
    # 3. Specs & Approval
    tx0 = ux0 + uv_w + 50
    ty0 = 340
    tw = w - tx0 - 140
    th = 2300
    draw.rounded_rectangle([tx0, ty0, tx0 + tw, ty0 + th], radius=16, fill=(255, 252, 254), outline=LUXOR_GOLD, width=2)
    
    draw.text((tx0 + tw // 2, ty0 + 40), "HONEY PACKAGING PRODUCTION SPECS", fill=IMPERIAL_BURGUNDY, font=load_font(22, bold=True), anchor="mm")
    draw.text((tx0 + tw // 2, ty0 + 75), "مواصفات مواد وخامات طباعة العسل الطبيعي", fill=IMPERIAL_BURGUNDY, font=load_font(18, bold=True), anchor="mm")
    draw.line([(tx0 + 30, ty0 + 105), (tx0 + tw - 30, ty0 + 105)], fill=LUXOR_GOLD, width=1)
    
    specs = [
        ("Brand / Division", "Mariam Natural Honey & Superfoods"),
        ("Product Line", "Mountain Sidr Honey 500g (SKU-H03)"),
        ("Label Geometry", "Wrap-Around Band: 220mm × 85mm"),
        ("Tamper Ribbon", "18mm × 45mm (Crown Crest)"),
        ("Substrate Material", "Fasson Curvetec Cream Linen 95gsm"),
        ("Substrate Shade", "Petal Blush Pink (#F5B7C2 / Pantone 496)"),
        ("Adhesive Type", "S2000N High-Tack Permanent Acrylic"),
        ("Release Liner", "BG40 White Supercalendered Glassine"),
        ("Printing Process", "6-Color UV Rotary Flexography"),
        ("Ink Sequence", "Process CMYK + Spot Gold + Spot Burgundy"),
        ("Metallic Foil", "Kurz Luxor 428 Hot Foil Stamping"),
        ("Spot Typography", "Deep Wine Burgundy (#76122E / Pantone 7428)"),
        ("Surface Coating", "Food-Grade Soft-Touch Matte Aqueous"),
        ("Embossing Spec", "CNC Brass Multi-Level 0.35mm Crown"),
        ("Die Tooling", "Magnetic Rotary Flexible Die #M-500H"),
        ("Winding Direction", "Winding #4 (Left Edge Leading, Out)"),
        ("Core Diameter", "76 mm (3.0 inches) Industry Standard"),
        ("Inspection Standard", "100% Optical In-Line Video Inspection"),
        ("Barcode Verification", "ISO/IEC 15416 Grade A (Score: 4.0/4.0)"),
    ]
    cur_sy = ty0 + 140
    for label, val in specs:
        draw.text((tx0 + 30, cur_sy), label + ":", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=True), anchor="lm")
        draw.text((tx0 + tw - 30, cur_sy), val, fill=PURE_BLACK, font=load_font(15, bold=False), anchor="rm")
        draw.line([(tx0 + 30, cur_sy + 20), (tx0 + tw - 30, cur_sy + 20)], fill=GRAY_LIGHT, width=1)
        cur_sy += 54
        
    app_y = cur_sy + 40
    draw.rounded_rectangle([tx0 + 20, app_y, tx0 + tw - 20, app_y + 400], radius=12, fill=WARM_IVORY, outline=IMPERIAL_BURGUNDY, width=2)
    draw.text((tx0 + tw // 2, app_y + 35), "FORMAL HONEY PRESS APPROVAL SIGN-OFF", fill=IMPERIAL_BURGUNDY, font=load_font(20, bold=True), anchor="mm")
    draw.text((tx0 + tw // 2, app_y + 65), "نموذج اعتماد طباعة عسل مريم النهائي للمطابع", fill=IMPERIAL_BURGUNDY, font=load_font(16, bold=True), anchor="mm")
    
    app_fields = [
        "Client Representative: Mariam Brand Director",
        "Approval Status: APPROVED FOR MASS PRINTING",
        "Total Print Run: 50,000 Units",
        "QA Production Manager Signature: __________________",
        "Lead Press Operator Signature: ___________________",
        "Date of Approval: September 22, 2026",
    ]
    for idx, af in enumerate(app_fields):
        col = IMPERIAL_BURGUNDY if "APPROVED" in af else PURE_BLACK
        bld = True if "APPROVED" in af else False
        draw.text((tx0 + 40, app_y + 115 + idx * 45), af, fill=col, font=load_font(16, bold=bld), anchor="lm")
        
    draw.line([(140, h - 220), (w - 140, h - 220)], fill=LUXOR_GOLD, width=2)
    draw_cmyk_pantone_swatches(draw, base_x=220, base_y=h - 180, swatch_w=60, swatch_h=35)
    draw.text((w // 2 + 200, h - 140), "ISO 12647-2 PRINT COMPLIANCE • CERTIFIED HONEY PACKAGING BLUEPRINT", fill=GRAY_LINE, font=load_font(18, bold=True), anchor="mm")
    
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_honey_master_press_proof_sheet_a3_300dpi.png")
    brain_path = os.path.join(BRAIN_DIR, "mariam_honey_master_press_proof_sheet_a3_300dpi.png")
    sheet.convert("RGB").save(out_path, "PNG")
    sheet.convert("RGB").save(brain_path, "PNG")
    print(f"Saved: {out_path}")

# ==============================================================================
# 6. BUILD HONEY PACKAGING EVALUATION BOARD (4K 3840 × 2160)
# ==============================================================================
def build_honey_evaluation_board():
    """Builds packaging agency presentation evaluation board for Honey."""
    w, h = 3840, 2160
    im = Image.new("RGBA", (w, h), DARK_OBSIDIAN)
    draw = ImageDraw.Draw(im)
    
    draw.rectangle([60, 60, w - 60, h - 60], outline=LUXOR_GOLD, width=3)
    draw.rectangle([76, 76, w - 76, h - 76], outline=CHAMPAGNE_GOLD, width=1)
    
    gold_logo_eval = get_tinted_logo(target_w=240, color=LUXOR_GOLD)
    if gold_logo_eval:
        im.alpha_composite(gold_logo_eval, (120, 110))
        
    draw.text((400, 140), "MARIAM NATURAL HONEY & SUPERFOODS — PACKAGING PRINT EVALUATION BOARD", fill=WARM_IVORY, font=load_font(34, bold=True), anchor="lm")
    draw.text((400, 190), "لوحة اعتماد ومراجعة الطباعة والموكاب ثلاثي الأبعاد • عسل السدر الجبلي الملكي 500 جم", fill=LUXOR_GOLD, font=load_font(24, bold=False), anchor="lm")
    draw.line([(120, 240), (w - 120, 240)], fill=LUXOR_GOLD, width=2)
    
    mid_x = 1750
    draw.line([(mid_x, 260), (mid_x, h - 140)], fill=LUXOR_GOLD, width=2)
    
    draw.text((mid_x // 2, 290), "[ 3D FINISHED PRODUCT MOCKUP • نموذج عبوة العسل الحقيقي ]", fill=CHAMPAGNE_GOLD, font=load_font(22, bold=True), anchor="mm")
    
    sidr_path = os.path.join(OUTPUT_IMAGERY, "mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg")
    if os.path.exists(sidr_path):
        jar_raw = Image.open(sidr_path).convert("RGB")
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
            (jx + target_w // 2, jy + 600, "Cursive Mariam Logo (#76122E)", "right"),
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
    dl_h = int(dl_w * (1004 / 2598))
    dl_img = render_mountain_sidr_label_300dpi(dl_w, dl_h)
    dx0 = mid_x + 80
    dy0 = 360
    im.alpha_composite(dl_img, (dx0, dy0))
    draw.rectangle([dx0, dy0, dx0 + dl_w, dy0 + dl_h], outline=LUXOR_GOLD, width=2)
    
    sp_y = dy0 + dl_h + 50
    draw.rounded_rectangle([dx0, sp_y, dx0 + dl_w, h - 160], radius=14, fill=(28, 22, 24), outline=LUXOR_GOLD, width=2)
    
    draw.text((dx0 + 40, sp_y + 40), "HONEY PRODUCTION & SUBSTRATE SPECIFICATIONS:", fill=LUXOR_GOLD, font=load_font(22, bold=True), anchor="lm")
    specs_summary = [
        "• Material: Fasson Curvetec Cream Textured Linen 95gsm with S2000N Permanent Adhesive.",
        "• Printing: 6-Color UV Rotary Flexo (Process CMYK + Kurz Luxor 428 Gold Foil + Wine Burgundy).",
        "• Finishes: Soft-touch matte background + Spot 3D Raised High-Build Gloss UV on cartouche.",
        "• Dimensions: 220mm (W) × 85mm (H) Full Wrap | 18mm × 45mm Tamper Seal with Crown.",
        "• QA Compliance: ISO 12647-2 Flexo Standards | EAN-13 Barcode Grade A Certified.",
        "• Pure Honey: 100% Raw Single-Origin Sidr Honey with zero additives.",
    ]
    for idx, ss in enumerate(specs_summary):
        draw.text((dx0 + 40, sp_y + 90 + idx * 45), ss, fill=WARM_IVORY, font=load_font(18, bold=False), anchor="lm")
        
    draw_cmyk_pantone_swatches(draw, base_x=dx0 + 40, base_y=sp_y + 390, swatch_w=48, swatch_h=26)
    
    out_path = os.path.join(OUTPUT_MOCKUPS, "mariam_honey_packaging_evaluation_board_4k.jpg")
    brain_path = os.path.join(BRAIN_DIR, "mariam_honey_packaging_evaluation_board_4k.jpg")
    im.convert("RGB").save(out_path, "JPEG", quality=98)
    im.convert("RGB").save(brain_path, "JPEG", quality=98)
    print(f"Saved: {out_path}")

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    print("Generating dedicated professional honey print mockup suite...")
    print("1. Building A4 1:1 Printable Proof Sheet (Mountain Sidr Honey 500g)...")
    build_sidr_honey_a4_printable_sheet()
    
    print("2. Building A4 1:1 Printable Proof Sheet (Royal Mix 500g - 100% Solid Pink)...")
    build_royal_mix_pink_a4_printable_sheet()
    
    print("3. Building A3 Industrial Press Proof Sheet (Honey Suite)...")
    build_honey_master_a3_press_proof()
    
    print("4. Building 4K Photorealistic 3D Print Mockup (Mountain Sidr Honey 500g)...")
    build_sidr_honey_photorealistic_4k_mockup()
    
    print("5. Building 4K Honey Packaging Evaluation Board...")
    build_honey_evaluation_board()
    
    print("Professional honey print mockups successfully generated and saved to output/mockups/ and brain dir!")

if __name__ == "__main__":
    main()
