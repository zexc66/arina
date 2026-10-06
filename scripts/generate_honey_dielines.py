#!/usr/bin/env python3
"""
Mariam Luxury Brand - Honey & Superfoods Packaging Die-Line Generator
Generates high-resolution, print-calibrated packaging label blueprints with:
- Exact mechanical dimensions across all 6 honey and superfood formats:
  1. dieline_honey_500g_standard.png (2200 × 900 px @ 254 DPI, 220mm × 90mm)
  2. dieline_honey_1kg_family.png (2600 × 1100 px @ 254 DPI, 260mm × 110mm)
  3. dieline_royal_mix_500g_wide.png (2400 × 850 px @ 254 DPI, 240mm × 85mm)
  4. dieline_honeycomb_500g_hex.png (1800 × 900 px @ 254 DPI, 180mm × 90mm)
  5. dieline_tamper_ribbon_crown.png (450 × 1125 px @ 254 DPI, 18mm × 45mm)
  6. dieline_discovery_flight_50g.png (1200 × 400 px @ 254 DPI, 120mm × 40mm)
- Official Honey & Superfoods palette (calibrated to authentic product reference photo):
  * Mariam Petal Blush Pink: RGB(245, 183, 194) / #F5B7C2
  * Deep Wine Burgundy: RGB(118, 18, 46) / #76122E
  * Luxor Gold Foil: RGB(218, 172, 54) / #DAAC36
  * Warm Ivory Blush: RGB(255, 245, 247) / #FFF5F7
- High contrast typography: on blush pink, all typography is strictly Deep Wine Burgundy (#76122E)
- Authentic cursive logo: mariam-logo-gold.png composited with balanced proportions and zero text collisions
- Royal Mix 500g features the authentic baroque scalloped cartouche from the user reference photo
- Tamper ribbon features 18mm × 45mm geometry, gold crown crest, perforation score, and crisp wine burgundy text
"""

import json
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

# Official Brand Palette Constants - Calibrated to Authentic Reference Photo
BLUSH_PINK = (245, 183, 194)        # #F5B7C2 (Petal Blush Pink sampled from user photo)
BLUSH_PINK_LIGHT = (252, 220, 227)  # #FCDCE3 (Light Petal Tint)
IMPERIAL_BURGUNDY = (118, 18, 46)   # #76122E (Deep Wine Burgundy sampled from user photo)
LUXOR_GOLD = (218, 172, 54)         # #DAAC36 (Kurz Luxor 428 Gold)
WARM_IVORY = (255, 245, 247)        # #FFF5F7 (Warm Ivory Blush)
HONEY_AMBER = (226, 149, 39)        # #E29527
CHAMPAGNE_GOLD = (238, 212, 142)    # #EED48E
DEEP_BURGUNDY = (75, 12, 32)        # #4B0C20

def load_font(size, bold=False):
    """Load local Tajawal font if available, fallback to default."""
    font_path = "fonts/Tajawal-Bold.ttf" if bold else "fonts/Tajawal-Medium.ttf"
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def get_tinted_logo(logo_img, color):
    """Create a tinted version of the authentic logo preserving its exact alpha mask."""
    if not logo_img:
        return None
    r, g, b, a = logo_img.split()
    tinted = Image.new("RGBA", logo_img.size, (*color, 255))
    tinted.putalpha(a)
    return tinted

def draw_crosshair(draw, x, y, size=18, color=LUXOR_GOLD, width=2):
    """Draw high-precision optical registration crosshair."""
    draw.line([(x - size, y), (x + size, y)], fill=color, width=width)
    draw.line([(x, y - size), (x, y + size)], fill=color, width=width)
    draw.ellipse([x - 6, y - 6, x + 6, y + 6], outline=color, width=1)
    draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=color)

def draw_dashed_line(draw, start, end, fill, width=1, dash_length=8, gap_length=4):
    """Draw a dashed line between start and end coordinates."""
    x1, y1 = start
    x2, y2 = end
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0:
        return
    vx = (x2 - x1) / dist
    vy = (y2 - y1) / dist
    cur = 0.0
    while cur < dist:
        seg_end = min(cur + dash_length, dist)
        draw.line([
            (int(x1 + vx * cur), int(y1 + vy * cur)),
            (int(x1 + vx * seg_end), int(y1 + vy * seg_end))
        ], fill=fill, width=width)
        cur += dash_length + gap_length

def draw_crown(draw, cx, cy, width, height, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY):
    """
    Draw an embossed royal crown crest with 5 peaks, pearls, and jeweled base band.
    """
    w2 = width // 2
    h2 = height // 2
    h_center = h2
    h_outer = int(h2 * 0.72)
    h_inner = int(h2 * 0.52)
    
    # Base band
    base_h = max(5, int(height * 0.20))
    base_y = cy + h2 - base_h
    draw.rectangle([cx - w2, base_y, cx + w2, cy + h2], fill=color)
    
    # Base band jewels
    jewel_r = max(2, base_h // 4)
    for jx in [-w2 * 0.65, -w2 * 0.22, w2 * 0.22, w2 * 0.65]:
        draw.ellipse([
            cx + jx - jewel_r, base_y + base_h // 2 - jewel_r,
            cx + jx + jewel_r, base_y + base_h // 2 + jewel_r
        ], fill=jewel_color)
    
    # Crown body polygon
    pts = [
        (cx - w2, base_y),
        (cx - w2 - 3, cy - h_outer),
        (cx - int(w2 * 0.50), cy + int(h2 * 0.10)),
        (cx - int(w2 * 0.26), cy - h_inner),
        (cx - int(w2 * 0.10), cy + int(h2 * 0.05)),
        (cx, cy - h_center),
        (cx + int(w2 * 0.10), cy + int(h2 * 0.05)),
        (cx + int(w2 * 0.26), cy - h_inner),
        (cx + int(w2 * 0.50), cy + int(h2 * 0.10)),
        (cx + w2 + 3, cy - h_outer),
        (cx + w2, base_y),
    ]
    draw.polygon(pts, fill=color)
    
    # Pearls on top of peaks
    pr = max(2, int(width * 0.038))
    draw.ellipse([cx - pr, cy - h_center - pr * 2, cx + pr, cy - h_center], fill=color)
    draw.ellipse([cx - int(w2 * 0.26) - pr, cy - h_inner - pr * 2, cx - int(w2 * 0.26) + pr, cy - h_inner], fill=color)
    draw.ellipse([cx + int(w2 * 0.26) - pr, cy - h_inner - pr * 2, cx + int(w2 * 0.26) + pr, cy - h_inner], fill=color)
    draw.ellipse([cx - w2 - 3 - pr, cy - h_outer - pr * 2, cx - w2 - 3 + pr, cy - h_outer], fill=color)
    draw.ellipse([cx + w2 + 3 - pr, cy - h_outer - pr * 2, cx + w2 + 3 + pr, cy - h_outer], fill=color)

def get_scalloped_cartouche_polygon(x0, y0, x1, y1, r=36, arch_h=22):
    """
    Construct mathematically precise baroque scalloped cartouche with inward concave notches
    and gentle convex arches at top and bottom, matching the authentic reference jar label.
    """
    cx = (x0 + x1) / 2
    pts = []
    
    # 1. Top Arch: from (x0 + r, y0 + arch_h) to (x1 - r, y0 + arch_h) peaking at (cx, y0)
    n_arch = 30
    for i in range(n_arch + 1):
        t = i / n_arch
        px = (x0 + r) + t * (x1 - x0 - 2 * r)
        py = y0 + (1.0 - math.sin(t * math.pi)) * arch_h
        pts.append((px, py))
        
    # 2. Top-Right Concave Corner Notch
    n_corner = 12
    for i in range(1, n_corner + 1):
        ang = math.radians(180 + i * (90 / n_corner))
        px = x1 + r * math.cos(ang)
        py = (y0 + arch_h) - r * math.sin(ang)
        pts.append((px, py))
        
    # 3. Right edge
    pts.append((x1, y1 - arch_h - r))
    
    # 4. Bottom-Right Concave Corner Notch
    for i in range(1, n_corner + 1):
        ang = math.radians(90 + i * (90 / n_corner))
        px = x1 + r * math.cos(ang)
        py = (y1 - arch_h) - r * math.sin(ang)
        pts.append((px, py))
        
    # 5. Bottom Arch: from (x1 - r, y1 - arch_h) to (x0 + r, y1 - arch_h) dipping at (cx, y1)
    for i in range(n_arch + 1):
        t = i / n_arch
        px = (x1 - r) - t * (x1 - x0 - 2 * r)
        py = y1 - (1.0 - math.sin(t * math.pi)) * arch_h
        pts.append((px, py))
        
    # 6. Bottom-Left Concave Corner Notch
    for i in range(1, n_corner + 1):
        ang = math.radians(0 + i * (90 / n_corner))
        px = x0 + r * math.cos(ang)
        py = (y1 - arch_h) - r * math.sin(ang)
        pts.append((px, py))
        
    # 7. Left edge
    pts.append((x0, y0 + arch_h + r))
    
    # 8. Top-Left Concave Corner Notch
    for i in range(1, n_corner + 1):
        ang = math.radians(270 + i * (90 / n_corner))
        px = x0 + r * math.cos(ang)
        py = (y0 + arch_h) - r * math.sin(ang)
        pts.append((px, py))
        
    return [(int(round(px)), int(round(py))) for px, py in pts]

def draw_hexagon(draw, cx, cy, radius, outline=LUXOR_GOLD, width=2):
    """Draw a regular hexagon centered at (cx, cy)."""
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, outline=outline, width=width)

def draw_barcode(draw, x, y, w, h, code_text, bar_color=LUXOR_GOLD, text_color=WARM_IVORY, font=None):
    """Draw a realistic EAN-13 barcode mockup with guard bars and text."""
    random.seed(code_text)
    cur_x = x + 12
    end_x = x + w - 12
    bar_h = h - 22
    
    # Start guard bars
    draw.line([(cur_x, y), (cur_x, y + bar_h + 8)], fill=bar_color, width=2)
    cur_x += 4
    draw.line([(cur_x, y), (cur_x, y + bar_h + 8)], fill=bar_color, width=2)
    cur_x += 6
    
    # Realistic data bars
    while cur_x < end_x - 14:
        bw = random.choice([1, 2, 3, 2, 1, 4, 2])
        gap = random.choice([2, 3, 4, 2, 3])
        draw.rectangle([cur_x, y, cur_x + bw, y + bar_h], fill=bar_color)
        cur_x += bw + gap
        
    # End guard bars
    draw.line([(end_x - 6, y), (end_x - 6, y + bar_h + 8)], fill=bar_color, width=2)
    draw.line([(end_x - 2, y), (end_x - 2, y + bar_h + 8)], fill=bar_color, width=2)
    
    # Barcode human-readable digits
    if font:
        draw.text((x + w // 2, y + h - 6), code_text, fill=text_color, font=font, anchor="mm")

def draw_swatches_grid(draw, base_x, base_y, max_w, font, text_color=None, swatch_w=20, swatch_h=11):
    """Draw official color calibration swatches in a neat 2x2 grid."""
    swatches = [
        (BLUSH_PINK, "Petal Blush #F5B7C2"),
        (IMPERIAL_BURGUNDY, "Wine Burgundy #76122E"),
        (LUXOR_GOLD, "Luxor Gold #DAAC36"),
        (WARM_IVORY, "Warm Ivory #FFF5F7"),
    ]
    col_w = max(max_w // 2, 125)
    for idx, (color, name) in enumerate(swatches):
        row = idx // 2
        col = idx % 2
        sx = base_x + col * col_w
        sy = base_y + row * (swatch_h + 5)
        lbl_col = text_color if text_color else (LUXOR_GOLD if color in [BLUSH_PINK, LUXOR_GOLD] else WARM_IVORY)
        draw.rectangle([sx, sy, sx + swatch_w, sy + swatch_h], fill=color, outline=LUXOR_GOLD, width=1)
        draw.text((sx + swatch_w + 5, sy + swatch_h // 2), name, fill=lbl_col, font=font, anchor="lm")

def generate_tamper_ribbon(output_dir="output/dielines", logo_img=None):
    """
    Generate dieline_tamper_ribbon_crown.png:
    - 450 × 1125 px @ 254 DPI (18mm × 45mm physical).
    - Background: Strictly Petal Blush Pink (245, 183, 194).
    - All typography strictly in Deep Wine Burgundy (#76122E) for high contrast and legibility.
    - Embossed Luxor Gold (218, 172, 54) crown crest in the center medallion.
    - Perforation break score guide at lid junction.
    - Authentic Mariam cursive logo tinted in Deep Wine Burgundy (#76122E).
    """
    w, h = 450, 1125
    im = Image.new("RGBA", (w, h), (*BLUSH_PINK, 255))
    draw = ImageDraw.Draw(im)
    
    # 1. Outer die-cut gold border with 18px inset
    draw.rounded_rectangle([18, 18, w - 18, h - 18], radius=18, outline=LUXOR_GOLD, width=3)
    
    # 2. Inner safety guide line (28px inset) in Deep Wine Burgundy
    draw.rounded_rectangle([28, 28, w - 28, h - 28], radius=14, outline=IMPERIAL_BURGUNDY, width=1)
    
    # 3. Four corner registration crosshairs
    draw_crosshair(draw, 18, 18, size=14, color=LUXOR_GOLD)
    draw_crosshair(draw, w - 18, 18, size=14, color=LUXOR_GOLD)
    draw_crosshair(draw, 18, h - 18, size=14, color=LUXOR_GOLD)
    draw_crosshair(draw, w - 18, h - 18, size=14, color=LUXOR_GOLD)
    
    # Fonts
    title_font = load_font(17, bold=True)
    sub_font = load_font(13, bold=True)
    meta_font = load_font(11, bold=False)
    bold_meta_font = load_font(11, bold=True)
    small_font = load_font(9, bold=False)
    
    # ==================== TOP ZONE: METALLIC LID ADHERENCE ====================
    draw.text((w // 2, 45), "MARIAM PACKAGING BLUEPRINT", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, 68), "TAMPER-EVIDENT RIBBON", fill=IMPERIAL_BURGUNDY, font=title_font, anchor="mm")
    draw.text((w // 2, 90), "18mm x 45mm @ 254 DPI", fill=IMPERIAL_BURGUNDY, font=meta_font, anchor="mm")
    
    # Top decorative horizontal gold bar
    draw.line([(45, 108), (w - 45, 108)], fill=LUXOR_GOLD, width=2)
    
    # Scaled authentic cursive logo tinted in Deep Wine Burgundy for high legibility
    if logo_img:
        burgundy_logo = get_tinted_logo(logo_img, IMPERIAL_BURGUNDY)
        lw, lh = burgundy_logo.size
        scale = min(260 / lw, 95 / lh)
        nw, nh = int(lw * scale), int(lh * scale)
        scaled_logo = burgundy_logo.resize((nw, nh), Image.Resampling.LANCZOS)
        im.alpha_composite(scaled_logo, (w // 2 - nw // 2, 128))
        
    draw.text((w // 2, 245), "NATURAL HONEY & SUPERFOODS", fill=IMPERIAL_BURGUNDY, font=sub_font, anchor="mm")
    draw.text((w // 2, 270), "Pure Goodness, Naturally.", fill=IMPERIAL_BURGUNDY, font=meta_font, anchor="mm")
    draw.text((w // 2, 310), "[ METALLIC LID ADHERENCE ZONE ]", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, 330), "Firm adhesive bond across twist cap surface", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    
    # Vertical guideline down towards center
    draw_dashed_line(draw, (w // 2, 355), (w // 2, 435), fill=IMPERIAL_BURGUNDY, width=1, dash_length=6, gap_length=4)
    
    # ==================== CENTER ZONE: CROWN CREST & PERFORATION ====================
    cy_mid = 562
    
    # Perforation Score Line across ribbon
    draw_dashed_line(draw, (30, cy_mid), (w - 30, cy_mid), fill=IMPERIAL_BURGUNDY, width=2, dash_length=8, gap_length=4)
    draw.text((w // 2, cy_mid - 118), "-- PERFORATION BREAK SCORE --", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    
    # Center Medallion
    medallion_r = 95
    # Outer gold ring
    draw.ellipse([w // 2 - medallion_r, cy_mid - medallion_r, w // 2 + medallion_r, cy_mid + medallion_r],
                 fill=BLUSH_PINK, outline=LUXOR_GOLD, width=3)
    # Inner gold ring
    draw.ellipse([w // 2 - medallion_r + 6, cy_mid - medallion_r + 6, w // 2 + medallion_r - 6, cy_mid + medallion_r - 6],
                 outline=LUXOR_GOLD, width=1)
                 
    # Medallion Header
    draw.text((w // 2, cy_mid - 62), "MARIAM ROYAL SEAL", fill=IMPERIAL_BURGUNDY, font=sub_font, anchor="mm")
    
    # Embossed Luxor Gold Crown Crest in center of medallion
    draw_crown(draw, cx=w // 2, cy=cy_mid - 2, width=110, height=58, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
    
    # Medallion Subtext
    draw.text((w // 2, cy_mid + 56), "- AUTHENTIC & PURE -", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, cy_mid + 74), "TAMPER EVIDENT", fill=IMPERIAL_BURGUNDY, font=bold_meta_font, anchor="mm")
    
    # ==================== BOTTOM ZONE: SHOULDER GLASS ANCHOR ====================
    draw_dashed_line(draw, (w // 2, cy_mid + 115), (w // 2, cy_mid + 175), fill=IMPERIAL_BURGUNDY, width=1, dash_length=6, gap_length=4)
    
    draw.text((w // 2, 755), "[ FLINT GLASS ANCHOR ZONE ]", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, 778), "SECURED TO FLINT GLASS SHOULDER", fill=IMPERIAL_BURGUNDY, font=sub_font, anchor="mm")
    
    draw.text((w // 2, 825), "DO NOT ACCEPT IF SEAL IS BROKEN", fill=IMPERIAL_BURGUNDY, font=sub_font, anchor="mm")
    draw.text((w // 2, 852), "إذا كان الختم مكسوراً لا تقبل العبوة", fill=IMPERIAL_BURGUNDY, font=meta_font, anchor="mm")
    draw.text((w // 2, 885), "Single-Harvest Terroir Guarantee", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    
    # Technical specs
    draw.text((w // 2, 925), "Substrate: Fasson Estate Velvet 90gsm", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, 945), "Adhesive: Permanent Acrylic High-Tack", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, 965), "Finish: Kurz Luxor Gold Hot Foil Stamping", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    
    # Bottom decorative gold bar
    draw.line([(45, 995), (w - 45, 995)], fill=LUXOR_GOLD, width=2)
    
    # Swatches on bottom of ribbon - labels strictly in Deep Wine Burgundy
    sw_y = 1025
    draw.rectangle([50, sw_y, 75, sw_y + 12], fill=BLUSH_PINK, outline=LUXOR_GOLD, width=1)
    draw.text((82, sw_y + 6), "#F5B7C2", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="lm")
    
    draw.rectangle([175, sw_y, 200, sw_y + 12], fill=LUXOR_GOLD, outline=IMPERIAL_BURGUNDY, width=1)
    draw.text((207, sw_y + 6), "#DAAC36", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="lm")
    
    draw.rectangle([300, sw_y, 325, sw_y + 12], fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=1)
    draw.text((332, sw_y + 6), "#76122E", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="lm")
    
    out_path = os.path.join(output_dir, "dieline_tamper_ribbon_crown.png")
    im.save(out_path)
    print(f"Generated: {out_path} ({w}x{h} px)")
    return out_path

def generate_horizontal_dieline(config, catalog_data, output_dir="output/dielines", logo_img=None, producer_img=None):
    """
    Generate horizontal 3-zone print dieline:
    - Outer cut border with registration crosshairs
    - Inner safety guide
    - Zone 1 (Left 28%): Regulatory / Nutrition / Allergen / Warning / Color Calibration Swatches
    - Zone 2 (Center 44%): Blueprint Header / Hero Brand / Authentic Cursive Logo / Descriptor / Title / Sensory Triad
    - Zone 3 (Right 28%): Terroir / Logistics / Barcode / Producer Emblem / Certifications
    """
    filename = config["filename"]
    w = config["width"]
    h = config["height"]
    physical = config["physical"]
    sku_id = config.get("sku_id")
    bg_color = config.get("bg_color", IMPERIAL_BURGUNDY)
    special_mode = config.get("special_mode")
    is_royal = (special_mode == "royal_mix")
    
    # Retrieve SKU data if available
    sku_info = None
    if catalog_data and sku_id:
        for fam in catalog_data.get("families", []):
            for item in fam.get("items", []):
                if item.get("sku") == sku_id:
                    sku_info = item
                    break
            if sku_info:
                break
                
    im = Image.new("RGBA", (w, h), (*bg_color, 255))
    draw = ImageDraw.Draw(im)
    
    scale_ref = min(w, h)
    
    # 1. Outer die-cut gold border with 30px inset (20px for petite 400px height)
    outer_inset = 30 if h >= 600 else 20
    draw.rounded_rectangle([outer_inset, outer_inset, w - outer_inset, h - outer_inset],
                           radius=25 if h >= 600 else 15, outline=LUXOR_GOLD, width=4 if h >= 600 else 3)
                           
    # 2. Inner thin ivory safety guide with 45px inset (30px for petite)
    inner_inset = 45 if h >= 600 else 30
    draw.rounded_rectangle([inner_inset, inner_inset, w - inner_inset, h - inner_inset],
                           radius=20 if h >= 600 else 12, outline=WARM_IVORY, width=2)
                           
    # 3. Registration Crosshairs at 4 corners
    cross_size = 18 if h >= 600 else 14
    draw_crosshair(draw, outer_inset, outer_inset, size=cross_size, color=LUXOR_GOLD)
    draw_crosshair(draw, w - outer_inset, outer_inset, size=cross_size, color=LUXOR_GOLD)
    draw_crosshair(draw, outer_inset, h - outer_inset, size=cross_size, color=LUXOR_GOLD)
    draw_crosshair(draw, w - outer_inset, h - outer_inset, size=cross_size, color=LUXOR_GOLD)
    
    # 4. Grid dividers: Zone 1 (28%), Zone 2 (44%), Zone 3 (28%)
    cx0 = int(w * 0.28)
    cx1 = int(w * 0.72)
    draw.line([(cx0, inner_inset), (cx0, h - inner_inset)], fill=LUXOR_GOLD, width=2)
    draw.line([(cx1, inner_inset), (cx1, h - inner_inset)], fill=LUXOR_GOLD, width=2)
    
    # Font scales based on dieline dimensions
    title_font = load_font(max(15, int(scale_ref * 0.034)), bold=True)
    sub_font = load_font(max(12, int(scale_ref * 0.022)), bold=False)
    meta_font = load_font(max(10, int(scale_ref * 0.017)), bold=False)
    bold_meta_font = load_font(max(10, int(scale_ref * 0.017)), bold=True)
    section_font = load_font(max(12, int(scale_ref * 0.022)), bold=True)
    hero_font = load_font(max(18, int(scale_ref * 0.042)), bold=True)
    small_font = load_font(max(9, int(scale_ref * 0.014)), bold=False)
    
    # ==================== ZONE 2: CENTER HERO BRANDING ====================
    # A. TOP BLUEPRINT HEADER (Positioned cleanly at top of Zone 2, above the packaging graphic)
    header_top = inner_inset + (18 if h >= 600 else 10)
    draw.text((w // 2, header_top), "MARIAM LUXURY PACKAGING BLUEPRINT", fill=LUXOR_GOLD, font=bold_meta_font, anchor="mm")
    
    product_title = config.get("title", "MARIAM NATURAL HONEY")
    draw.text((w // 2, header_top + 22), product_title, fill=WARM_IVORY, font=sub_font, anchor="mm")
    
    spec_line = f"SPECIFICATION: {physical} • {w}x{h} px @ 254 DPI"
    draw.text((w // 2, header_top + 42), spec_line, fill=LUXOR_GOLD, font=small_font, anchor="mm")
    
    # Subtle dashed divider line separating blueprint header from packaging art
    art_y_top = header_top + 58
    draw_dashed_line(draw, (cx0 + 40, art_y_top), (cx1 - 40, art_y_top), fill=LUXOR_GOLD, width=1, dash_length=6, gap_length=4)
    
    # B. BOTTOM BLUEPRINT FOOTER (Positioned safely above bottom inner margin)
    footer_y = h - inner_inset - (18 if h >= 600 else 12)
    draw.text((w // 2, footer_y), "[ CENTRAL LUXURY BRANDING & EMBOSS PANEL ]", fill=WARM_IVORY, font=small_font, anchor="mm")
    art_y_bottom = footer_y - 18
    
    # C. PACKAGING ART IN ZONE 2 (Between art_y_top + 15 and art_y_bottom)
    avail_h = art_y_bottom - (art_y_top + 15)
    
    if is_royal:
        # ================= ROYAL MIX SCALLOPED BAROQUE CARTOUCHE =================
        # Exactly sized and proportioned to match the authentic reference photo:
        cart_w = min(cx1 - cx0 - 80, 680)
        cart_h = min(avail_h - 10, 530)
        cart_cx = w // 2
        cart_cy = (art_y_top + 15 + art_y_bottom) // 2
        
        c_x0 = cart_cx - cart_w // 2
        c_x1 = cart_cx + cart_w // 2
        c_y0 = cart_cy - cart_h // 2
        c_y1 = cart_cy + cart_h // 2
        
        # Draw Scalloped Baroque Cartouche with concave corner cutouts
        cart_r = max(24, int(cart_w * 0.055))
        cart_arch = max(16, int(cart_h * 0.045))
        pts_outer = get_scalloped_cartouche_polygon(c_x0, c_y0, c_x1, c_y1, r=cart_r, arch_h=cart_arch)
        draw.polygon(pts_outer, fill=BLUSH_PINK, outline=LUXOR_GOLD, width=3)
        
        # Inner thin gold pinstripe
        pts_inner = get_scalloped_cartouche_polygon(c_x0 + 7, c_y0 + 7, c_x1 - 7, c_y1 - 7, r=cart_r - 4, arch_h=cart_arch - 2)
        draw.polygon(pts_inner, outline=LUXOR_GOLD, width=1)
        
        # 1. Royal Crown Crest at top of cartouche
        crown_w = min(80, int(cart_w * 0.14))
        crown_h = int(crown_w * 0.52)
        crown_cy = c_y0 + cart_arch + crown_h // 2 + 16
        draw_crown(draw, cx=cart_cx, cy=crown_cy, width=crown_w, height=crown_h, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
        
        # 2. Authentic Mariam cursive logo tinted in Deep Wine Burgundy (#76122E)
        if logo_img:
            burgundy_logo = get_tinted_logo(logo_img, IMPERIAL_BURGUNDY)
            lw, lh = burgundy_logo.size
            max_lw = min(cart_w - 90, 360)
            max_lh = min(int(cart_h * 0.24), 130)
            scale = min(max_lw / lw, max_lh / lh)
            nw, nh = int(lw * scale), int(lh * scale)
            scaled_logo = burgundy_logo.resize((nw, nh), Image.Resampling.LANCZOS)
            logo_y = crown_cy + crown_h // 2 + 12
            im.alpha_composite(scaled_logo, (cart_cx - nw // 2, logo_y))
            next_y = logo_y + nh + 14
        else:
            next_y = crown_cy + crown_h // 2 + 40
            
        # 3. Sub-Brand Descriptor: NATURAL HONEY & SUPERFOODS
        draw.text((cart_cx, next_y), "NATURAL HONEY & SUPERFOODS", fill=IMPERIAL_BURGUNDY, font=bold_meta_font, anchor="mm")
        next_y += 28
        
        # 4. Product Hero Title: MARIAM ROYAL MIX
        draw.text((cart_cx, next_y), "MARIAM ROYAL MIX", fill=IMPERIAL_BURGUNDY, font=hero_font, anchor="mm")
        next_y += 26
        
        # 5. Arabic Subhead
        draw.text((cart_cx, next_y), "الخلطة الملكية الفاخرة • عسل طبيعي ومكسرات وغذاء ملكات", fill=IMPERIAL_BURGUNDY, font=meta_font, anchor="mm")
        next_y += 32
        
        # 6. Hero Distinction Ribbon: 0% PEANUTS • 100% TREE NUTS • 5% ROYAL JELLY
        ribbon_w = min(cart_w - 60, 480)
        ribbon_h = 28
        draw.rounded_rectangle([cart_cx - ribbon_w // 2, next_y - ribbon_h // 2,
                                cart_cx + ribbon_w // 2, next_y + ribbon_h // 2],
                               radius=6, fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=1)
        draw.text((cart_cx, next_y), "• 0% PEANUTS • 100% TREE NUTS • 5% ROYAL JELLY •",
                  fill=WARM_IVORY, font=bold_meta_font, anchor="mm")
        next_y += 30
        
        # 7. Sensory Triad
        triad = config.get("triad", "Crunchy • Opulent • Energizing")
        draw.text((cart_cx, next_y), triad, fill=IMPERIAL_BURGUNDY, font=meta_font, anchor="mm")
        next_y += 24
        
        # 8. Delicate Gold Filigree Divider
        draw.line([(cart_cx - 60, next_y), (cart_cx - 10, next_y)], fill=LUXOR_GOLD, width=1)
        draw.line([(cart_cx + 10, next_y), (cart_cx + 60, next_y)], fill=LUXOR_GOLD, width=1)
        draw.ellipse([cart_cx - 3, next_y - 3, cart_cx + 3, next_y + 3], fill=LUXOR_GOLD)
        next_y += 24
        
        # 9. Net Weight
        weight_str = config.get("weight", "Net Wt. 500g e (17.6 oz)")
        draw.text((cart_cx, next_y), weight_str, fill=IMPERIAL_BURGUNDY, font=bold_meta_font, anchor="mm")
        
    else:
        # ================= STANDARD HONEY / HONEYCOMB / FLIGHT PANEL =================
        panel_w = cx1 - cx0 - 80
        panel_cx = w // 2
        p_x0 = panel_cx - panel_w // 2
        p_x1 = panel_cx + panel_w // 2
        
        # Proportional frame height centered in Zone 2
        panel_h = min(avail_h - 10, int(scale_ref * 0.62)) if h >= 600 else avail_h - 5
        panel_cy = (art_y_top + 15 + art_y_bottom) // 2
        p_y0 = panel_cy - panel_h // 2
        p_y1 = panel_cy + panel_h // 2
        
        # Double gold rounded frame
        draw.rounded_rectangle([p_x0, p_y0, p_x1, p_y1], radius=18, outline=LUXOR_GOLD, width=2)
        draw.rounded_rectangle([p_x0 + 6, p_y0 + 6, p_x1 - 6, p_y1 - 6], radius=14, outline=LUXOR_GOLD, width=1)
        
        # 1. Crown Crest at top
        crown_w = min(75, int(panel_w * 0.12))
        crown_h = int(crown_w * 0.52)
        crown_cy = p_y0 + (40 if h >= 600 else 24)
        draw_crown(draw, cx=panel_cx, cy=crown_cy, width=crown_w, height=crown_h, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
        
        # 2. Authentic Mariam Cursive Gold Logo
        if logo_img:
            lw, lh = logo_img.size
            max_lw = min(panel_w - 80, 380)
            max_lh = min(int(panel_h * 0.26), 140)
            scale = min(max_lw / lw, max_lh / lh)
            nw, nh = int(lw * scale), int(lh * scale)
            scaled_logo = logo_img.resize((nw, nh), Image.Resampling.LANCZOS)
            logo_y = crown_cy + crown_h // 2 + (12 if h >= 600 else 8)
            im.alpha_composite(scaled_logo, (panel_cx - nw // 2, logo_y))
            next_y = logo_y + nh + (16 if h >= 600 else 8)
        else:
            next_y = crown_cy + crown_h // 2 + 40
            
        # 3. Sub-Brand Descriptor: NATURAL HONEY & SUPERFOODS
        draw.text((panel_cx, next_y), "NATURAL HONEY & SUPERFOODS", fill=WARM_IVORY, font=bold_meta_font, anchor="mm")
        next_y += (28 if h >= 600 else 18)
        
        # 4. Hero Product Title
        hero_title = config.get("hero_title", product_title)
        draw.text((panel_cx, next_y), hero_title, fill=LUXOR_GOLD, font=hero_font, anchor="mm")
        next_y += (28 if h >= 600 else 20)
        
        # 5. Hexagon icon if Honeycomb format
        if special_mode == "hex":
            draw_hexagon(draw, panel_cx, next_y, radius=14, outline=LUXOR_GOLD, width=2)
            draw_hexagon(draw, panel_cx, next_y, radius=9, outline=WARM_IVORY, width=1)
            next_y += 24
            
        # 6. Subtitle / Terroir Descriptor
        subtitle = config.get("subtitle", "Pure Single-Origin Natural Honey")
        draw.text((panel_cx, next_y), subtitle, fill=WARM_IVORY, font=meta_font, anchor="mm")
        next_y += (30 if h >= 600 else 20)
        
        # 7. Sensory Triad Pill Badge
        triad = config.get("triad", "Pure • Natural • Golden")
        triad_w = min(panel_w - 100, int(len(triad) * scale_ref * 0.014) + 60)
        triad_h = 26 if h >= 600 else 20
        draw.rounded_rectangle([panel_cx - triad_w // 2, next_y - triad_h // 2,
                                panel_cx + triad_w // 2, next_y + triad_h // 2],
                               radius=6, fill=DEEP_BURGUNDY, outline=LUXOR_GOLD, width=1)
        draw.text((panel_cx, next_y), triad, fill=LUXOR_GOLD, font=bold_meta_font, anchor="mm")
        next_y += (30 if h >= 600 else 20)
        
        # 8. Delicate Gold Divider (for tall labels)
        if h >= 600:
            draw.line([(panel_cx - 50, next_y), (panel_cx - 10, next_y)], fill=LUXOR_GOLD, width=1)
            draw.line([(panel_cx + 10, next_y), (panel_cx + 50, next_y)], fill=LUXOR_GOLD, width=1)
            draw.ellipse([panel_cx - 3, next_y - 3, panel_cx + 3, next_y + 3], fill=LUXOR_GOLD)
            next_y += 24
            
        # 9. Net Weight
        weight_str = config.get("weight", "Net Wt. 500g (17.6 oz)")
        draw.text((panel_cx, next_y), weight_str, fill=WARM_IVORY, font=bold_meta_font, anchor="mm")
        
    # ==================== ZONE 1: REGULATORY & NUTRITION ====================
    left_cx = (inner_inset + cx0) // 2
    z1_top = inner_inset + (20 if h >= 600 else 12)
    draw.text((left_cx, z1_top), "ZONE 1: REGULATORY & NUTRITION", fill=LUXOR_GOLD, font=section_font, anchor="mm")
    
    nbox_x0 = inner_inset + 18
    nbox_x1 = cx0 - 18
    nbox_y0 = z1_top + (24 if h >= 600 else 16)
    nbox_h = int(scale_ref * 0.28) if h >= 600 else int(scale_ref * 0.24)
    nbox_y1 = nbox_y0 + nbox_h
    
    # Nutrition Facts Box
    draw.rectangle([nbox_x0, nbox_y0, nbox_x1, nbox_y1], outline=WARM_IVORY, width=1)
    draw.text((nbox_x0 + 10, nbox_y0 + 12), "NUTRITION FACTS / VALEUR NUTRITIVE", fill=LUXOR_GOLD, font=bold_meta_font, anchor="lm")
    draw.line([(nbox_x0, nbox_y0 + 22), (nbox_x1, nbox_y0 + 22)], fill=WARM_IVORY, width=1)
    
    nut_lines = config.get("nutrition", [
        "Serving Size / Portion: 20g (1 tbsp)",
        "Calories / Energie: 61 kcal (304 kcal / 100g)",
        "Total Fat / Lipides: 0g (0% DV)",
        "Total Carbohydrate / Glucides: 16.5g (82g / 100g)",
        "  Sugars / Sucres: 16.4g (82g / 100g)",
        "Protein / Proteines: 0.1g",
        "Sodium / Sel: 1mg (<1% DV)"
    ])
    
    line_y = nbox_y0 + 36
    spacing = int((nbox_h - 44) / max(len(nut_lines), 1))
    for nl in nut_lines:
        draw.text((nbox_x0 + 10, line_y), nl, fill=WARM_IVORY, font=small_font, anchor="lm")
        line_y += spacing
        
    # Ingredients List
    ing_top = nbox_y1 + (12 if h >= 600 else 8)
    draw.text((nbox_x0, ing_top), "INGREDIENTS / INGREDIENTS:", fill=LUXOR_GOLD, font=bold_meta_font, anchor="lm")
    
    ingredients_str = config.get("ingredients", "100% Pure Raw Natural Honey.")
    words = ingredients_str.split(" ")
    lines = []
    cur_line = ""
    max_line_len = 44 if w >= 2200 else 32
    for word in words:
        if len(cur_line) + len(word) + 1 <= max_line_len:
            cur_line += (" " if cur_line else "") + word
        else:
            lines.append(cur_line)
            cur_line = word
    if cur_line:
        lines.append(cur_line)
        
    cur_ing_y = ing_top + 16
    max_ing_lines = 4 if h >= 600 else 2
    for l in lines[:max_ing_lines]:
        draw.text((nbox_x0, cur_ing_y), l, fill=WARM_IVORY, font=small_font, anchor="lm")
        cur_ing_y += 14
        
    # Allergen and Warnings
    warn_y = cur_ing_y + 10
    allergen_text = config.get("allergens", "Allergens: None. Pure Natural Honey.")
    draw.text((nbox_x0, warn_y), allergen_text, fill=BLUSH_PINK, font=bold_meta_font, anchor="lm")
    draw.text((nbox_x0, warn_y + 16), "Infant Warning: Not for infants under 12 months.", fill=WARM_IVORY, font=small_font, anchor="lm")
    if h >= 600:
        draw.text((nbox_x0, warn_y + 32), "Storage: Store at room temperature away from sunlight.", fill=WARM_IVORY, font=small_font, anchor="lm")
    
    # Swatches inside Zone 1 at bottom
    swatch_y = h - inner_inset - 36
    draw_swatches_grid(draw, nbox_x0, swatch_y, cx0 - nbox_x0, small_font)
    
    # ==================== ZONE 3: ORIGIN & LOGISTICS ====================
    right_cx = (cx1 + w - inner_inset) // 2
    z3_top = inner_inset + (20 if h >= 600 else 12)
    draw.text((right_cx, z3_top), "ZONE 3: ORIGIN & LOGISTICS", fill=LUXOR_GOLD, font=section_font, anchor="mm")
    
    rbox_x0 = cx1 + 18
    rbox_x1 = w - inner_inset - 18
    
    # Single-Estate Terroir Notes
    cur_r_y = z3_top + 28
    draw.text((rbox_x0, cur_r_y), "SINGLE-ESTATE TERROIR:", fill=LUXOR_GOLD, font=bold_meta_font, anchor="lm")
    terroir_str = config.get("terroir", "Estate Grown Mediterranean Terroir")
    draw.text((rbox_x0, cur_r_y + 18), terroir_str, fill=WARM_IVORY, font=small_font, anchor="lm")
    draw.text((rbox_x0, cur_r_y + 34), "Direct From Hive to Jar • Cold Extracted", fill=WARM_IVORY, font=small_font, anchor="lm")
    
    # Producer Logo & Details
    cur_r_y += 58
    draw.text((rbox_x0, cur_r_y), "PRODUCED & PACKED BY:", fill=LUXOR_GOLD, font=bold_meta_font, anchor="lm")
    draw.text((rbox_x0, cur_r_y + 18), "Khaeer Alwadi (خير الوادي)", fill=WARM_IVORY, font=sub_font, anchor="lm")
    
    if producer_img and h >= 600:
        pw, ph = producer_img.size
        pscale = min(150 / pw, 55 / ph)
        pnw, pnh = int(pw * pscale), int(ph * pscale)
        scaled_prod = producer_img.resize((pnw, pnh), Image.Resampling.LANCZOS)
        im.alpha_composite(scaled_prod, (rbox_x1 - pnw, cur_r_y - 10))
        
    # EAN-13 Barcode Mockup
    cur_r_y += 50
    barcode_w = min(rbox_x1 - rbox_x0, 270)
    barcode_h = int(scale_ref * 0.10)
    draw_barcode(draw, rbox_x0, cur_r_y, barcode_w, barcode_h,
                 config.get("barcode", "6 281001 029101"),
                 bar_color=LUXOR_GOLD, text_color=WARM_IVORY, font=small_font)
                 
    # Quality & Compliance Badges (using bullet '•' to prevent missing glyphs)
    cur_r_y += barcode_h + 18
    badges = config.get("badges", [
        "• 100% Raw & Unpasteurized",
        "• Cold Extracted Single-Harvest",
        "• Zero Additives or Sugars",
        "• Recyclable Flint Glass"
    ])
    max_badges = 4 if h >= 600 else 2
    for b in badges[:max_badges]:
        draw.text((rbox_x0, cur_r_y), b, fill=WARM_IVORY, font=small_font, anchor="lm")
        cur_r_y += 16
        
    draw.text((rbox_x0, cur_r_y + 4), "LOT: MHM-2609 • EXP: 09/2029", fill=LUXOR_GOLD, font=bold_meta_font, anchor="lm")
    
    out_path = os.path.join(output_dir, filename)
    im.save(out_path)
    print(f"Generated: {out_path} ({w}x{h} px)")
    return out_path

def generate_all_dielines(output_dir="output/dielines"):
    """
    Main generator for all 6 Mariam Honey & Superfoods dielines.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Load catalog data
    catalog_path = "data/mariam_honey_catalog.json"
    catalog_data = None
    if os.path.exists(catalog_path):
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                catalog_data = json.load(f)
        except Exception as e:
            print(f"Notice: Could not load catalog data ({e})")
            
    # Load authentic cursive gold logo
    logo_path = "arina-logo-gold.png" if os.path.exists("arina-logo-gold.png") else "mariam-logo-gold.png"
    logo_img = None
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path).convert("RGBA")
        except Exception as e:
            print(f"Notice: Could not load logo ({e})")
            
    # Load producer emblem
    prod_path = "khaeer-alwadi-logo-gold.png"
    producer_img = None
    if os.path.exists(prod_path):
        try:
            producer_img = Image.open(prod_path).convert("RGBA")
        except Exception as e:
            print(f"Notice: Could not load producer logo ({e})")

    # Specifications for the 5 horizontal dielines
    horizontal_configs = [
        {
            "filename": "dieline_honey_500g_standard.png",
            "width": 2200,
            "height": 900,
            "physical": "220mm x 90mm",
            "sku_id": "SKU-H03",
            "title": "MARIAM MOUNTAIN SIDR HONEY — 500G JAR",
            "hero_title": "MOUNTAIN SIDR HONEY",
            "subtitle": "Royal Reserve Wild Mountain Sidr (Ziziphus)",
            "triad": "Rich • Velvety • Raw",
            "weight": "Net Wt. 500g (17.6 oz)",
            "barcode": "6 281001 029103",
            "terroir": "Untouched Highland Valleys & Mountain Slopes",
            "ingredients": "100% Pure Wild Mountain Sidr (Ziziphus spina-christi) Honey.",
            "allergens": "Allergens: None. 100% Pure Raw Honey.",
            "special_mode": "standard",
            "nutrition": [
                "Serving Size / Portion: 20g (1 tbsp)",
                "Calories / Energie: 61 kcal (304 kcal / 100g)",
                "Total Fat / Lipides: 0g (0% DV)",
                "Total Carbohydrate / Glucides: 16.5g (82.4g / 100g)",
                "  Sugars / Sucres: 16.4g (82.1g / 100g)",
                "Protein / Proteines: 0.1g (0.3g / 100g)",
                "Sodium / Sel: < 1mg (<1% DV)"
            ],
            "badges": [
                "• 100% Pure Monofloral Mountain Sidr",
                "• Unpasteurized & Cold Extracted",
                "• High Antibacterial & Enzyme Potency",
                "• Ultra-Clear Flint Glass Jar"
            ]
        },
        {
            "filename": "dieline_honey_1kg_family.png",
            "width": 2600,
            "height": 1100,
            "physical": "260mm x 110mm",
            "sku_id": "SKU-H01",
            "title": "MARIAM CLOVER HONEY — 1KG FAMILY SIZE",
            "hero_title": "PURE CLOVER HONEY",
            "subtitle": "Pure Monofloral Clover Blossom Honey • Family Bulk Size",
            "triad": "Delicate • Floral • Pure",
            "weight": "Net Wt. 1kg (1000g / 35.2 oz)",
            "barcode": "6 281001 029101",
            "terroir": "Lush Mediterranean River Plains & Wild Meadows",
            "ingredients": "100% Pure Natural Clover Blossom Honey.",
            "allergens": "Allergens: None. Pure Natural Honey.",
            "special_mode": "standard",
            "nutrition": [
                "Serving Size / Portion: 20g (1 tbsp)",
                "Calories / Energie: 61 kcal (304 kcal / 100g)",
                "Total Fat / Lipides: 0g (0% DV)",
                "Total Carbohydrate / Glucides: 16.4g (82g / 100g)",
                "  Sugars / Sucres: 16.4g (82g / 100g)",
                "Protein / Proteines: 0.1g (0.3g / 100g)",
                "Sodium / Sel: 1mg (<1% DV)"
            ],
            "badges": [
                "• 100% Pure Natural Clover Honey",
                "• Family Bulk Reserve • 1000g Standard",
                "• Unpasteurized & Cold Extracted",
                "• Recyclable Heavy Flint Glass"
            ]
        },
        {
            "filename": "dieline_royal_mix_500g_wide.png",
            "width": 2400,
            "height": 850,
            "physical": "240mm x 85mm",
            "sku_id": "SKU-SF01",
            "title": "MARIAM ROYAL MIX — 500G WIDE-MOUTH JAR",
            "hero_title": "MARIAM ROYAL MIX",
            "subtitle": "Natural Honey with Selected Tree Nuts, Super Seeds & Royal Jelly",
            "triad": "Crunchy • Opulent • Energizing",
            "weight": "Net Wt. 500g (17.6 oz)",
            "barcode": "6 281001 029201",
            "terroir": "Estate Grown Mediterranean Terroir & Highland Apiaries",
            "ingredients": "Pure Mountain Honey (55%), Fresh Royal Jelly (5%), Raw Pistachios (8%), Cashews (7%), Almonds (5%), Walnuts (5%), Pumpkin Seeds (4%), Chia Seeds (3%), Flaxseeds (3%), Sesame (3%), Nigella Seeds (2%).",
            "allergens": "ALLERGENS: CONTAINS TREE NUTS & SESAME. STRICT 0% PEANUTS.",
            "special_mode": "royal_mix",
            "nutrition": [
                "Serving Size / Portion: 30g (2 tbsp)",
                "Calories / Energie: 135 kcal (449 kcal / 100g)",
                "Total Fat / Lipides: 5.0g (Saturated: 0.6g)",
                "Total Carbohydrate / Glucides: 15.6g (Sugars: 14.4g)",
                "Dietary Fiber / Fibres: 1.7g",
                "Protein / Proteines: 2.5g (8.2g / 100g)",
                "Sodium / Sel: 4mg (<1% DV)"
            ],
            "badges": [
                "• 0% Peanuts Policy — Exclusively Tree Nuts & Seeds",
                "• Fortified with 5% Fresh Queen Bee Royal Jelly",
                "• Rich in Plant Protein, Omega-3 & Zinc",
                "• 12mm Solid Base Glass Jar Architecture"
            ]
        },
        {
            "filename": "dieline_honeycomb_500g_hex.png",
            "width": 1800,
            "height": 900,
            "physical": "180mm x 90mm",
            "sku_id": "SKU-H06",
            "title": "RAW HONEYCOMB IN HONEY — 500G HEX JAR",
            "hero_title": "RAW HONEYCOMB IN HONEY",
            "subtitle": "Fresh Natural Hexagonal Comb Immersed in Pure Raw Honey",
            "triad": "Raw • Hexagonal • Unfiltered",
            "weight": "Net Wt. 500g (17.6 oz)",
            "barcode": "6 281001 029106",
            "terroir": "Artisanal Certified Apiaries — Direct Hive to Jar",
            "ingredients": "100% Pure Raw Natural Honey, 100% Virgin Natural Beeswax Honeycomb Section.",
            "allergens": "Allergens: None. 100% Edible Natural Beeswax.",
            "special_mode": "hex",
            "nutrition": [
                "Serving Size / Portion: 20g (1 tbsp)",
                "Calories / Energie: 61 kcal (304 kcal / 100g)",
                "Total Fat / Lipides: 0g (0% DV)",
                "Total Carbohydrate / Glucides: 16.4g (82.2g / 100g)",
                "  Sugars / Sucres: 16.4g (82.0g / 100g)",
                "Protein / Proteines: 0.1g (0.3g / 100g)",
                "Sodium / Sel: 1mg (<1% DV)"
            ],
            "badges": [
                "• Direct From Hive to Jar Without Processing",
                "• Naturally Contains Bee Propolis & Enzymes",
                "• 100% Edible Natural Virgin Comb",
                "• Faceted Hexagonal Glass Showpiece"
            ]
        },
        {
            "filename": "dieline_discovery_flight_50g.png",
            "width": 1200,
            "height": 400,
            "physical": "120mm x 40mm",
            "sku_id": "SKU-GF01",
            "title": "DISCOVERY FLIGHT — 50G PETITE TASTING JAR",
            "hero_title": "DISCOVERY TASTING FLIGHT",
            "subtitle": "Curated Tasting Flight of 6 Rare Artisanal Varieties (6 x 50g)",
            "triad": "Curated • Elegant • Complete",
            "weight": "Net Wt. 50g (1.76 oz)",
            "barcode": "6 281001 029301",
            "terroir": "Across 6 Protected Mediterranean Terroirs",
            "ingredients": "100% Pure Raw Mediterranean Artisan Honey Varieties.",
            "allergens": "Allergens: None. 100% Pure Raw Honey.",
            "special_mode": "flight",
            "nutrition": [
                "Serving Size / Portion: 20g (1 tbsp)",
                "Calories / Energie: 61 kcal (304 kcal / 100g)",
                "Total Fat / Lipides: 0g (0% DV)",
                "Total Carbohydrate / Glucides: 16.4g (82g / 100g)",
                "Protein / Proteines: 0.1g",
                "Sodium / Sel: < 1mg"
            ],
            "badges": [
                "• 6 Terroirs Discovery Sampling Edition",
                "• 100% Pure Raw Honey Varieties",
                "• Hand-Poured Petite Flint Glass",
                "• Gifting & Tasting Guide Included"
            ]
        }
    ]
    
    # Generate the 5 horizontal dielines
    for config in horizontal_configs:
        generate_horizontal_dieline(config, catalog_data, output_dir, logo_img, producer_img)
        
    # Generate the vertical tamper ribbon dieline with crown crest
    generate_tamper_ribbon(output_dir, logo_img)
    
    print("\nAll 6 Honey & Superfoods dielines generated successfully!")

if __name__ == "__main__":
    generate_all_dielines()
