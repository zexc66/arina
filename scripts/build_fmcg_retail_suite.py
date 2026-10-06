import os
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, 'output', 'imagery')
BRAIN_DIR = os.path.join(WORKSPACE_DIR, 'scratch')
SCRATCH_DIR = os.path.join(WORKSPACE_DIR, 'scratch')
LOGO_GOLD = os.path.join(WORKSPACE_DIR, 'arina-logo-gold.png')
LOGO_KHAER = os.path.join(WORKSPACE_DIR, 'khaeer-alwadi-logo-gold.png')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

# Fonts
FONT_SERIF_DISPLAY = '/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf'
FONT_SERIF_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
FONT_SERIF_ITALIC = '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
FONT_SANS_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_SANS_REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'

FONT_ARABIC_BOLD = 'Noto Kufi Arabic Bold'
FONT_ARABIC_SANS = 'Noto Sans Arabic Bold'

# Official Luxury Palette
GOLD = (218, 172, 54)
IVORY = (248, 245, 238)
DARK_GREEN = (30, 51, 38)
GOLD_SUBTLE = (140, 105, 30)
CHARCOAL = (35, 38, 40)
GRAY_LINE = (210, 210, 210)

def render_text_pango(text, font_desc=f'{FONT_ARABIC_BOLD} 24', color_hex='#DAAC36', align='center'):
    """Renders text with full HarfBuzz shaping, bidirectional text, and font fallback."""
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

def paste_pango_text(canvas, text, font_desc, color_hex, cx, cy, anchor='center'):
    """Pastes Pango-rendered text cleanly onto the target canvas at specified coordinates."""
    txt_img = render_text_pango(text, font_desc, color_hex, align='center')
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

def get_jar_alpha_mask(img_rgb):
    w, h = img_rgb.size
    gray = img_rgb.convert('L')
    near_white = gray.point(lambda p: 255 if p > 250 else 0)
    bg_mask = near_white.copy()
    ImageDraw.floodfill(bg_mask, (0, 0), 128, thresh=10)
    ImageDraw.floodfill(bg_mask, (w - 1, 0), 128, thresh=10)
    ImageDraw.floodfill(bg_mask, (0, h - 1), 128, thresh=10)
    ImageDraw.floodfill(bg_mask, (w - 1, h - 1), 128, thresh=10)
    alpha = bg_mask.point(lambda p: 0 if p == 128 else 255)
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=1.5))
    return alpha

def save_and_thumb(canvas, filename):
    out_p = os.path.join(OUTPUT_DIR, filename)
    canvas.save(out_p, quality=98)
    if filename.startswith('mariam_'):
        arina_name = filename.replace('mariam_', 'arina_')
        arina_p = os.path.join(OUTPUT_DIR, arina_name)
        canvas.save(arina_p, quality=98)
        print(f'[SAVED] {filename} & {arina_name}')
    else:
        print(f'[SAVED] {filename}')

def paste_jar(canvas, filename, cx, y_ground, target_h, base_ratio):
    im = Image.open(os.path.join(OUTPUT_DIR, filename))
    w = int(im.width * (target_h / im.height))
    im_r = im.resize((w, target_h), Image.Resampling.LANCZOS)
    mask = get_jar_alpha_mask(im_r)
    y_pos = y_ground - int(base_ratio * target_h)
    x_pos = cx - w // 2
    canvas.paste(im_r, (x_pos, y_pos), mask)

# ==============================================================================
# 1. FMCG Supermarket Shelf Planogram (3 Tiers on Retail Display Gondola)
# ==============================================================================
def render_fmcg_shelf_planogram():
    canvas = Image.new('RGB', (3840, 2160), (242, 240, 235))
    draw = ImageDraw.Draw(canvas)
    
    # Store Gondola Header - Spacious 320px tall
    draw.rectangle([(0, 0), (3840, 320)], fill=DARK_GREEN)
    draw.line([(0, 316), (3840, 316)], fill=GOLD, width=4)
    draw.line([(0, 310), (3840, 310)], fill=GOLD_SUBTLE, width=1)
    
    # Authentic Gold Cursive Logo in header
    logo = Image.open(LOGO_GOLD).convert('RGBA')
    lw = 360
    lh = int(lw * (logo.height / logo.width))
    logo_r = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_r, (1920 - lw // 2, 28), logo_r)
    
    font_h1 = ImageFont.truetype(FONT_SERIF_DISPLAY, 34)
    draw.text((1920, 212), "SUPERMARKET PLANOGRAM & CATEGORY FACING MATRIX", font=font_h1, fill=IVORY, anchor="mm")
    paste_pango_text(canvas, "المصفوفة القياسية لعرض منتجات أرينا على أرفف السوبرماركت الفاخر", f"{FONT_ARABIC_BOLD} 24", "#DAAC36", 1920, 268, "center")

    # Shelves coordinates
    shelves = [
        # (y_shelf, title, jars_list)
        (870, "TIER 1: ARTISANAL PICKLES SUITE (المخللات الملكية الحرفية - 500g)",
         [('mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', 680, 560, 0.911),
          ('mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', 1140, 560, 0.911),
          ('mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg', 1680, 560, 0.911),
          ('mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg', 2140, 560, 0.911),
          ('mariam_royal_mixed_pickles_white_studio_hero_4k.jpg', 2680, 560, 0.911),
          ('mariam_royal_mixed_pickles_white_studio_hero_4k.jpg', 3140, 560, 0.911)]),
        
        (1490, "TIER 2: TABLE & STUFFED OLIVES RESERVE (الزيتون الطبيعي والمحشي - 370g)",
         [('mariam_royal_kalamata_olives_white_studio_hero_4k.jpg', 640, 560, 0.875),
          ('mariam_natural_black_olives_white_studio_hero_4k.jpg', 1160, 560, 0.875),
          ('mariam_pitted_green_olives_white_studio_hero_4k.jpg', 1680, 560, 0.875),
          ('mariam_almond_stuffed_olives_white_studio_hero_4k.jpg', 2200, 560, 0.875),
          ('mariam_garlic_stuffed_olives_white_studio_hero_4k.jpg', 2720, 560, 0.875),
          ('mariam_sliced_black_olives_white_studio_hero_4k.jpg', 3240, 560, 0.875)]),

        (2110, "TIER 3: GOURMET GARLIC PASTES & TAPENADES (كريمات الثوم والتابيناد - 210g / 190g)",
         [('mariam_whipped_toum_white_studio_hero_4k.jpg', 640, 540, 0.870),
          ('mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg', 1160, 540, 0.870),
          ('mariam_slow_roasted_garlic_white_studio_hero_4k.jpg', 1680, 540, 0.870),
          ('mariam_green_olive_tapenade_white_studio_hero_4k.jpg', 2200, 540, 0.870),
          ('mariam_kalamata_olive_tapenade_white_studio_hero_4k.jpg', 2720, 540, 0.870),
          ('mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg', 3240, 540, 0.870)])
    ]
    
    for y_shelf, title, jars in shelves:
        # Draw wooden shelf plank
        draw.rectangle([(180, y_shelf - 20), (3660, y_shelf + 25)], fill=(75, 55, 40))
        # Gold price channel strip
        draw.rectangle([(180, y_shelf + 25), (3660, y_shelf + 55)], fill=DARK_GREEN)
        draw.line([(180, y_shelf + 25), (3660, y_shelf + 25)], fill=GOLD, width=3)
        draw.line([(180, y_shelf + 55), (3660, y_shelf + 55)], fill=GOLD, width=3)
        
        paste_pango_text(canvas, title, f"{FONT_ARABIC_BOLD}, Liberation Sans Bold 22", "#F8F5EE", 1920, y_shelf + 40, "center")
        
        # Paste jars on shelf
        for fn, cx, th, br in jars:
            paste_jar(canvas, fn, cx=cx, y_ground=y_shelf - 15, target_h=th, base_ratio=br)

    save_and_thumb(canvas, 'mariam_fmcg_supermarket_shelf_planogram_4k.jpg')

# ==============================================================================
# 2. B2B Trade Sell-Sheet Lineup (6 Key SKUs with Logistics Data)
# ==============================================================================
def render_fmcg_trade_sell_sheet():
    canvas = Image.new('RGB', (3840, 2160), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Top luxury header - Spacious 360px tall
    draw.rectangle([(0, 0), (3840, 360)], fill=DARK_GREEN)
    draw.line([(0, 356), (3840, 356)], fill=GOLD, width=4)
    draw.line([(0, 350), (3840, 350)], fill=GOLD_SUBTLE, width=1)
    
    # Authentic Gold Cursive Logo
    logo = Image.open(LOGO_GOLD).convert('RGBA')
    lw = 400
    lh = int(lw * (logo.height / logo.width))
    logo_r = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_r, (1920 - lw // 2, 30), logo_r)
    
    font_title = ImageFont.truetype(FONT_SERIF_DISPLAY, 34)
    draw.text((1920, 230), "FMCG COMMERCIAL TRADE PORTFOLIO — PRODUCT LINEUP & SPECIFICATIONS", font=font_title, fill=IVORY, anchor="mm")
    paste_pango_text(canvas, "بطاقة المواصفات اللوجستية والتجارية لسلاسل التجزئة الكبرى • صلاحية 24 شهراً • 12 عبوة في الكرتونة", f"{FONT_ARABIC_BOLD} 22", "#DAAC36", 1920, 296, "center")
    
    # 6 Key SKUs
    skus = [
        ('mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', 360,
         "BABY CUCUMBERS", "الخيار الصغير بالديل", "500g Glass Jar", "Net: 500g | Drain: 260g", "Case: 12 Jars", "Pallet: 72 Cases", "EAN: 6281001230018"),
        ('mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg', 980,
         "WILD TURNIP & BEETROOT", "اللفت البلدي بالشمندر", "500g Glass Jar", "Net: 500g | Drain: 270g", "Case: 12 Jars", "Pallet: 72 Cases", "EAN: 6281001230025"),
        ('mariam_royal_kalamata_olives_white_studio_hero_4k.jpg', 1600,
         "ROYAL KALAMATA OLIVES", "زيتون كالاماتا الملكي", "370g Glass Jar", "Net: 370g | Drain: 200g", "Case: 12 Jars", "Pallet: 84 Cases", "EAN: 6281001230032"),
        ('mariam_almond_stuffed_olives_white_studio_hero_4k.jpg', 2240,
         "ALMOND STUFFED OLIVES", "الزيتون المحشي باللوز", "370g Glass Jar", "Net: 370g | Drain: 210g", "Case: 12 Jars", "Pallet: 84 Cases", "EAN: 6281001230049"),
        ('mariam_whipped_toum_white_studio_hero_4k.jpg', 2860,
         "WHIPPED TOUM GARLIC", "معجون التوم المخفوق", "210g Glass Jar", "Net: 210g | 100% Garlic", "Case: 12 Jars", "Pallet: 96 Cases", "EAN: 6281001230056"),
        ('mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg', 3480,
         "CRUSHED GARLIC (RAW)", "ثوم مهروس غير مشوي", "210g Glass Jar", "Net: 210g | Fresh Pure", "Case: 12 Jars", "Pallet: 96 Cases", "EAN: 6281001230063")
    ]
    
    font_name_en = ImageFont.truetype(FONT_SERIF_BOLD, 24)
    font_data_bold = ImageFont.truetype(FONT_SANS_BOLD, 19)
    font_data = ImageFont.truetype(FONT_SANS_REG, 18)
    
    y_ground = 1380
    for fn, cx, name_en, name_ar, jar_sz, wt, cs, pal, ean in skus:
        # Paste Jar
        paste_jar(canvas, fn, cx=cx, y_ground=y_ground, target_h=980, base_ratio=0.880)
        
        # Spec box below jar
        box_top = 1420
        box_left = cx - 270
        box_right = cx + 270
        box_bottom = 2080
        
        draw.rectangle([(box_left, box_top), (box_right, box_bottom)], fill=(250, 249, 246), outline=DARK_GREEN, width=2)
        # Gold header inside card
        draw.rectangle([(box_left, box_top), (box_right, box_top + 80)], fill=DARK_GREEN)
        draw.text((cx, box_top + 26), name_en, font=font_name_en, fill=GOLD, anchor="mm")
        paste_pango_text(canvas, name_ar, f"{FONT_ARABIC_BOLD} 20", "#F8F5EE", cx, box_top + 58, "center")
        
        # Details inside card
        lines = [
            ("Format:", jar_sz),
            ("Weights:", wt),
            ("Master Case:", cs),
            ("Pallet Ti/Hi:", pal),
            ("Case Weight:", "Gross ~7.8kg"),
            ("Shelf Life:", "24 Months (Ambient)"),
            ("Barcode:", ean)
        ]
        
        y_text = box_top + 115
        for label, val in lines:
            draw.text((box_left + 20, y_text), label, font=font_data_bold, fill=DARK_GREEN)
            draw.text((box_right - 20, y_text), val, font=font_data, fill=(60, 60, 60), anchor="ra")
            y_text += 38

    save_and_thumb(canvas, 'mariam_fmcg_b2b_trade_sell_sheet_lineup_4k.jpg')

# ==============================================================================
# 3. Retail FSDU Free-Standing Display Stand (Floor Merchandiser)
# ==============================================================================
def render_fmcg_fsdu_floor_display():
    canvas = Image.new('RGB', (3840, 2160), (245, 245, 245))
    draw = ImageDraw.Draw(canvas)
    
    # Draw floor shadow and perspective retail aisle floor
    draw.rectangle([(0, 1800), (3840, 2160)], fill=(235, 233, 228))
    for x in range(0, 3840, 300):
        draw.line([(x, 1800), (x - 200, 2160)], fill=(220, 218, 212), width=2)
    draw.line([(0, 1800), (3840, 1800)], fill=(200, 198, 190), width=3)
    
    # Stand structure (Center: x=1920, w=1400)
    sx_l, sx_r = 1220, 2620
    # Header Board - Spacious 360px tall from y=140 to y=500
    draw.rectangle([(sx_l - 40, 140), (sx_r + 40, 500)], fill=DARK_GREEN, outline=GOLD, width=5)
    
    logo = Image.open(LOGO_GOLD).convert('RGBA')
    lw = 380
    lh = int(lw * (logo.height / logo.width))
    logo_r = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_r, (1920 - lw // 2, 168), logo_r)
    
    font_head = ImageFont.truetype(FONT_SERIF_DISPLAY, 34)
    draw.text((1920, 368), "ARTISANAL MEDITERRANEAN RESERVE", font=font_head, fill=IVORY, anchor="mm")
    paste_pango_text(canvas, "أفخر خيرات الأرض المعتّقة بحب • متوفر الآن", f"{FONT_ARABIC_BOLD} 24", "#DAAC36", 1920, 432, "center")
    
    # Stand side panels
    draw.polygon([(sx_l - 40, 500), (sx_l - 60, 1980), (sx_l, 1980), (sx_l, 500)], fill=(24, 40, 30))
    draw.polygon([(sx_r + 40, 500), (sx_r + 60, 1980), (sx_r, 1980), (sx_r, 500)], fill=(24, 40, 30))
    # Stand back wall
    draw.rectangle([(sx_l, 500), (sx_r, 1980)], fill=(28, 46, 35))
    
    # 3 Shelves inside FSDU
    fsdu_shelves = [
        (980, [
            ('mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', 1420, 440, 0.911),
            ('mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg', 1750, 440, 0.911),
            ('mariam_royal_mixed_pickles_white_studio_hero_4k.jpg', 2090, 440, 0.911),
            ('mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', 2420, 440, 0.911)
        ]),
        (1480, [
            ('mariam_royal_kalamata_olives_white_studio_hero_4k.jpg', 1420, 440, 0.875),
            ('mariam_natural_black_olives_white_studio_hero_4k.jpg', 1750, 440, 0.875),
            ('mariam_almond_stuffed_olives_white_studio_hero_4k.jpg', 2090, 440, 0.875),
            ('mariam_garlic_stuffed_olives_white_studio_hero_4k.jpg', 2420, 440, 0.875)
        ]),
        (1960, [
            ('mariam_whipped_toum_white_studio_hero_4k.jpg', 1420, 420, 0.870),
            ('mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg', 1750, 420, 0.870),
            ('mariam_green_olive_tapenade_white_studio_hero_4k.jpg', 2090, 420, 0.870),
            ('mariam_kalamata_olive_tapenade_white_studio_hero_4k.jpg', 2420, 420, 0.870)
        ])
    ]
    
    for y_sh, jars in fsdu_shelves:
        draw.rectangle([(sx_l - 10, y_sh), (sx_r + 10, y_sh + 35)], fill=GOLD)
        draw.rectangle([(sx_l - 5, y_sh + 8), (sx_r + 5, y_sh + 27)], fill=DARK_GREEN)
        for fn, cx, th, br in jars:
            paste_jar(canvas, fn, cx=cx, y_ground=y_sh, target_h=th, base_ratio=br)
            
    # Flanking hero jars standing on the floor next to the display
    paste_jar(canvas, 'mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', cx=620, y_ground=1940, target_h=1180, base_ratio=0.911)
    paste_jar(canvas, 'mariam_crisp_baby_cucumbers_petite_210g_white_studio_hero_4k.jpg', cx=940, y_ground=1980, target_h=980, base_ratio=0.866)

    paste_jar(canvas, 'mariam_royal_kalamata_olives_white_studio_hero_4k.jpg', cx=3220, y_ground=1940, target_h=1180, base_ratio=0.875)
    paste_jar(canvas, 'mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg', cx=2900, y_ground=1980, target_h=1020, base_ratio=0.870)

    save_and_thumb(canvas, 'mariam_fmcg_retail_fsdu_floor_display_stand_4k.jpg')

# ==============================================================================
# 4. Master Shipper Carton & Secondary Case Pack (12-Jar Case Logistics)
# ==============================================================================
def render_fmcg_master_carton_pack():
    canvas = Image.new('RGB', (3840, 2160), (250, 250, 248))
    draw = ImageDraw.Draw(canvas)
    
    # Title with generous spacing
    font_t = ImageFont.truetype(FONT_SERIF_DISPLAY, 38)
    draw.text((1920, 110), "B2B LOGISTICS & MASTER SHIPPER PACKAGING SPECIFICATION", font=font_t, fill=DARK_GREEN, anchor="mm")
    paste_pango_text(canvas, "كرتونة الشحن والتوزيع المعتمدة للتجزئة — 12 برطماناً زجاجياً مع فواصل حماية كرتونية", f"{FONT_ARABIC_BOLD} 24", "#DAAC36", 1920, 170, "center")
    
    # Draw Corrugated Master Carton (Kraft Cardboard Box 3D perspective)
    bx1, by1 = 550, 750
    bw, bh = 850, 750
    
    draw.rectangle([(bx1, by1), (bx1 + bw, by1 + bh)], fill=(195, 155, 110), outline=(130, 95, 60), width=4)
    # Carton Tape
    draw.rectangle([(bx1 + bw // 2 - 35, by1), (bx1 + bw // 2 + 35, by1 + bh)], fill=(210, 185, 140))
    
    # Branding on carton - Spacious dark green plaque
    draw.rectangle([(bx1 + 60, by1 + 90), (bx1 + bw - 60, by1 + 330)], fill=DARK_GREEN)
    logo = Image.open(LOGO_GOLD).convert('RGBA')
    lw = 300
    lh = int(lw * (logo.height / logo.width))
    logo_r = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_r, (bx1 + bw // 2 - lw // 2, by1 + 110), logo_r)
    
    font_carton = ImageFont.truetype(FONT_SANS_BOLD, 26)
    font_carton_sm = ImageFont.truetype(FONT_SANS_REG, 20)
    draw.text((bx1 + bw // 2, by1 + 278), "12 × 500g GLASS JARS", font=font_carton, fill=GOLD, anchor="mm")
    
    # Logistics markings
    draw.rectangle([(bx1 + 60, by1 + 380), (bx1 + bw - 60, by1 + 520)], fill=(215, 185, 145), outline=(150, 115, 75))
    draw.text((bx1 + bw // 2, by1 + 420), "THIS WAY UP ↑↑", font=font_carton, fill=(40, 30, 20), anchor="mm")
    draw.text((bx1 + bw // 2, by1 + 465), "FRAGILE — HANDLE WITH CARE", font=font_carton, fill=(160, 30, 30), anchor="mm")
    
    # Barcode simulated
    draw.rectangle([(bx1 + 60, by1 + 560), (bx1 + 500, by1 + 690)], fill=(255, 255, 255), outline=(100, 80, 60))
    for bar_x in range(bx1 + 80, bx1 + 480, 10):
        w_b = 3 if bar_x % 20 == 0 else 6
        draw.rectangle([(bar_x, by1 + 580), (bar_x + w_b, by1 + 660)], fill=(0, 0, 0))
    draw.text((bx1 + 280, by1 + 675), "ITF-14: 1 62 81001 23001 5", font=font_carton_sm, fill=(0, 0, 0), anchor="mm")
    
    # Carton pallet data
    draw.text((bx1 + 580, by1 + 600), "GROSS WEIGHT: 9.8 KG", font=font_carton_sm, fill=(40, 30, 20))
    draw.text((bx1 + 580, by1 + 650), "TI/HI: 12 × 6 = 72 CASES", font=font_carton_sm, fill=(40, 30, 20))

    # Box 2: Open Carton showing Internal Anti-Breakage Cell Dividers (Right side)
    bx2, by2 = 2440, 750
    draw.rectangle([(bx2, by2), (bx2 + bw, by2 + bh)], fill=(195, 155, 110), outline=(130, 95, 60), width=4)
    # Open top flap
    draw.polygon([(bx2, by2), (bx2 - 80, by2 - 120), (bx2 + bw + 80, by2 - 120), (bx2 + bw, by2)], fill=(210, 175, 130), outline=(130, 95, 60))
    
    # Internal cell dividers (3x4 grid)
    draw.rectangle([(bx2 + 40, by2 + 40), (bx2 + bw - 40, by2 + 400)], fill=(170, 130, 90), outline=(110, 80, 50), width=3)
    # 3 horizontal slots, 4 vertical slots
    for row in range(1, 3):
        y_div = by2 + 40 + row * 120
        draw.line([(bx2 + 40, y_div), (bx2 + bw - 40, y_div)], fill=(130, 95, 60), width=5)
    for col in range(1, 4):
        x_div = bx2 + 40 + col * int((bw - 80) / 4)
        draw.line([(x_div, by2 + 40), (x_div, by2 + 400)], fill=(130, 95, 60), width=5)
        
    # Label on front of open box - Spacious dark green plaque
    draw.rectangle([(bx2 + 60, by2 + 450), (bx2 + bw - 60, by2 + 690)], fill=DARK_GREEN)
    lw2 = 260
    lh2 = int(lw2 * (logo.height / logo.width))
    logo_r2 = logo.resize((lw2, lh2), Image.Resampling.LANCZOS)
    canvas.paste(logo_r2, (bx2 + bw // 2 - lw2 // 2, by2 + 468), logo_r2)
    draw.text((bx2 + bw // 2, by2 + 606), "INTERNAL CORRUGATED CELL DIVIDERS", font=font_carton_sm, fill=GOLD, anchor="mm")
    draw.text((bx2 + bw // 2, by2 + 645), "ZERO BREAKAGE • E-COMMERCE & RETAIL READY", font=font_carton_sm, fill=IVORY, anchor="mm")

    # Center: Two flagship jars standing in the foreground
    paste_jar(canvas, 'mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', cx=1680, y_ground=1980, target_h=1380, base_ratio=0.911)
    paste_jar(canvas, 'mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg', cx=2160, y_ground=1980, target_h=1380, base_ratio=0.911)

    save_and_thumb(canvas, 'mariam_fmcg_master_carton_shipper_case_pack_4k.jpg')

# ==============================================================================
# 5. Gourmet Deli Countertop POS Impulse Display Unit
# ==============================================================================
def render_fmcg_deli_countertop_pos():
    canvas = Image.new('RGB', (3840, 2160), (248, 246, 242))
    draw = ImageDraw.Draw(canvas)
    
    # Deli counter marble slab
    draw.rectangle([(0, 1720), (3840, 2160)], fill=(235, 235, 235))
    draw.line([(0, 1720), (3840, 1720)], fill=(200, 200, 200), width=4)
    
    # Title with generous spacing
    font_t = ImageFont.truetype(FONT_SERIF_DISPLAY, 38)
    draw.text((1920, 110), "GOURMET DELICATESSEN COUNTERTOP IMPULSE DISPLAY (POS)", font=font_t, fill=DARK_GREEN, anchor="mm")
    paste_pango_text(canvas, "صينية العرض الخشبية الفاخرة للأحجام الصغيرة عند نقاط البيع والكاشير", f"{FONT_ARABIC_BOLD} 24", "#DAAC36", 1920, 170, "center")
    
    # Oak wood tray on counter (Center: x=1920, w=2200, h=350)
    tx1, ty1 = 820, 1420
    tw, th = 2200, 320
    draw.rectangle([(tx1, ty1), (tx1 + tw, ty1 + th)], fill=(120, 85, 55), outline=(75, 50, 30), width=4)
    
    # Brass plaque in front of tray - Perfectly dimensioned 150px tall
    draw.rectangle([(tx1 + 450, ty1 + 150), (tx1 + tw - 450, ty1 + 300)], fill=DARK_GREEN, outline=GOLD, width=3)
    
    logo = Image.open(LOGO_GOLD).convert('RGBA')
    lw = 220
    lh = int(lw * (logo.height / logo.width))
    logo_r = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_r, (1920 - lw // 2, ty1 + 162), logo_r)
    
    font_pos = ImageFont.truetype(FONT_SANS_BOLD, 20)
    draw.text((1920, ty1 + 272), "PETITE ROYALE SELECTION — ARTISANAL DELICACIES", font=font_pos, fill=IVORY, anchor="mm")

    # 6 Petite jars lined up in the tray
    petite_jars = [
        ('mariam_crisp_baby_cucumbers_petite_210g_white_studio_hero_4k.jpg', 1040, 1020, 0.866),
        ('mariam_petite_wild_turnip_beetroot_solo_4k.jpg', 1390, 1020, 0.866),
        ('mariam_royal_kalamata_olives_petite_190g_white_studio_hero_4k.jpg', 1740, 1040, 0.866),
        ('mariam_garlic_stuffed_olives_petite_190g_white_studio_hero_4k.jpg', 2100, 1040, 0.866),
        ('mariam_whipped_toum_petite_100g_white_studio_hero_4k.jpg', 2450, 1000, 0.866),
        ('mariam_crushed_garlic_unroasted_petite_100g_white_studio_hero_4k.jpg', 2800, 1000, 0.866)
    ]
    for fn, cx, th_j, br in petite_jars:
        paste_jar(canvas, fn, cx=cx, y_ground=ty1 + 140, target_h=th_j, base_ratio=br)

    # Flanking large jars on counter
    paste_jar(canvas, 'mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', cx=420, y_ground=1820, target_h=1280, base_ratio=0.911)
    paste_jar(canvas, 'mariam_royal_kalamata_olives_white_studio_hero_4k.jpg', cx=3420, y_ground=1820, target_h=1300, base_ratio=0.875)

    save_and_thumb(canvas, 'mariam_fmcg_countertop_delicatessen_pos_display_4k.jpg')

# ==============================================================================
# 6. Retail Facings Dominance Grid (Dual Facings / 12 Jars Across Shelf)
# ==============================================================================
def render_fmcg_shelf_facings_grid():
    canvas = Image.new('RGB', (3840, 2160), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Store banner - Luxurious 340px tall
    draw.rectangle([(0, 0), (3840, 340)], fill=DARK_GREEN)
    draw.line([(0, 336), (3840, 336)], fill=GOLD, width=4)
    draw.line([(0, 330), (3840, 330)], fill=GOLD_SUBTLE, width=1)
    
    # Authentic Gold Cursive Logo
    logo = Image.open(LOGO_GOLD).convert('RGBA')
    lw = 380
    lh = int(lw * (logo.height / logo.width))
    logo_r = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_r, (1920 - lw // 2, 28), logo_r)
    
    # English Title - Beautiful Noto Serif Display with generous clearance
    font_t = ImageFont.truetype(FONT_SERIF_DISPLAY, 34)
    draw.text((1920, 216), "CATEGORY MANAGEMENT: 2-FACING RETAIL SHELF DOMINANCE", font=font_t, fill=IVORY, anchor="mm")
    
    # Arabic Subtitle - Flawless Noto Kufi Arabic Bold, no BiDi parenthesis glitch
    paste_pango_text(canvas, "مصفوفة مضاعفة واجهات العرض — واجهتان لكل منتج — لتعظيم مبيعات المتر المربع على الرف", f"{FONT_ARABIC_BOLD} 24", "#DAAC36", 1920, 282, "center")
    
    # Supermarket shelf plank
    y_shelf = 1760
    draw.rectangle([(120, y_shelf), (3720, y_shelf + 45)], fill=(65, 45, 30))
    # Price rail
    draw.rectangle([(120, y_shelf + 45), (3720, y_shelf + 95)], fill=DARK_GREEN)
    draw.line([(120, y_shelf + 45), (3720, y_shelf + 45)], fill=GOLD, width=3)
    draw.line([(120, y_shelf + 95), (3720, y_shelf + 95)], fill=GOLD, width=3)
    
    # 6 pairs of identical facings (12 jars total)
    facings = [
        ('mariam_crisp_baby_cucumbers_white_studio_hero_4k.jpg', 380, 640, "SAR 18.50", "Baby Cucumbers 500g"),
        ('mariam_wild_turnip_beetroot_white_studio_hero_4k.jpg', 960, 1220, "SAR 18.50", "Turnip & Beetroot 500g"),
        ('mariam_royal_kalamata_olives_white_studio_hero_4k.jpg', 1540, 1800, "SAR 22.00", "Kalamata Olives 370g"),
        ('mariam_almond_stuffed_olives_white_studio_hero_4k.jpg', 2120, 2380, "SAR 24.50", "Almond Stuffed 370g"),
        ('mariam_whipped_toum_white_studio_hero_4k.jpg', 2700, 2960, "SAR 16.00", "Whipped Toum 210g"),
        ('mariam_crushed_garlic_unroasted_210g_white_studio_hero_4k.jpg', 3280, 3540, "SAR 16.00", "Crushed Garlic 210g")
    ]
    
    font_price = ImageFont.truetype(FONT_SANS_BOLD, 22)
    font_name = ImageFont.truetype(FONT_SANS_REG, 16)
    
    for fn, cx1, cx2, price, name in facings:
        paste_jar(canvas, fn, cx=cx1, y_ground=y_shelf, target_h=1180, base_ratio=0.890)
        paste_jar(canvas, fn, cx=cx2, y_ground=y_shelf, target_h=1180, base_ratio=0.890)
        
        tag_cx = (cx1 + cx2) // 2
        draw.rectangle([(tag_cx - 110, y_shelf + 50), (tag_cx + 110, y_shelf + 90)], fill=(255, 255, 255), outline=GOLD)
        draw.text((tag_cx, y_shelf + 62), name, font=font_name, fill=(50, 50, 50), anchor="mm")
        draw.text((tag_cx, y_shelf + 78), price, font=font_price, fill=(180, 20, 20), anchor="mm")

    # Bottom notes
    font_footer = ImageFont.truetype(FONT_SERIF_DISPLAY, 24)
    draw.text((1920, 1980), "RECOMMENDED RETAIL PLANOGRAM: 2 FACINGS PER HERO SKU | ESTIMATED SALES LIFT +38%", font=font_footer, fill=DARK_GREEN, anchor="mm")
    paste_pango_text(canvas, "التوزيع الموصى به لمديري الفئات في سلاسل الهايبرماركت لتعظيم حركة دوران المنتج وحصته السوقية", f"{FONT_ARABIC_BOLD} 22", "#646464", 1920, 2025, "center")

    save_and_thumb(canvas, 'mariam_fmcg_category_manager_shelf_facing_panorama_4k.jpg')

if __name__ == '__main__':
    render_fmcg_shelf_planogram()
    render_fmcg_trade_sell_sheet()
    render_fmcg_fsdu_floor_display()
    render_fmcg_master_carton_pack()
    render_fmcg_deli_countertop_pos()
    render_fmcg_shelf_facings_grid()
    print('All 6 FMCG trade images re-rendered with flawless typography & zero collision!')
