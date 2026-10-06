#!/usr/bin/env python3
"""
Mariam Luxury Brand - Packaging Label Die-Line Template & Dimension Generator
Generates high-resolution, print-calibrated packaging label blueprints with:
- Exact mechanical dimensions across all packaging formats
- Official brand palette (Pantone 5605 C Forest Green, Kurz Luxor 428 Gold Foil, Warm Ivory)
- Rounded die-cut border guides and inner safety margin
- Layout grid zones (Regulatory / Hero Branding / Origin & Logistics)
- Technical blueprint annotations, dimension callouts, and registration crosshairs
- Official Mariam gold calligraphy asset integration
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Color constants
FOREST_GREEN = (30, 51, 38)      # Pantone 5605 C (#1E3326)
GOLD_FOIL = (212, 175, 55)        # Kurz Luxor 428 Metallic Gold (#D4AF37)
WARM_IVORY = (234, 230, 223)      # Pantone 7527 C Warm Organic Ivory (#EAE6DF)

FORMATS = [
    ("dieline_370g_jar.png", 2200, 850, "WHOLE GREEN OLIVES - 370G / 700G JAR", "220mm x 85mm"),
    ("dieline_500ml_evoo.png", 750, 1400, "FIRST HARVEST RESERVE EVOO - 500ML BOTTLE", "75mm x 140mm"),
    ("dieline_200ml_spray.png", 1300, 1100, "EVOO CULINARY AIR-SPRAY - 200ML CAN", "130mm x 110mm"),
    ("dieline_190g_tapenade.png", 1900, 450, "RUSTIC GREEN TAPENADE - 190G JAR BELLY-BAND", "190mm x 45mm"),
    ("dieline_50g_pouch.png", 1100, 1600, "LIQUID-FREE OLIVE SNACK - 50G DOYPACK", "110mm x 160mm"),
]

def load_font(size, bold=False):
    font_path = "fonts/Tajawal-Bold.ttf" if bold else "fonts/Tajawal-Medium.ttf"
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_crosshair(draw, x, y, size=18, color=GOLD_FOIL, width=2):
    draw.line([(x - size, y), (x + size, y)], fill=color, width=width)
    draw.line([(x, y - size), (x, y + size)], fill=color, width=width)
    draw.ellipse([x - 6, y - 6, x + 6, y + 6], outline=color, width=1)

def generate_dielines(output_dir="output/dielines"):
    os.makedirs(output_dir, exist_ok=True)
    
    logo_path = "arina-logo-gold.png" if os.path.exists("arina-logo-gold.png") else "mariam-logo-gold.png"
    logo_img = None
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path).convert("RGBA")
        except Exception:
            logo_img = None

    for filename, w, h, title, physical in FORMATS:
        im = Image.new("RGBA", (w, h), FOREST_GREEN)
        draw = ImageDraw.Draw(im)
        
        # 1. Outer die-cut gold border with 30px inset
        draw.rounded_rectangle([30, 30, w - 30, h - 30], radius=25, outline=GOLD_FOIL, width=4)
        
        # 2. Inner thin ivory safety guide with 45px inset
        draw.rounded_rectangle([45, 45, w - 45, h - 45], radius=20, outline=WARM_IVORY, width=2)
        
        # 3. Grid sections: Center 40% reserved for brand & product name
        cx0, cx1 = int(w * 0.30), int(w * 0.70)
        draw.line([(cx0, 45), (cx0, h - 45)], fill=GOLD_FOIL, width=2)
        draw.line([(cx1, 45), (cx1, h - 45)], fill=GOLD_FOIL, width=2)
        
        # 4. Corner registration crosshairs
        draw_crosshair(draw, 30, 30, size=18, color=GOLD_FOIL)
        draw_crosshair(draw, w - 30, 30, size=18, color=GOLD_FOIL)
        draw_crosshair(draw, 30, h - 30, size=18, color=GOLD_FOIL)
        draw_crosshair(draw, w - 30, h - 30, size=18, color=GOLD_FOIL)
        
        # Font scales based on dieline dimensions
        scale_ref = min(w, h)
        title_font = load_font(max(18, int(scale_ref * 0.042)), bold=True)
        sub_font = load_font(max(13, int(scale_ref * 0.026)), bold=False)
        meta_font = load_font(max(11, int(scale_ref * 0.020)), bold=False)
        section_font = load_font(max(12, int(scale_ref * 0.024)), bold=True)
        
        # Center Panel Header & Title
        header_y = int(h * 0.10) if h >= 600 else 65
        draw.text((w // 2, header_y), "MARIAM — MADE WITH LOVE", fill=GOLD_FOIL, font=title_font, anchor="mm")
        draw.text((w // 2, header_y + int(scale_ref * 0.05)), title, fill=WARM_IVORY, font=sub_font, anchor="mm")
        draw.text((w // 2, header_y + int(scale_ref * 0.09)), f"SPECIFICATION: {physical} • {w}x{h} px @ 254 DPI", fill=GOLD_FOIL, font=meta_font, anchor="mm")
        
        # Integrate Mariam official gold calligraphy logo in center panel
        if logo_img:
            center_box_w = cx1 - cx0 - 60
            center_box_h = int(h * 0.35)
            lw, lh = logo_img.size
            scale = min(center_box_w / lw, center_box_h / lh, 0.65)
            nw, nh = int(lw * scale), int(lh * scale)
            if nw > 0 and nh > 0:
                scaled_logo = logo_img.resize((nw, nh), Image.Resampling.LANCZOS)
                logo_x = w // 2 - nw // 2
                logo_y = int(h * 0.42) - nh // 2
                im.alpha_composite(scaled_logo, (logo_x, logo_y))
        
        # Panel Section Annotations
        # Left Panel: Regulatory & Nutrition
        left_cx = cx0 // 2
        draw.text((left_cx, int(h * 0.15)), "ZONE 1: REGULATORY", fill=GOLD_FOIL, font=section_font, anchor="mm")
        draw.text((left_cx, int(h * 0.22)), "• Net / Drained Weight\n• Nutrition Facts Table\n• Ingredients List\n• Allergen Information", fill=WARM_IVORY, font=meta_font, anchor="ma")
        
        # Center Panel Footer
        draw.text((w // 2, h - int(h * 0.15)), "[ CENTRAL LUXURY BRANDING & EMBOSS PANEL ]", fill=WARM_IVORY, font=section_font, anchor="mm")
        
        # Right Panel: Origin & Barcode
        right_cx = cx1 + (w - cx1) // 2
        draw.text((right_cx, int(h * 0.15)), "ZONE 3: ORIGIN & LOGISTICS", fill=GOLD_FOIL, font=section_font, anchor="mm")
        draw.text((right_cx, int(h * 0.22)), "• Single-Estate Terroir Notes\n• EAN-13 Barcode / QR Authenticity\n• Recycling & Lot Number\n• Certification Badges", fill=WARM_IVORY, font=meta_font, anchor="ma")
        
        # Color Calibration Swatches on Bottom Left
        swatch_w, swatch_h = 28, 14
        base_y = h - 60
        if base_y < h - 25:
            # Forest Green Swatch
            draw.rectangle([60, base_y, 60 + swatch_w, base_y + swatch_h], fill=FOREST_GREEN, outline=WARM_IVORY, width=1)
            draw.text((95, base_y + swatch_h // 2), "Pantone 5605 C", fill=WARM_IVORY, font=meta_font, anchor="lm")
            
            # Gold Foil Swatch
            draw.rectangle([210, base_y, 210 + swatch_w, base_y + swatch_h], fill=GOLD_FOIL, outline=WARM_IVORY, width=1)
            draw.text((245, base_y + swatch_h // 2), "Kurz Luxor 428 Gold", fill=GOLD_FOIL, font=meta_font, anchor="lm")
            
            # Warm Ivory Swatch
            draw.rectangle([390, base_y, 390 + swatch_w, base_y + swatch_h], fill=WARM_IVORY, outline=FOREST_GREEN, width=1)
            draw.text((425, base_y + swatch_h // 2), "Pantone 7527 C Ivory", fill=WARM_IVORY, font=meta_font, anchor="lm")
        
        out_path = os.path.join(output_dir, filename)
        im.save(out_path)
        print(f"Generated: {out_path} ({w}x{h})")

if __name__ == "__main__":
    generate_dielines()
