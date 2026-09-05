import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Fonts paths
AR_BOLD = 'fonts/Tajawal-Bold.ttf' if os.path.exists('fonts/Tajawal-Bold.ttf') else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
AR_REG = 'fonts/Tajawal-Regular.ttf' if os.path.exists('fonts/Tajawal-Regular.ttf') else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
EN_BOLD = 'fonts/Tajawal-Bold.ttf' if os.path.exists('fonts/Tajawal-Bold.ttf') else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
EN_REG = 'fonts/Tajawal-Regular.ttf' if os.path.exists('fonts/Tajawal-Regular.ttf') else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def load_fonts(scale=1.0):
    return {
        'title_en': ImageFont.truetype(EN_BOLD, int(34 * scale)),
        'h2_en': ImageFont.truetype(EN_BOLD, int(26 * scale)),
        'h3_en': ImageFont.truetype(EN_BOLD, int(20 * scale)),
        'body_en': ImageFont.truetype(EN_REG, int(17 * scale)),
        'sub_en': ImageFont.truetype(EN_REG, int(15 * scale)),
        'badge': ImageFont.truetype(EN_BOLD, int(14 * scale)),
    }

def draw_header_en(im, draw, f, W, title, category, sub=None, is_mobile=False):
    y_start = 40 if is_mobile else 35
    if os.path.exists('khaeer-alwadi-logo.png'):
        logo = Image.open('khaeer-alwadi-logo.png').convert('RGBA')
        max_h = 75 if is_mobile else 65
        logo.thumbnail((260, max_h), Image.Resampling.LANCZOS)
        if is_mobile:
            im.paste(logo, (int((W - logo.width) / 2), y_start), logo)
            y_title = y_start + logo.height + 15
            draw.text((W/2, y_title), title, font=f['h2_en'], fill='#D4A836', anchor='mm')
            draw.text((W/2, y_title + 38), category, font=f['h3_en'], fill='#FFFFFF', anchor='mm')
            if sub:
                draw.text((W/2, y_title + 74), sub, font=f['sub_en'], fill='#94A3B8', anchor='mm')
                y_div = y_title + 110
            else:
                y_div = y_title + 80
            draw.line([(60, y_div), (W-60, y_div)], fill='#2D5232', width=2)
            return y_div + 25
        else:
            im.paste(logo, (60, y_start), logo)
            draw.text((W - 60, y_start), title, font=f['h2_en'], fill='#D4A836', anchor='rt')
            draw.text((W - 60, y_start + 40), category, font=f['h3_en'], fill='#FFFFFF', anchor='rt')
            draw.line([(60, y_start + 85), (W - 60, y_start + 85)], fill='#2D5232', width=2)
            return y_start + 110

def draw_footer_bar_en(im, draw, f, W, H, is_mobile=False):
    if is_mobile:
        y = H - 125
        draw.rounded_rectangle([50, y, W-50, y+85], radius=18, fill='#0B3B26', outline='#10B981', width=2)
        draw.text((W/2, y+24), "Direct WhatsApp: +20 10 08716714  |  Cairo, Egypt", font=f['badge'], fill='#FFFFFF', anchor='mm')
        draw.text((W/2, y+58), "Khaeer Alwadi Food Industries • ISO 22000 • HACCP • FDA", font=f['badge'], fill='#10B981', anchor='mm')
    else:
        y = H - 65
        draw.line([(60, y), (W - 60, y)], fill='#2D5232', width=1)
        draw.text((60, y + 20), "Khaeer Alwadi Food Industries  |  Cairo, Egypt", font=f['badge'], fill='#94A3B8', anchor='lt')
        draw.text((W/2, y + 20), "ISO 22000 • HACCP • FDA Registered • Halal • ISO 9001", font=f['badge'], fill='#D4A836', anchor='mm')
        draw.text((W - 60, y + 20), "Direct WhatsApp: +20 10 08716714  |  wa.me/201008716714", font=f['badge'], fill='#10B981', anchor='rt')

# ----------------- ENGLISH PRESENTATION SLIDES (1920 x 1080) -----------------
def generate_english_presentation_slides():
    W, H = 1920, 1080
    f = load_fonts(scale=1.1)
    slides = []

    # Slide 1: Cover Landscape
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Khaeer Alwadi Food Industries", "Official B2B Export Portfolio", is_mobile=False)

    col_w = 880
    left_x = 60
    right_x = 980

    draw.text((left_x, y + 20), "Mediterranean Table Olives & Pickled Specialties", font=f['title_en'], fill='#D4A836', anchor='lt')
    draw.text((left_x, y + 75), "Industrial Processing, Direct Grove Sourcing & Turnkey OEM Solutions", font=f['h3_en'], fill='#FFFFFF', anchor='lt')
    
    pillars = [
        ("Direct Agro Terroir", "Contract grove sourcing across Nile Delta; 15–25% landed cost advantage over Southern Europe."),
        ("Industrial Scale", "Automated olive pitting lines, rotary slicing drums, and overpressure autoclave retort sterilization."),
        ("Rapid Maritime Corridors", "3–5 days transit to Southern Europe; 4–7 days to GCC markets via Alexandria, Damietta & Port Said."),
        ("International Compliance", "Certified ISO 22000, HACCP, FDA Registered (US FSMA & 21 CFR Part 117), Halal & ISO 9001.")
    ]
    py = y + 130
    for p_t, p_d in pillars:
        draw.rounded_rectangle([left_x, py, right_x - 40, py + 95], radius=14, fill='#10221A', outline='#2D5232', width=1)
        draw.text((left_x + 25, py + 18), p_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((left_x + 25, py + 52), p_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        py += 115

    draw.rounded_rectangle([left_x, py + 10, right_x - 40, py + 85], radius=14, fill='#0B3B26', outline='#10B981', width=2)
    draw.text((left_x + 25, py + 28), "Direct Procurement & WhatsApp Desk:", font=f['badge'], fill='#FFFFFF', anchor='lt')
    draw.text((left_x + 25, py + 52), "+20 10 08716714  •  wa.me/201008716714  •  Cairo, Egypt", font=f['h3_en'], fill='#10B981', anchor='lt')

    img_path = "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg"
    if os.path.exists(img_path):
        p_img = Image.open(img_path).convert('RGB')
        p_img.thumbnail((col_w, H - y - 120), Image.Resampling.LANCZOS)
        im.paste(p_img, (right_x + int((col_w - p_img.width)/2), y + 20))

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 2: Strategic Supply Advantage Landscape
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "The Egyptian Strategic Supply Advantage", "Section 01 // Geographic Terroir, Maritime Corridors & Free Trade", is_mobile=False)

    draw.rounded_rectangle([60, y, W - 60, y + 100], radius=16, fill='#163024', outline='#D4A836', width=2)
    draw.text((W/2, y + 30), "15%–25% Landed Cost Advantage vs Southern European Competitors", font=f['h2_en'], fill='#D4A836', anchor='mm')
    draw.text((W/2, y + 70), "Agricultural yield, competitive manufacturing & short-sea feeder lanes to European & Arab markets", font=f['sub_en'], fill='#FFFFFF', anchor='mm')
    y += 130

    col_w3 = 580
    ports = [
        ("Alexandria Port (2.5h)", "Major Mediterranean Gateway", "Egypt's premier Mediterranean deepwater container hub; weekly direct feeder lines to Southern Europe."),
        ("Damietta Port (2.5h)", "Modern Container Terminal", "State-of-the-art container terminal with rapid customs processing & specialized agro-logistics."),
        ("Port Said Port (2.0h)", "Suez Canal Hub", "Strategic port at the mouth of the Suez Canal; immediate transit routes to GCC, Arabian Gulf & Asia.")
    ]
    px = 60
    for p_t, p_sub, p_d in ports:
        draw.rounded_rectangle([px, y, px + col_w3, y + 200], radius=16, fill='#10221A', outline='#2D5232', width=1)
        draw.text((px + 25, y + 25), p_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((px + 25, y + 65), p_sub, font=f['sub_en'], fill='#FFFFFF', anchor='lt')
        draw.text((px + 25, y + 115), p_d, font=f['body_en'], fill='#94A3B8', anchor='lt')
        px += col_w3 + 30
    y += 235

    draw.text((60, y), "Multilateral Free Trade Agreements & Tariff Exemptions:", font=f['h3_en'], fill='#D4A836', anchor='lt')
    y += 40
    pacts = [
        ("GAFTA Agreement", "0% Customs across all Arab League & GCC member states."),
        ("COMESA Free Trade", "Duty-free commercial access across 21 African nations."),
        ("Agadir Agreement", "Euro-Mediterranean accumulation of industrial origin."),
        ("Egypt–EU Association", "Preferential duty-free entry into European Union markets.")
    ]
    col_w4 = 425
    px = 60
    for p_t, p_d in pacts:
        draw.rounded_rectangle([px, y, px + col_w4, y + 140], radius=14, fill='#10221A', outline='#2D5232', width=1)
        draw.text((px + 20, y + 20), p_t, font=f['h3_en'], fill='#FFFFFF', anchor='lt')
        draw.text((px + 20, y + 65), p_d, font=f['body_en'], fill='#94A3B8', anchor='lt')
        px += col_w4 + 33

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 3: Industrial Infrastructure & Global Compliance
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Industrial Infrastructure & Global Compliance", "Section 02 // Processing Technology, Quality Control & Audits", is_mobile=False)

    img1 = "WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg"
    img2 = "WhatsApp Image 2026-09-05 at 12.52.17 PM.jpeg"
    if os.path.exists(img1) and os.path.exists(img2):
        i1 = Image.open(img1).convert('RGB')
        i2 = Image.open(img2).convert('RGB')
        i1.thumbnail((500, 360), Image.Resampling.LANCZOS)
        i2.thumbnail((500, 360), Image.Resampling.LANCZOS)
        im.paste(i1, (1360, y + 20))
        im.paste(i2, (1360, y + 410))

    col_w_left = 1260
    techs = [
        ("Automated High-Throughput Pitting Lines", "Mechanical Pitting", "Precision mechanical stone extraction with <1% fragment tolerance; preserves natural fruit cellular integrity."),
        ("Rotary Drum Slicing Lines", "Calibrated Slicing", "Uniform 3.2mm ±0.2mm ring thickness; delivers optimal melt-coverage for international pizza chains & catering."),
        ("Overpressure Autoclave Retort Sterilization", "Autoclave Retort", "Computer-controlled counter-pressure thermal processing achieving F0 ≥ 4.0; guarantees 36-month commercial sterility.")
    ]
    ty = y + 20
    for t_t, t_sub, t_d in techs:
        draw.rounded_rectangle([60, ty, col_w_left, ty + 125], radius=16, fill='#10221A', outline='#2D5232', width=1)
        draw.text((85, ty + 20), t_t, font=f['h2_en'], fill='#D4A836', anchor='lt')
        draw.text((col_w_left - 200, ty + 25), t_sub, font=f['sub_en'], fill='#10B981', anchor='lt')
        draw.text((85, ty + 70), t_d, font=f['body_en'], fill='#94A3B8', anchor='lt')
        ty += 145

    draw.rounded_rectangle([60, ty + 20, col_w_left, ty + 175], radius=16, fill='#0B2E1E', outline='#10B981', width=2)
    draw.text((85, ty + 40), "International Quality Certifications & Regulatory Registrations:", font=f['h3_en'], fill='#D4A836', anchor='lt')
    badges_str = "ISO 22000:2018  •  HACCP Certified  •  FDA Registered (US FSMA)  •  Halal Certified  •  ISO 9001:2015"
    draw.text((col_w_left/2 + 30, ty + 105), badges_str, font=f['h3_en'], fill='#FFFFFF', anchor='mm')

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 4: Table Olives Portfolio
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Core Line I: Premium Table Olives Portfolio", "Section 03 // Black & Green Olives (Whole, Pitted, Sliced & Stuffed)", is_mobile=False)

    products_olives = [
        ("Sliced Black Olives (3.2mm)", "Caliber 200/220", "WhatsApp Image 2026-09-05 at 12.52.20 PM.jpeg", "Pizza chains & food service", "Firm ring structure"),
        ("Pitted Black Olives", "Caliber 180/200", "WhatsApp Image 2026-09-05 at 12.52.16 PM (5).jpeg", "Wholesale & repacking", "Meaty, rich texture"),
        ("Picual Green Olives", "Caliber 240/260", "WhatsApp Image 2026-09-05 at 12.52.17 PM (6).jpeg", "Retail jars & delis", "Vibrant orchard green"),
        ("Pimento-Stuffed Olives", "100% Natural Paste", "WhatsApp Image 2026-09-05 at 12.52.17 PM (5).jpeg", "Supermarket retail packs", "Classic savory cocktail"),
        ("Kalamata-Style Dark", "Natural Fermentation", "WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg", "Gourmet retail & catering", "Olive oil & wine brine")
    ]
    card_w = 340
    cx = 60
    for p_t, p_cal, img_p, p_line1, p_line2 in products_olives:
        draw.rounded_rectangle([cx, y + 20, cx + card_w, y + 680], radius=18, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((card_w - 30, 260), Image.Resampling.LANCZOS)
            im.paste(p_img, (cx + int((card_w - p_img.width)/2), y + 35))
        draw.text((cx + card_w/2, y + 325), p_t, font=f['h3_en'], fill='#D4A836', anchor='mt')
        draw.text((cx + card_w/2, y + 370), p_cal, font=f['body_en'], fill='#FFFFFF', anchor='mt')
        draw.text((cx + card_w/2, y + 415), p_line1, font=f['sub_en'], fill='#E2E8F0', anchor='mt')
        draw.text((cx + card_w/2, y + 450), p_line2, font=f['sub_en'], fill='#94A3B8', anchor='mt')
        
        draw.rounded_rectangle([cx + 20, y + 540, cx + card_w - 20, y + 640], radius=10, fill='#163024')
        draw.text((cx + card_w/2, y + 570), "Drained Weight ≥ 52%", font=f['sub_en'], fill='#10B981', anchor='mm')
        draw.text((cx + card_w/2, y + 610), "Ring Caliber: 3.2mm ±0.2", font=f['sub_en'], fill='#D4A836', anchor='mm')
        cx += card_w + 25

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 5: Pickled Specialties
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Core Line II: Pickled Specialties & Gourmet Peppers", "Section 04 // Tuscan Pepperoncini, Red Chilis, Turshi & Gherkins", is_mobile=False)

    products_pickles = [
        ("Golden Tuscan Pepperoncini", "A10 Cans & Glass Jars", "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg", "Mild warmth, vibrant yellow hue & crisp snap; preferred across pizza & sandwich chains."),
        ("Gourmet Hot Red Chilis", "Pickled Whole Pods", "WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg", "Hand-selected fiery red chili peppers; packed in calibrated vinegar brine with intact calyx."),
        ("Traditional Turshi Baladi", "Authentic Egyptian Mix", "WhatsApp Image 2026-09-05 at 12.52.16 PM (2).jpeg", "Carrots, turnips, cucumbers & peppers in authentic heritage spiced brine with zero artificial dyes."),
        ("Crisp Pickled Gherkins", "Petite Cucumbers", "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg", "Unrivaled crunchy texture snap; infused with yellow mustard seeds, fresh dill & distilled vinegar.")
    ]
    card_w4 = 430
    cx = 60
    for p_t, p_tag, img_p, p_d in products_pickles:
        draw.rounded_rectangle([cx, y + 20, cx + card_w4, y + 680], radius=18, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((card_w4 - 40, 260), Image.Resampling.LANCZOS)
            im.paste(p_img, (cx + int((card_w4 - p_img.width)/2), y + 35))
        draw.text((cx + 20, y + 325), p_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((cx + 20, y + 370), p_tag, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        draw.text((cx + 20, y + 420), p_d, font=f['sub_en'], fill='#94A3B8', anchor='lt')
        
        draw.rounded_rectangle([cx + 20, y + 540, cx + card_w4 - 20, y + 640], radius=10, fill='#163024')
        draw.text((cx + card_w4/2, y + 570), "Acidity Index: pH 3.2 – 3.6", font=f['sub_en'], fill='#10B981', anchor='mm')
        draw.text((cx + card_w4/2, y + 610), "Crisp Snap • Zero Artificial Colors", font=f['sub_en'], fill='#D4A836', anchor='mm')
        cx += card_w4 + 26

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 6: Packaging Architecture
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Multi-Tier Packaging Architecture", "Section 05 // Foodservice Cans, Bulk HDPE Drums, Retail Jars & Pallets", is_mobile=False)

    tiers = [
        ("Foodservice A10 Cans", "Institutional Packaging", "WhatsApp Image 2026-09-05 at 12.52.17 PM (7).jpeg", "Food-grade double-lacquered tinplate with hermetic double-seam; 3kg & 5kg gross; 36-month shelf life."),
        ("Industrial Bulk HDPE Drums", "Bulk Repacking & OEM", "WhatsApp Image 2026-09-05 at 12.52.17 PM (4).jpeg", "150kg to 220kg food-grade high-density polymer barrels; airtight lever-lock ring for industrial repacking."),
        ("Retail Glass Jars", "Supermarket Shelves", "WhatsApp Image 2026-09-05 at 12.52.16 PM (4).jpeg", "370ml, 500ml, 720ml & 1000ml crystal-clear flint glass; vacuum twist-off safety caps with tamper-evident button."),
        ("Palletization & Moisture Wrap", "Intermodal Export Security", "WhatsApp Image 2026-09-05 at 12.52.15 PM (5).jpeg", "ISPM-15 certified heat-treated timber pallets; multi-layer automated stretch film & container desiccant poles.")
    ]
    card_w4 = 430
    cx = 60
    for p_t, p_tag, img_p, p_d in tiers:
        draw.rounded_rectangle([cx, y + 20, cx + card_w4, y + 680], radius=18, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((card_w4 - 40, 260), Image.Resampling.LANCZOS)
            im.paste(p_img, (cx + int((card_w4 - p_img.width)/2), y + 35))
        draw.text((cx + 20, y + 325), p_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((cx + 20, y + 370), p_tag, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        draw.text((cx + 20, y + 420), p_d, font=f['sub_en'], fill='#94A3B8', anchor='lt')
        cx += card_w4 + 26

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 7: Private Label & OEM
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Turnkey Private Label & OEM Solutions", "Section 06 // Custom Recipes, Regulatory Compliance & Labeling", is_mobile=False)

    col_w_l = 1060
    stages = [
        ("1. Cultivar Selection & Agro Sourcing", "Direct farm-gate contract sourcing across Fayoum, Ismailia & Sinai groves."),
        ("2. Custom Brine & Flavor Formulation", "Customized salinity, acidity, and aromatic herb infusions (dill, garlic, chili)."),
        ("3. Precision Calibrated Cutting", "Calibrated 3.2mm slicing, whole pitted, or custom diced geometries."),
        ("4. Multi-Jurisdictional Compliance", "Full compliance with US FDA FSMA, EU FIC 1169/2011, and Gulf GSO standards."),
        ("5. Primary Packaging & Litho Printing", "Private brand label application, barcode verification, and reinforced export cartons."),
        ("6. QC Release & Container Dispatch", "Microbiological inspection, COA issuance, and phytosanitary clearance.")
    ]
    sy = y + 20
    for s_t, s_d in stages:
        draw.rounded_rectangle([60, sy, col_w_l, sy + 95], radius=14, fill='#10221A', outline='#2D5232', width=1)
        draw.text((85, sy + 18), s_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((85, sy + 54), s_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        sy += 112

    img_oem = "WhatsApp Image 2026-09-05 at 12.52.19 PM (1).jpeg"
    if os.path.exists(img_oem):
        oi = Image.open(img_oem).convert('RGB')
        oi.thumbnail((700, 360), Image.Resampling.LANCZOS)
        im.paste(oi, (1140, y + 20))

    draw.rounded_rectangle([1140, y + 400, W - 60, y + 680], radius=18, fill='#163024', outline='#D4A836', width=2)
    draw.text(((1140 + W - 60)/2, y + 440), "Dual Brand Strategic Flexibility", font=f['h2_en'], fill='#D4A836', anchor='mm')
    draw.text(((1140 + W - 60)/2, y + 490), "• Khaeer Alwadi Brand: Turnkey, shelf-ready brand for immediate distribution", font=f['body_en'], fill='#E2E8F0', anchor='mm')
    draw.text(((1140 + W - 60)/2, y + 550), "• Private Label (OEM): Complete customized manufacturing under client's trademark", font=f['body_en'], fill='#E2E8F0', anchor='mm')
    draw.text(((1140 + W - 60)/2, y + 610), "Full confidentiality agreements (NDA) & international trade compliance guaranteed", font=f['sub_en'], fill='#10B981', anchor='mm')

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 8: Technical Specs & Freight Matrix
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Technical Specifications & Container Freight Matrix", "Section 07 // Quality Parameters & FCL Freight Payloads", is_mobile=False)

    draw.rounded_rectangle([60, y + 20, 1100, y + 680], radius=18, fill='#10221A', outline='#2D5232', width=2)
    draw.text((90, y + 55), "Quality Specification & Chemical Standard Matrix:", font=f['h2_en'], fill='#D4A836', anchor='lt')
    
    specs = [
        ("Table Olives (Whole & Pitted)", "Drained Weight ≥ 52% | pH 3.8–4.2 | Salinity 5.0–6.0% | Defects < 1.0%"),
        ("Sliced Black Olives (3.2mm)", "Drained Weight ≥ 50% | Ring Thickness 3.2mm | Fragment < 1.5% | Salinity 4.5–5.5%"),
        ("Gourmet Pickled Peppers & Pepperoncini", "Drained Weight ≥ 52% | pH 3.2–3.6 | Salinity 3.5–4.5% | Crunchy Snap"),
        ("Traditional Turshi Baladi & Gherkins", "Drained Weight ≥ 50% | pH 3.3–3.7 | Salinity 4.0–5.0% | No Artificial Colors")
    ]
    ty = y + 120
    for sp_t, sp_d in specs:
        draw.rounded_rectangle([90, ty, 1070, ty + 105], radius=12, fill='#163024')
        draw.text((120, ty + 20), sp_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((120, ty + 60), sp_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        ty += 130

    draw.rounded_rectangle([1140, y + 20, W - 60, y + 680], radius=18, fill='#0B261A', outline='#10B981', width=2)
    draw.text(((1140 + W - 60)/2, y + 55), "Ocean Freight Intermodal Container Loading (FCL)", font=f['h2_en'], fill='#10B981', anchor='mm')
    draw.line([(1170, y + 95), (W - 90, y + 95)], fill='#2D5232', width=1)

    draw.text((1170, y + 140), "20ft FCL Standard Dry Container:", font=f['h3_en'], fill='#D4A836', anchor='lt')
    draw.text((1170, y + 185), "• Capacity: 10 ISPM-15 heat-treated wood pallets", font=f['body_en'], fill='#FFFFFF', anchor='lt')
    draw.text((1170, y + 230), "• Net Payload: 18,000 – 21,000 kg (packaging dependent)", font=f['body_en'], fill='#E2E8F0', anchor='lt')

    draw.text((1170, y + 320), "40ft High Cube Container (40ft HC):", font=f['h3_en'], fill='#D4A836', anchor='lt')
    draw.text((1170, y + 365), "• Capacity: 20 to 22 standard pallets", font=f['body_en'], fill='#FFFFFF', anchor='lt')
    draw.text((1170, y + 410), "• Net Payload: 24,500 – 26,000 kg (max legal road limit)", font=f['body_en'], fill='#E2E8F0', anchor='lt')

    draw.rounded_rectangle([1170, y + 520, W - 90, y + 640], radius=14, fill='#10221A')
    draw.text(((1140 + W - 60)/2, y + 560), "Maritime Moisture & Condensation Protection", font=f['h3_en'], fill='#FFFFFF', anchor='mm')
    draw.text(((1140 + W - 60)/2, y + 600), "Desiccant poles installed in every export container", font=f['body_en'], fill='#94A3B8', anchor='mm')

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 9: Commercial Partnership Desk & Direct Line
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Commercial Partnerships & Direct Line", "Section 08 // Onboarding Protocol, Quotations & Contracting", is_mobile=False)

    col_w_l = 980
    onboardings = [
        ("1. Express Sample Dispatch Protocol", "Courier dispatch via DHL / FedEx within 48 hours for sensory & lab evaluation."),
        ("2. 24-Hour Formal Quotation Turnaround", "Transparent Incoterms (FOB Alexandria/Damietta/Port Said, CIF major global ports)."),
        ("3. Flexible & Secure Payment Terms", "Irrevocable Letter of Credit (L/C at sight) or T/T (30% advance, 70% against B/L)."),
        ("4. Fast-Track Production Laycan", "Standard order turnaround of 10–14 days from contract signing to vessel loading.")
    ]
    oy = y + 20
    for o_t, o_d in onboardings:
        draw.rounded_rectangle([60, oy, col_w_l, oy + 125], radius=16, fill='#10221A', outline='#2D5232', width=1)
        draw.text((85, oy + 25), o_t, font=f['h2_en'], fill='#D4A836', anchor='lt')
        draw.text((85, oy + 75), o_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        oy += 155

    draw.rounded_rectangle([1060, y + 20, W - 60, y + 680], radius=24, fill='#0B261A', outline='#10B981', width=3)
    cx_r = (1060 + W - 60) / 2
    
    if os.path.exists('khaeer-alwadi-logo.png'):
        logo = Image.open('khaeer-alwadi-logo.png').convert('RGBA')
        logo.thumbnail((320, 100), Image.Resampling.LANCZOS)
        im.paste(logo, (int(cx_r - logo.width/2), y + 55), logo)

    draw.text((cx_r, y + 190), "Khaeer Alwadi Food Industries", font=f['title_en'], fill='#D4A836', anchor='mm')
    draw.text((cx_r, y + 245), "Cairo Industrial Zone, Arab Republic of Egypt", font=f['h3_en'], fill='#FFFFFF', anchor='mm')
    draw.text((cx_r, y + 295), "Commercial Export & Procurement Desk", font=f['body_en'], fill='#94A3B8', anchor='mm')
    
    draw.rounded_rectangle([1120, y + 360, W - 120, y + 470], radius=20, fill='#10B981')
    draw.text((cx_r, y + 395), "Direct Orders & WhatsApp Line:", font=f['badge'], fill='#000000', anchor='mm')
    draw.text((cx_r, y + 438), "+20 10 08716714", font=f['title_en'], fill='#000000', anchor='mm')

    draw.text((cx_r, y + 520), "Direct Chat: wa.me/201008716714", font=f['h3_en'], fill='#10B981', anchor='mm')
    draw.text((cx_r, y + 575), "ISO 22000 • HACCP • FDA Registered • Halal • ISO 9001", font=f['badge'], fill='#D4A836', anchor='mm')
    draw.text((cx_r, y + 625), "Ready for immediate contract manufacturing & global export", font=f['body_en'], fill='#E2E8F0', anchor='mm')

    draw_footer_bar_en(im, draw, f, W, H, False)
    slides.append(im)

    return slides

# ----------------- ENGLISH MOBILE SLIDES (1080 x 1920) -----------------
def generate_english_mobile_slides():
    W, H = 1080, 1920
    f = load_fonts(scale=1.0)
    slides = []

    # Slide 1: Cover Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Khaeer Alwadi Food Industries", "Official B2B Export Portfolio",
                       "Cairo, Egypt • Mediterranean Agro Processing & Export", True)
    
    img_path = "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg"
    if os.path.exists(img_path):
        p_img = Image.open(img_path).convert('RGB')
        p_img.thumbnail((W - 140, 420), Image.Resampling.LANCZOS)
        im.paste(p_img, (int((W - p_img.width)/2), int(y)))
        y += p_img.height + 25

    draw.text((W/2, y+10), "Mediterranean Table Olives & Pickled Specialties", font=f['h2_en'], fill='#D4A836', anchor='mm')
    draw.text((W/2, y+48), "Direct Grove Sourcing & Turnkey OEM Solutions", font=f['h3_en'], fill='#FFFFFF', anchor='mm')
    y += 85

    pillars = [
        ("Direct Agro Sourcing", "15–25% landed cost advantage over Southern Europe."),
        ("Automated Processing", "High-speed pitting lines, rotary slicing & autoclave retort."),
        ("Tri-Port Logistics", "3–5 days to EU; 4–7 days to GCC via Alexandria & Damietta."),
        ("International Compliance", "Certified ISO 22000, HACCP, FDA Registered & Halal.")
    ]
    for p_t, p_d in pillars:
        draw.rounded_rectangle([60, y, W-60, y+115], radius=14, fill='#10221A', outline='#2D5232', width=2)
        draw.text((85, y+22), p_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((85, y+60), p_d, font=f['body_en'], fill='#F8FAFC', anchor='lt')
        y += 130

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 2: Strategic Supply Advantage Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "The Egyptian Supply Advantage", "Tri-Port Proximity & Free Trade Agreements",
                       "Short-Sea Shipping & 0% Tariff Corridors", True)

    draw.rounded_rectangle([60, y, W-60, y+150], radius=16, fill='#1A3324', outline='#D4A836', width=2)
    draw.text((W/2, y+35), "15%–25% Landed Cost Advantage vs Southern Europe", font=f['h3_en'], fill='#D4A836', anchor='mm')
    draw.text((W/2, y+80), "Agricultural yield • Competitive manufacturing • Short-sea feeder corridors", font=f['body_en'], fill='#FFFFFF', anchor='mm')
    y += 175

    draw.text((65, y), "Tri-Port Maritime Corridors:", font=f['h2_en'], fill='#D4A836', anchor='lt')
    y += 45
    ports = [
        ("Alexandria Port (2.5h)", "Major Mediterranean hub; direct feeder lines to EU"),
        ("Damietta Port (2.5h)", "Modern container terminal; rapid customs clearance"),
        ("Port Said Port (2.0h)", "Suez Canal entrance; instant access to Arabian Gulf")
    ]
    for p_t, p_d in ports:
        draw.rounded_rectangle([60, y, W-60, y+95], radius=14, fill='#10221A', outline='#2D5232', width=2)
        draw.text((85, y+20), p_t, font=f['h3_en'], fill='#FFFFFF', anchor='lt')
        draw.text((85, y+55), p_d, font=f['body_en'], fill='#94A3B8', anchor='lt')
        y += 110

    y += 10
    draw.text((65, y), "Multilateral Free Trade Pacts:", font=f['h2_en'], fill='#D4A836', anchor='lt')
    y += 45
    pacts = [
        ("GAFTA (Greater Arab Free Trade)", "0% customs across all Arab League & GCC states"),
        ("COMESA Free Trade Area", "Duty-free access across 21 African member countries"),
        ("Agadir Euro-Mediterranean Agreement", "Accumulation of industrial origin with the EU"),
        ("Egypt–EU Association Agreement", "Preferential duty-free entry into European markets")
    ]
    for pact_t, pact_d in pacts:
        draw.rounded_rectangle([60, y, W-60, y+90], radius=12, fill='#10221A', outline='#2D5232', width=1)
        draw.text((85, y+18), pact_t, font=f['h3_en'], fill='#FFFFFF', anchor='lt')
        draw.text((85, y+52), pact_d, font=f['sub_en'], fill='#94A3B8', anchor='lt')
        y += 105

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 3: Infrastructure Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Infrastructure & Compliance", "Automated Machinery & Food Safety Audits",
                       "High-Throughput Pitting, Rotary Slicing & Autoclave Retort", True)

    img_auto = "WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg"
    if os.path.exists(img_auto):
        ai = Image.open(img_auto).convert('RGB')
        ai.thumbnail((W - 140, 360), Image.Resampling.LANCZOS)
        im.paste(ai, (int((W - ai.width)/2), int(y)))
        y += ai.height + 25

    techs = [
        ("Automated Pitting Lines", "Precision stone removal with <1% fragment tolerance"),
        ("Rotary Slicing Drums", "Uniform 3.2mm ±0.2mm ring cuts for pizza chains"),
        ("Overpressure Autoclave Retort", "Controlled thermal processing; F0 ≥ 4.0; 36-mo shelf life")
    ]
    for t_t, t_d in techs:
        draw.rounded_rectangle([60, y, W-60, y+100], radius=14, fill='#10221A', outline='#2D5232', width=2)
        draw.text((85, y+20), t_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((85, y+58), t_d, font=f['body_en'], fill='#94A3B8', anchor='lt')
        y += 115

    y += 10
    draw.text((65, y), "International Certifications:", font=f['h2_en'], fill='#D4A836', anchor='lt')
    y += 45
    badges = [
        ("ISO 22000:2018", "Food Safety Management System Certified"),
        ("HACCP Certified", "Hazard Analysis Critical Control Points"),
        ("FDA Registered", "US FSMA & 21 CFR Part 117 Compliant"),
        ("Halal Certified", "100% Halal Compliant Processing Plant"),
        ("ISO 9001:2015", "Quality Management System Certified")
    ]
    for b_t, b_d in badges:
        draw.rounded_rectangle([60, y, W-60, y+65], radius=10, fill='#0F281E', outline='#10B981', width=1)
        draw.text((85, y+20), b_t, font=f['badge'], fill='#10B981', anchor='lt')
        draw.text((W-85, y+20), b_d, font=f['body_en'], fill='#FFFFFF', anchor='rt')
        y += 78

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 4: Table Olives Portfolio Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Table Olives Portfolio", "Core Line I: Whole, Pitted, Sliced & Stuffed",
                       "Premium Mediterranean Olives in Heavy Cans & Jars", True)

    products_olives = [
        ("Sliced Black Olives (3.2mm)", "Caliber 200/220 • Pizza & Foodservice", "WhatsApp Image 2026-09-05 at 12.52.20 PM.jpeg"),
        ("Pitted Black Olives", "Caliber 180/200 • Firm Meaty Texture", "WhatsApp Image 2026-09-05 at 12.52.16 PM (5).jpeg"),
        ("Picual & Manzanilla Green", "Caliber 240/260 • Crisp Orchard Snap", "WhatsApp Image 2026-09-05 at 12.52.17 PM (6).jpeg"),
        ("Pimento-Stuffed Olives", "100% Natural Paste • Supermarket Jars", "WhatsApp Image 2026-09-05 at 12.52.17 PM (5).jpeg"),
        ("Kalamata-Style Dark", "Natural Fermentation • Oil & Herb Brine", "WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg")
    ]
    for p_t, p_d, img_p in products_olives:
        draw.rounded_rectangle([60, y, W-60, y+195], radius=16, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((170, 170), Image.Resampling.LANCZOS)
            im.paste(p_img, (75, y+12))
        draw.text((275, y+25), p_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((275, y+75), p_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        draw.rounded_rectangle([275, y+125, 520, y+165], radius=8, fill='#1E3A24')
        draw.text((397, y+145), "Drained Weight ≥ 52%", font=f['sub_en'], fill='#10B981', anchor='mm')
        y += 215

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 5: Pickled Specialties Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Pickled Specialties & Peppers", "Core Line II: Pepperoncini, Chilis & Pickles",
                       "Golden Pepperoncini, Red Chilis, Turshi & Gherkins", True)

    products_pickles = [
        ("Golden Tuscan Pepperoncini", "Mild heat & tangy crunch • A10 Tins & Jars", "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg"),
        ("Gourmet Hot Red Chilis", "Selected whole vibrant chili pods", "WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg"),
        ("Traditional Turshi Baladi", "Carrots, turnips & cucumbers in spiced brine", "WhatsApp Image 2026-09-05 at 12.52.16 PM (2).jpeg"),
        ("Crisp Pickled Gherkins", "Unmatched crunch in dill & yellow mustard brine", "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg")
    ]
    for p_t, p_d, img_p in products_pickles:
        draw.rounded_rectangle([60, y, W-60, y+240], radius=16, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((210, 210), Image.Resampling.LANCZOS)
            im.paste(p_img, (75, y+15))
        draw.text((310, y+35), p_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((310, y+90), p_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        draw.rounded_rectangle([310, y+150, 560, y+190], radius=8, fill='#1E3A24')
        draw.text((435, y+170), "Acidity: pH 3.2–3.6", font=f['sub_en'], fill='#10B981', anchor='mm')
        y += 265

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 6: Packaging Architecture Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Packaging Architecture", "Multi-Tier Formats: Cans, Drums, Jars & Pallets",
                       "Institutional A10, Bulk HDPE & Supermarket Glass", True)

    tiers = [
        ("Foodservice A10 Cans", "3kg & 5kg cans; hermetic seam; 36-month shelf life", "WhatsApp Image 2026-09-05 at 12.52.17 PM (7).jpeg"),
        ("Bulk Polymer Drums", "150kg to 220kg HDPE drums with clamp ring seal", "WhatsApp Image 2026-09-05 at 12.52.17 PM (4).jpeg"),
        ("Retail Glass Jars", "370ml to 1,000ml flint glass with safety twist-off caps", "WhatsApp Image 2026-09-05 at 12.52.16 PM (4).jpeg"),
        ("Palletization & Wrap", "ISPM-15 heat-treated pallets & stretch barrier wrap", "WhatsApp Image 2026-09-05 at 12.52.15 PM (5).jpeg")
    ]
    for p_t, p_d, img_p in tiers:
        draw.rounded_rectangle([60, y, W-60, y+240], radius=16, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((210, 210), Image.Resampling.LANCZOS)
            im.paste(p_img, (75, y+15))
        draw.text((310, y+40), p_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((310, y+95), p_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        y += 265

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 7: Private Label Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Private Label & OEM Solutions", "Turnkey Manufacturing for Global Food Brands",
                       "Integrated 6-Stage Contract Production Workflow", True)

    img_oem = "WhatsApp Image 2026-09-05 at 12.52.19 PM (1).jpeg"
    if os.path.exists(img_oem):
        oi = Image.open(img_oem).convert('RGB')
        oi.thumbnail((W - 140, 360), Image.Resampling.LANCZOS)
        im.paste(oi, (int((W - oi.width)/2), int(y)))
        y += oi.height + 25

    stages = [
        ("1. Cultivar Selection & Sourcing", "Direct farm-gate contract sourcing across Fayoum & Sinai."),
        ("2. Custom Brine Formulation", "Adjusted salinity, acidity, and aromatic spice recipes."),
        ("3. Precision Calibrated Cutting", "Uniform 3.2mm slices, whole, or pitted geometries."),
        ("4. Regulatory Label Compliance", "Full compliance with US FDA, EU FIC & GSO standards."),
        ("5. Custom Secondary Packaging", "Private brand label application & reinforced cartons."),
        ("6. QC Release & Shipping", "Microbiological inspection & COA phytosanitary dispatch.")
    ]
    for s_t, s_d in stages:
        draw.rounded_rectangle([60, y, W-60, y+95], radius=12, fill='#10221A', outline='#2D5232', width=1)
        draw.text((85, y+18), s_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((85, y+55), s_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        y += 115

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 8: Technical Specs Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Technical Specifications & Freight", "Quality Matrix & Container Intermodal Capacities",
                       "Quality Parameters, Tolerances & Pallet Load Limits", True)

    draw.rounded_rectangle([60, y, W-60, y+200], radius=16, fill='#163024', outline='#D4A836', width=2)
    draw.text((W/2, y+25), "Intermodal Container Payload Capacity (FCL)", font=f['h3_en'], fill='#D4A836', anchor='mm')
    draw.line([(90, y+55), (W-90, y+55)], fill='#2D5232', width=1)
    
    draw.text((90, y+80), "20ft FCL Standard Container:", font=f['h3_en'], fill='#FFFFFF', anchor='lt')
    draw.text((90, y+115), "10 ISPM-15 Wood Pallets • Net: ~18,000 – 21,000 kg", font=f['body_en'], fill='#94A3B8', anchor='lt')
    
    draw.text((90, y+145), "40ft High Cube Container (HC):", font=f['h3_en'], fill='#FFFFFF', anchor='lt')
    draw.text((90, y+180), "20–22 Pallets • Net: ~24,500 – 26,000 kg (Road Limit)", font=f['body_en'], fill='#94A3B8', anchor='lt')
    y += 230

    draw.text((65, y), "Chemical & Physical Quality Matrix:", font=f['h2_en'], fill='#D4A836', anchor='lt')
    y += 45

    specs = [
        ("Table Olives (Whole & Pitted)", "Drained Weight ≥ 52% • pH 3.8–4.2 • Salinity 5–6% • Defects < 1%"),
        ("Sliced Black Olives (3.2mm)", "Drained Weight ≥ 50% • Thickness 3.2mm • Fragment < 1.5%"),
        ("Gourmet Pickled Peppers", "Drained Weight ≥ 52% • pH 3.2–3.6 • Salinity 3.5–4.5% • Crisp"),
        ("Turshi Baladi & Gherkins", "Drained Weight ≥ 50% • pH 3.3–3.7 • Salinity 4.0–5.0% • Clean")
    ]
    for sp_t, sp_d in specs:
        draw.rounded_rectangle([60, y, W-60, y+115], radius=14, fill='#10221A', outline='#2D5232', width=1)
        draw.text((85, y+20), sp_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((85, y+62), sp_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        y += 135

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 9: Commercial Desk Mobile
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header_en(im, draw, f, W, "Commercial Partnerships Desk", "Sample Dispatch, Formal Quotations & Direct Line",
                       "Fast-Track Buyer Onboarding & Procurement Hotline", True)

    onboardings = [
        ("1. Express Sample Dispatch", "DHL / FedEx courier kits dispatched within 48 hours"),
        ("2. 24-Hour Formal Quotation", "Transparent pricing under FOB Egypt or CIF global ports"),
        ("3. Flexible Payment Terms", "Irrevocable L/C at sight or secure wire transfer T/T"),
        ("4. Standard Laycan Dispatch", "10 to 14 days standard production turnaround to vessel")
    ]
    for o_t, o_d in onboardings:
        draw.rounded_rectangle([60, y, W-60, y+95], radius=12, fill='#10221A', outline='#2D5232', width=1)
        draw.text((85, y+18), o_t, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((85, y+55), o_d, font=f['body_en'], fill='#FFFFFF', anchor='lt')
        y += 115

    y += 15
    draw.rounded_rectangle([60, y, W-60, y+380], radius=24, fill='#0B261A', outline='#10B981', width=3)
    draw.text((W/2, y+45), "Khaeer Alwadi Food Industries", font=f['title_en'], fill='#D4A836', anchor='mm')
    draw.text((W/2, y+95), "Cairo Industrial Zone, Arab Republic of Egypt", font=f['h3_en'], fill='#FFFFFF', anchor='mm')
    draw.text((W/2, y+140), "Global Agro-Processing & Export Desk", font=f['body_en'], fill='#94A3B8', anchor='mm')
    
    draw.rounded_rectangle([100, y+180, W-100, y+270], radius=18, fill='#10B981')
    draw.text((W/2, y+212), "Direct WhatsApp & Orders:", font=f['badge'], fill='#000000', anchor='mm')
    draw.text((W/2, y+245), "+20 10 08716714", font=f['title_en'], fill='#000000', anchor='mm')

    draw.text((W/2, y+310), "Direct WhatsApp Link: wa.me/201008716714", font=f['h3_en'], fill='#10B981', anchor='mm')
    draw.text((W/2, y+350), "ISO 22000 • HACCP • FDA Registered • Halal • ISO 9001", font=f['badge'], fill='#D4A836', anchor='mm')

    draw_footer_bar_en(im, draw, f, W, H, True)
    slides.append(im)

    return slides

def main():
    print("Building English Widescreen Presentation Deck (1920x1080 landscape)...")
    en_pres = generate_english_presentation_slides()
    en_pres_path = "Khaeer-Alwadi-Presentation-Deck-EN.pdf"
    en_pres[0].save(en_pres_path, save_all=True, append_images=en_pres[1:], resolution=150.0)
    print(f"Generated {en_pres_path} successfully ({len(en_pres)} slides, size: {os.path.getsize(en_pres_path)/1024:.1f} KB)")

    en_b2b_path = "Khaeer-Alwadi-B2B-Deck-EN.pdf"
    en_pres[0].save(en_b2b_path, save_all=True, append_images=en_pres[1:], resolution=150.0)
    print(f"Generated {en_b2b_path} successfully ({len(en_pres)} slides, size: {os.path.getsize(en_b2b_path)/1024:.1f} KB)")

    print("Building English Mobile-Optimized Deck (1080x1920 portrait)...")
    en_mob = generate_english_mobile_slides()
    en_mob_path = "Khaeer-Alwadi-Mobile-Deck-EN.pdf"
    en_mob[0].save(en_mob_path, save_all=True, append_images=en_mob[1:], resolution=150.0)
    print(f"Generated {en_mob_path} successfully ({len(en_mob)} slides, size: {os.path.getsize(en_mob_path)/1024:.1f} KB)")

if __name__ == '__main__':
    main()
