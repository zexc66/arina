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
        'title_ar': ImageFont.truetype(AR_BOLD, int(42 * scale)),
        'title_en': ImageFont.truetype(EN_BOLD, int(30 * scale)),
        'h2_ar': ImageFont.truetype(AR_BOLD, int(32 * scale)),
        'h2_en': ImageFont.truetype(EN_BOLD, int(24 * scale)),
        'h3_ar': ImageFont.truetype(AR_BOLD, int(24 * scale)),
        'h3_en': ImageFont.truetype(EN_BOLD, int(18 * scale)),
        'body_ar': ImageFont.truetype(AR_REG, int(20 * scale)),
        'body_en': ImageFont.truetype(EN_REG, int(16 * scale)),
        'sub_ar': ImageFont.truetype(AR_REG, int(18 * scale)),
        'sub_en': ImageFont.truetype(EN_REG, int(14 * scale)),
        'badge': ImageFont.truetype(EN_BOLD, int(14 * scale)),
        'badge_ar': ImageFont.truetype(AR_REG, int(15 * scale)),
    }

def draw_header(im, draw, f, W, title_ar, title_en, sub_ar=None, sub_en=None, is_mobile=False):
    # Header container
    y_start = 40 if is_mobile else 35
    
    # Logo
    if os.path.exists('khaeer-alwadi-logo.png'):
        logo = Image.open('khaeer-alwadi-logo.png').convert('RGBA')
        max_h = 75 if is_mobile else 65
        logo.thumbnail((260, max_h), Image.Resampling.LANCZOS)
        if is_mobile:
            im.paste(logo, (int((W - logo.width) / 2), y_start), logo)
            y_title = y_start + logo.height + 15
            draw.text((W/2, y_title), title_ar, font=f['h2_ar'], fill='#D4A836', anchor='mm', direction='rtl')
            draw.text((W/2, y_title + 38), title_en, font=f['h2_en'], fill='#FFFFFF', anchor='mm')
            if sub_ar and sub_en:
                draw.text((W/2, y_title + 74), sub_ar, font=f['sub_ar'], fill='#94A3B8', anchor='mm', direction='rtl')
                draw.text((W/2, y_title + 102), sub_en, font=f['sub_en'], fill='#94A3B8', anchor='mm')
                y_div = y_title + 130
            else:
                y_div = y_title + 80
            draw.line([(60, y_div), (W-60, y_div)], fill='#2D5232', width=2)
            return y_div + 25
        else:
            im.paste(logo, (60, y_start), logo)
            draw.text((W - 60, y_start), title_ar, font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
            draw.text((W - 60, y_start + 42), title_en, font=f['h3_en'], fill='#FFFFFF', anchor='rt')
            draw.line([(60, y_start + 85), (W - 60, y_start + 85)], fill='#2D5232', width=2)
            return y_start + 110

def draw_footer_bar(im, draw, f, W, H, is_mobile=False):
    if is_mobile:
        y = H - 125
        draw.rounded_rectangle([50, y, W-50, y+85], radius=18, fill='#0B3B26', outline='#10B981', width=2)
        draw.text((W/2, y+24), "واتساب: +20 10 08716714  |  خير الوادي للصناعات الغذائية", font=f['badge_ar'], fill='#FFFFFF', anchor='mm', direction='rtl')
        draw.text((W/2, y+58), "Direct WhatsApp: +20 10 08716714 • Cairo, Egypt", font=f['badge'], fill='#10B981', anchor='mm')
    else:
        y = H - 65
        draw.line([(60, y), (W - 60, y)], fill='#2D5232', width=1)
        draw.text((W - 60, y + 20), "خير الوادي للصناعات الغذائية  |  القاهرة، مصر", font=f['badge_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        draw.text((60, y + 20), "Direct WhatsApp: +20 10 08716714  |  wa.me/201008716714", font=f['badge'], fill='#10B981', anchor='lt')
        draw.text((W/2, y + 20), "ISO 22000 • HACCP • FDA Registered • Halal • ISO 9001", font=f['badge'], fill='#D4A836', anchor='mm')

# ----------------- MOBILE SLIDES (1080 x 1920) -----------------
def generate_mobile_slides():
    W, H = 1080, 1920
    f = load_fonts(scale=1.0)
    slides = []

    # Slide 1: Cover
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "خير الوادي للصناعات الغذائية", "Khaeer Alwadi Food Industries",
                    "القاهرة، مصر • تصنيع زراعي متقدم وتصدير دولي", "Cairo, Egypt • Mediterranean Agro Processing & Export", True)
    
    img_path = "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg"
    if os.path.exists(img_path):
        p_img = Image.open(img_path).convert('RGB')
        p_img.thumbnail((W - 140, 420), Image.Resampling.LANCZOS)
        im.paste(p_img, (int((W - p_img.width)/2), int(y)))
        y += p_img.height + 25

    draw.text((W/2, y+10), "زيتون مائدة متوسطي فاخر ومخللات تخصصية", font=f['h2_ar'], fill='#D4A836', anchor='mm', direction='rtl')
    draw.text((W/2, y+48), "Mediterranean Table Olives & Pickled Specialties", font=f['h3_en'], fill='#FFFFFF', anchor='mm')
    y += 85

    pillars = [
        ("التوريد الزراعي المباشر", "وفر 15-25% مقارنة بجنوب أوروبا", "Direct Agro Sourcing • 15-25% Cost Advantage"),
        ("طاقة صناعية مؤتمتة", "خطوط نزع نواة وتقطيع دقيق 3.2 مم", "Automated Pitting & Rotary Slicing Drum"),
        ("موانئ تصدير سريعة", "3-5 أيام لأوروبا و 4-7 أيام للخليج", "Tri-Port Corridors: 3-5 Days EU / 4-7 Days GCC"),
        ("اعتمادات دولية شاملة", "مطابقة كاملة: ISO, HACCP, FDA, Halal", "Global Compliance: ISO 22000, HACCP, FDA, Halal")
    ]
    for ar_t, ar_d, en_l in pillars:
        draw.rounded_rectangle([60, y, W-60, y+115], radius=14, fill='#10221A', outline='#2D5232', width=2)
        draw.text((W-85, y+18), ar_t, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((W-85, y+52), ar_d, font=f['body_ar'], fill='#F8FAFC', anchor='rt', direction='rtl')
        draw.text((85, y+85), en_l, font=f['sub_en'], fill='#94A3B8', anchor='lt')
        y += 130

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 2: Strategic Supply Advantage
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "الميزة التنافسية والتصديرية", "Egyptian Strategic Supply Advantage",
                    "موقع جغرافي استراتيجي واتفاقيات تجارة حرة عالمية", "Tri-Port Proximity & Duty-Free Trade Agreements", True)

    # Cost Thesis Card
    draw.rounded_rectangle([60, y, W-60, y+160], radius=16, fill='#1A3324', outline='#D4A836', width=2)
    draw.text((W/2, y+30), "وفر تكلفة إجمالية 15% - 25% مقارنة بجنوب أوروبا", font=f['h3_ar'], fill='#D4A836', anchor='mm', direction='rtl')
    draw.text((W/2, y+70), "15–25% Landed Cost Advantage vs Spain, Greece & Italy", font=f['h3_en'], fill='#FFFFFF', anchor='mm')
    draw.text((W/2, y+110), "إنتاجية زراعية مستدامة • تكاليف طاقة وعمالة تنافسية • شحن بحري سريع", font=f['sub_ar'], fill='#94A3B8', anchor='mm', direction='rtl')
    y += 185

    # Ports
    draw.text((W-65, y), "شبكة الموانئ المصرية الثلاثية:", font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    y += 45
    ports = [
        ("ميناء الإسكندرية", "Alexandria Port", "2.5 ساعة من المصنع • أكبر موانئ المتوسط"),
        ("ميناء دمياط", "Damietta Port", "2.5 ساعة من المصنع • محطة حاويات حديثة"),
        ("ميناء بورسعيد", "Port Said Port", "2.0 ساعة من المصنع • مدخل قناة السويس")
    ]
    for p_ar, p_en, p_sub in ports:
        draw.rounded_rectangle([60, y, W-60, y+100], radius=14, fill='#10221A', outline='#2D5232', width=2)
        draw.text((W-85, y+18), p_ar, font=f['h3_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        draw.text((85, y+22), p_en, font=f['h3_en'], fill='#D4A836', anchor='lt')
        draw.text((W-85, y+58), p_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        y += 115

    y += 10
    draw.text((W-65, y), "اتفاقيات التجارة الحرة والإعفاء الجمركي:", font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    y += 45
    pacts = [
        ("منطقة التجارة العربية الكبرى (GAFTA)", "0% جمارك لكافة الدول العربية والخليج"),
        ("السوق المشتركة لشرق وجنوب أفريقيا (COMESA)", "إعفاء جمركي كامل لأسواق شرق أفريقيا"),
        ("اتفاقية أغادير الأورومتوسطية (Agadir)", "تراكم المنشأ الصناعي مع أوروبا والمغرب العربي"),
        ("اتفاقية الشراكة المصرية الأوروبية (EU)", "نفاذ تفضيلي مباشر للأسواق الأوروبية")
    ]
    for pact_ar, pact_sub in pacts:
        draw.rounded_rectangle([60, y, W-60, y+90], radius=12, fill='#10221A', outline='#2D5232', width=1)
        draw.text((W-85, y+16), pact_ar, font=f['h3_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        draw.text((W-85, y+50), pact_sub, font=f['sub_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        y += 105

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 3: Infrastructure & Certifications
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "البنية الصناعية والاعتمادات", "Industrial Infrastructure & Certifications",
                    "خطوط إنتاج مؤتمتة وتعقيم أوتوكلاف واعتمادات سلامة عالمية", "Automated Lines, Overpressure Autoclaves & ISO Certifications", True)

    img_auto = "WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg"
    if os.path.exists(img_auto):
        ai = Image.open(img_auto).convert('RGB')
        ai.thumbnail((W - 140, 360), Image.Resampling.LANCZOS)
        im.paste(ai, (int((W - ai.width)/2), int(y)))
        y += ai.height + 25

    techs = [
        ("خطوط نزع النوى الآلية المتطورة", "Automated Pitting Lines", "نزع نوى ميكانيكي عالي الدقة مع نسبة تكسير أقل من 1%"),
        ("أسطوانات التقطيع الدوارة", "Rotary Slicing Drums", "تقطيع حلزوني منتظم بسماكة محايدة 3.2 مم ±0.2 مم"),
        ("أوتوكلاف التعقيم بالضغط الزائد", "Overpressure Autoclave Retort", "تعقيم حراري وميكروبيولوجي تجاري كامل مع قيمة F0 ≥ 4.0")
    ]
    for t_ar, t_en, t_sub in techs:
        draw.rounded_rectangle([60, y, W-60, y+110], radius=14, fill='#10221A', outline='#2D5232', width=2)
        draw.text((W-85, y+16), t_ar, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((85, y+20), t_en, font=f['h3_en'], fill='#FFFFFF', anchor='lt')
        draw.text((W-85, y+60), t_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        y += 125

    y += 10
    draw.text((W-65, y), "الشهادات والاعتمادات الدولية:", font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    y += 45
    badges = [
        ("ISO 22000:2018", "Food Safety Management System • معتمد"),
        ("HACCP Certified", "Hazard Analysis Critical Control Points"),
        ("FDA Registered", "US FSMA & 21 CFR Part 117 Compliant"),
        ("Halal Certified", "حلال معتمد 100% لكافة الأسواق الإسلامية"),
        ("ISO 9001:2015", "Quality Management System • جودة شاملة")
    ]
    for b_title, b_sub in badges:
        draw.rounded_rectangle([60, y, W-60, y+65], radius=10, fill='#0F281E', outline='#10B981', width=1)
        draw.text((85, y+20), b_title, font=f['badge'], fill='#10B981', anchor='lt')
        draw.text((W-85, y+20), b_sub, font=f['badge_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        y += 78

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 4: Table Olives Portfolio
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "تشكيلة زيتون المائدة الفاخر", "Premium Table Olives Portfolio",
                    "زيتون أسود وأخضر (كامل، مخلي، شرائح ومحشي بيمينتو)", "Whole, Pitted, Sliced & Pimento-Stuffed Olives", True)

    products_olives = [
        ("زيتون أسود شرائح 3.2 مم", "Sliced Black Olives", "WhatsApp Image 2026-09-05 at 12.52.20 PM.jpeg", "عيار 200/220 • بيتزا وخدمات غذائية"),
        ("زيتون أسود كامل ومفرغ", "Pitted & Whole Black Olives", "WhatsApp Image 2026-09-05 at 12.52.16 PM (5).jpeg", "عيار 180/200 • قوام متماسك ونكهة غنية"),
        ("زيتون أخضر بيكوال ومانزانيلا", "Picual & Manzanilla Green Olives", "WhatsApp Image 2026-09-05 at 12.52.17 PM (6).jpeg", "عيار 240/260 • قرمشة ولون زيتوني نضر"),
        ("زيتون أخضر محشي فلفل بيمينتو", "Pimento-Stuffed Green Olives", "WhatsApp Image 2026-09-05 at 12.52.17 PM (5).jpeg", "حشو طبيعي 100% • برطمانات وتجزئة فاخرة"),
        ("زيتون كالاماتا طبيعي داكن", "Kalamata-Style Natural Olives", "WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg", "تخمير طبيعي • محلول ملحي وزيت زيتون")
    ]
    for p_ar, p_en, img_p, p_sub in products_olives:
        draw.rounded_rectangle([60, y, W-60, y+200], radius=16, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((180, 180), Image.Resampling.LANCZOS)
            im.paste(p_img, (75, y+10))
        draw.text((W-85, y+25), p_ar, font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((W-85, y+75), p_en, font=f['h3_en'], fill='#FFFFFF', anchor='rt')
        draw.text((W-85, y+120), p_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        draw.rounded_rectangle([W-320, y+155, W-85, y+188], radius=8, fill='#1E3A24')
        draw.text((W-202, y+171), "الوزن المصفى ≥ 52%", font=f['sub_ar'], fill='#10B981', anchor='mm', direction='rtl')
        y += 225

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 5: Pickled Specialties
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "المخللات التخصصية والفلفل", "Pickled Specialties & Gourmet Peppers",
                    "فلفل بيبرونشيني، فلفل أحمر حار، طرشي بلدي مصري وخيار مقرمش", "Pepperoncini, Red Chilis, Traditional Turshi & Gherkins", True)

    products_pickles = [
        ("فلفل بيبرونشيني أصفر ذهبي", "Golden Tuscan Pepperoncini", "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg", "قرمشة عالية ونكهة معتدلة • عبوات A10 وبرطمانات"),
        ("فلفل أحمر حار مخلل", "Gourmet Hot Red Chili Peppers", "WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg", "قرون كاملة منتقاة بعناية • حرارة متوازنة"),
        ("طرشي بلدي مصري مشكل", "Traditional Egyptian Turshi Baladi", "WhatsApp Image 2026-09-05 at 12.52.16 PM (2).jpeg", "جزر، لفت، خيار وفلفل • خلطة بهارات شرقية أصيلة"),
        ("خيار مخلل مقرمش (قثاء)", "Crisp Pickled Gherkins & Cucumbers", "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg", "قرمشة استثنائية • محلول خل وشبت وبذور خردل")
    ]
    for p_ar, p_en, img_p, p_sub in products_pickles:
        draw.rounded_rectangle([60, y, W-60, y+245], radius=16, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((220, 220), Image.Resampling.LANCZOS)
            im.paste(p_img, (75, y+12))
        draw.text((W-85, y+30), p_ar, font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((W-85, y+85), p_en, font=f['h3_en'], fill='#FFFFFF', anchor='rt')
        draw.text((W-85, y+140), p_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        draw.rounded_rectangle([W-360, y+190, W-85, y+228], radius=8, fill='#1E3A24')
        draw.text((W-222, y+209), "درجة حموضة pH 3.2–3.6", font=f['sub_ar'], fill='#10B981', anchor='mm', direction='rtl')
        y += 275

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 6: Packaging Architecture
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "هندسة العبوات والتغليف", "Multi-Tier Packaging Architecture",
                    "حلول تعبئة مرنة: صفيح، براميل صناعية، برطمانات ومنصات تصدير", "Cans, Bulk HDPE Drums, Retail Jars & ISPM-15 Pallets", True)

    tiers = [
        ("عبوات الصفيح A10 للخدمات الغذائية", "Foodservice A10 Cans", "WhatsApp Image 2026-09-05 at 12.52.17 PM (7).jpeg", "سعة 3 كجم و 5 كجم • لحام مزدوج محكم • صلاحية 36 شهراً"),
        ("براميل بوليمر صناعية للأغذية", "Industrial Bulk HDPE Drums", "WhatsApp Image 2026-09-05 at 12.52.17 PM (4).jpeg", "سعة 150 كجم إلى 220 كجم • حلقة إغلاق معدنية محكمة"),
        ("برطمانات زجاجية فائقة النقاء", "Retail Supermarket Glass Jars", "WhatsApp Image 2026-09-05 at 12.52.16 PM (4).jpeg", "أحجام 370 مل، 500 مل، 720 مل و 1000 مل • أغطية أمان تويست أوف"),
        ("منصات شحن وحماية الرطوبة", "Palletization & Barrier Wrap", "WhatsApp Image 2026-09-05 at 12.52.15 PM (5).jpeg", "طبالي خشبية معالجة حرارياً ISPM-15 • تغليف استريتش حراري")
    ]
    for p_ar, p_en, img_p, p_sub in tiers:
        draw.rounded_rectangle([60, y, W-60, y+245], radius=16, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((220, 220), Image.Resampling.LANCZOS)
            im.paste(p_img, (75, y+12))
        draw.text((W-85, y+30), p_ar, font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((W-85, y+85), p_en, font=f['h3_en'], fill='#FFFFFF', anchor='rt')
        draw.text((W-85, y+140), p_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        y += 275

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 7: Private Label & OEM
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "حلول التصنيع للغير (Private Label)", "Turnkey OEM & Private Label Solutions",
                    "حلول تصنيع متكاملة للعلامات التجارية العالمية وسلاسل التوزيع", "End-to-End Production for Global Food Brands & Supermarkets", True)

    img_oem = "WhatsApp Image 2026-09-05 at 12.52.19 PM (1).jpeg"
    if os.path.exists(img_oem):
        oi = Image.open(img_oem).convert('RGB')
        oi.thumbnail((W - 140, 360), Image.Resampling.LANCZOS)
        im.paste(oi, (int((W - oi.width)/2), int(y)))
        y += oi.height + 25

    stages = [
        ("1. التوريد الزراعي وانتقاء الأصناف", "Agro Sourcing: اختيار أفضل مزارع وادي النطرون وسيناء"),
        ("2. تطوير المحاليل الملحية المخصصة", "Custom Brines: ضبط درجات الحموضة والملوحة والبهارات"),
        ("3. التقطيع الدقيق وتخصيص الأحجام", "Precision Geometry: شرائح 3.2 مم، كامل أو مخلي"),
        ("4. المطابقة التنظيمية وتصميم البطاقات", "Regulatory Compliance: مطابقة FDA, EU FIC, GSO"),
        ("5. التعبئة والتغليف الثانوي المحمي", "Packaging: طباعة علامات العملاء وتغليف كرتوني مقوى"),
        ("6. الإفراج المخبري وشحن الحاويات", "QC & Dispatch: فحص ميكروبيولوجي وإصدار شهادات التحليل")
    ]
    for s_title, s_desc in stages:
        draw.rounded_rectangle([60, y, W-60, y+95], radius=12, fill='#10221A', outline='#2D5232', width=1)
        draw.text((W-85, y+18), s_title, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((W-85, y+55), s_desc, font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        y += 115

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 8: Technical Specifications & Freight
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "المواصفات الفنية ولوجستيات الشحن", "Technical Specifications & Logistics",
                    "مصفوفة الجودة القياسية وبيانات حمولة الحاويات الدولية", "Quality Metrics & International Container Payload Capacity", True)

    # Container Freight Box
    draw.rounded_rectangle([60, y, W-60, y+200], radius=16, fill='#163024', outline='#D4A836', width=2)
    draw.text((W/2, y+25), "بيانات تحميل الحاويات الدولية (FCL Intermodal Capacity)", font=f['h3_ar'], fill='#D4A836', anchor='mm', direction='rtl')
    draw.line([(90, y+55), (W-90, y+55)], fill='#2D5232', width=1)
    
    draw.text((W-90, y+80), "حاوية 20 قدم FCL Standard Dry:", font=f['h3_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
    draw.text((W-90, y+115), "10 طبالي ISPM-15 • صافي حمولة 18–21 طن متري", font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
    
    draw.text((W-90, y+145), "حاوية 40 قدم FCL High Cube:", font=f['h3_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
    draw.text((W-90, y+180), "20 إلى 22 طبلية • أقصى استيعاب وزني 24–26 طن متري", font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
    y += 230

    draw.text((W-65, y), "مصفوفة الجودة والمطابقة الكيميائية:", font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    y += 45

    specs = [
        ("زيتون مائدة كامل ومخلي", "وزن مصفى ≥ 52% • حموضة pH 3.8-4.2 • ملوحة 5-6% • عيوب < 1.0%"),
        ("زيتون مائدة شرائح 3.2 مم", "وزن مصفى ≥ 50% • سماكة دقيقة 3.2 مم • تكسير < 1.5% • ملوحة 4.5-5.5%"),
        ("فلفل بيبرونشيني وفاخر", "وزن مصفى ≥ 52% • حموضة pH 3.2-3.6 • ملوحة 3.5-4.5% • قوام مقرمش"),
        ("طرشي بلدي وخيار مخلل", "وزن مصفى ≥ 50% • حموضة pH 3.3-3.7 • ملوحة 4.0-5.0% • بدون أصباغ ضارة")
    ]
    for sp_title, sp_line in specs:
        draw.rounded_rectangle([60, y, W-60, y+115], radius=14, fill='#10221A', outline='#2D5232', width=1)
        draw.text((W-85, y+20), sp_title, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((W-85, y+62), sp_line, font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        y += 135

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    # Slide 9: Commercial Desk
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "مكتب الشراكات التجارية والطلبات", "Commercial Partnerships & Direct Line",
                    "إجراءات التعاقد السريع، إرسال العينات والتواصل المباشر", "Sample Dispatch, Formal Quotations & Direct Procurement Desk", True)

    onboardings = [
        ("1. بروتوكول إرسال العينات الفورية", "Express Samples: شحن عينات جوية عبر DHL / FedEx خلال 48 ساعة"),
        ("2. عروض أسعار تفصيلية خلال 24 ساعة", "Formal Quotation: أسعار شفافة وفق شروط FOB أو CIF لكافة الموانئ"),
        ("3. شروط دفع مرنة وآمنة", "Payment Terms: اعتماد مستندي معزز L/C at sight أو تحويل بنكي T/T"),
        ("4. جدول إنتاج وشحن سريع", "Rapid Laycan: جاهزية شحن وتعبئة قياسية خلال 10 إلى 14 يوماً فقط")
    ]
    for o_t, o_d in onboardings:
        draw.rounded_rectangle([60, y, W-60, y+95], radius=12, fill='#10221A', outline='#2D5232', width=1)
        draw.text((W-85, y+18), o_t, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((W-85, y+55), o_d, font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        y += 115

    y += 15
    # Big Procurement Contact Card
    draw.rounded_rectangle([60, y, W-60, y+380], radius=24, fill='#0B261A', outline='#10B981', width=3)
    draw.text((W/2, y+45), "خير الوادي للصناعات الغذائية", font=f['title_ar'], fill='#D4A836', anchor='mm', direction='rtl')
    draw.text((W/2, y+95), "Khaeer Alwadi Food Industries", font=f['title_en'], fill='#FFFFFF', anchor='mm')
    draw.text((W/2, y+140), "المقر الرئيسي: القاهرة، جمهورية مصر العربية", font=f['h3_ar'], fill='#94A3B8', anchor='mm', direction='rtl')
    
    draw.rounded_rectangle([100, y+180, W-100, y+270], radius=18, fill='#10B981')
    draw.text((W/2, y+212), "للتواصل المباشر والطلبات عبر واتساب:", font=f['badge_ar'], fill='#000000', anchor='mm', direction='rtl')
    draw.text((W/2, y+245), "+20 10 08716714", font=f['title_en'], fill='#000000', anchor='mm')

    draw.text((W/2, y+310), "رابط الدردشة المباشر: wa.me/201008716714", font=f['h3_en'], fill='#10B981', anchor='mm')
    draw.text((W/2, y+350), "ISO 22000  •  HACCP  •  FDA Registered  •  Halal  •  ISO 9001", font=f['badge'], fill='#D4A836', anchor='mm')

    draw_footer_bar(im, draw, f, W, H, True)
    slides.append(im)

    return slides

# ----------------- PRESENTATION SLIDES (1920 x 1080) -----------------
def generate_presentation_slides():
    W, H = 1920, 1080
    f = load_fonts(scale=1.1)
    slides = []

    # Slide 1: Cover Landscape
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "خير الوادي للصناعات الغذائية", "Khaeer Alwadi Food Industries", is_mobile=False)

    # 2-column layout: Left column info, Right column photo
    col_w = 880
    left_x = 60
    right_x = 980

    # Left content
    draw.text((right_x - 40, y + 20), "زيتون مائدة متوسطي ومخللات تخصصية", font=f['title_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    draw.text((left_x, y + 80), "Mediterranean Table Olives & Pickled Specialties — Industrial Processing & Export", font=f['h3_en'], fill='#FFFFFF', anchor='lt')
    
    pillars = [
        ("التوريد الزراعي المباشر", "Direct Agro Terroir: وفر 15-25% في تكلفة التوريد مقارنة بإسبانيا واليونان"),
        ("الطاقة الصناعية المؤتمتة", "Automated Scale: خطوط نزع نوى وتقطيع دقيق 3.2 مم وتعقيم أوتوكلاف"),
        ("لوجستيات الموانئ السريعة", "Rapid Shipping: موانئ الإسكندرية ودمياط وبورسعيد (3-5 أيام لأوروبا، 4-7 للخليج)"),
        ("الاعتمادات والمطابقة الدولية", "Global Standards: ISO 22000, HACCP, FDA Registered, Halal, ISO 9001")
    ]
    py = y + 140
    for p_t, p_d in pillars:
        draw.rounded_rectangle([left_x, py, right_x - 40, py + 95], radius=14, fill='#10221A', outline='#2D5232', width=1)
        draw.text((right_x - 65, py + 16), p_t, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((right_x - 65, py + 52), p_d, font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        py += 115

    # WhatsApp card on left
    draw.rounded_rectangle([left_x, py + 10, right_x - 40, py + 85], radius=14, fill='#0B3B26', outline='#10B981', width=2)
    draw.text((right_x - 65, py + 28), "للتواصل المباشر والطلبات عبر واتساب:", font=f['badge_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
    draw.text((left_x + 25, py + 32), "+20 10 08716714  •  wa.me/201008716714", font=f['h3_en'], fill='#10B981', anchor='lt')

    # Right column photo
    img_path = "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg"
    if os.path.exists(img_path):
        p_img = Image.open(img_path).convert('RGB')
        p_img.thumbnail((col_w, H - y - 120), Image.Resampling.LANCZOS)
        im.paste(p_img, (right_x + int((col_w - p_img.width)/2), y + 20))

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 2: Strategic Supply Advantage Landscape
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "الميزة التنافسية للزراعة والتصدير المصري", "The Egyptian Strategic Supply Advantage", is_mobile=False)

    draw.rounded_rectangle([60, y, W - 60, y + 100], radius=16, fill='#163024', outline='#D4A836', width=2)
    draw.text((W/2, y + 30), "وفر تكلفة إجمالية 15% - 25% مقارنة بالمنافسين في إسبانيا واليونان وإيطاليا", font=f['h2_ar'], fill='#D4A836', anchor='mm', direction='rtl')
    draw.text((W/2, y + 70), "15–25% Landed Cost Advantage vs Southern European Competitors", font=f['h3_en'], fill='#FFFFFF', anchor='mm')
    y += 130

    # 3 Ports Columns
    col_w3 = 580
    ports = [
        ("ميناء الإسكندرية (2.5 ساعة)", "Alexandria Port", "أكبر موانئ مصر المتوسطية • خطوط شحن مباشرة لكافة موانئ العالم"),
        ("ميناء دمياط (2.5 ساعة)", "Damietta Port", "محطة حاويات متطورة • سرعة فائقة في الإجراءات الجمركية والترانزيت"),
        ("ميناء بورسعيد (2.0 ساعة)", "Port Said Port", "موقع محوري على قناة السويس • ربط فوري مع موانئ الخليج وآسيا")
    ]
    px = 60
    for p_ar, p_en, p_sub in ports:
        draw.rounded_rectangle([px, y, px + col_w3, y + 200], radius=16, fill='#10221A', outline='#2D5232', width=1)
        draw.text((px + col_w3 - 25, y + 25), p_ar, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((px + 25, y + 65), p_en, font=f['h3_en'], fill='#FFFFFF', anchor='lt')
        draw.text((px + col_w3 - 25, y + 115), p_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        px += col_w3 + 30
    y += 235

    # 4 Trade Pacts
    draw.text((W - 60, y), "اتفاقيات التجارة الحرة والإعفاءات الجمركية الدولية:", font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    y += 40
    pacts = [
        ("اتفاقية التجارة العربية (GAFTA)", "0% جمارك لكافة أسواق الدول العربية والخليج"),
        ("اتفاقية الكوميسا (COMESA)", "إعفاء جمركي لأسواق شرق وجنوب القارة الأفريقية"),
        ("اتفاقية أغادير (Agadir)", "تراكم منشأ حر مع الاتحاد الأوروبي والمغرب العربي"),
        ("الشراكة المصرية الأوروبية (EU)", "نفاذ تفضيلي وإعفاءات جمركية لأسواق أوروبا")
    ]
    col_w4 = 425
    px = 60
    for p_ar, p_sub in pacts:
        draw.rounded_rectangle([px, y, px + col_w4, y + 140], radius=14, fill='#10221A', outline='#2D5232', width=1)
        draw.text((px + col_w4 - 20, y + 20), p_ar, font=f['h3_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        draw.text((px + col_w4 - 20, y + 65), p_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        px += col_w4 + 33

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 3: Infrastructure & Compliance Landscape
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "البنية الصناعية، التكنولوجيا والمطابقة الدولية", "Industrial Infrastructure & Global Compliance", is_mobile=False)

    # 2 photos in center/right
    img1 = "WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg"
    img2 = "WhatsApp Image 2026-09-05 at 12.52.17 PM.jpeg"
    if os.path.exists(img1) and os.path.exists(img2):
        i1 = Image.open(img1).convert('RGB')
        i2 = Image.open(img2).convert('RGB')
        i1.thumbnail((500, 360), Image.Resampling.LANCZOS)
        i2.thumbnail((500, 360), Image.Resampling.LANCZOS)
        im.paste(i1, (1360, y + 20))
        im.paste(i2, (1360, y + 410))

    # Left content machinery
    col_w_left = 1260
    techs = [
        ("خطوط نزع النوى الآلية فائقة الدقة", "Automated Pitting Lines", "نزع نوى ميكانيكي عالي الدقة بدون إتلاف قوام الحبة مع نسبة تكسير أقل من 1%"),
        ("أسطوانات التقطيع الدوارة المنتظمة", "Rotary Slicing Drums", "تقطيع حلزوني دقيق بسماكة موحدة 3.2 مم ±0.2 مم لضمان أعلى جودة لقطاع البيتزا والمطاعم"),
        ("أوتوكلاف التعقيم بالضغط الزائد", "Overpressure Autoclave Retort", "تعقيم حراري وميكروبيولوجي متقدم يحقق قيمة F0 ≥ 4.0 لتأمين صلاحية تجارية 36 شهراً")
    ]
    ty = y + 20
    for t_ar, t_en, t_sub in techs:
        draw.rounded_rectangle([60, ty, col_w_left, ty + 125], radius=16, fill='#10221A', outline='#2D5232', width=1)
        draw.text((col_w_left - 25, ty + 20), t_ar, font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((85, ty + 25), t_en, font=f['h3_en'], fill='#FFFFFF', anchor='lt')
        draw.text((col_w_left - 25, ty + 70), t_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        ty += 145

    # Certifications Bar
    draw.rounded_rectangle([60, ty + 20, col_w_left, ty + 175], radius=16, fill='#0B2E1E', outline='#10B981', width=2)
    draw.text((col_w_left - 30, ty + 40), "الشهادات والاعتمادات الدولية المعتمدة لمصنع خير الوادي:", font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    badges_str = "ISO 22000:2018  •  HACCP Certified  •  FDA Registered  •  Halal Certified  •  ISO 9001:2015"
    draw.text((col_w_left/2 + 30, ty + 105), badges_str, font=f['h3_en'], fill='#FFFFFF', anchor='mm')

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 4: Table Olives Landscape (5 Cards)
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "خط الإنتاج الأول: تشكيلة زيتون المائدة الفاخر", "Core Line I: Premium Table Olives Portfolio", is_mobile=False)

    font_card_title = ImageFont.truetype(AR_BOLD, int(20 * 1.1))
    products_olives = [
        ("زيتون أسود شرائح 3.2 مم", "Sliced Black Olives", "WhatsApp Image 2026-09-05 at 12.52.20 PM.jpeg", "عيار 200/220", "سلاسل البيتزا والمطاعم"),
        ("زيتون أسود كامل ومفرغ", "Pitted Black Olives", "WhatsApp Image 2026-09-05 at 12.52.16 PM (5).jpeg", "عيار 180/200", "قوام متماسك وطعم غني"),
        ("زيتون أخضر بيكوال فاخر", "Picual Green Olives", "WhatsApp Image 2026-09-05 at 12.52.17 PM (6).jpeg", "عيار 240/260", "قرمشة ونضارة زيتونية"),
        ("زيتون محشي فلفل بيمينتو", "Pimento-Stuffed Olives", "WhatsApp Image 2026-09-05 at 12.52.17 PM (5).jpeg", "حشو طبيعي 100%", "تجزئة وسوبرماركت"),
        ("زيتون كالاماتا طبيعي داكن", "Kalamata-Style Dark", "WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg", "تخمير طبيعي", "محلول ملحي وزيت زيتون")
    ]
    card_w = 340
    cx = 60
    for p_ar, p_en, img_p, p_line1, p_line2 in products_olives:
        draw.rounded_rectangle([cx, y + 20, cx + card_w, y + 680], radius=18, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((card_w - 30, 260), Image.Resampling.LANCZOS)
            im.paste(p_img, (cx + int((card_w - p_img.width)/2), y + 35))
        draw.text((cx + card_w/2, y + 325), p_ar, font=font_card_title, fill='#D4A836', anchor='mt', direction='rtl')
        draw.text((cx + card_w/2, y + 365), p_en, font=f['sub_en'], fill='#FFFFFF', anchor='mt')
        draw.text((cx + card_w/2, y + 410), p_line1, font=f['sub_ar'], fill='#E2E8F0', anchor='mt', direction='rtl')
        draw.text((cx + card_w/2, y + 445), p_line2, font=f['sub_ar'], fill='#94A3B8', anchor='mt', direction='rtl')
        
        # Spec Box
        draw.rounded_rectangle([cx + 20, y + 540, cx + card_w - 20, y + 640], radius=10, fill='#163024')
        draw.text((cx + card_w/2, y + 570), "نسبة الوزن المصفى ≥ 52%", font=f['sub_ar'], fill='#10B981', anchor='mm', direction='rtl')
        draw.text((cx + card_w/2, y + 610), "سماكة الشريحة 3.2 مم", font=f['sub_ar'], fill='#D4A836', anchor='mm', direction='rtl')
        cx += card_w + 25

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 5: Pickled Specialties Landscape (4 Cards)
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "خط الإنتاج الثاني: المخللات التخصصية والفلفل", "Core Line II: Pickled Specialties & Gourmet Peppers", is_mobile=False)

    products_pickles = [
        ("فلفل بيبرونشيني أصفر ذهبي", "Golden Tuscan Pepperoncini", "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg", "فلفل توسكاني أصفر مقرمش خفيف الحرارة • مثالي لقطاع البيتزا والبرجر والسلطات"),
        ("فلفل أحمر حار مخلل", "Gourmet Hot Red Chili Peppers", "WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg", "قرون فلفل حمراء كاملة منتقاة بعناية • حرارة متوازنة ونضارة عالية"),
        ("طرشي بلدي مصري مشكل", "Traditional Egyptian Turshi Baladi", "WhatsApp Image 2026-09-05 at 12.52.16 PM (2).jpeg", "مزيج فاخر من الجزر، اللفت، الخيار والفلفل • خلطة التخليل المصرية التقليدية الشهيرة"),
        ("خيار مخلل صغير مقرمش (قثاء)", "Crisp Gherkins & Pickled Cucumbers", "WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg", "خيار طازج ذو قرمشة طبيعية فائقة • محلول تخليل متبل بالشبت وبذور الخردل")
    ]
    card_w4 = 430
    cx = 60
    for p_ar, p_en, img_p, p_sub in products_pickles:
        draw.rounded_rectangle([cx, y + 20, cx + card_w4, y + 680], radius=18, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((card_w4 - 40, 260), Image.Resampling.LANCZOS)
            im.paste(p_img, (cx + int((card_w4 - p_img.width)/2), y + 35))
        draw.text((cx + card_w4 - 20, y + 325), p_ar, font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((cx + 20, y + 375), p_en, font=f['h3_en'], fill='#FFFFFF', anchor='lt')
        draw.text((cx + card_w4 - 20, y + 430), p_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        
        draw.rounded_rectangle([cx + 20, y + 540, cx + card_w4 - 20, y + 640], radius=10, fill='#163024')
        draw.text((cx + card_w4/2, y + 570), "درجة الحموضة pH 3.2 – 3.6", font=f['sub_ar'], fill='#10B981', anchor='mm', direction='rtl')
        draw.text((cx + card_w4/2, y + 610), "قرمشة استثنائية وبدون ألوان صناعية", font=f['sub_ar'], fill='#D4A836', anchor='mm', direction='rtl')
        cx += card_w4 + 26

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 6: Packaging Architecture Landscape (4 Tiers)
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "هندسة العبوات والتعبئة متعددة المستويات", "Multi-Tier Packaging Architecture", is_mobile=False)

    tiers = [
        ("عبوات الصفيح A10 للخدمات الغذائية", "Foodservice A10 Cans", "WhatsApp Image 2026-09-05 at 12.52.17 PM (7).jpeg", "صفيح غذائي معتمد مطلي بالورنيش الواقي • لحام مزدوج هيرميتيك • صلاحية 36 شهراً"),
        ("براميل بوليمر صناعية للأغذية", "Industrial Bulk HDPE Drums", "WhatsApp Image 2026-09-05 at 12.52.17 PM (4).jpeg", "سعة 150 كجم إلى 220 كجم من البولي إيثيلين الغذائي • طوق إغلاق معدني محكم لإعادة التعبئة"),
        ("برطمانات زجاجية للتجزئة والسوبرماركت", "Retail Supermarket Glass Jars", "WhatsApp Image 2026-09-05 at 12.52.16 PM (4).jpeg", "أحجام 370، 500، 720 و 1000 مل • زجاج فائق النقاء مع أغطية أمان تويست أوف مفرغة من الهواء"),
        ("منصات شحن وحماية الرطوبة", "Palletization & Moisture Barrier", "WhatsApp Image 2026-09-05 at 12.52.15 PM (5).jpeg", "طبالي خشبية معالجة حرارياً ISPM-15 • تغليف استريتش آلي متعدد الطبقات وحواجز تجفيف")
    ]
    card_w4 = 430
    cx = 60
    for p_ar, p_en, img_p, p_sub in tiers:
        draw.rounded_rectangle([cx, y + 20, cx + card_w4, y + 680], radius=18, fill='#10221A', outline='#2D5232', width=2)
        if os.path.exists(img_p):
            p_img = Image.open(img_p).convert('RGB')
            p_img.thumbnail((card_w4 - 40, 260), Image.Resampling.LANCZOS)
            im.paste(p_img, (cx + int((card_w4 - p_img.width)/2), y + 35))
        draw.text((cx + card_w4 - 20, y + 325), p_ar, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((cx + 20, y + 375), p_en, font=f['h3_en'], fill='#FFFFFF', anchor='lt')
        draw.text((cx + card_w4 - 20, y + 430), p_sub, font=f['body_ar'], fill='#94A3B8', anchor='rt', direction='rtl')
        cx += card_w4 + 26

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 7: Private Label & OEM Landscape
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "حلول التصنيع للغير والعلامات التجارية الخاصة", "Private Label & Turnkey OEM Solutions", is_mobile=False)

    # Left: 6-stage workflow, Right: Photo & Dual Brand
    col_w_l = 1060
    stages = [
        ("1. التوريد الزراعي وانتقاء الأصناف", "Agro Sourcing: عقود توريد زراعي مباشر مع مزارع وادي النطرون وسيناء"),
        ("2. تطوير المحاليل الملحية المخصصة", "Brine Formulation: ضبط دقيق للملوحة والحموضة وإضافة البهارات العطرية"),
        ("3. التقطيع الدقيق وتخصيص الأحجام", "Calibrated Geometry: تقطيع شرائح 3.2 مم أو حبات كاملة أو مخلية"),
        ("4. المطابقة التنظيمية متعددة الأسواق", "Regulatory Compliance: مطابقة تشريعات FDA الأمريكية و EU FIC الأوروبية و GSO الخليجية"),
        ("5. التعبئة الأولية والتغليف الكرتوني", "Packaging & Labeling: طباعة علامات العملاء وتغليف كرتوني مقوى للشحن البحري"),
        ("6. الإفراج المخبري واللوجستيات", "QC & Dispatch: فحص مخبري شامل قبل الإفراج وإصدار شهادات التحليل الرسمية")
    ]
    sy = y + 20
    for s_t, s_d in stages:
        draw.rounded_rectangle([60, sy, col_w_l, sy + 95], radius=14, fill='#10221A', outline='#2D5232', width=1)
        draw.text((col_w_l - 20, sy + 16), s_t, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((col_w_l - 20, sy + 54), s_d, font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        sy += 112

    # Right: Photo & Dual Brand Strategy
    img_oem = "WhatsApp Image 2026-09-05 at 12.52.19 PM (1).jpeg"
    if os.path.exists(img_oem):
        oi = Image.open(img_oem).convert('RGB')
        oi.thumbnail((700, 360), Image.Resampling.LANCZOS)
        im.paste(oi, (1140, y + 20))

    draw.rounded_rectangle([1140, y + 400, W - 60, y + 680], radius=18, fill='#163024', outline='#D4A836', width=2)
    draw.text(((1140 + W - 60)/2, y + 435), "استراتيجية العلامة التجارية المزدوجة", font=f['h2_ar'], fill='#D4A836', anchor='mm', direction='rtl')
    draw.text(((1140 + W - 60)/2, y + 480), "Dual Brand Strategy: Khaeer Alwadi & Client OEM", font=f['h3_en'], fill='#FFFFFF', anchor='mm')
    draw.text(((1140 + W - 60)/2, y + 540), "• توريد بعلامة خير الوادي الرسمية جاهزة للتوزيع الفوري", font=f['body_ar'], fill='#E2E8F0', anchor='mm', direction='rtl')
    draw.text(((1140 + W - 60)/2, y + 590), "• تصنيع وتعبئة كاملة تحت العلامة التجارية الخاصة بالعميل (Private Label)", font=f['body_ar'], fill='#E2E8F0', anchor='mm', direction='rtl')

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 8: Technical Specs & Freight Matrix Landscape
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "مصفوفة المواصفات الفنية ولوجستيات الشحن", "Technical Specifications & Logistics Matrix", is_mobile=False)

    # Quality table
    draw.rounded_rectangle([60, y + 20, 1100, y + 680], radius=18, fill='#10221A', outline='#2D5232', width=2)
    draw.text((1060, y + 55), "مصفوفة المواصفات القياسية للجودة:", font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    
    specs = [
        ("زيتون مائدة كامل ومخلي", "وزن مصفى ≥ 52% | pH 3.8-4.2 | ملوحة 5-6% | عيوب < 1.0%"),
        ("زيتون مائدة شرائح 3.2 مم", "وزن مصفى ≥ 50% | سماكة 3.2 مم | تكسير < 1.5% | ملوحة 4.5-5.5%"),
        ("فلفل بيبرونشيني وفاخر", "وزن مصفى ≥ 52% | pH 3.2-3.6 | ملوحة 3.5-4.5% | قوام مقرمش"),
        ("طرشي بلدي وخيار مخلل", "وزن مصفى ≥ 50% | pH 3.3-3.7 | ملوحة 4.0-5.0% | بدون ألوان صناعية")
    ]
    ty = y + 120
    for sp_t, sp_d in specs:
        draw.rounded_rectangle([90, ty, 1070, ty + 105], radius=12, fill='#163024')
        draw.text((1040, ty + 20), sp_t, font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((1040, ty + 60), sp_d, font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        ty += 130

    # Freight calculations on right
    draw.rounded_rectangle([1140, y + 20, W - 60, y + 680], radius=18, fill='#0B261A', outline='#10B981', width=2)
    draw.text(((1140 + W - 60)/2, y + 55), "بيانات حمولة الحاويات البحرية (FCL Freight)", font=f['h2_ar'], fill='#10B981', anchor='mm', direction='rtl')
    draw.line([(1170, y + 95), (W - 90, y + 95)], fill='#2D5232', width=1)

    draw.text((W - 90, y + 140), "حاوية 20 قدم قياسية (20ft FCL):", font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    draw.text((W - 90, y + 190), "• سعة التحميل: 10 منصات خشبية مبخرة ISPM-15", font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
    draw.text((W - 90, y + 235), "• الوزن الصافي: 18 إلى 21 طن متري حسب نوع العبوة", font=f['body_ar'], fill='#E2E8F0', anchor='rt', direction='rtl')

    draw.text((W - 90, y + 330), "حاوية 40 قدم عالية السعة (40ft High Cube):", font=f['h3_ar'], fill='#D4A836', anchor='rt', direction='rtl')
    draw.text((W - 90, y + 380), "• سعة التحميل: 20 إلى 22 منصة خشبية قياسية", font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
    draw.text((W - 90, y + 425), "• الوزن الصافي: 24 إلى 26 طن متري (الحد الأقصى للسلامة)", font=f['body_ar'], fill='#E2E8F0', anchor='rt', direction='rtl')

    draw.rounded_rectangle([1170, y + 520, W - 90, y + 640], radius=14, fill='#10221A')
    draw.text(((1140 + W - 60)/2, y + 560), "حماية متقدمة ضد الرطوبة أثناء الشحن البحري", font=f['h3_ar'], fill='#FFFFFF', anchor='mm', direction='rtl')
    draw.text(((1140 + W - 60)/2, y + 600), "أعمدة امتصاص الرطوبة Desiccant Poles داخل كل حاوية", font=f['body_ar'], fill='#94A3B8', anchor='mm', direction='rtl')

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    # Slide 9: Commercial Desk & Direct Contact Landscape
    im = Image.new('RGB', (W, H), color='#091410')
    draw = ImageDraw.Draw(im)
    y = draw_header(im, draw, f, W, "مكتب الشراكات التجارية والتواصل المباشر", "Commercial Partnerships & Direct Line", is_mobile=False)

    # Left: 4 Onboarding Steps
    col_w_l = 980
    onboardings = [
        ("1. بروتوكول إرسال العينات السريعة", "Express Samples: شحن عينات جوية عبر DHL / FedEx خلال 48 ساعة"),
        ("2. عروض أسعار رسمية وتفصيلية خلال 24 ساعة", "Formal Quotation: تسعير فوري وشفاف بشروط FOB أو CIF لكافة الموانئ"),
        ("3. شروط دفع تجارية مرنة وموثوقة", "Payment Terms: اعتماد مستندي معزز وغير قابل للإلغاء L/C at sight أو T/T"),
        ("4. جدول زمني قياسي للتصنيع والشحن", "Rapid Laycan: جاهزية شحن وتعبئة قياسية خلال 10 إلى 14 يوماً فقط")
    ]
    oy = y + 20
    for o_t, o_d in onboardings:
        draw.rounded_rectangle([60, oy, col_w_l, oy + 125], radius=16, fill='#10221A', outline='#2D5232', width=1)
        draw.text((col_w_l - 20, oy + 25), o_t, font=f['h2_ar'], fill='#D4A836', anchor='rt', direction='rtl')
        draw.text((col_w_l - 20, oy + 75), o_d, font=f['body_ar'], fill='#FFFFFF', anchor='rt', direction='rtl')
        oy += 155

    # Right: Executive Contact Card
    draw.rounded_rectangle([1060, y + 20, W - 60, y + 680], radius=24, fill='#0B261A', outline='#10B981', width=3)
    cx_r = (1060 + W - 60) / 2
    
    if os.path.exists('khaeer-alwadi-logo.png'):
        logo = Image.open('khaeer-alwadi-logo.png').convert('RGBA')
        logo.thumbnail((320, 100), Image.Resampling.LANCZOS)
        im.paste(logo, (int(cx_r - logo.width/2), y + 55), logo)

    draw.text((cx_r, y + 190), "خير الوادي للصناعات الغذائية", font=f['title_ar'], fill='#D4A836', anchor='mm', direction='rtl')
    draw.text((cx_r, y + 245), "Khaeer Alwadi Food Industries", font=f['title_en'], fill='#FFFFFF', anchor='mm')
    draw.text((cx_r, y + 295), "المقر الرئيسي: القاهرة، جمهورية مصر العربية", font=f['h3_ar'], fill='#94A3B8', anchor='mm', direction='rtl')
    
    # WhatsApp Big Button
    draw.rounded_rectangle([1120, y + 360, W - 120, y + 470], radius=20, fill='#10B981')
    draw.text((cx_r, y + 395), "للتواصل المباشر والطلبات عبر واتساب:", font=f['h3_ar'], fill='#000000', anchor='mm', direction='rtl')
    draw.text((cx_r, y + 438), "+20 10 08716714", font=f['title_en'], fill='#000000', anchor='mm')

    draw.text((cx_r, y + 520), "رابط الدردشة الفوري: wa.me/201008716714", font=f['h3_en'], fill='#10B981', anchor='mm')
    draw.text((cx_r, y + 575), "الاعتمادات: ISO 22000 • HACCP • FDA Registered • Halal • ISO 9001", font=f['badge'], fill='#D4A836', anchor='mm')
    draw.text((cx_r, y + 625), "جاهزية فورية للتعاقد والتوريد لكافة الأسواق العالمية", font=f['body_ar'], fill='#E2E8F0', anchor='mm', direction='rtl')

    draw_footer_bar(im, draw, f, W, H, False)
    slides.append(im)

    return slides

def main():
    print("Building Mobile-Optimized Deck (1080x1920 portrait)...")
    mobile_slides = generate_mobile_slides()
    mobile_path = "Khaeer-Alwadi-Mobile-Deck.pdf"
    mobile_slides[0].save(mobile_path, save_all=True, append_images=mobile_slides[1:], resolution=150.0)
    print(f"Generated {mobile_path} successfully ({len(mobile_slides)} slides, size: {os.path.getsize(mobile_path)/1024:.1f} KB)")

    print("Building Widescreen Presentation Deck (1920x1080 landscape)...")
    pres_slides = generate_presentation_slides()
    pres_path = "Khaeer-Alwadi-Presentation-Deck.pdf"
    pres_slides[0].save(pres_path, save_all=True, append_images=pres_slides[1:], resolution=150.0)
    print(f"Generated {pres_path} successfully ({len(pres_slides)} slides, size: {os.path.getsize(pres_path)/1024:.1f} KB)")

    # Also symlink or copy to Khaeer-Alwadi-B2B-Deck.pdf
    b2b_path = "Khaeer-Alwadi-B2B-Deck.pdf"
    pres_slides[0].save(b2b_path, save_all=True, append_images=pres_slides[1:], resolution=150.0)
    print(f"Generated {b2b_path} successfully ({len(pres_slides)} slides, size: {os.path.getsize(b2b_path)/1024:.1f} KB)")

if __name__ == '__main__':
    main()
