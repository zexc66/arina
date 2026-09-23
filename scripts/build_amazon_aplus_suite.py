#!/usr/bin/env python3
"""
Mariam Natural Honey & Superfoods — Amazon A+ Content & Infographic Suite Generator
Renders 6 ultra-high-resolution (Cinema 4K) Amazon A+ modules:
1. Brand Story Hero Header (3840 x 1200)
2. Quality Pillar Card 1: 0% Peanuts & Whole Tree Nuts (1200 x 1200)
3. Quality Pillar Card 2: 100% Heavy Inert Flint Glass (1200 x 1200)
4. Quality Pillar Card 3: Cold-Extracted Living Enzymes (1200 x 1200)
5. Flagship Comparison Matrix Chart (3840 x 2160)
6. Daily Functional Wellness Ritual Infographic Banner (3840 x 1800)
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
    """Extracts a smooth alpha mask for jars photographed on 100% white studio background."""
    w, h = img_rgb.size
    gray = img_rgb.convert('L')
    near_white = gray.point(lambda p: 255 if p > 252 else 0)
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
        shadow_w = int(target_w * 0.75)
        shadow_h = int(target_h * 0.08)
        shadow_img = Image.new('RGBA', (shadow_w, shadow_h), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow_img)
        sdraw.ellipse([(0, 0), (shadow_w, shadow_h)], fill=(0, 0, 0, 120))
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=10))
        canvas.paste(shadow_img, (cx - shadow_w // 2, y_base - shadow_h // 2), shadow_img)

    canvas.paste(im_resized, (x_pos, y_pos), mask)

def paste_gold_logo(canvas, cx, cy, target_w):
    logo = Image.open(LOGO_GOLD).convert('RGBA')
    lh = int(target_w * (logo.height / logo.width))
    logo_r = logo.resize((target_w, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_r, (cx - target_w // 2, cy - lh // 2), logo_r)
    return lh

# ==============================================================================
# 1. AMAZON A+ BRAND STORY HERO HEADER (3840 x 1200)
# ==============================================================================
def render_amazon_brand_story_hero():
    w, h = 3840, 1200
    canvas = Image.new('RGB', (w, h), FOREST_OBSIDIAN)
    draw = ImageDraw.Draw(canvas)

    # Ambient radial gradient
    for r in range(800, 0, -20):
        alpha = int(12 * (1 - r / 800))
        col = (20 + alpha * 2, 8 + alpha, 14 + alpha)
        draw.ellipse([(1920 - r * 2, 600 - r), (1920 + r * 2, 600 + r)], fill=col)

    # Border trim
    draw.rectangle([(20, 20), (w - 20, h - 20)], outline=GOLD_DARK, width=2)
    draw.rectangle([(26, 26), (w - 26, h - 26)], outline=GOLD, width=1)

    # Corner ornaments
    for (cx, cy) in [(40, 40), (w - 40, 40), (40, h - 40), (w - 40, h - 40)]:
        draw.rectangle([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=GOLD)

    # Authentic Gold Cursive Logo
    logo_h = paste_gold_logo(canvas, cx=1920, cy=120, target_w=520)

    # Sub-Brand Pill Badge
    badge_text = "NATURAL HONEY & SUPERFOODS • 0% PEANUTS GUARANTEE"
    font_badge = ImageFont.truetype(FONT_SANS_BOLD, 22)
    bbox = font_badge.getbbox(badge_text)
    bw = bbox[2] - bbox[0] + 60
    draw.rounded_rectangle([(1920 - bw // 2, 185), (1920 + bw // 2, 230)], radius=22, fill=BURGUNDY, outline=GOLD, width=2)
    draw.text((1920, 207), badge_text, font=font_badge, fill=BLUSH_PINK, anchor="mm")

    # Main Headline
    font_head = ImageFont.truetype(FONT_SERIF_BOLD, 52)
    draw.text((1920, 275), "The Royal Connoisseur Collection", font=font_head, fill=IVORY, anchor="mm")

    font_sub = ImageFont.truetype(FONT_SERIF_ITALIC, 32)
    draw.text((1920, 330), "Artisanal Monofloral Mountain Nectars & Tree Nut Power Blends in Heavy Nordic Glass Jars", font=font_sub, fill=GOLD_LIGHT, anchor="mm")

    # Arabic Heritage Subtitle
    paste_pango(canvas, "عسل مريم الطبيعي والخلطات الملكية الفائقة • من أخصب المحميات الجبلية إلى موائد النخبة العالمية", f"{FONT_ARABIC_BOLD} 26", "#DAAC36", 1920, 380, "center")

    # Jars Showcase Row
    y_ground = 1120
    jars_config = [
        ('mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg', 650, 590),
        ('mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg', 1280, 590),
        ('mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg', 1920, 660), # Hero Center
        ('mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg', 2560, 590),
        ('mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg', 3190, 620),
    ]

    for fn, cx, jh in jars_config:
        paste_studio_jar(canvas, fn, cx, y_ground, target_h=jh, shadow=True)

    # Key Quality Pillars callouts along bottom
    pillars = [
        ("100% Raw & Unheated", "Preserves Living Bioactive Enzymes"),
        ("Single-Estate Nectars", "Harvested from Wild Mountain Flora"),
        ("0% Peanuts Certified", "California Almonds, Turkish Hazelnuts & Cashews"),
        ("Heavy Nordic Glass", "15mm Thick Base • Zero Plastic Leaching"),
    ]
    font_p_title = ImageFont.truetype(FONT_SANS_BOLD, 20)
    font_p_sub = ImageFont.truetype(FONT_SANS_REG, 16)

    for i, (p_title, p_desc) in enumerate(pillars):
        px = 480 + i * 960
        draw.text((px, 1140), p_title.upper(), font=font_p_title, fill=GOLD, anchor="mm")
        draw.text((px, 1168), p_desc, font=font_p_sub, fill=IVORY, anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, 'mariam_amazon_aplus_01_brand_story_hero_4k.jpg')
    canvas.save(out_file, quality=98)
    print(f'[SAVED] {out_file}')

# ==============================================================================
# 2. QUALITY PILLAR CARD 1: 0% PEANUTS & WHOLE TREE NUTS (1200 x 1200)
# ==============================================================================
def render_pillar_card_01_tree_nuts():
    w, h = 1200, 1200
    canvas = Image.new('RGB', (w, h), (18, 12, 16))
    draw = ImageDraw.Draw(canvas)

    # Outer decorative frame
    draw.rectangle([(20, 20), (w - 20, h - 20)], outline=BURGUNDY, width=3)
    draw.rectangle([(28, 28), (w - 28, h - 28)], outline=GOLD, width=1)

    # Top Header Pill
    paste_gold_logo(canvas, cx=600, cy=100, target_w=280)

    # Badge
    font_badge = ImageFont.truetype(FONT_SANS_BOLD, 18)
    draw.rounded_rectangle([(320, 160), (880, 205)], radius=18, fill=BURGUNDY, outline=GOLD, width=2)
    draw.text((600, 182), "ALLERGY PURITY GUARANTEE", font=font_badge, fill=BLUSH_PINK, anchor="mm")

    # Headline
    font_head = ImageFont.truetype(FONT_SERIF_BOLD, 42)
    draw.text((600, 260), "ZERO PEANUTS GUARANTEE", font=font_head, fill=IVORY, anchor="mm")
    
    font_sub = ImageFont.truetype(FONT_SERIF_ITALIC, 22)
    draw.text((600, 305), "100% Whole Hand-Selected Crunchy Tree Nuts", font=font_sub, fill=GOLD_LIGHT, anchor="mm")

    # Hero Open Jar Image in Center
    paste_studio_jar(canvas, 'mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg', cx=600, y_base=850, target_h=520, shadow=True)

    # Ingredient Feature Badges
    items = [
        "California Roasted Almonds",
        "Golden Jumbo Cashews",
        "Turkish Hazelnuts",
        "Fresh Pure Royal Jelly"
    ]
    font_item = ImageFont.truetype(FONT_SANS_BOLD, 17)
    for i, it in enumerate(items):
        ix = 230 + (i % 2) * 740
        iy = 890 + (i // 2) * 55
        draw.rounded_rectangle([(ix - 180, iy - 20), (ix + 180, iy + 20)], radius=15, fill=(35, 20, 26), outline=GOLD_DARK, width=1)
        draw.text((ix, iy), it, font=font_item, fill=IVORY, anchor="mm")

    # Arabic Footer
    paste_pango(canvas, "خالٍ 100% من الفول السوداني • مكسرات فاخرة محشوة بعسل السدر والغذاء الملكي", f"{FONT_ARABIC_BOLD} 20", "#DAAC36", 600, 1040, "center")

    # Micro specs
    font_spec = ImageFont.truetype(FONT_SANS_REG, 15)
    draw.text((600, 1120), "Processed in an exclusively certified peanut-free facility • CODEX STAN 12-1981", font=font_spec, fill=(160, 160, 160), anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, 'mariam_amazon_aplus_02_card_tree_nuts_purity_4k.jpg')
    canvas.save(out_file, quality=98)
    print(f'[SAVED] {out_file}')

# ==============================================================================
# 3. QUALITY PILLAR CARD 2: 100% HEAVY INERT FLINT GLASS (1200 x 1200)
# ==============================================================================
def render_pillar_card_02_nordic_glass():
    w, h = 1200, 1200
    canvas = Image.new('RGB', (w, h), (12, 18, 16))
    draw = ImageDraw.Draw(canvas)

    # Frame
    draw.rectangle([(20, 20), (w - 20, h - 20)], outline=FOREST_DARK, width=3)
    draw.rectangle([(28, 28), (w - 28, h - 28)], outline=GOLD, width=1)

    paste_gold_logo(canvas, cx=600, cy=100, target_w=280)

    # Badge
    font_badge = ImageFont.truetype(FONT_SANS_BOLD, 18)
    draw.rounded_rectangle([(320, 160), (880, 205)], radius=18, fill=FOREST_DARK, outline=GOLD, width=2)
    draw.text((600, 182), "PACKAGING INTEGRITY STANDARD", font=font_badge, fill=GOLD_LIGHT, anchor="mm")

    # Headline
    font_head = ImageFont.truetype(FONT_SERIF_BOLD, 42)
    draw.text((600, 260), "100% INERT FLINT GLASS", font=font_head, fill=IVORY, anchor="mm")

    font_sub = ImageFont.truetype(FONT_SERIF_ITALIC, 22)
    draw.text((600, 305), "Zero Plastic Leaching • 15mm Heavyweight Base", font=font_sub, fill=GOLD_LIGHT, anchor="mm")

    # 45-degree angle Jar Image in Center
    paste_studio_jar(canvas, 'mariam_honey_sidr_500g_45deg_angle_white_studio_4k.jpg', cx=600, y_base=850, target_h=520, shadow=True)

    # Technical Metrics
    metrics = [
        "15mm Heavy Glass Base",
        "82mm Airtight Gold Cap",
        "Hermetic Crown Ribbon",
        "24-Month Ambient Shelf Life"
    ]
    font_item = ImageFont.truetype(FONT_SANS_BOLD, 17)
    for i, m in enumerate(metrics):
        ix = 230 + (i % 2) * 740
        iy = 890 + (i // 2) * 55
        draw.rounded_rectangle([(ix - 180, iy - 20), (ix + 180, iy + 20)], radius=15, fill=(18, 30, 24), outline=GOLD_DARK, width=1)
        draw.text((ix, iy), m, font=font_item, fill=IVORY, anchor="mm")

    # Arabic Footer
    paste_pango(canvas, "برطمانات زجاجية نقية 100% تضمن الحفاظ التام على الإنزيمات الحيوية والنكهة الطبيعية", f"{FONT_ARABIC_BOLD} 20", "#DAAC36", 600, 1040, "center")

    font_spec = ImageFont.truetype(FONT_SANS_REG, 15)
    draw.text((600, 1120), "USP Type III Soda-Lime Flint Glass • Fully Recyclable • Tamper-Evident Crown Ribbon", font=font_spec, fill=(160, 160, 160), anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, 'mariam_amazon_aplus_03_card_nordic_glass_4k.jpg')
    canvas.save(out_file, quality=98)
    print(f'[SAVED] {out_file}')

# ==============================================================================
# 4. QUALITY PILLAR CARD 3: COLD-EXTRACTED LIVING ENZYMES (1200 x 1200)
# ==============================================================================
def render_pillar_card_03_raw_enzymes():
    w, h = 1200, 1200
    canvas = Image.new('RGB', (w, h), (20, 16, 12))
    draw = ImageDraw.Draw(canvas)

    # Frame
    draw.rectangle([(20, 20), (w - 20, h - 20)], outline=BURGUNDY_DARK, width=3)
    draw.rectangle([(28, 28), (w - 28, h - 28)], outline=GOLD, width=1)

    paste_gold_logo(canvas, cx=600, cy=100, target_w=280)

    # Badge
    font_badge = ImageFont.truetype(FONT_SANS_BOLD, 18)
    draw.rounded_rectangle([(320, 160), (880, 205)], radius=18, fill=BURGUNDY, outline=GOLD, width=2)
    draw.text((600, 182), "RAW BIOACTIVE STANDARD", font=font_badge, fill=BLUSH_PINK, anchor="mm")

    # Headline
    font_head = ImageFont.truetype(FONT_SERIF_BOLD, 42)
    draw.text((600, 260), "RAW & UNPASTEURIZED", font=font_head, fill=IVORY, anchor="mm")

    font_sub = ImageFont.truetype(FONT_SERIF_ITALIC, 22)
    draw.text((600, 305), "Unheated Cold Extraction • Living Bioactive Vitality", font=font_sub, fill=GOLD_LIGHT, anchor="mm")

    # Hexagonal Honeycomb Jar Image in Center
    paste_studio_jar(canvas, 'mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg', cx=600, y_base=850, target_h=520, shadow=True)

    # Enzymes & Lab Certifications
    lab_points = [
        "Diastase Activity >= 8",
        "HMF < 10 mg/kg Purity",
        "Moisture Content < 17.5%",
        "Intact Virgin Beeswax"
    ]
    font_item = ImageFont.truetype(FONT_SANS_BOLD, 17)
    for i, lp in enumerate(lab_points):
        ix = 230 + (i % 2) * 740
        iy = 890 + (i // 2) * 55
        draw.rounded_rectangle([(ix - 180, iy - 20), (ix + 180, iy + 20)], radius=15, fill=(35, 25, 18), outline=GOLD_DARK, width=1)
        draw.text((ix, iy), lp, font=font_item, fill=IVORY, anchor="mm")

    # Arabic Footer
    paste_pango(canvas, "عسل خام غير مبستر ومعصور على البارد • يحتفظ بكامل مضادات الأكسدة وحبوب اللقاح الطبيعية", f"{FONT_ARABIC_BOLD} 20", "#DAAC36", 600, 1040, "center")

    font_spec = ImageFont.truetype(FONT_SANS_REG, 15)
    draw.text((600, 1120), "Lab-tested for active diastase enzymes • 100% Egyptian & Mediterranean Protected Flora", font=font_spec, fill=(160, 160, 160), anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, 'mariam_amazon_aplus_04_card_raw_enzymes_4k.jpg')
    canvas.save(out_file, quality=98)
    print(f'[SAVED] {out_file}')

# ==============================================================================
# 5. FLAGSHIP COMPARISON MATRIX CHART (3840 x 2160)
# ==============================================================================
def render_comparison_matrix_chart():
    w, h = 3840, 2160
    canvas = Image.new('RGB', (w, h), FOREST_OBSIDIAN)
    draw = ImageDraw.Draw(canvas)

    # Header section
    draw.rectangle([(0, 0), (w, 360)], fill=(15, 28, 22))
    draw.line([(0, 360), (w, 360)], fill=GOLD, width=4)
    draw.line([(0, 352), (w, 352)], fill=GOLD_DARK, width=1)

    paste_gold_logo(canvas, cx=1920, cy=95, target_w=460)

    font_kicker = ImageFont.truetype(FONT_SANS_BOLD, 22)
    draw.text((1920, 180), "CONNOISSEUR PRODUCT SELECTION & SPECIFICATION MATRIX", font=font_kicker, fill=BLUSH_PINK, anchor="mm")

    font_head = ImageFont.truetype(FONT_SERIF_BOLD, 46)
    draw.text((1920, 240), "Compare Mariam Natural Honey & Superfood Blends", font=font_head, fill=IVORY, anchor="mm")

    paste_pango(canvas, "دليل المقارنة والمواصفات الفنية المعتمدة لتشكيلة عسل مريم الطبيعي والخلطات الملكية", f"{FONT_ARABIC_BOLD} 24", "#DAAC36", 1920, 305, "center")

    # Table Layout
    x_start = 120
    x_end = 3720
    total_w = x_end - x_start # 3600
    col0_w = 600
    col_w = (total_w - col0_w) // 4 # 750 px per product column

    col_xs = [
        x_start,
        x_start + col0_w,
        x_start + col0_w + col_w,
        x_start + col0_w + col_w * 2,
        x_start + col0_w + col_w * 3,
        x_end
    ]

    # Product Jar Hero Images Row (y: 380 to 920)
    products = [
        {
            'name': 'MARIAM ROYAL MIX',
            'sub': 'Hero Flagship Superfood (500g)',
            'img': 'mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg',
            'color': BURGUNDY,
            'source': 'Wildflower & Amber Mountain Nectar',
            'grade': 'Rich Dark Amber (Pfund: 85mm)',
            'nuts': 'Cashews, Almonds, Hazelnuts & Royal Jelly',
            'diastase': '>= 12.5 Schade (Very High)',
            'texture': 'Viscous & Crunchy Whole Nuts',
            'pairing': 'Artisan Cheese, Greek Yogurt, Fasting Spoon',
            'best_for': 'Daily Stamina & Cognitive Vitality'
        },
        {
            'name': 'MOUNTAIN SIDR HONEY',
            'sub': 'Single-Estate Pure Reserve (500g)',
            'img': 'mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg',
            'color': (25, 45, 35),
            'source': 'Ziziphus Spina-Christi (Mountain Sidr)',
            'grade': 'Golden Butterscotch (Pfund: 65mm)',
            'nuts': '0% Nuts (100% Monofloral Raw Honey)',
            'diastase': '>= 15.0 Schade (Therapeutic)',
            'texture': 'Velvety Smooth, Slow Crystal Form',
            'pairing': 'Warm Water with Lemon, French Brioche',
            'best_for': 'Digestive Health & Deep Immune Support'
        },
        {
            'name': 'RAW CUT HONEYCOMB',
            'sub': 'Geometric Hexagonal Jar (500g)',
            'img': 'mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg',
            'color': (45, 30, 15),
            'source': 'Wild Mountain Meadow & Acacia Bloom',
            'grade': 'Luminous Floral Gold (Pfund: 35mm)',
            'nuts': 'Intact Natural Beeswax Comb Slab',
            'diastase': '>= 9.0 Schade (Raw Living Enzymes)',
            'texture': 'Chewy Pure Virgin Beeswax Cells',
            'pairing': 'Ricotta Flatbread, Charcuterie Board',
            'best_for': 'Respiratory Relief & Sensory Connoisseurs'
        },
        {
            'name': 'CLOVER BLOSSOM FAMILY',
            'sub': 'Monumental Reserve Format (1kg)',
            'img': 'mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg',
            'color': (30, 40, 20),
            'source': 'Trifolium Alexandrinum (Egyptian Clover)',
            'grade': 'Clear Light Amber (Pfund: 30mm)',
            'nuts': '0% Nuts (Pure Floral Nectar 1kg)',
            'diastase': '>= 8.5 Schade (Codex Standard)',
            'texture': 'Light & Silky, Delicate Sweet Bouquet',
            'pairing': 'Pancakes, Herbal Tea, Gourmet Baking',
            'best_for': 'Family Wellness & Natural Sweetener'
        }
    ]

    # Draw product headers with images
    for i, p in enumerate(products):
        col_cx = col_xs[i + 1] + col_w // 2
        # Card background header
        draw.rounded_rectangle([(col_xs[i + 1] + 15, 380), (col_xs[i + 2] - 15, 920)], radius=20, fill=p['color'], outline=GOLD_DARK, width=2)
        paste_studio_jar(canvas, p['img'], cx=col_cx, y_base=780, target_h=370, shadow=True)

        font_pname = ImageFont.truetype(FONT_SERIF_BOLD, 26)
        draw.text((col_cx, 830), p['name'], font=font_pname, fill=IVORY, anchor="mm")
        font_psub = ImageFont.truetype(FONT_SANS_REG, 17)
        draw.text((col_cx, 865), p['sub'], font=font_psub, fill=GOLD_LIGHT, anchor="mm")

    # Metrics Rows
    metric_rows = [
        ('Terroir & Botanical Source', 'source'),
        ('Color Grade & Optical Density', 'grade'),
        ('Nut & Superfood Enrichment', 'nuts'),
        ('Diastase Bioactive Activity', 'diastase'),
        ('Mouthfeel & Crystallization', 'texture'),
        ('Gastronomy & Culinary Pairing', 'pairing'),
        ('Primary Wellness Application', 'best_for')
    ]

    y_row_start = 940
    row_h = 160

    font_m_label = ImageFont.truetype(FONT_SANS_BOLD, 20)
    font_m_val = ImageFont.truetype(FONT_SANS_REG, 19)
    font_m_val_bold = ImageFont.truetype(FONT_SANS_BOLD, 19)

    for r_idx, (label, key) in enumerate(metric_rows):
        ry = y_row_start + r_idx * row_h
        bg_col = (18, 30, 24) if r_idx % 2 == 0 else (12, 22, 18)

        # Full row band
        draw.rectangle([(x_start, ry), (x_end, ry + row_h)], fill=bg_col)
        draw.line([(x_start, ry), (x_end, ry)], fill=(45, 65, 50), width=1)

        # Metric label in col 0
        draw.text((x_start + 30, ry + row_h // 2), label, font=font_m_label, fill=GOLD, anchor="lm")

        # Values for each product
        for p_idx, p in enumerate(products):
            col_cx = col_xs[p_idx + 1] + col_w // 2
            val = p[key]

            # Highlight Royal Mix nut purity
            is_hero_feature = (p_idx == 0 and key in ('nuts', 'best_for'))
            val_col = BLUSH_PINK if is_hero_feature else IVORY
            f_val = font_m_val_bold if is_hero_feature else font_m_val

            # Wrap if long
            if len(val) > 36:
                words = val.split(', ')
                if len(words) == 2:
                    draw.text((col_cx, ry + row_h // 2 - 14), words[0] + ',', font=f_val, fill=val_col, anchor="mm")
                    draw.text((col_cx, ry + row_h // 2 + 16), words[1], font=f_val, fill=val_col, anchor="mm")
                else:
                    draw.text((col_cx, ry + row_h // 2), val, font=f_val, fill=val_col, anchor="mm")
            else:
                draw.text((col_cx, ry + row_h // 2), val, font=f_val, fill=val_col, anchor="mm")

    # Column vertical separators
    for x in col_xs:
        draw.line([(x, 940), (x, y_row_start + len(metric_rows) * row_h)], fill=GOLD_DARK, width=1)

    # Footer banner
    draw.rectangle([(0, 2060), (w, 2160)], fill=(8, 16, 12))
    draw.line([(0, 2060), (w, 2060)], fill=GOLD, width=2)
    font_foot = ImageFont.truetype(FONT_SANS_REG, 18)
    draw.text((1920, 2110), "ALL PRODUCTS GUARANTEED 100% RAW & UNPASTEURIZED • PRODUCED & PACKED BY MARIAM FOOD INDUSTRIES • CODEX STAN 12-1981 COMPLIANT", font=font_foot, fill=GOLD_LIGHT, anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, 'mariam_amazon_aplus_05_comparison_matrix_chart_4k.jpg')
    canvas.save(out_file, quality=98)
    print(f'[SAVED] {out_file}')

# ==============================================================================
# 6. DAILY FUNCTIONAL WELLNESS RITUAL INFOGRAPHIC BANNER (3840 x 1800)
# ==============================================================================
def render_functional_wellness_infographic():
    w, h = 3840, 1800
    canvas = Image.new('RGB', (w, h), (14, 18, 22))
    draw = ImageDraw.Draw(canvas)

    # Ambient gradient glow
    for r in range(900, 0, -30):
        alpha = int(14 * (1 - r / 900))
        draw.ellipse([(1920 - r * 2, 900 - r), (1920 + r * 2, 900 + r)], fill=(25 + alpha * 2, 20 + alpha, 10 + alpha))

    # Border trim
    draw.rectangle([(25, 25), (w - 25, h - 25)], outline=GOLD, width=2)

    # Header
    paste_gold_logo(canvas, cx=1920, cy=140, target_w=520)

    font_kicker = ImageFont.truetype(FONT_SANS_BOLD, 24)
    draw.text((1920, 240), "THE CONNOISSEUR DAILY CHRONO-NUTRITION PROTOCOL", font=font_kicker, fill=BLUSH_PINK, anchor="mm")

    font_head = ImageFont.truetype(FONT_SERIF_BOLD, 54)
    draw.text((1920, 310), "Four Daily Rituals of Vitality & Gourmet Pleasure", font=font_head, fill=IVORY, anchor="mm")

    paste_pango(canvas, "بروتوكول الطاقة الحيوية اليومي مع عسل مريم — من الصباح الباكر حتى النوم الهادئ", f"{FONT_ARABIC_BOLD} 26", "#DAAC36", 1920, 375, "center")

    # 4 Chrono-Nutrition Pillars
    rituals = [
        {
            'time': '07:00 AM',
            'title': 'MORNING FASTING SPOON',
            'product': 'Single-Estate Mountain Sidr 500g',
            'desc': 'One tablespoon on an empty stomach in warm water. Activates natural digestive enzymes, soothes stomach lining, and provides clean cellular hydration.',
            'img': 'mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg',
            'color': BURGUNDY,
            'tag': 'IMMUNITY & GUT RESTORATION'
        },
        {
            'time': '01:00 PM',
            'title': 'COGNITIVE POWER BOOST',
            'product': 'Mariam Royal Mix 500g (Nuts & Honey)',
            'desc': 'Raw amber honey packed with whole roasted almonds, cashews, and hazelnuts. Sustained brain food that beats afternoon brain fog without blood sugar spikes.',
            'img': 'mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg',
            'color': (25, 45, 35),
            'tag': 'SUSTAINED BRAIN ENERGY'
        },
        {
            'time': '05:00 PM',
            'title': 'PRE-WORKOUT CELLULAR FUEL',
            'product': 'Raw Cut Honeycomb in Honey 500g',
            'desc': 'Chewable raw beeswax comb delivers instant natural glycogen and bioflavonoids. Fuels high-intensity athletic performance and respiratory stamina.',
            'img': 'mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg',
            'color': (45, 30, 15),
            'tag': 'NATURAL ATHLETIC GLYCOGEN'
        },
        {
            'time': '09:30 PM',
            'title': 'EVENING RESTORATIVE SLEEP',
            'product': 'Egyptian Clover Blossom 1kg',
            'desc': 'One teaspoon in warm chamomile infusion. Triggers healthy melatonin synthesis, promotes deep restorative sleep, and stabilizes nocturnal blood glucose.',
            'img': 'mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg',
            'color': (20, 30, 45),
            'tag': 'DEEP SLEEP & RELAXATION'
        }
    ]

    card_w = 820
    card_h = 1150
    spacing = 60
    start_x = (w - (4 * card_w + 3 * spacing)) // 2

    font_time = ImageFont.truetype(FONT_SANS_BOLD, 28)
    font_rtitle = ImageFont.truetype(FONT_SERIF_BOLD, 26)
    font_tag = ImageFont.truetype(FONT_SANS_BOLD, 15)
    font_rprod = ImageFont.truetype(FONT_SANS_BOLD, 19)
    font_rdesc = ImageFont.truetype(FONT_SANS_REG, 17)

    for i, r in enumerate(rituals):
        cx = start_x + i * (card_w + spacing) + card_w // 2
        card_x1 = start_x + i * (card_w + spacing)
        card_x2 = card_x1 + card_w
        card_y1 = 460
        card_y2 = card_y1 + card_h

        # Card container
        draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y2)], radius=24, fill=r['color'], outline=GOLD_DARK, width=2)

        # Time Header Tag
        draw.rounded_rectangle([(card_x1 + 30, card_y1 + 30), (card_x1 + 220, card_y1 + 80)], radius=15, fill=(0, 0, 0, 180), outline=GOLD, width=1)
        draw.text((card_x1 + 125, card_y1 + 55), r['time'], font=font_time, fill=GOLD, anchor="mm")

        # Pillar Tag
        draw.text((card_x2 - 30, card_y1 + 55), r['tag'], font=font_tag, fill=BLUSH_PINK, anchor="rm")

        # Ritual Title
        draw.text((cx, card_y1 + 130), r['title'], font=font_rtitle, fill=IVORY, anchor="mm")

        # Product Sub
        draw.text((cx, card_y1 + 175), r['product'], font=font_rprod, fill=GOLD_LIGHT, anchor="mm")

        # Jar Packshot
        paste_studio_jar(canvas, r['img'], cx=cx, y_base=card_y1 + 750, target_h=490, shadow=True)

        # Description block
        words = r['desc'].split(' ')
        lines = []
        curr_line = []
        for word in words:
            curr_line.append(word)
            if len(' '.join(curr_line)) > 38:
                lines.append(' '.join(curr_line))
                curr_line = []
        if curr_line:
            lines.append(' '.join(curr_line))

        for l_idx, line in enumerate(lines):
            draw.text((cx, card_y1 + 840 + l_idx * 30), line, font=font_rdesc, fill=IVORY, anchor="mm")

        # Guaranteed Safe Line
        draw.line([(card_x1 + 40, card_y2 - 60), (card_x2 - 40, card_y2 - 60)], fill=GOLD_DARK, width=1)
        draw.text((cx, card_y2 - 30), "100% NATURAL • NO PRESERVATIVES • ZERO REFINED SUGAR", font=font_tag, fill=GOLD_LIGHT, anchor="mm")

    out_file = os.path.join(OUTPUT_DIR, 'mariam_amazon_aplus_06_functional_wellness_infographic_4k.jpg')
    canvas.save(out_file, quality=98)
    print(f'[SAVED] {out_file}')

if __name__ == '__main__':
    print('Generating Amazon A+ Content & Infographic Suite in Cinema 4K...')
    render_amazon_brand_story_hero()
    render_pillar_card_01_tree_nuts()
    render_pillar_card_02_nordic_glass()
    render_pillar_card_03_raw_enzymes()
    render_comparison_matrix_chart()
    render_functional_wellness_infographic()
    print('All 6 Amazon A+ 4K modules generated successfully!')
