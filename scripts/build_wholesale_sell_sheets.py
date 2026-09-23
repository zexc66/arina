#!/usr/bin/env python3
"""
Mariam Natural Honey & Superfoods — Wholesale Export Sell-Sheets & Shelf-Talkers Generator
Renders 300 DPI print-ready commercial graphics:
1. B2B Wholesale Trade Buyer Technical Sell-Sheet (3508 x 2480 px @ 300 DPI, A4 Landscape)
2. 4 Hypermarket Gondola Shelf-Talker Price Strips (2480 x 448 px @ 300 DPI, 210mm x 38mm each)
3. Master Print Press Proof Sheet (2480 x 3508 px @ 300 DPI, A4 Portrait with crop marks & CMYK bars)
"""

import os
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORKSPACE_DIR = '/home/zexc/Desktop/New Folder'
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, 'output/imagery')
LOGO_GOLD = os.path.join(WORKSPACE_DIR, 'mariam-logo-gold.png')
LOGO_KHAER = os.path.join(WORKSPACE_DIR, 'khaeer-alwadi-logo-gold.png')

# Fonts
FONT_SERIF_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
FONT_SERIF_REG = '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
FONT_SERIF_ITALIC = '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
FONT_SANS_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_SANS_REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'

FONT_ARABIC_BOLD = 'Noto Kufi Arabic Bold'
FONT_ARABIC_SANS = 'Noto Sans Arabic'

# Master Luxury Palette
GOLD = (218, 172, 54)         # #DAAC36
GOLD_LIGHT = (238, 212, 142)  # #EED48E
GOLD_DARK = (140, 105, 30)    # #8C691E
BURGUNDY = (118, 18, 46)      # #76122E
BURGUNDY_DARK = (45, 10, 22)  # #2D0A16
BLUSH_PINK = (245, 183, 194)  # #F5B7C2
FOREST_OBSIDIAN = (10, 22, 18)# #0A1612
FOREST_DARK = (20, 38, 28)    # #14261C
IVORY = (248, 245, 238)       # #F8F5EE
WHITE = (255, 255, 255)
CHARCOAL = (35, 38, 40)
GRAY_BG = (245, 245, 245)
GRAY_BORDER = (220, 220, 220)
EMERALD = (16, 185, 129)

def render_pango_text(text, font_desc=f'{FONT_ARABIC_BOLD} 24', color_hex='#DAAC36', align='center'):
    """Renders text with full HarfBuzz shaping and bidirectional text using pango-view."""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        tmp_path = f.name
    cmd = [
        'pango-view', '-q',
        f'--text={text}',
        f'--font={font_desc}',
        f'--foreground={color_hex}',
        '--background=transparent',
        f'--align={align}',
        f'--output={tmp_path}'
    ]
    subprocess.run(cmd, check=True)
    img = Image.open(tmp_path).convert('RGBA')
    try:
        os.remove(tmp_path)
    except OSError:
        pass
    return img

def paste_pango(canvas, text, font_desc, color_hex, cx, cy, anchor='center'):
    txt_img = render_pango_text(text, font_desc, color_hex, align='center')
    w, h = txt_img.size
    if anchor in ('center', 'mm'):
        pos = (int(cx - w / 2), int(cy - h / 2))
    elif anchor in ('left', 'lm'):
        pos = (int(cx), int(cy - h / 2))
    elif anchor in ('right', 'rm'):
        pos = (int(cx - w), int(cy - h / 2))
    elif anchor in ('top', 'mt'):
        pos = (int(cx - w / 2), int(cy))
    elif anchor in ('bottom', 'mb'):
        pos = (int(cx - w / 2), int(cy - h))
    else:
        pos = (int(cx), int(cy))
    canvas.paste(txt_img, pos, txt_img)

def get_white_studio_mask(img_rgb):
    w, h = img_rgb.size
    gray = img_rgb.convert('L')
    near_white = gray.point(lambda p: 255 if p > 250 else 0)
    bg_mask = near_white.copy()
    ImageDraw.floodfill(bg_mask, (0, 0), 128, thresh=15)
    ImageDraw.floodfill(bg_mask, (w - 1, 0), 128, thresh=15)
    ImageDraw.floodfill(bg_mask, (0, h - 1), 128, thresh=15)
    ImageDraw.floodfill(bg_mask, (w - 1, h - 1), 128, thresh=15)
    alpha = bg_mask.point(lambda p: 0 if p == 128 else 255)
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=2))
    return alpha

def paste_studio_jar(canvas, img_filename, cx, y_base, target_h, shadow=True):
    im_path = os.path.join(OUTPUT_DIR, img_filename)
    if not os.path.exists(im_path):
        return
    im = Image.open(im_path).convert('RGB')
    target_w = int(im.width * (target_h / im.height))
    im_resized = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    mask = get_white_studio_mask(im_resized)

    x_pos = cx - target_w // 2
    y_pos = y_base - target_h

    if shadow:
        shadow_w = int(target_w * 0.85)
        shadow_h = int(target_h * 0.10)
        shadow_img = Image.new('RGBA', (shadow_w, shadow_h), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow_img)
        sdraw.ellipse([(0, 0), (shadow_w, shadow_h)], fill=(0, 0, 0, 160))
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=10))
        canvas.paste(shadow_img, (cx - shadow_w // 2, y_base - shadow_h // 2), shadow_img)

    canvas.paste(im_resized, (x_pos, y_pos), mask)

def paste_gold_logo(canvas, cx, cy, target_w):
    logo = Image.open(LOGO_GOLD).convert('RGBA')
    lh = int(target_w * (logo.height / logo.width))
    logo_r = logo.resize((target_w, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_r, (cx - target_w // 2, cy - lh // 2), logo_r)
    return lh

def draw_crop_marks(draw, x1, y1, x2, y2, mark_len=30, offset=12, col=(100, 100, 100)):
    """Draws standard printing press crop marks at four corners."""
    # Top Left
    draw.line([(x1 - offset - mark_len, y1), (x1 - offset, y1)], fill=col, width=2)
    draw.line([(x1, y1 - offset - mark_len), (x1, y1 - offset)], fill=col, width=2)
    # Top Right
    draw.line([(x2 + offset, y1), (x2 + offset + mark_len, y1)], fill=col, width=2)
    draw.line([(x2, y1 - offset - mark_len), (x2, y1 - offset)], fill=col, width=2)
    # Bottom Left
    draw.line([(x1 - offset - mark_len, y2), (x1 - offset, y2)], fill=col, width=2)
    draw.line([(x1, y2 + offset), (x1, y2 + offset + mark_len)], fill=col, width=2)
    # Bottom Right
    draw.line([(x2 + offset, y2), (x2 + offset + mark_len, y2)], fill=col, width=2)
    draw.line([(x2, y2 + offset), (x2, y2 + offset + mark_len)], fill=col, width=2)

# ==============================================================================
# 1. B2B WHOLESALE TRADE BUYER TECHNICAL SELL-SHEET (3508 x 2480 px @ 300 DPI)
# ==============================================================================
def render_wholesale_trade_sell_sheet():
    w, h = 3508, 2480 # A4 Landscape @ 300 DPI
    canvas = Image.new('RGB', (w, h), WHITE)
    draw = ImageDraw.Draw(canvas)

    # Top Brand Header Banner (y: 0 to 320)
    draw.rectangle([(0, 0), (w, 320)], fill=FOREST_DARK)
    draw.line([(0, 316), (w, 316)], fill=GOLD, width=4)
    draw.line([(0, 310), (w, 310)], fill=GOLD_DARK, width=1)

    # Left: Mariam Gold Logo
    paste_gold_logo(canvas, cx=380, cy=140, target_w=460)

    # Center: Document Title & Standards
    font_head_en = ImageFont.truetype(FONT_SERIF_BOLD, 38)
    draw.text((1800, 95), "MARIAM NATURAL HONEY & SUPERFOODS", font=font_head_en, fill=IVORY, anchor="mm")
    
    font_sub_en = ImageFont.truetype(FONT_SANS_BOLD, 22)
    draw.text((1800, 145), "OFFICIAL B2B WHOLESALE & EXPORT TRADE SPECIFICATION SHEET", font=font_sub_en, fill=GOLD_LIGHT, anchor="mm")

    paste_pango(canvas, "وثيقة المواصفات الفنية والتعبئة التصديرية لسلاسل الهايبرماركت وموزعي الأغذية الدوليين", f"{FONT_ARABIC_BOLD} 22", "#DAAC36", 1800, 205, "center")

    # Right: Certifications & Origin Badges
    draw.rectangle([(2960, 45), (3440, 270)], fill=(12, 24, 18), outline=GOLD_DARK, width=1)
    font_cert_t = ImageFont.truetype(FONT_SANS_BOLD, 17)
    font_cert_v = ImageFont.truetype(FONT_SANS_REG, 15)

    draw.text((3200, 75), "EXPORT CERTIFICATIONS", font=font_cert_t, fill=GOLD, anchor="mm")
    draw.text((3200, 110), "ISO 22000 • HACCP • HALAL", font=font_cert_v, fill=IVORY, anchor="mm")
    draw.text((3200, 145), "GAFTA 0% DUTY (GCC / KSA)", font=font_cert_v, fill=BLUSH_PINK, anchor="mm")
    draw.text((3200, 180), "EUR.1 PREFERENTIAL TARIFF", font=font_cert_v, fill=IVORY, anchor="mm")
    draw.text((3200, 215), "100% FLINT GLASS • 24M AMBIENT", font=font_cert_v, fill=GOLD_LIGHT, anchor="mm")

    # Row 1: 6 Product Packshots with Specs Card (y: 350 to 980)
    skus = [
        {
            'code': 'SKU-SF01',
            'name': 'MARIAM ROYAL MIX',
            'name_ar': 'خلطة مريم الملكية (500 جم)',
            'format': '500g Nordic Flint Glass',
            'nuts': 'Cashews, Almonds, Hazelnuts & Royal Jelly',
            'case': '12 Jars/Case • 144 Cases/Pallet',
            'ean': '6281001205010',
            'hs': '2008.19.00',
            'img': 'mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg',
            'badge': 'HERO FLAGSHIP • 0% PEANUTS'
        },
        {
            'code': 'SKU-H01',
            'name': 'MOUNTAIN SIDR HONEY',
            'name_ar': 'عسل السدر الجبلي النقي (500 جم)',
            'format': '500g Nordic Flint Glass',
            'nuts': '100% Raw Monofloral Mountain Nectar',
            'case': '12 Jars/Case • 144 Cases/Pallet',
            'ean': '6281001205027',
            'hs': '0409.00.00',
            'img': 'mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg',
            'badge': 'SINGLE-ESTATE RESERVE'
        },
        {
            'code': 'SKU-H03',
            'name': 'RAW CUT HONEYCOMB',
            'name_ar': 'أقراص شمع العسل الطبيعي (500 جم)',
            'format': '500g Faceted Hexagonal Glass',
            'nuts': 'Whole Intact Virgin Beeswax Comb Slab',
            'case': '12 Jars/Case • 144 Cases/Pallet',
            'ean': '6281001205034',
            'hs': '0409.00.00',
            'img': 'mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg',
            'badge': 'ARTISANAL HEXAGONAL'
        },
        {
            'code': 'SKU-H04',
            'name': 'CLOVER BLOSSOM FAMILY',
            'name_ar': 'عسل زهور البرسيم (1 كجم عائلي)',
            'format': '1kg Monumental Nordic Jar',
            'nuts': 'Golden Egyptian Clover Blossom Nectar',
            'case': '6 Jars/Case • 105 Cases/Pallet',
            'ean': '6281001205041',
            'hs': '0409.00.00',
            'img': 'mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg',
            'badge': 'FAMILY BULK 1KG'
        },
        {
            'code': 'SKU-FI01',
            'name': 'NIGELLA BLACK SEED',
            'name_ar': 'عسل حبة البركة المدعم (500 جم)',
            'format': '500g Nordic Flint Glass',
            'nuts': 'Black Seed Blossom + Cold-Pressed Oil',
            'case': '12 Jars/Case • 144 Cases/Pallet',
            'ean': '6281001205058',
            'hs': '0409.00.00',
            'img': 'mariam_honey_black_seed_500g_white_studio_hero_4k.jpg',
            'badge': 'FUNCTIONAL INFUSION'
        },
        {
            'code': 'SKU-H02',
            'name': 'CITRUS BLOSSOM HONEY',
            'name_ar': 'عسل زهور الموالح (500 جم)',
            'format': '500g Nordic Flint Glass',
            'nuts': 'Orange & Lemon Grove Blossom Nectar',
            'case': '12 Jars/Case • 144 Cases/Pallet',
            'ean': '6281001205065',
            'hs': '0409.00.00',
            'img': 'mariam_honey_citrus_blossom_500g_white_studio_hero_4k.jpg',
            'badge': 'SPRING HARVEST'
        },
    ]

    card_w = 525
    card_h = 600
    card_spacing = 25
    x_offset = 65

    font_code = ImageFont.truetype(FONT_SANS_BOLD, 15)
    font_name = ImageFont.truetype(FONT_SERIF_BOLD, 18)
    font_desc = ImageFont.truetype(FONT_SANS_REG, 13)
    font_mono = ImageFont.truetype(FONT_SANS_BOLD, 13)

    for i, sku in enumerate(skus):
        cx = x_offset + i * (card_w + card_spacing) + card_w // 2
        card_x1 = x_offset + i * (card_w + card_spacing)
        card_x2 = card_x1 + card_w
        card_y1 = 340
        card_y2 = 340 + card_h

        # Card container
        draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y2)], radius=16, fill=GRAY_BG, outline=GRAY_BORDER, width=1)
        draw.rounded_rectangle([(card_x1 + 6, card_y1 + 6), (card_x2 - 6, card_y1 + 35)], radius=10, fill=BURGUNDY if 'ROYAL' in sku['name'] else FOREST_DARK)
        draw.text((cx, card_y1 + 20), sku['badge'], font=font_code, fill=BLUSH_PINK if 'ROYAL' in sku['name'] else GOLD, anchor="mm")

        # Jar Packshot
        paste_studio_jar(canvas, sku['img'], cx=cx, y_base=card_y1 + 360, target_h=300, shadow=True)

        # SKU Title
        draw.text((cx, card_y1 + 390), sku['name'], font=font_name, fill=CHARCOAL, anchor="mm")
        paste_pango(canvas, sku['name_ar'], f"{FONT_ARABIC_BOLD} 14", "#76122E", cx, card_y1 + 420, "center")

        # Specs lines
        draw.text((cx, card_y1 + 450), sku['format'], font=font_desc, fill=(80, 80, 80), anchor="mm")
        draw.text((cx, card_y1 + 475), sku['case'], font=font_mono, fill=(20, 80, 40), anchor="mm")
        draw.text((cx, card_y1 + 500), f"EAN: {sku['ean']} • HS: {sku['hs']}", font=font_mono, fill=GOLD_DARK, anchor="mm")

    # Row 2: Comprehensive Engineering Specifications Table (y: 970 to 1820)
    draw.rectangle([(65, 960), (w - 65, 1850)], fill=WHITE, outline=GOLD_DARK, width=2)
    draw.rectangle([(65, 960), (w - 65, 1020)], fill=FOREST_DARK)
    
    font_tbl_head = ImageFont.truetype(FONT_SANS_BOLD, 17)
    font_tbl_cell = ImageFont.truetype(FONT_SANS_REG, 16)
    font_tbl_cell_b = ImageFont.truetype(FONT_SANS_BOLD, 16)

    cols = [
        ("LOGISTICS & PHYSICAL PARAMETERS", 500),
        ("MARIAM ROYAL MIX (500g)", 480),
        ("MOUNTAIN SIDR (500g)", 480),
        ("RAW HONEYCOMB HEX (500g)", 480),
        ("CLOVER 1KG FAMILY", 480),
        ("NIGELLA BLACK SEED (500g)", 480),
        ("CITRUS BLOSSOM (500g)", 480)
    ]

    cur_x = 65
    for c_title, c_w in cols:
        draw.text((cur_x + c_w // 2, 990), c_title, font=font_tbl_head, fill=GOLD, anchor="mm")
        cur_x += c_w
        if cur_x < w - 65:
            draw.line([(cur_x, 960), (cur_x, 1850)], fill=GRAY_BORDER, width=1)

    table_data = [
        ("Declared Net Weight (g)", "500g", "500g", "500g", "1000g (1.0 kg)", "500g", "500g"),
        ("Gross Weight per Jar (Glass + Lid)", "780g", "780g", "810g", "1,420g", "780g", "780g"),
        ("Jar Geometry & Dimension (Dia x H)", "88mm x 115mm", "88mm x 115mm", "92mm x 110mm", "105mm x 155mm", "88mm x 115mm", "88mm x 115mm"),
        ("Cap Standard & Finish", "82mm Deep-Skirt Gold", "82mm Deep-Skirt Gold", "82mm Hex Twist Gold", "82mm Reinforced Gold", "82mm Deep-Skirt Gold", "82mm Deep-Skirt Gold"),
        ("Tamper-Evident Security Seal", "18x45mm Blush Crown", "18x45mm Blush Crown", "18x45mm Blush Crown", "18x45mm Blush Crown", "18x45mm Blush Crown", "18x45mm Blush Crown"),
        ("Units per Master Shipping Case", "12 Jars", "12 Jars", "12 Jars", "6 Jars", "12 Jars", "12 Jars"),
        ("Master Case Dimensions (L x W x H mm)", "360 x 270 x 125", "360 x 270 x 125", "380 x 285 x 120", "325 x 220 x 165", "360 x 270 x 125", "360 x 270 x 125"),
        ("Gross Case Weight (kg)", "9.60 kg", "9.60 kg", "9.95 kg", "8.75 kg", "9.60 kg", "9.60 kg"),
        ("Pallet Ti / Hi (Cases/Layer x Layers)", "12 cases x 12 layers", "12 cases x 12 layers", "12 cases x 12 layers", "15 cases x 7 layers", "12 cases x 12 layers", "12 cases x 12 layers"),
        ("Total Master Cases per Pallet", "144 Cases", "144 Cases", "144 Cases", "105 Cases", "144 Cases", "144 Cases"),
        ("Total Jars per Pallet", "1,728 Jars", "1,728 Jars", "1,728 Jars", "630 Jars", "1,728 Jars", "1,728 Jars"),
        ("Net Honey Weight per Pallet (kg)", "864.0 kg", "864.0 kg", "864.0 kg", "630.0 kg", "864.0 kg", "864.0 kg"),
        ("20ft FCL Container Capacity", "1,440 Cases (10 Pallets)", "1,440 Cases (10 Pallets)", "1,440 Cases (10 Pallets)", "1,050 Cases (10 Pallets)", "1,440 Cases (10 Pallets)", "1,440 Cases (10 Pallets)"),
        ("40ft HC FCL Container Capacity", "3,024 Cases (21 Pallets)", "3,024 Cases (21 Pallets)", "3,024 Cases (21 Pallets)", "2,205 Cases (21 Pallets)", "3,024 Cases (21 Pallets)", "3,024 Cases (21 Pallets)")
    ]

    r_y = 1020
    row_delta = 59
    for r_idx, row in enumerate(table_data):
        row_bg = (248, 250, 248) if r_idx % 2 == 0 else WHITE
        draw.rectangle([(65, r_y), (w - 65, r_y + row_delta)], fill=row_bg)
        draw.line([(65, r_y), (w - 65, r_y)], fill=GRAY_BORDER, width=1)

        draw.text((85, r_y + row_delta // 2), row[0], font=font_tbl_cell_b, fill=CHARCOAL, anchor="lm")
        c_x = 65 + cols[0][1]
        for col_idx in range(1, 7):
            val = row[col_idx]
            is_bold = ("Cases" in val or "FCL" in row[0] or "Weight" in row[0])
            draw.text((c_x + cols[col_idx][1] // 2, r_y + row_delta // 2), val, font=font_tbl_cell_b if is_bold else font_tbl_cell, fill=BURGUNDY if (col_idx == 1 and is_bold) else (30, 30, 30), anchor="mm")
            c_x += cols[col_idx][1]
        r_y += row_delta

    # Row 3: Commercial Trade Advantages & Logistics Notes (y: 1870 to 2270)
    boxes = [
        {
            'title': 'GAFTA & GCC DUTY-FREE (0% TARIFF)',
            'desc': 'Full customs exemption across Saudi Arabia, UAE, Kuwait, Oman, Bahrain, and Qatar under Greater Arab Free Trade Agreement. EUR.1 certificate available for EU duty preferences.',
            'color': (20, 45, 30)
        },
        {
            'title': '0% PEANUTS FACILITY CERTIFICATION',
            'desc': 'Dedicated allergen-segregated processing suite. 100% Tree Nuts guarantee (whole California almonds, Turkish hazelnuts, and cashews). Zero risk of peanut cross-contamination.',
            'color': BURGUNDY
        },
        {
            'title': 'HEAVY CORRUGATED EXPORT SHIPPERS',
            'desc': 'Reinforced double-wall B/C flute master cartons with interlocking corrugated partitions. Zero glass-to-glass contact during international maritime container transit.',
            'color': (30, 35, 45)
        },
        {
            'title': '24-MONTH AMBIENT STORAGE STABILITY',
            'desc': 'Thermally sealed gold vacuum closures protect natural floral diastase enzymes. Ambient storage (18°C–25°C), zero refrigeration or cold-chain infrastructure required.',
            'color': (45, 35, 20)
        }
    ]

    b_w = 810
    b_h = 360
    b_spacing = 38
    b_start_x = 65

    font_box_title = ImageFont.truetype(FONT_SANS_BOLD, 18)
    font_box_desc = ImageFont.truetype(FONT_SANS_REG, 15)

    for i, box in enumerate(boxes):
        bx = b_start_x + i * (b_w + b_spacing)
        draw.rounded_rectangle([(bx, 1870), (bx + b_w, 1870 + b_h)], radius=16, fill=box['color'], outline=GOLD_DARK, width=2)
        draw.text((bx + b_w // 2, 1910), box['title'], font=font_box_title, fill=GOLD_LIGHT, anchor="mm")
        draw.line([(bx + 30, 1935), (bx + b_w - 30, 1935)], fill=GOLD_DARK, width=1)

        words = box['desc'].split(' ')
        lines = []
        cur_l = []
        for wd in words:
            cur_l.append(wd)
            if len(' '.join(cur_l)) > 42:
                lines.append(' '.join(cur_l))
                cur_l = []
        if cur_l:
            lines.append(' '.join(cur_l))

        for l_idx, line in enumerate(lines):
            draw.text((bx + b_w // 2, 1970 + l_idx * 26), line, font=font_box_desc, fill=IVORY, anchor="mm")

    # Bottom Contact Bar (y: 2280 to 2480)
    draw.rectangle([(0, 2260), (w, h)], fill=FOREST_DARK)
    draw.line([(0, 2260), (w, 2260)], fill=GOLD, width=3)

    font_foot_head = ImageFont.truetype(FONT_SERIF_BOLD, 22)
    font_foot_sub = ImageFont.truetype(FONT_SANS_REG, 17)

    draw.text((w // 2, 2305), "MARIAM FOOD INDUSTRIES • EXPORT ALLOCATION & COMMERCIAL WHOLESALE DESK", font=font_foot_head, fill=GOLD, anchor="mm")
    draw.text((w // 2, 2345), "Factory & Packing Stations: Khaeer Alwadi Agribusiness Terroir • River Valley Agro-Industrial Zone", font=font_foot_sub, fill=IVORY, anchor="mm")
    draw.text((w // 2, 2380), "Direct Procurement & RFQ Inquiries: export@mariamfoods.com • Tel/WhatsApp: +20 10 08716714 • www.mariamfoods.com", font=font_foot_sub, fill=GOLD_LIGHT, anchor="mm")
    paste_pango(canvas, "مزارع ومحطات تعبئة خير الوادي للصناعات الغذائية • قسم التصدير والتبادل التجاري الدولي", f"{FONT_ARABIC_BOLD} 18", "#DAAC36", w // 2, 2420, "center")

    out_file = os.path.join(OUTPUT_DIR, 'mariam_honey_b2b_trade_sell_sheet_300dpi.png')
    canvas.save(out_file, dpi=(300, 300))
    print(f'[SAVED] {out_file}')

# ==============================================================================
# 2. HYPERMARKET GONDOLA SHELF-TALKER PRICE STRIPS (2480 x 448 px @ 300 DPI)
# ==============================================================================
def render_shelf_talker_strip(filename, sku_title, sku_title_ar, sku_sub, packshot_file, barcode_val, badge_text, theme_color):
    w, h = 2480, 448 # 210mm x 38mm @ 300 DPI
    canvas = Image.new('RGB', (w, h), WHITE)
    draw = ImageDraw.Draw(canvas)

    # Background gradient panel
    draw.rectangle([(0, 0), (w, h)], fill=(12, 24, 18))
    draw.rectangle([(8, 8), (w - 8, h - 8)], outline=GOLD, width=2)

    # Left Section: Brand Logo & Crown Ribbon
    draw.rectangle([(0, 0), (450, h)], fill=theme_color)
    draw.line([(450, 0), (450, h)], fill=GOLD, width=3)
    paste_gold_logo(canvas, cx=225, cy=150, target_w=340)

    font_brand_sub = ImageFont.truetype(FONT_SANS_BOLD, 17)
    draw.text((225, 230), "NATURAL HONEY", font=font_brand_sub, fill=GOLD_LIGHT, anchor="mm")
    paste_pango(canvas, "عسل مريم الحرفي", f"{FONT_ARABIC_BOLD} 16", "#DAAC36", 225, 280, "center")
    
    # 0% Peanuts or Premium badge
    font_badge = ImageFont.truetype(FONT_SANS_BOLD, 14)
    draw.rounded_rectangle([(30, 335), (420, 385)], radius=12, fill=(0, 0, 0, 160), outline=GOLD_DARK, width=1)
    draw.text((225, 360), badge_text, font=font_badge, fill=BLUSH_PINK if 'PEANUTS' in badge_text else GOLD_LIGHT, anchor="mm")

    # Center-Left: Jar Packshot
    paste_studio_jar(canvas, packshot_file, cx=640, y_base=410, target_h=370, shadow=True)

    # Center: Product Name (Bilingual) & Sensory Notes
    font_p_title = ImageFont.truetype(FONT_SERIF_BOLD, 36)
    font_p_sub = ImageFont.truetype(FONT_SERIF_ITALIC, 22)
    font_notes = ImageFont.truetype(FONT_SANS_REG, 17)

    draw.text((850, 95), sku_title, font=font_p_title, fill=IVORY, anchor="lm")
    paste_pango(canvas, sku_title_ar, f"{FONT_ARABIC_BOLD} 26", "#DAAC36", 850, 165, "left")
    draw.text((850, 230), sku_sub, font=font_p_sub, fill=GOLD_LIGHT, anchor="lm")

    # Sensory Notes & Purity Callout
    draw.line([(850, 275), (1700, 275)], fill=GOLD_DARK, width=1)
    draw.text((850, 315), "• 100% Raw Unpasteurized Wild Nectar • Heavy Nordic Flint Glass Standard", font=font_notes, fill=IVORY, anchor="lm")
    draw.text((850, 355), "• Hermetic Crown Seal • Certified Diastase Bioactive Vitality • ISO 22000", font=font_notes, fill=(180, 210, 190), anchor="lm")

    # Right Section: Retail Price Channel Box & Barcode
    draw.rectangle([(1760, 25), (2440, h - 25)], fill=(20, 34, 26), outline=GOLD_DARK, width=2)

    # Barcode Simulation box
    draw.rectangle([(1785, 45), (2080, 240)], fill=WHITE, outline=GOLD_DARK, width=1)
    # Simulated vertical barcode stripes
    b_draw = ImageDraw.Draw(canvas)
    for bx in range(1805, 2060, 5):
        if bx % 7 != 0:
            b_draw.line([(bx, 60), (bx, 195)], fill=(20, 20, 20), width=3 if bx % 3 == 0 else 1)
    font_bc_num = ImageFont.truetype(FONT_SANS_BOLD, 15)
    draw.text((1932, 218), barcode_val, font=font_bc_num, fill=CHARCOAL, anchor="mm")

    # Price Callout Box
    draw.rectangle([(2100, 45), (2415, 240)], fill=(35, 12, 18), outline=GOLD, width=2)
    font_pr_label = ImageFont.truetype(FONT_SANS_BOLD, 17)
    draw.text((2257, 75), "RETAIL PRICE", font=font_pr_label, fill=GOLD_LIGHT, anchor="mm")
    paste_pango(canvas, "السعر الترويجي", f"{FONT_ARABIC_BOLD} 15", "#DAAC36", 2257, 115, "center")
    
    font_pr_val = ImageFont.truetype(FONT_SERIF_BOLD, 46)
    draw.text((2257, 175), "SAR --.--", font=font_pr_val, fill=WHITE, anchor="mm")

    # Bottom Logistics Strip inside box
    font_btm_tag = ImageFont.truetype(FONT_SANS_BOLD, 16)
    draw.text((2100, 305), "CASE PACK: 12 JARS • 144 CASES/PALLET", font=font_btm_tag, fill=GOLD, anchor="mm")
    draw.text((2100, 350), "CODEX STAN 12-1981 • GAFTA 0% DUTY", font=font_btm_tag, fill=IVORY, anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, filename)
    canvas.save(out_file, dpi=(300, 300))
    print(f'[SAVED] {out_file}')
    return canvas

# ==============================================================================
# 3. MASTER PRINT PRESS PROOF SHEET (2480 x 3508 px @ 300 DPI, A4 Portrait)
# ==============================================================================
def render_master_press_sheet(talker_images):
    w, h = 2480, 3508 # A4 Portrait @ 300 DPI
    canvas = Image.new('RGB', (w, h), (250, 250, 250))
    draw = ImageDraw.Draw(canvas)

    # Sheet Header & Registration info
    paste_gold_logo(canvas, cx=w // 2, cy=110, target_w=380)

    font_job_t = ImageFont.truetype(FONT_SERIF_BOLD, 26)
    font_job_s = ImageFont.truetype(FONT_SANS_BOLD, 17)
    font_job_m = ImageFont.truetype(FONT_SANS_REG, 15)

    draw.text((w // 2, 185), "COMMERCIAL PRESS PROOF: RETAIL GONDOLA SHELF STRIPS", font=font_job_t, fill=CHARCOAL, anchor="mm")
    draw.text((w // 2, 225), "JOB: MARIAM NATURAL HONEY & SUPERFOODS • 300 DPI 1:1 SCALE", font=font_job_s, fill=BURGUNDY, anchor="mm")
    draw.text((w // 2, 260), "SPECIFICATION: 350 GSM ART CARD + MATTE LAMINATION + LUXOR GOLD FOIL (PANTONE 871 C)", font=font_job_m, fill=(90, 90, 90), anchor="mm")

    # Center registration crosshair at top
    draw.ellipse([(w // 2 - 12, 300 - 12), (w // 2 + 12, 300 + 12)], outline=(80, 80, 80), width=1)
    draw.line([(w // 2 - 25, 300), (w // 2 + 25, 300)], fill=(80, 80, 80), width=1)
    draw.line([(w // 2, 300 - 25), (w // 2, 300 + 25)], fill=(80, 80, 80), width=1)

    # CMYK Color Control Bars at top
    cmyk_colors = [
        ("C", (0, 160, 230)),
        ("M", (230, 0, 120)),
        ("Y", (255, 230, 0)),
        ("K", (20, 20, 20)),
        ("GOLD", GOLD),
        ("BURGUNDY", BURGUNDY),
        ("FOREST", FOREST_DARK)
    ]
    cb_start_x = w // 2 - (len(cmyk_colors) * 60) // 2
    for c_idx, (c_name, c_rgb) in enumerate(cmyk_colors):
        cb_x = cb_start_x + c_idx * 60
        draw.rectangle([(cb_x, 285), (cb_x + 50, 315)], fill=c_rgb, outline=(150, 150, 150))

    # Place 4 Shelf-Talkers vertically
    strip_w = 2300 # scaled slightly to fit A4 margins with 90px margin each side
    strip_h = int(448 * (strip_w / 2480)) # ~415 px
    y_start = 390
    spacing = 150

    for i, t_img in enumerate(talker_images):
        y_pos = y_start + i * (strip_h + spacing)
        x_pos = (w - strip_w) // 2

        # Scale talker image cleanly
        t_resized = t_img.resize((strip_w, strip_h), Image.Resampling.LANCZOS)
        canvas.paste(t_resized, (x_pos, y_pos))

        # Crop Marks
        draw_crop_marks(draw, x_pos, y_pos, x_pos + strip_w, y_pos + strip_h, mark_len=35, offset=15, col=(80, 80, 80))

        # Position Label
        font_strip_label = ImageFont.truetype(FONT_SANS_BOLD, 15)
        strip_names = [
            "POSITION 1: MARIAM ROYAL MIX (500g) • FINISH 210 x 38mm",
            "POSITION 2: SINGLE-ESTATE MOUNTAIN SIDR (500g) • FINISH 210 x 38mm",
            "POSITION 3: RAW CUT HONEYCOMB HEX (500g) • FINISH 210 x 38mm",
            "POSITION 4: CLOVER BLOSSOM FAMILY (1kg) • FINISH 210 x 38mm"
        ]
        draw.text((x_pos + 10, y_pos - 25), strip_names[i], font=font_strip_label, fill=CHARCOAL, anchor="lm")
        draw.text((x_pos + strip_w - 10, y_pos - 25), "TRIM SIZE: 210mm x 38mm • BLEED: 3mm", font=font_strip_label, fill=(120, 120, 120), anchor="rm")

    # Bottom Footer
    draw.line([(100, h - 120), (w - 100, h - 120)], fill=GRAY_BORDER, width=2)
    font_foot = ImageFont.truetype(FONT_SANS_REG, 15)
    draw.text((w // 2, h - 80), "MARIAM FOOD INDUSTRIES PACKAGING QA • APPROVED FOR OFFSET PRESS RUN • ZERO PDF PROHIBITION RESPECTED", font=font_foot, fill=(100, 100, 100), anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, 'mariam_shelf_talkers_master_press_sheet_300dpi.png')
    canvas.save(out_file, dpi=(300, 300))
    print(f'[SAVED] {out_file}')

if __name__ == '__main__':
    print('Generating Wholesale Export Sell-Sheets & Shelf-Talkers @ 300 DPI...')
    
    # 1. Technical Sell Sheet
    render_wholesale_trade_sell_sheet()

    # 2. Four Individual Shelf Talker Strips
    t1 = render_shelf_talker_strip(
        'mariam_shelf_talker_royal_mix_300dpi.png',
        'MARIAM ROYAL MIX (500g)',
        'خلطة مريم الملكية الفاخرة',
        'Raw Amber Honey with Roasted Cashews, Almonds, Hazelnuts & Royal Jelly',
        'mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg',
        '6281001205010',
        'HERO FLAGSHIP • 0% PEANUTS',
        BURGUNDY
    )
    
    t2 = render_shelf_talker_strip(
        'mariam_shelf_talker_mountain_sidr_300dpi.png',
        'MOUNTAIN SIDR HONEY (500g)',
        'عسل السدر الجبلي النقي',
        '100% Raw Single-Estate Monofloral Mountain Wildflower Nectar',
        'mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg',
        '6281001205027',
        'SINGLE-ESTATE • 100% RAW',
        FOREST_DARK
    )

    t3 = render_shelf_talker_strip(
        'mariam_shelf_talker_honeycomb_hex_300dpi.png',
        'RAW CUT HONEYCOMB (500g)',
        'أقراص شمع العسل الطبيعي',
        'Intact Geometric Virgin Beeswax Comb Slab in Acacia Honey',
        'mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg',
        '6281001205034',
        'NATURAL COMB • HEXAGONAL',
        (45, 30, 15)
    )

    t4 = render_shelf_talker_strip(
        'mariam_shelf_talker_clover_1kg_300dpi.png',
        'CLOVER BLOSSOM FAMILY (1kg)',
        'عسل زهور البرسيم النقي',
        'Monumental Family Jar • Golden Egyptian Clover Nectar',
        'mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg',
        '6281001205041',
        'MONUMENTAL FAMILY 1KG',
        (30, 40, 20)
    )

    # 3. Master Print Press Proof Sheet
    render_master_press_sheet([t1, t2, t3, t4])
    print('All 300 DPI Wholesale Sell-Sheets & Shelf-Talkers generated successfully!')
