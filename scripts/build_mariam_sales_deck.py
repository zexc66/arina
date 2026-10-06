import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FOREST_GREEN = (22, 38, 28)
DARK_CARD = (15, 27, 20)
GOLD_FOIL = (212, 175, 55)
WARM_IVORY = (234, 230, 223)
MUTED_TEXT = (165, 180, 170)
WHITE = (255, 255, 255)
ACCENT_GREEN = (46, 125, 50)

# Fonts setup
FONT_BOLD = "fonts/Tajawal-Bold.ttf" if os.path.exists("fonts/Tajawal-Bold.ttf") else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "fonts/Tajawal-Regular.ttf" if os.path.exists("fonts/Tajawal-Regular.ttf") else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

f_title = ImageFont.truetype(FONT_BOLD, 42)
f_h2 = ImageFont.truetype(FONT_BOLD, 28)
f_h3 = ImageFont.truetype(FONT_BOLD, 22)
f_body = ImageFont.truetype(FONT_REG, 17)
f_body_bold = ImageFont.truetype(FONT_BOLD, 17)
f_small = ImageFont.truetype(FONT_REG, 14)
f_badge = ImageFont.truetype(FONT_BOLD, 14)

def draw_slide_base(title, category):
    im = Image.new("RGB", (W, H), FOREST_GREEN)
    draw = ImageDraw.Draw(im)
    
    # Outer luxury frame
    draw.rectangle([25, 25, W - 25, H - 25], outline=GOLD_FOIL, width=2)
    draw.rectangle([35, 35, W - 35, H - 35], outline=(40, 70, 50), width=1)
    
    # Header zone
    draw.text((70, 50), "MARIAM", font=ImageFont.truetype(FONT_BOLD, 26), fill=GOLD_FOIL)
    draw.text((185, 54), "made with love", font=ImageFont.truetype(FONT_REG, 20), fill=WARM_IVORY)
    
    draw.text((W - 70, 52), title.upper(), font=f_h2, fill=WHITE, anchor="rt")
    draw.text((W - 70, 88), category.upper(), font=f_small, fill=GOLD_FOIL, anchor="rt")
    
    draw.line([(70, 120), (W - 70, 120)], fill=(50, 85, 60), width=1)
    
    # Footer zone
    y_foot = H - 55
    draw.line([(70, y_foot - 15), (W - 70, y_foot - 15)], fill=(50, 85, 60), width=1)
    draw.text((70, y_foot), "Mariam Mediterranean Gourmet Foods | International Export Division", font=f_small, fill=MUTED_TEXT)
    draw.text((W / 2, y_foot), "ISO 22000 • FSSC 22000 • FDA Registered • EU Organic • Halal • Kosher", font=f_badge, fill=GOLD_FOIL, anchor="mt")
    draw.text((W - 70, y_foot), "USA & Europe Expansion Deck 2026", font=f_small, fill=MUTED_TEXT, anchor="rt")
    
    return im, draw

def add_image_card(im, draw, img_path, box, corner_radius=16):
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x + w, y + h], radius=corner_radius, fill=DARK_CARD, outline=GOLD_FOIL, width=2)
    if os.path.exists(img_path):
        sub_im = Image.open(img_path).convert("RGB")
        # Aspect fit / crop
        sub_ratio = sub_im.width / sub_im.height
        box_ratio = (w - 12) / (h - 12)
        if sub_ratio > box_ratio:
            new_h = h - 12
            new_w = int(new_h * sub_ratio)
        else:
            new_w = w - 12
            new_h = int(new_w / sub_ratio)
        
        resized = sub_im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        # Center crop
        cx = (new_w - (w - 12)) // 2
        cy = (new_h - (h - 12)) // 2
        cropped = resized.crop((cx, cy, cx + w - 12, cy + h - 12))
        im.paste(cropped, (x + 6, y + 6))

slides = []

# ==================== SLIDE 1: COVER ====================
s1 = Image.new("RGB", (W, H), FOREST_GREEN)
d1 = ImageDraw.Draw(s1)
d1.rectangle([30, 30, W - 30, H - 30], outline=GOLD_FOIL, width=3)
d1.rectangle([45, 45, W - 45, H - 45], outline=(50, 90, 65), width=1)

# Cover Image left
add_image_card(s1, d1, "output/imagery/mariam_packaging_mockup_4k.jpg", (80, 160, 950, 750), 20)

# Right Text Block
rx = 1080
d1.text((rx, 220), "INTERNATIONAL B2B SALES DECK", font=f_small, fill=GOLD_FOIL)
d1.text((rx, 260), "MARIAM", font=ImageFont.truetype(FONT_BOLD, 64), fill=GOLD_FOIL)
d1.text((rx + 290, 292), "made with love", font=ImageFont.truetype(FONT_REG, 32), fill=WARM_IVORY)
d1.line([(rx, 355), (W - 80, 355)], fill=GOLD_FOIL, width=2)

d1.text((rx, 385), "Disrupting the $22B Olive Category", font=ImageFont.truetype(FONT_BOLD, 32), fill=WHITE)
d1.text((rx, 430), "in the USA & Europe", font=ImageFont.truetype(FONT_BOLD, 32), fill=GOLD_FOIL)

pitch_bullets = [
    "• Super-Premium Mediterranean Gourmet House with Mass Scalability",
    "• Clean Label: 100% Natural Sea Salt Brine, Zero Chemical Additives",
    "• High-Velocity Shelf Magnetism: 3D Gold Foil on Forest Green",
    "• Category-Leading Retailer Gross Margins: 46% to 55%",
    "• Full Regulatory Compliance: FDA Registered, FSMA, EU 1169/2011",
    "• Turnkey Logistics: 24–36 Mo Ambient Shelf Life, DDP / CIF Shipping",
]
y_cur = 490
for b in pitch_bullets:
    d1.text((rx, y_cur), b, font=f_body, fill=WARM_IVORY)
    y_cur += 42

# Badges box bottom right
d1.rounded_rectangle([rx, y_cur + 20, W - 80, y_cur + 110], radius=12, fill=DARK_CARD, outline=GOLD_FOIL, width=1)
d1.text((rx + 20, y_cur + 35), "READY FOR IMMEDIATE RETAIL ONBOARDING & SAMPLING", font=f_badge, fill=GOLD_FOIL)
d1.text((rx + 20, y_cur + 65), "Targets: Whole Foods, Wegmans, Eataly, Harrods, Marks & Spencer", font=f_small, fill=MUTED_TEXT)
slides.append(s1)

# ==================== SLIDE 2: THE MARKET OPPORTUNITY ====================
s2, d2 = draw_slide_base("The Market Opportunity", "Why Olive Aisles Are Ripe for Disruption")

# Left Column: Problem & Solution
d2.rounded_rectangle([70, 150, 850, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d2.text((100, 180), "THE RETAIL DILEMMA", font=f_h2, fill=GOLD_FOIL)

problems = [
    ("Commoditized Shelf Space", "Dominated by legacy industrial canned brands designed in the 1980s with zero emotional connection."),
    ("Artificial Color & Firming", "Conventional black olives are chemically blackened with ferrous gluconate and soaked in synthetic preservatives."),
    ("The Missing Middle Ground", "Consumers are forced to choose between boring $2.50 supermarket cans or $18 boutique imports.")
]
y_p = 230
for title, desc in problems:
    d2.text((100, y_p), f"❌  {title}", font=f_body_bold, fill=WHITE)
    d2.text((100, y_p + 28), desc, font=f_small, fill=MUTED_TEXT)
    y_p += 75

d2.line([(100, y_p + 10), (820, y_p + 10)], fill=(50, 85, 60), width=1)
y_p += 30

d2.text((100, y_p), "THE MARIAM SOLUTION: ACCESSIBLE LUXURY", font=f_h2, fill=GOLD_FOIL)
solutions = [
    ("Michelin Quality at $4.99–$6.99 SRP", "Delivers luxury aesthetics, fresh natural crunch, and estate-cured terroir at accessible price points."),
    ("100% Clean Label Transparency", "Only 4 natural ingredients: hand-picked olives, spring water, sea salt, extra virgin olive oil. Non-GMO, Vegan, Keto."),
    ("Charcuterie & Tapas Ready", "Engineered to sit directly on holiday grazing tables, pizza counters, and home cocktail bars.")
]
y_p += 50
for title, desc in solutions:
    d2.text((100, y_p), f"✅  {title}", font=f_body_bold, fill=GOLD_FOIL)
    d2.text((100, y_p + 28), desc, font=f_small, fill=WARM_IVORY)
    y_p += 75

# Right Column Image
add_image_card(s2, d2, "output/imagery/mariam_collection_campaign_4k.jpg", (880, 150, 970, 820), 16)
slides.append(s2)

# ==================== SLIDE 3: CORE TABLE OLIVES ====================
s3, d3 = draw_slide_base("Core Table Olives", "High-Velocity Staples | Whole, Sliced, Pitted & Kalamata")

add_image_card(s3, d3, "output/imagery/mariam_green_olives_4k.jpg", (70, 150, 750, 820), 16)

# Right Specs Column
d3.rounded_rectangle([850, 150, 1850, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d3.text((880, 180), "CORE TABLE OLIVE LINE SPECIFICATIONS", font=f_h2, fill=GOLD_FOIL)

skus = [
    ("Whole Green Olives (370g & 700g)", "Crisp Mediterranean table olives in sea-salt spring brine. Case pack: 12 / 6 units. 36 Mo shelf life."),
    ("Sliced Green Olive Rings (370g)", "Perfect uniform circular rings with clean pitted centers for pizzas, salads, and focaccias. Case pack: 12."),
    ("Pitted Green Olives (370g)", "Convenient, whole unblemished pitted olives for warm culinary dishes and dirty martinis. Case pack: 12."),
    ("Royal Kalamata Olives (370g)", "Naturally tree-ripened deep purple Greek-style Kalamatas in red wine vinegar & EVOO. Matte-black lid. Case: 12."),
    ("Natural Black Olives (370g)", "Naturally aged on the bough, zero ferrous gluconate artificial dye. Rich, mellow, tender texture. Case: 12.")
]
y_s = 240
for title, desc in skus:
    d3.text((880, y_s), f"• {title}", font=f_body_bold, fill=WHITE)
    d3.text((895, y_s + 26), desc, font=f_small, fill=WARM_IVORY)
    y_s += 68

d3.line([(880, y_s + 10), (1820, y_s + 10)], fill=(50, 85, 60), width=1)
y_s += 30

d3.text((880, y_s), "RETAILER COMMERCIAL ADVANTAGES:", font=f_h3, fill=GOLD_FOIL)
y_s += 38
d3.text((880, y_s), "1. Landed Cost: $2.60–$3.10  |  SRP: $4.99–$5.99  |  Gross Margin: 47%–48%", font=f_body_bold, fill=WHITE)
y_s += 32
d3.text((880, y_s), "2. Low Shrink: Long 36-month ambient shelf life with hermetic vacuum seals.", font=f_body, fill=MUTED_TEXT)
y_s += 28
d3.text((880, y_s), "3. High Repeat Basket Velocity: Versatile across snacking, cooking, and cocktail garnishes.", font=f_body, fill=MUTED_TEXT)

slides.append(s3)

# ==================== SLIDE 4: STUFFED & SPECIALTY OLIVES ====================
s4, d4 = draw_slide_base("Artisan Hand-Stuffed Line", "Gourmet Charcuterie Favorites | Almond, Garlic & Piquillo")

add_image_card(s4, d4, "output/imagery/mariam_kalamata_stuffed_collection_4k.jpg", (70, 150, 780, 820), 16)

# Right Details
d4.rounded_rectangle([880, 150, 1850, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d4.text((910, 180), "HAND-STUFFED ARTISAN PORTFOLIO", font=f_h2, fill=GOLD_FOIL)

stuffed_items = [
    ("Toasted Spanish Almond Stuffed", "Large green olives stuffed by hand with crunchy, golden toasted whole almonds. The undisputed #1 charcuterie board bestseller. SRP: $6.99 | Margin: 48.5%"),
    ("Slow-Roasted Garlic Clove Stuffed", "Stuffed with sweet, mellow caramelized garlic cloves and wild oregano. Pairs exceptionally with antipasto platters and dry red wines. SRP: $6.49 | Margin: 46.1%"),
    ("Piquillo Chili & Sweet Pepper Stuffed", "Tangy, mildly smoky roasted sweet peppers hand-stuffed for a vibrant color and zesty flavor contrast. SRP: $6.49 | Margin: 46.1%"),
    ("Preserved Mediterranean Lemon Stuffed", "Sun-ripened salted lemon rind offering bright citrus notes. Essential for seafood pairings and tagines. SRP: $6.49 | Margin: 46.1%")
]
y_st = 240
for title, desc in stuffed_items:
    d4.text((910, y_st), f"★ {title}", font=f_body_bold, fill=WHITE)
    d4.text((925, y_st + 26), desc, font=f_small, fill=WARM_IVORY)
    y_st += 80

d4.line([(910, y_st + 10), (1820, y_st + 10)], fill=(50, 85, 60), width=1)
y_st += 35

d4.text((910, y_st), "THE CHARCUTERIE MERCHANDISING ADVANTAGE", font=f_h3, fill=GOLD_FOIL)
y_st += 38
d4.text((910, y_st), "Place directly in specialty cheese aisles and wine counters to capture lucrative secondary sales.", font=f_body, fill=WHITE)
y_st += 30
d4.text((910, y_st), "Stuffed olives carry 35% higher average basket value than plain table olives.", font=f_body_bold, fill=GOLD_FOIL)
slides.append(s4)

# ==================== SLIDE 5: EVOO & AIR-SPRAY ====================
s5, d5 = draw_slide_base("Single-Estate EVOO & Sprays", "First Cold-Harvest Oils & Pure Bag-on-Valve Culinary Spray")

add_image_card(s5, d5, "output/imagery/mariam_evoo_and_spray_4k.jpg", (70, 150, 780, 820), 16)

# Right Column
d5.rounded_rectangle([880, 150, 1850, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d5.text((910, 180), "LIQUID GOLD: SINGLE-ESTATE OLIVE OIL", font=f_h2, fill=GOLD_FOIL)

evoo_items = [
    ("First Harvest Grand Reserve EVOO (500ml)", "Milled within 4 hours of picking. Acidity < 0.25%, Polyphenols > 450 mg/kg. Bottled in opaque dark-green glass with gold wax seal to block 99% UV light. Landed: $8.90 | SRP: $16.99 | Margin: 47.6%"),
    ("Everyday Gourmet EVOO (750ml & 1L)", "Smooth, buttery, balanced finishing and everyday cooking oil in transparent flint glass bottle. Landed: $6.80 | SRP: $12.99 | Margin: 47.7%"),
    ("EVOO Culinary Air-Spray (200ml)", "Revolutionary Bag-on-Valve aerosol system. 100% pure oil with zero propellants or gases. Huge demand among air-fryer users, keto diets, and portion-controlled cooking. Landed: $4.20 | SRP: $7.99 | Margin: 47.4%"),
    ("Black Summer Truffle & Infused Oils (250ml)", "Cold-infused with real Italian black summer truffle, wild rosemary, or fresh lemon peel. SRP: $11.99 | Margin: 48.0%")
]
y_ev = 240
for title, desc in evoo_items:
    d5.text((910, y_ev), f"◆ {title}", font=f_body_bold, fill=WHITE)
    d5.text((925, y_ev + 26), desc, font=f_small, fill=WARM_IVORY)
    y_ev += 85

slides.append(s5)

# ==================== SLIDE 6: TAPENADES & CONDIMENTS ====================
s6, d6 = draw_slide_base("Tapenades & Gourmet Condiments", "Artisan Spreads, Aged Modena Balsamic & Smoked Sea Salt")

add_image_card(s6, d6, "output/imagery/mariam_tapenades_and_condiments_4k.jpg", (70, 150, 780, 820), 16)

# Right Column
d6.rounded_rectangle([880, 150, 1850, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d6.text((910, 180), "MEDITERRANEAN PANTRY SUITE", font=f_h2, fill=GOLD_FOIL)

cond_items = [
    ("Rustic Green Olive Tapenade (190g)", "Coarsely crushed green olives with capers, garlic, and cold-pressed extra virgin olive oil. Landed: $2.80 | SRP: $5.49 | Margin: 49.0%"),
    ("Black Kalamata Olive Pâté (190g)", "Deep, velvety spread of Kalamata olives, balsamic glaze, and fresh wild thyme. Landed: $2.85 | SRP: $5.49 | Margin: 48.1%"),
    ("Marinated Roman Artichoke Hearts (280g)", "Tender artichoke quarters preserved in herb-infused olive oil. Landed: $3.80 | SRP: $7.29 | Margin: 47.9%"),
    ("Aged Modena Balsamic Vinegar Glaze (250ml)", "Slender glass bottle with gold foil neck. Dense, syrupy IGP Modena reduction. Landed: $4.50 | SRP: $8.99 | Margin: 49.9%"),
    ("Smoked Olive Leaf Finishing Sea Salt (120g)", "Crystalline flaked sea salt cold-smoked over olive wood cuttings. Landed: $2.60 | SRP: $5.29 | Margin: 50.9%")
]
y_cn = 240
for title, desc in cond_items:
    d6.text((910, y_cn), f"▪ {title}", font=f_body_bold, fill=WHITE)
    d6.text((925, y_cn + 26), desc, font=f_small, fill=WARM_IVORY)
    y_cn += 72

slides.append(s6)

# ==================== SLIDE 7: POUCHES & GIFT VAULT ====================
s7, d7 = draw_slide_base("On-the-Go Pouches & Gift Vault", "Impulse Checkout Snacks & Luxury Holiday Gifting Chests")

add_image_card(s7, d7, "output/imagery/mariam_pouches_and_gift_vault_4k.jpg", (70, 150, 780, 820), 16)

# Right Column
d7.rounded_rectangle([880, 150, 1850, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d7.text((910, 180), "HIGH-MARGIN CATEGORY INNOVATIONS", font=f_h2, fill=GOLD_FOIL)

d7.text((910, 240), "1. LIQUID-FREE OLIVE SNACK POUCHES (50g DOYPACK)", font=f_h3, fill=GOLD_FOIL)
pouch_details = [
    "• Pitted Green Olives with Wild Thyme & Lemon  |  Pitted Kalamata with Chili & Herbs",
    "• 100% Mess-Free: Zero liquid brine spills. Moist-marinated in cold-pressed oil.",
    "• Retail Channels: Checkout lanes, airline first class, airport delis, and gym nutrition bars.",
    "• Landed Cost: $1.10  |  SRP: $2.49  |  Retailer Gross Margin: 55.8%"
]
y_p = 275
for line in pouch_details:
    d7.text((930, y_p), line, font=f_small, fill=WARM_IVORY)
    y_p += 28

d7.line([(910, y_p + 15), (1820, y_p + 15)], fill=(50, 85, 60), width=1)
y_p += 35

d7.text((910, y_p), "2. THE CONNOISSEUR HEIRLOOM GIFT CHEST", font=f_h3, fill=GOLD_FOIL)
vault_details = [
    "• Handcrafted solid olive-wood presentation chest with emerald green velvet interior.",
    "• Includes: 500ml Grand Reserve EVOO, 2 Reserve Olive Jars, and 3 gold-plated tasting picks.",
    "• Q4 Holiday Anchor: Perfect for corporate gifting, luxury department store holiday catalogs.",
    "• Landed Cost: $38.00  |  SRP: $85.00  |  Retailer Gross Margin: 55.3%"
]
y_p += 35
for line in vault_details:
    d7.text((930, y_p), line, font=f_small, fill=WARM_IVORY)
    y_p += 28

slides.append(s7)

# ==================== SLIDE 8: ECONOMICS & SUPPLY CHAIN ====================
s8, d8 = draw_slide_base("Economics & Global Supply Chain", "Frictionless Import Logistics & High-Margin Unit Economics")

# Left Column: Table of Economics
d8.rounded_rectangle([70, 150, 950, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d8.text((100, 180), "UNIT ECONOMICS & MARGIN ARCHITECTURE", font=f_h2, fill=GOLD_FOIL)

headers = ["Product Line", "Case", "Landed", "US SRP", "EU SRP", "Margin"]
d8.text((100, 230), f"{headers[0]:<28} {headers[1]:<6} {headers[2]:<8} {headers[3]:<9} {headers[4]:<9} {headers[5]}", font=f_body_bold, fill=GOLD_FOIL)
d8.line([(100, 260), (920, 260)], fill=(50, 85, 60), width=1)

rows = [
    ("Whole Green Olives (370g)", "12", "$2.60", "$4.99", "€4.49", "47.9%"),
    ("Sliced Green Olive Rings (370g)", "12", "$2.65", "$4.99", "€4.49", "46.9%"),
    ("Pitted Green Olives (370g)", "12", "$2.75", "$5.29", "€4.79", "48.0%"),
    ("Royal Kalamata Olives (370g)", "12", "$3.10", "$5.99", "€5.49", "48.2%"),
    ("Almond Stuffed Olives (370g)", "12", "$3.60", "$6.99", "€6.29", "48.5%"),
    ("First Harvest EVOO (500ml)", "6", "$8.90", "$16.99", "€14.99", "47.6%"),
    ("Everyday Gourmet EVOO (750ml)", "6", "$6.80", "$12.99", "€11.49", "47.7%"),
    ("EVOO Culinary Air-Spray (200ml)", "12", "$4.20", "$7.99", "€7.29", "47.4%"),
    ("Rustic Green Tapenade (190g)", "12", "$2.80", "$5.49", "€4.99", "49.0%"),
    ("To-Go Snack Pouch (50g)", "24", "$1.10", "$2.49", "€2.19", "55.8%"),
    ("Connoisseur Gift Chest", "1", "$38.00", "$85.00", "€79.00", "55.3%")
]
y_r = 275
for r in rows:
    d8.text((100, y_r), f"{r[0]:<28} {r[1]:<6} {r[2]:<8} {r[3]:<9} {r[4]:<9} {r[5]}", font=f_body, fill=WHITE)
    y_r += 32

# Right Column: Supply Chain & Certifications
d8.rounded_rectangle([980, 150, 1850, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d8.text((1010, 180), "WESTERN COMPLIANCE & LOGISTICS", font=f_h2, fill=GOLD_FOIL)

logistics_points = [
    ("FDA & FSMA Registered", "Full compliance with US Food Safety Modernization Act and Foreign Supplier Verification Program (FSVP)."),
    ("EU FIC 1169/2011 Standard", "All nutrition panels, net weights, allergens, and multi-lingual ingredient decks calibrated for European borders."),
    ("Container Efficiency", "20ft FCL: 11 EUR/US Pallets (18,000 jars / 1,500 cases).\n40ft High Cube: 25 Pallets (38,000 jars / 3,200 cases)."),
    ("Shipping Terms Available", "FOB Mediterranean Port, DDP / CIF to US East/West Coast (NY/Newark, Long Beach), CIF Rotterdam/Hamburg/Genoa."),
    ("GFSI Certifications", "FSSC 22000, ISO 22000, HACCP, Halal, Kosher, Non-GMO Verified, USDA/EU Organic certified batches."),
    ("Lead Times", "14 to 21 business days from PO confirmation to port loading.")
]
y_l = 230
for title, desc in logistics_points:
    d8.text((1010, y_l), f"✔ {title}", font=f_body_bold, fill=GOLD_FOIL)
    d8.text((1030, y_l + 24), desc, font=f_small, fill=WARM_IVORY)
    y_l += 68

slides.append(s8)

# ==================== SLIDE 9: RETAIL PARTNERSHIP PROGRAM ====================
s9, d9 = draw_slide_base("Retail Partnership Program", "Frictionless Onboarding & Sell-Through Velocity Guarantee")

# Left Column: Sell-Through Support
d9.rounded_rectangle([70, 150, 950, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d9.text((100, 180), "HOW WE DRIVE SELL-THROUGH VELOCITY", font=f_h2, fill=GOLD_FOIL)

support_items = [
    ("Co-Op Advertising Allowance", "Up to 5% of net invoice credited toward retailer circulars, end-cap feature displays, and loyalty app promotions."),
    ("Turnkey Merchandising Shippers", "Pre-packed 96-unit corrugated floor displays featuring the Top 3 best-sellers ready for instant retail deployment."),
    ("Geo-Targeted Social Advertising", "Meta & TikTok digital campaigns geotargeted within 5 miles of stocking retail locations driving verified shopper traffic."),
    ("Smart QR Farm-to-Table Engagement", "Every jar connects consumers to live grove maps, polyphenol lab tests, and Michelin-star chef recipe pairings.")
]
y_sp = 240
for title, desc in support_items:
    d9.text((100, y_sp), f"★ {title}", font=f_body_bold, fill=WHITE)
    d9.text((115, y_sp + 26), desc, font=f_small, fill=WARM_IVORY)
    y_sp += 75

# Right Column: Pilot Offer
d9.rounded_rectangle([980, 150, 1850, 970], radius=16, fill=DARK_CARD, outline=(50, 85, 60), width=1)
d9.text((1010, 180), "THE LOW-RISK PILOT TRIAL PROGRAM", font=f_h2, fill=GOLD_FOIL)

pilot_steps = [
    ("1. Low Barrier Pilot Order", "Test Mariam in a 3-Pallet regional store cluster or mixed test container before committing to chain-wide rollout."),
    ("2. Proven Bestseller Starter SKU Mix", "40% Whole Green Olives (370g)\n25% Royal Kalamata Olives (370g)\n20% Sliced Green Olive Rings (370g)\n15% Toasted Almond Stuffed Olives (370g)"),
    ("3. Zero-Risk Breakage Guarantee", "100% instant credit replacement policy for any transit handling damage."),
    ("4. Free Weekend Tasting Kits", "2 free demo cases included per store for weekend sampling and staff tasting education.")
]
y_pi = 240
for title, desc in pilot_steps:
    d9.text((1010, y_pi), title, font=f_body_bold, fill=GOLD_FOIL)
    d9.text((1025, y_pi + 26), desc, font=f_small, fill=WARM_IVORY)
    y_pi += 72

d9.line([(1010, y_pi + 10), (1820, y_pi + 10)], fill=GOLD_FOIL, width=2)
y_pi += 30

d9.text((1010, y_pi), "READY TO ALLOCATE TEST CONTAINERS & TASTING KITS", font=f_h3, fill=WHITE)
y_pi += 32
d9.text((1010, y_pi), "Contact US & European Export Desk | Inquire for Immediate Container Slot Allocation", font=f_small, fill=MUTED_TEXT)

slides.append(s9)

# Save Master PDF
pdf_path = "/home/zexc/Desktop/New Folder/Mariam-Luxury-Sales-Pitch-USA-EU.pdf"
slides[0].save(pdf_path, "PDF", resolution=150.0, save_all=True, append_images=slides[1:])
print(f"Master B2B Sales Pitch Deck PDF successfully compiled: {pdf_path} ({len(slides)} slides)")
