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
- Official Honey & Superfoods palette:
  * Mariam Blush Pink: RGB(232, 197, 200) / #E8C5C8
  * Imperial Burgundy: RGB(105, 22, 48) / #691630
  * Luxor Gold Foil: RGB(218, 172, 54) / #DAAC36
  * Warm Ivory: RGB(248, 245, 238) / #F8F5EE
- Rounded die-cut border guides and inner safety margin
- 3-zone layout (Zone 1: Regulatory/Nutrition/Allergen; Zone 2: Hero Brand; Zone 3: Terroir/Logistics)
- Authentic cursive gold logo: mariam-logo-gold.png
- High-precision vector registration crosshairs, mechanical dimension callouts, and barcodes
- Dedicated crown crest and tamper-evident perforation score on tamper ribbon
"""

import json
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

# Official Brand Palette Constants - Calibrated to User Photo Reference
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

def draw_crown(draw, cx, cy, width, height, color=LUXOR_GOLD, jewel_color=BLUSH_PINK):
    """
    Draw an embossed royal crown crest with 5 peaks, pearls, and jeweled base band.
    """
    w2 = width // 2
    h2 = height // 2
    h_center = h2
    h_outer = int(h2 * 0.72)
    h_inner = int(h2 * 0.52)
    
    # Base band
    base_h = max(6, int(height * 0.18))
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
        (cx - w2 - 4, cy - h_outer),
        (cx - int(w2 * 0.52), cy + int(h2 * 0.12)),
        (cx - int(w2 * 0.28), cy - h_inner),
        (cx - int(w2 * 0.12), cy + int(h2 * 0.06)),
        (cx, cy - h_center),
        (cx + int(w2 * 0.12), cy + int(h2 * 0.06)),
        (cx + int(w2 * 0.28), cy - h_inner),
        (cx + int(w2 * 0.52), cy + int(h2 * 0.12)),
        (cx + w2 + 4, cy - h_outer),
        (cx + w2, base_y),
    ]
    draw.polygon(pts, fill=color)
    
    # Pearls on top of peaks
    pr = max(3, int(width * 0.038))
    draw.ellipse([cx - pr, cy - h_center - pr * 2, cx + pr, cy - h_center], fill=color)
    draw.ellipse([cx - int(w2 * 0.28) - pr, cy - h_inner - pr * 2, cx - int(w2 * 0.28) + pr, cy - h_inner], fill=color)
    draw.ellipse([cx + int(w2 * 0.28) - pr, cy - h_inner - pr * 2, cx + int(w2 * 0.28) + pr, cy - h_inner], fill=color)
    draw.ellipse([cx - w2 - 4 - pr, cy - h_outer - pr * 2, cx - w2 - 4 + pr, cy - h_outer], fill=color)
    draw.ellipse([cx + w2 + 4 - pr, cy - h_outer - pr * 2, cx + w2 + 4 + pr, cy - h_outer], fill=color)

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
    
    # Random realistic data bars
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

def draw_swatches_grid(draw, base_x, base_y, max_w, font, swatch_w=22, swatch_h=12):
    """Draw official color calibration swatches in a neat 2x2 grid inside Zone 1."""
    swatches = [
        (BLUSH_PINK, "Petal Blush #F5B7C2", LUXOR_GOLD),
        (IMPERIAL_BURGUNDY, "Wine Burgundy #76122E", WARM_IVORY),
        (LUXOR_GOLD, "Luxor Gold #DAAC36", LUXOR_GOLD),
        (WARM_IVORY, "Warm Ivory #FFF5F7", WARM_IVORY),
    ]
    col_w = max(max_w // 2, 130)
    for idx, (color, name, label_col) in enumerate(swatches):
        row = idx // 2
        col = idx % 2
        sx = base_x + col * col_w
        sy = base_y + row * (swatch_h + 6)
        draw.rectangle([sx, sy, sx + swatch_w, sy + swatch_h], fill=color, outline=LUXOR_GOLD, width=1)
        draw.text((sx + swatch_w + 6, sy + swatch_h // 2), name, fill=label_col, font=font, anchor="lm")

def generate_tamper_ribbon(output_dir="output/dielines", logo_img=None):
    """
    Generate dieline_tamper_ribbon_crown.png:
    - 450 × 1125 px @ 254 DPI (18mm × 45mm physical).
    - Background: Strictly Blush Pink (232, 197, 200).
    - Embossed Luxor Gold (218, 172, 54) crown crest in the center.
    - Break score guide at lid junction.
    - Authentic Mariam gold logo composited.
    """
    w, h = 450, 1125
    im = Image.new("RGBA", (w, h), (*BLUSH_PINK, 255))
    draw = ImageDraw.Draw(im)
    
    # 1. Outer die-cut gold border with 20px inset
    draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=20, outline=LUXOR_GOLD, width=3)
    
    # 2. Inner safety guide line (32px inset) in Imperial Burgundy
    draw.rounded_rectangle([32, 32, w - 32, h - 32], radius=15, outline=IMPERIAL_BURGUNDY, width=1)
    
    # 3. Four corner registration crosshairs
    draw_crosshair(draw, 20, 20, size=15, color=LUXOR_GOLD)
    draw_crosshair(draw, w - 20, 20, size=15, color=LUXOR_GOLD)
    draw_crosshair(draw, 20, h - 20, size=15, color=LUXOR_GOLD)
    draw_crosshair(draw, w - 20, h - 20, size=15, color=LUXOR_GOLD)
    
    # Fonts
    title_font = load_font(18, bold=True)
    sub_font = load_font(14, bold=True)
    meta_font = load_font(11, bold=False)
    small_font = load_font(10, bold=False)
    crest_title_font = load_font(13, bold=True)
    
    # ==================== TOP ZONE: METALLIC LID ADHERENCE ====================
    draw.text((w // 2, 48), "MARIAM PACKAGING BLUEPRINT", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, 72), "TAMPER-EVIDENT RIBBON", fill=LUXOR_GOLD, font=title_font, anchor="mm")
    draw.text((w // 2, 95), "18mm × 45mm @ 254 DPI", fill=IMPERIAL_BURGUNDY, font=meta_font, anchor="mm")
    
    # Top decorative horizontal bar
    draw.line([(50, 115), (w - 50, 115)], fill=LUXOR_GOLD, width=2)
    
    # Scaled authentic cursive logo
    if logo_img:
        lw, lh = logo_img.size
        scale = min(280 / lw, 100 / lh)
        nw, nh = int(lw * scale), int(lh * scale)
        scaled_logo = logo_img.resize((nw, nh), Image.Resampling.LANCZOS)
        im.alpha_composite(scaled_logo, (w // 2 - nw // 2, 140))
        
    draw.text((w // 2, 260), "NATURAL HONEY & SUPERFOODS", fill=IMPERIAL_BURGUNDY, font=sub_font, anchor="mm")
    draw.text((w // 2, 285), "Pure Goodness, Naturally.", fill=LUXOR_GOLD, font=meta_font, anchor="mm")
    draw.text((w // 2, 330), "[ LID ADHERENCE OVERLAP ZONE ]", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, 350), "Adheres firmly over metallic lid top surface", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    
    # Guideline down towards center
    draw_dashed_line(draw, (w // 2, 380), (w // 2, 450), fill=IMPERIAL_BURGUNDY, width=1, dash_length=6, gap_length=4)
    
    # ==================== CENTER ZONE: CROWN CREST & PERFORATION ====================
    cy_mid = 562
    
    # Perforation Score Line across ribbon
    draw_dashed_line(draw, (35, cy_mid), (w - 35, cy_mid), fill=IMPERIAL_BURGUNDY, width=2, dash_length=8, gap_length=4)
    draw.text((w // 2, cy_mid - 110), "✂ PERFORATION SCORE LINE ✂", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    
    # Medallion background
    medallion_r = 95
    # Inner medallion filled with Blush Pink and bordered with Luxor Gold
    draw.ellipse([w // 2 - medallion_r, cy_mid - medallion_r, w // 2 + medallion_r, cy_mid + medallion_r],
                 fill=BLUSH_PINK, outline=LUXOR_GOLD, width=3)
    draw.ellipse([w // 2 - medallion_r + 6, cy_mid - medallion_r + 6, w // 2 + medallion_r - 6, cy_mid + medallion_r - 6],
                 outline=LUXOR_GOLD, width=1)
                 
    # Medallion Header
    draw.text((w // 2, cy_mid - 60), "MARIAM ROYAL SEAL", fill=LUXOR_GOLD, font=crest_title_font, anchor="mm")
    
    # Embossed Luxor Gold Crown Crest
    draw_crown(draw, cx=w // 2, cy=cy_mid + 2, width=115, height=65, color=LUXOR_GOLD, jewel_color=BLUSH_PINK)
    
    # Medallion Subtext
    draw.text((w // 2, cy_mid + 58), "★ AUTHENTIC & PURE ★", fill=LUXOR_GOLD, font=small_font, anchor="mm")
    draw.text((w // 2, cy_mid + 75), "TAMPER EVIDENT", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    
    # ==================== BOTTOM ZONE: SHOULDER GLASS ANCHOR ====================
    draw_dashed_line(draw, (w // 2, cy_mid + 115), (w // 2, cy_mid + 175), fill=IMPERIAL_BURGUNDY, width=1, dash_length=6, gap_length=4)
    
    draw.text((w // 2, 770), "[ GLASS SHOULDER ANCHOR ZONE ]", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="mm")
    draw.text((w // 2, 795), "SECURED TO FLINT GLASS SHOULDER", fill=LUXOR_GOLD, font=sub_font, anchor="mm")
    
    # Second Scaled Logo at shoulder
    if logo_img:
        lw, lh = logo_img.size
        scale2 = min(220 / lw, 75 / lh)
        nw2, nh2 = int(lw * scale2), int(lh * scale2)
        scaled_logo2 = logo_img.resize((nw2, nh2), Image.Resampling.LANCZOS)
        im.alpha_composite(scaled_logo2, (w // 2 - nw2 // 2, 825))
        
    draw.text((w // 2, 925), "DO NOT ACCEPT IF SEAL IS BROKEN", fill=IMPERIAL_BURGUNDY, font=sub_font, anchor="mm")
    draw.text((w // 2, 950), "إذا كان الختم مكسوراً لا تقبل العبوة", fill=IMPERIAL_BURGUNDY, font=meta_font, anchor="mm")
    draw.text((w // 2, 980), "Single-Harvest Raw Honey Guarantee", fill=LUXOR_GOLD, font=small_font, anchor="mm")
    
    # Swatches on bottom of ribbon
    sw_y = 1030
    draw.rectangle([55, sw_y, 80, sw_y + 12], fill=BLUSH_PINK, outline=LUXOR_GOLD, width=1)
    draw.text((88, sw_y + 6), "#F5B7C2", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="lm")
    
    draw.rectangle([180, sw_y, 205, sw_y + 12], fill=LUXOR_GOLD, outline=IMPERIAL_BURGUNDY, width=1)
    draw.text((213, sw_y + 6), "#DAAC36", fill=LUXOR_GOLD, font=small_font, anchor="lm")
    
    draw.rectangle([305, sw_y, 330, sw_y + 12], fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=1)
    draw.text((338, sw_y + 6), "#76122E", fill=IMPERIAL_BURGUNDY, font=small_font, anchor="lm")
    
    out_path = os.path.join(output_dir, "dieline_tamper_ribbon_crown.png")
    im.save(out_path)
    print(f"Generated: {out_path} ({w}x{h} px)")
    return out_path

def generate_horizontal_dieline(config, catalog_data, output_dir="output/dielines", logo_img=None, producer_img=None):
    """
    Generate horizontal 3-zone print dieline:
    - Outer cut border with registration crosshairs
    - Inner safety guide
    - Zone 1: Regulatory / Nutrition / Allergen / Warning / Color Calibration Swatches
    - Zone 2: Hero Brand / Authentic Cursive Logo / Descriptor / Title / Sensory Triad
    - Zone 3: Terroir / Logistics / Barcode / Producer Emblem / Certifications
    """
    filename = config["filename"]
    w = config["width"]
    h = config["height"]
    physical = config["physical"]
    sku_id = config.get("sku_id")
    bg_color = config.get("bg_color", IMPERIAL_BURGUNDY)
    special_mode = config.get("special_mode")
    
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
                           
    # 2. Inner thin ivory safety guide with 45px inset (32px for petite)
    inner_inset = 45 if h >= 600 else 32
    draw.rounded_rectangle([inner_inset, inner_inset, w - inner_inset, h - inner_inset],
                           radius=20 if h >= 600 else 12, outline=WARM_IVORY, width=2)
                           
    # 3. Registration Crosshairs at 4 corners
    cross_size = 18 if h >= 600 else 14
    draw_crosshair(draw, outer_inset, outer_inset, size=cross_size, color=LUXOR_GOLD)
    draw_crosshair(draw, w - outer_inset, outer_inset, size=cross_size, color=LUXOR_GOLD)
    draw_crosshair(draw, outer_inset, h - outer_inset, size=cross_size, color=LUXOR_GOLD)
    draw_crosshair(draw, w - outer_inset, h - outer_inset, size=cross_size, color=LUXOR_GOLD)
    
    # 4. Grid dividers: Zone 1 (~28%), Zone 2 (~44%), Zone 3 (~28%)
    cx0 = int(w * 0.28)
    cx1 = int(w * 0.72)
    draw.line([(cx0, inner_inset), (cx0, h - inner_inset)], fill=LUXOR_GOLD, width=2)
    draw.line([(cx1, inner_inset), (cx1, h - inner_inset)], fill=LUXOR_GOLD, width=2)
    
    # Font scaling
    title_font = load_font(max(16, int(scale_ref * 0.040)), bold=True)
    sub_font = load_font(max(12, int(scale_ref * 0.024)), bold=False)
    meta_font = load_font(max(10, int(scale_ref * 0.018)), bold=False)
    bold_meta_font = load_font(max(10, int(scale_ref * 0.018)), bold=True)
    section_font = load_font(max(12, int(scale_ref * 0.024)), bold=True)
    hero_font = load_font(max(18, int(scale_ref * 0.052)), bold=True)
    small_font = load_font(max(9, int(scale_ref * 0.015)), bold=False)
    
    # ==================== ZONE 2: CENTER HERO BRANDING ====================
    is_royal = (special_mode == "royal_mix")
    
    # 5. Zone 2 Center Luxury Panel / Baroque Cartouche
    center_box_w = cx1 - cx0 - 80
    cart_x0 = cx0 + 35
    cart_x1 = cx1 - 35
    cart_y0 = inner_inset + 18
    cart_y1 = h - inner_inset - 18
    
    if is_royal:
        # Draw the iconic Petal Blush Pink baroque cartouche with gold outline from reference photo
        draw.rounded_rectangle([cart_x0, cart_y0, cart_x1, cart_y1], radius=28, fill=BLUSH_PINK, outline=LUXOR_GOLD, width=3)
        draw.rounded_rectangle([cart_x0 + 8, cart_y0 + 8, cart_x1 - 8, cart_y1 - 8], radius=22, outline=LUXOR_GOLD, width=1)
        # Gold Crown on top
        draw_crown(draw, cx=w // 2, cy=cart_y0 + 48, width=70, height=40, color=LUXOR_GOLD, jewel_color=IMPERIAL_BURGUNDY)
    else:
        # Standard elegant frame
        draw.rounded_rectangle([cart_x0, cart_y0, cart_x1, cart_y1], radius=16, outline=LUXOR_GOLD, width=2)
    
    header_y = int(h * 0.09) if h >= 600 else 46
    top_title_col = IMPERIAL_BURGUNDY if is_royal else LUXOR_GOLD
    top_sub_col = IMPERIAL_BURGUNDY if is_royal else WARM_IVORY
    
    draw.text((w // 2, header_y), "MARIAM — MADE WITH LOVE", fill=top_title_col, font=title_font, anchor="mm")
    
    product_title = config.get("title", "NATURAL HONEY")
    draw.text((w // 2, header_y + int(scale_ref * 0.045)), product_title, fill=top_sub_col, font=sub_font, anchor="mm")
    draw.text((w // 2, header_y + int(scale_ref * 0.082)),
              f"SPECIFICATION: {physical} • {w}x{h} px @ 254 DPI", fill=LUXOR_GOLD, font=small_font, anchor="mm")
              
    # Central Logo integration
    center_box_h = int(h * 0.32)
    if logo_img:
        lw, lh = logo_img.size
        scale = min(center_box_w / lw, center_box_h / lh, 0.70)
        nw, nh = int(lw * scale), int(lh * scale)
        if nw > 0 and nh > 0:
            scaled_logo = logo_img.resize((nw, nh), Image.Resampling.LANCZOS)
            logo_x = w // 2 - nw // 2
            logo_y = int(h * 0.37) - nh // 2 if h >= 600 else int(h * 0.36) - nh // 2
            im.alpha_composite(scaled_logo, (logo_x, logo_y))
            
    # Sub-Brand Descriptor below logo
    desc_y = int(h * 0.53) if h >= 600 else int(h * 0.54)
    desc_col = IMPERIAL_BURGUNDY if is_royal else WARM_IVORY
    draw.text((w // 2, desc_y), "NATURAL HONEY & SUPERFOODS", fill=desc_col, font=sub_font, anchor="mm")
    
    # Hero Title
    hero_title = config.get("hero_title", product_title)
    hero_y = desc_y + int(scale_ref * 0.065)
    hero_col = IMPERIAL_BURGUNDY if is_royal else LUXOR_GOLD
    draw.text((w // 2, hero_y), hero_title, fill=hero_col, font=hero_font, anchor="mm")
    
    # Special Ribbon / Subhead for Royal Mix
    if is_royal:
        ribbon_w = min(center_box_w, 650)
        ribbon_h = int(scale_ref * 0.045)
        ribbon_y = hero_y + int(scale_ref * 0.055)
        draw.rounded_rectangle([w // 2 - ribbon_w // 2, ribbon_y, w // 2 + ribbon_w // 2, ribbon_y + ribbon_h],
                               radius=6, fill=IMPERIAL_BURGUNDY, outline=LUXOR_GOLD, width=2)
        draw.text((w // 2, ribbon_y + ribbon_h // 2),
                  "★ HERO FLAGSHIP • 0% PEANUTS • 5% FRESH ROYAL JELLY ★",
                  fill=WARM_IVORY, font=bold_meta_font, anchor="mm")
        sub_y = ribbon_y + ribbon_h + int(scale_ref * 0.035)
    elif special_mode == "hex":
        hex_y = hero_y + int(scale_ref * 0.055)
        draw_hexagon(draw, w // 2, hex_y, radius=18, outline=LUXOR_GOLD, width=2)
        draw_hexagon(draw, w // 2, hex_y, radius=12, outline=WARM_IVORY, width=1)
        sub_y = hex_y + int(scale_ref * 0.045)
    else:
        sub_y = hero_y + int(scale_ref * 0.055)
        
    subtitle = config.get("subtitle", "Pure Natural Honey")
    sub_col = IMPERIAL_BURGUNDY if is_royal else WARM_IVORY
    draw.text((w // 2, sub_y), subtitle, fill=sub_col, font=meta_font, anchor="mm")
    
    # Sensory Triad Box
    triad = config.get("triad", "Pure • Natural • Golden")
    triad_y = sub_y + int(scale_ref * 0.060)
    triad_box_w = int(len(triad) * scale_ref * 0.015) + 60
    triad_box_h = int(scale_ref * 0.048)
    triad_fill = BLUSH_PINK_LIGHT if is_royal else None
    draw.rounded_rectangle([w // 2 - triad_box_w // 2, triad_y - triad_box_h // 2,
                            w // 2 + triad_box_w // 2, triad_y + triad_box_h // 2],
                           radius=6, fill=triad_fill, outline=LUXOR_GOLD, width=1)
    triad_col = IMPERIAL_BURGUNDY if is_royal else LUXOR_GOLD
    draw.text((w // 2, triad_y), triad, fill=triad_col, font=bold_meta_font, anchor="mm")
    
    # Net Weight Banner
    weight_str = config.get("weight", "Net Wt. 500g (17.6 oz)")
    weight_y = triad_y + int(scale_ref * 0.052)
    weight_col = IMPERIAL_BURGUNDY if is_royal else WARM_IVORY
    draw.text((w // 2, weight_y), weight_str, fill=weight_col, font=bold_meta_font, anchor="mm")
    
    # Center Panel Footer
    footer_y = h - inner_inset - int(scale_ref * 0.035)
    footer_col = IMPERIAL_BURGUNDY if is_royal else WARM_IVORY
    draw.text((w // 2, footer_y), "[ CENTRAL LUXURY BRANDING & EMBOSS PANEL ]", fill=footer_col, font=small_font, anchor="mm")
    
    # ==================== ZONE 1: REGULATORY & NUTRITION ====================
    left_cx = (inner_inset + cx0) // 2
    z1_top = inner_inset + 20
    draw.text((left_cx, z1_top), "ZONE 1: REGULATORY & NUTRITION", fill=LUXOR_GOLD, font=section_font, anchor="mm")
    
    # Nutrition Facts Box
    nbox_x0 = inner_inset + 18
    nbox_x1 = cx0 - 18
    nbox_y0 = z1_top + int(scale_ref * 0.035)
    nbox_h = int(scale_ref * 0.28) if h >= 600 else int(scale_ref * 0.24)
    nbox_y1 = nbox_y0 + nbox_h
    
    draw.rectangle([nbox_x0, nbox_y0, nbox_x1, nbox_y1], outline=WARM_IVORY, width=1)
    draw.text((nbox_x0 + 10, nbox_y0 + 12), "NUTRITION FACTS / VALEUR NUTRITIVE", fill=LUXOR_GOLD, font=bold_meta_font, anchor="lm")
    draw.line([(nbox_x0, nbox_y0 + 22), (nbox_x1, nbox_y0 + 22)], fill=WARM_IVORY, width=1)
    
    nut_lines = config.get("nutrition", [
        "Serving Size / Portion: 20g (1 tbsp)",
        "Calories / Énergie: 61 kcal (304 kcal / 100g)",
        "Total Fat / Lipides: 0g (0% DV)",
        "Total Carbohydrate / Glucides: 16.5g (82g / 100g)",
        "  Sugars / Sucres: 16.4g (82g / 100g)",
        "Protein / Protéines: 0.1g",
        "Sodium / Sel: 1mg (<1% DV)"
    ])
    
    line_y = nbox_y0 + 36
    spacing = int((nbox_h - 44) / max(len(nut_lines), 1))
    for nl in nut_lines:
        draw.text((nbox_x0 + 10, line_y), nl, fill=WARM_IVORY, font=small_font, anchor="lm")
        line_y += spacing
        
    # Ingredients List
    ing_top = nbox_y1 + 10
    draw.text((nbox_x0, ing_top), "INGREDIENTS / INGRÉDIENTS:", fill=LUXOR_GOLD, font=bold_meta_font, anchor="lm")
    
    ingredients_str = config.get("ingredients", "100% Pure Raw Natural Honey.")
    words = ingredients_str.split(" ")
    lines = []
    cur_line = ""
    max_line_len = 45 if w >= 2200 else 32
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
    
    # Swatches inside Zone 1 at the bottom
    swatch_y = h - inner_inset - 38
    draw_swatches_grid(draw, nbox_x0, swatch_y, cx0 - nbox_x0, small_font)
    
    # ==================== ZONE 3: ORIGIN & LOGISTICS ====================
    right_cx = (cx1 + w - inner_inset) // 2
    z3_top = inner_inset + 20
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
        pscale = min(160 / pw, 60 / ph)
        pnw, pnh = int(pw * pscale), int(ph * pscale)
        scaled_prod = producer_img.resize((pnw, pnh), Image.Resampling.LANCZOS)
        im.alpha_composite(scaled_prod, (rbox_x1 - pnw, cur_r_y - 10))
        
    # EAN-13 Barcode Mockup
    cur_r_y += 50
    barcode_w = min(rbox_x1 - rbox_x0, 280)
    barcode_h = int(scale_ref * 0.10)
    draw_barcode(draw, rbox_x0, cur_r_y, barcode_w, barcode_h,
                 config.get("barcode", "6 281001 029101"),
                 bar_color=LUXOR_GOLD, text_color=WARM_IVORY, font=small_font)
                 
    # Quality & Compliance Badges
    cur_r_y += barcode_h + 18
    badges = config.get("badges", [
        "✓ 100% Raw & Unpasteurized",
        "✓ Cold Extracted Single-Harvest",
        "✓ Zero Additives or Sugars",
        "✓ Recyclable Flint Glass"
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
    logo_path = "mariam-logo-gold.png"
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
                "Calories / Énergie: 61 kcal (304 kcal / 100g)",
                "Total Fat / Lipides: 0g (0% DV)",
                "Total Carbohydrate / Glucides: 16.5g (82.4g / 100g)",
                "  Sugars / Sucres: 16.4g (82.1g / 100g)",
                "Protein / Protéines: 0.1g (0.3g / 100g)",
                "Sodium / Sel: < 1mg (<1% DV)"
            ],
            "badges": [
                "✓ 100% Pure Monofloral Mountain Sidr",
                "✓ Unpasteurized & Cold Extracted",
                "✓ High Antibacterial & Enzyme Potency",
                "✓ Ultra-Clear Flint Glass Jar"
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
                "Calories / Énergie: 61 kcal (304 kcal / 100g)",
                "Total Fat / Lipides: 0g (0% DV)",
                "Total Carbohydrate / Glucides: 16.4g (82g / 100g)",
                "  Sugars / Sucres: 16.4g (82g / 100g)",
                "Protein / Protéines: 0.1g (0.3g / 100g)",
                "Sodium / Sel: 1mg (<1% DV)"
            ],
            "badges": [
                "✓ 100% Pure Natural Clover Honey",
                "✓ Family Bulk Reserve • 1000g Standard",
                "✓ Unpasteurized & Cold Extracted",
                "✓ Recyclable Heavy Flint Glass"
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
                "Calories / Énergie: 135 kcal (449 kcal / 100g)",
                "Total Fat / Lipides: 5.0g (Saturated: 0.6g)",
                "Total Carbohydrate / Glucides: 15.6g (Sugars: 14.4g)",
                "Dietary Fiber / Fibres: 1.7g",
                "Protein / Protéines: 2.5g (8.2g / 100g)",
                "Sodium / Sel: 4mg (<1% DV)"
            ],
            "badges": [
                "✓ 0% Peanuts Policy — Exclusively Tree Nuts & Seeds",
                "✓ Fortified with 5% Fresh Queen Bee Royal Jelly",
                "✓ Rich in Plant Protein, Omega-3 & Zinc",
                "✓ 12mm Solid Base Glass Jar Architecture"
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
                "Calories / Énergie: 61 kcal (304 kcal / 100g)",
                "Total Fat / Lipides: 0g (0% DV)",
                "Total Carbohydrate / Glucides: 16.4g (82.2g / 100g)",
                "  Sugars / Sucres: 16.4g (82.0g / 100g)",
                "Protein / Protéines: 0.1g (0.3g / 100g)",
                "Sodium / Sel: 1mg (<1% DV)"
            ],
            "badges": [
                "✓ Direct From Hive to Jar Without Processing",
                "✓ Naturally Contains Bee Propolis & Enzymes",
                "✓ 100% Edible Natural Virgin Comb",
                "✓ Faceted Hexagonal Glass Showpiece"
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
                "Calories / Énergie: 61 kcal (304 kcal / 100g)",
                "Total Fat / Lipides: 0g (0% DV)",
                "Total Carbohydrate / Glucides: 16.4g (82g / 100g)",
                "Protein / Protéines: 0.1g",
                "Sodium / Sel: < 1mg"
            ],
            "badges": [
                "✓ 6 Terroirs Discovery Sampling Edition",
                "✓ 100% Pure Raw Honey Varieties",
                "✓ Hand-Poured Petite Flint Glass",
                "✓ Gifting & Tasting Guide Included"
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
