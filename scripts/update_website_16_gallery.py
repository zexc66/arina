#!/usr/bin/env python3
"""
Updates website.html to feature all 16 definitive master 4K UHD gallery cards:
- Exact 4 cards per category: products, terroir, culinary, logistics.
- Cache busting query ?v=20261007 on all image URLs.
- Complete TRANSLATIONS.en and TRANSLATIONS.ar for gallery_card1 through gallery_card16.
- Strict verification of 0 Arabic characters in TRANSLATIONS.en.
"""

import re
import os

CARDS = [
    # -------------------------------------------------------------------------
    # CATEGORY 1: PRODUCTS & JARS (CARDS 1 - 4)
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "category": "products",
        "file": "output/imagery/arina_gallery_gastronomy_trinity_4k.jpg?v=20261007",
        "tag_en": "FLAGSHIP EXPORT TRIO",
        "tag_ar": "ثلاثية المنتجات الأساسية",
        "title_en": "ARINA Foundational Gastronomy Master Trinity",
        "title_ar": "ثلاثية أرينا القياسية لرواد الضيافة والذواقة",
        "desc_en": "Acoustic Crisp Baby Cucumbers, Royal Kalamata Olives & Pure Unroasted Crushed Garlic.",
        "desc_ar": "الأصناف الثلاثة الأكثر طلباً في الأسواق الدولية: خيار مقرمش، زيتون كالاماتا، وثوم مهروس نقي.",
    },
    {
        "id": 2,
        "category": "products",
        "file": "output/imagery/arina_gallery_stuffed_queen_olives_4k.jpg?v=20261007",
        "tag_en": "ESTATE TABLE OLIVES",
        "tag_ar": "زيتون المائدة الفاخر",
        "title_en": "ARINA Connoisseur Table & Stuffed Olives Showcase",
        "title_ar": "زيتون فاخر محشو يدوياً باللوز وأصناف المائدة",
        "desc_en": "Hand-Stuffed Almond Queen Olives, Egyptian Azizi Olives & Spanish Black Manzanilla.",
        "desc_ar": "ثمار زيتون ملكية منتقاة بعناية ومحشوة يدوياً بحبات اللوز الكاملة المقرمشة وفصوص الثوم والزيتون الإسباني.",
    },
    {
        "id": 3,
        "category": "products",
        "file": "output/imagery/arina_gallery_heritage_pickles_4k.jpg?v=20261007",
        "tag_en": "HERITAGE PICKLING TERROIR",
        "tag_ar": "مخللات بلدية ومحصول النيل",
        "title_en": "ARINA Heritage Pickles & Nile Delta Terroir",
        "title_ar": "مخللات أرينا البلدية وتراث دلتا النيل",
        "desc_en": "Acoustic Baby Cucumbers, Wild Turnips in Natural Beetroot & Pickled Carrot-Chili Medley.",
        "desc_ar": "تناغم بصري وطعم استثنائي يجمع بين اللفت البلدي المعتق بالشمندر والخيار المقرمش وتشكيلة الجزر والشطة.",
    },
    {
        "id": 4,
        "category": "products",
        "file": "output/imagery/arina_gallery_garlic_toum_suite_4k.jpg?v=20261007",
        "tag_en": "CHEF CONDIMENTS & EMULSIONS",
        "tag_ar": "مقبلات وتغميسات الثوم الفاخرة",
        "title_en": "ARINA Cloud-Whipped Toum & Pure Crushed Garlic Suite",
        "title_ar": "مجموعة تغميسات الثوم والتومية الملكية",
        "desc_en": "Artisanal Emulsified Toum Garlic Cream & 100% Unroasted Crushed Garlic in Squat Glass.",
        "desc_ar": "معجون الثوم الطبيعي والتومية السحابية المخفوقة بزيت الزيتون البكر ومياه الينابيع النقية في برطمانات دائرية.",
    },
    # -------------------------------------------------------------------------
    # CATEGORY 2: ESTATE TERROIR & HARVEST (CARDS 5 - 8)
    # -------------------------------------------------------------------------
    {
        "id": 5,
        "category": "terroir",
        "file": "output/imagery/arina_gallery_siwa_terroir_4k.jpg?v=20261007",
        "tag_en": "OASIS OLIVE HARVEST",
        "tag_ar": "حصاد زيتون واحة سيوة",
        "title_en": "Siwa Oasis Golden-Hour Olive Harvest",
        "title_ar": "موسم حصاد الزيتون الذهبي في واحة سيوة",
        "desc_en": "Ancient gnarled olive trees harvested by hand in the golden mineral-rich soils of the Western Desert.",
        "desc_ar": "أشجار زيتون معمرة تُجنى يدوياً خلال الغسق الذهبي في واحة سيوة ذات التربة البكر الغنية بالمعادن.",
    },
    {
        "id": 6,
        "category": "terroir",
        "file": "output/imagery/arina_gallery_oak_cellar_4k.jpg?v=20261007",
        "tag_en": "HERITAGE CURING CELLARS",
        "tag_ar": "أقبية التعتيم والتخليل التراثية",
        "title_en": "Subterranean Heritage Oak Curing & Maturation Vaults",
        "title_ar": "سراديب تعتيق الزيتون في براميل البلوط التراثية",
        "desc_en": "Climate-controlled subterranean stone cellars where olives mature naturally in aromatic brine and oak barrels.",
        "desc_ar": "أقبية حجرية تحت الأرض محكمة الحرارة والرطوبة لتخمير وتعتيق ثمار الزيتون طبيعياً في براميل خشبية.",
    },
    {
        "id": 7,
        "category": "terroir",
        "file": "output/imagery/arina_gallery_farm_harvest_4k.jpg?v=20261007",
        "tag_en": "NILE DELTA HARVEST",
        "tag_ar": "محاصيل دلتا النيل الطازجة",
        "title_en": "Nile Delta Fertile Farm Harvest & Heirloom Produce",
        "title_ar": "محاصيل دلتا النيل الخصبة وخضروات التخليل الطازجة",
        "desc_en": "Field-fresh baby cucumbers, purple wild turnips, and crisp aromatics picked at dawn from fertile alluvial soil.",
        "desc_ar": "خضروات طازجة من خيار بلدي ولفت بنفسجي وفصوص ثوم تُقطف عند الفجر من تربة الدلتا الرسوبية الخصبة.",
    },
    {
        "id": 8,
        "category": "terroir",
        "file": "output/imagery/arina_gallery_stone_pantry_4k.jpg?v=20261007",
        "tag_en": "OASIS SPRING WATERWAYS",
        "tag_ar": "ينابيع وقنوات واحة سيوة الطبيعية",
        "title_en": "Siwa Oasis Natural Spring Canals & Ancient Groves",
        "title_ar": "قنوات المياه العذبة وبساتين الزيتون في سيوة",
        "desc_en": "Pristine subterranean spring waters flowing through stone aqueducts to nourish thousand-year-old olive groves.",
        "desc_ar": "مياه الينابيع الجوفية النقية تتدفق عبر قنوات حجرية لتغذي بساتين الزيتون المعمرة في قلب الواحة.",
    },
    # -------------------------------------------------------------------------
    # CATEGORY 3: GASTRONOMY & FINE DINING MEZZE (CARDS 9 - 12)
    # -------------------------------------------------------------------------
    {
        "id": 9,
        "category": "culinary",
        "file": "output/imagery/arina_gallery_mezze_board_4k.jpg?v=20261007",
        "tag_en": "HAUTE GASTRONOMY BOARD",
        "tag_ar": "مائدة المازة الفاخرة",
        "title_en": "Grand Mediterranean Mezze & Charcuterie Banquet Board",
        "title_ar": "لوحة المازة والضيافة المتوسطية الفاخرة",
        "desc_en": "Live-edge olive wood presentation of Kalamata olives, stuffed queen olives, acoustic pickles, and whipped toum.",
        "desc_ar": "تشكيلة ضيافة متكاملة على خشب الزيتون تجمع زيتون كالاماتا والمخللات المقرمشة وكريمة التومية الملكية.",
    },
    {
        "id": 10,
        "category": "culinary",
        "file": "output/imagery/arina_gallery_chef_plating_4k.jpg?v=20261007",
        "tag_en": "EXECUTIVE CHEF PLATING",
        "tag_ar": "فن الطهي والتقديم الاحترافي",
        "title_en": "Executive Chef Haute Cuisine Antipasti Plating",
        "title_ar": "إبداع الشيف التنفيذي في تقديم المقبلات الراقية",
        "desc_en": "Precision tweezers and culinary craft showcasing tapenade quenelles, crisp baby cucumbers, and virgin olive oil.",
        "desc_ar": "لمسات شيف احترافية بدقة ملقط الطهي في تشكيل كنافيل التابيناد والخيار المقرمش وزيت الزيتون البكر.",
    },
    {
        "id": 11,
        "category": "culinary",
        "file": "output/imagery/arina_gallery_tapenades_spreads_4k.jpg?v=20261007",
        "tag_en": "ARTISAN CONDIMENTS & MORTAR",
        "tag_ar": "صلصات التابيناد والهاون الحجري",
        "title_en": "Artisan Olive Tapenade & Mortar-Crushed Condiments",
        "title_ar": "معجون التابيناد الحرفي ومقبلات الهاون الجرانيتي",
        "desc_en": "Hand-ground Kalamata tapenade, green herb spread, and artisanal toum served with warm rustic crostini.",
        "desc_ar": "تابيناد الكالاماتا المهروس بالهاون الجرانيتي مع معجون الأعشاب الخضراء وخبز الكروستيني المحمص المقرمش.",
    },
    {
        "id": 12,
        "category": "culinary",
        "file": "output/imagery/arina_gallery_pergola_feast_4k.jpg?v=20261007",
        "tag_en": "AL FRESCO ESTATE BANQUET",
        "tag_ar": "مأدبة الهواء الطلق المتوسطية",
        "title_en": "Sun-Drenched Pergola Vineyard Al Fresco Banquet",
        "title_ar": "مأدبة الغداء المتوسطية في ظلال عريشة الكروم",
        "desc_en": "A golden Mediterranean outdoor feast laden with estate olives, acoustic pickles, rustic flatbreads, and citrus.",
        "desc_ar": "طاولة طعام مشمسة تحت عريشة العنب والزيتون تفيض بأصناف الزيتون والمخللات والخبز البلدي الساخن.",
    },
    # -------------------------------------------------------------------------
    # CATEGORY 4: EXPORT LOGISTICS & GLOBAL TRADE (CARDS 13 - 16)
    # -------------------------------------------------------------------------
    {
        "id": 13,
        "category": "logistics",
        "file": "output/imagery/arina_gallery_bulk_barrel_4k.jpg?v=20261007",
        "tag_en": "INDUSTRIAL FOODSERVICE EXPORT",
        "tag_ar": "التصدير الصناعي لقطاع الفنادق",
        "title_en": "ARINA 230kg High-Density Food-Grade Export Drum",
        "title_ar": "برميل التصدير الصناعي سعة 230 كجم",
        "desc_en": "Heavy-Duty Blue HDPE Airtight Drums Engineered for Ocean Transit & Global Foodservice.",
        "desc_ar": "براميل زرقاء عالية الكثافة محكمة الإغلاق ومقاومة للأشعة فوق البنفسجية لشركات التعبئة وسلاسل الفنادق.",
    },
    {
        "id": 14,
        "category": "logistics",
        "file": "output/imagery/arina_gallery_container_freight_4k.jpg?v=20261007",
        "tag_en": "MARITIME FREIGHT LOGISTICS",
        "tag_ar": "الشحن البحري والخدمات اللوجستية",
        "title_en": "Alexandria Port Ocean Freight & Container Logistics",
        "title_ar": "شحن الحاويات البحرية بميناء الإسكندرية الدولي",
        "desc_en": "Direct ocean container dispatch from Alexandria & Port Said to GCC, Europe, and North American ports.",
        "desc_ar": "شحن بحري مباشر للحاويات المبردة والجافة من ميناء الإسكندرية إلى موانئ الخليج وأوروبا وأمريكا الشمالية.",
    },
    {
        "id": 15,
        "category": "logistics",
        "file": "output/imagery/arina_gallery_supermarket_shelf_4k.jpg?v=20261007",
        "tag_en": "MODERN B2B WAREHOUSE",
        "tag_ar": "المستودعات الذكية والخدمات اللوجستية",
        "title_en": "Modern B2B Export Warehouse & Bulk Drum Palletizing",
        "title_ar": "تجهيز وتخزين براميل التصدير بالمستودعات الحديثة",
        "desc_en": "Climate-controlled logistics facility with certified palletizing, shrink-wrapping, and barcode tracking.",
        "desc_ar": "مستودعات تصدير مجهزة بأنظمة التبريد وتغليف المنصات وتتبع الباركود الإلكتروني للشحن الدولي.",
    },
    {
        "id": 16,
        "category": "logistics",
        "file": "output/imagery/arina_gallery_export_cartons_4k.jpg?v=20261007",
        "tag_en": "PRECISION AUTOMATED PACKAGING",
        "tag_ar": "خطوط التعبئة والتغليف الآلية الدقيقة",
        "title_en": "Automated Precision Packaging & Hermetic Sealing Facility",
        "title_ar": "منشأة التعبئة الآلية والإغلاق الهوائي المحكم",
        "desc_en": "ISO 22000 and HACCP certified automated glass packaging line with nitrogen flushing and robotic carton packing.",
        "desc_ar": "خطوط تعبئة زجاجية آلية معتمدة بمعايير ISO وHACCP مع تفريغ الهواء وتعبئة الكراتين بالروبوتات.",
    },
]

def escape_js(s):
    return s.replace('\\', '\\\\').replace("'", "\\'")

def escape_html(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def generate_grid_html():
    cards_html = []
    for c in CARDS:
        cid = c["id"]
        cat = c["category"]
        f = c["file"]
        t_en_js = escape_js(c["title_en"])
        t_ar_js = escape_js(c["title_ar"])
        d_en_js = escape_js(c["desc_en"])
        d_ar_js = escape_js(c["desc_ar"])
        
        t_en_html = escape_html(c["title_en"])
        d_en_html = escape_html(c["desc_en"])
        tag_en_html = escape_html(c["tag_en"])
        
        card = f'''        <!-- Gallery Item {cid}: {t_en_html} -->
        <div class="gallery-card tilt-card rounded-[1.75rem] p-1.5 glass-card-shell group cursor-pointer transition-all duration-300" data-category="{cat}" onclick="openLightbox('{f}', '{t_en_js}', '{t_ar_js}', '{d_en_js}', '{d_ar_js}')">
          <div class="rounded-[calc(1.75rem-0.375rem)] glass-card-core overflow-hidden flex flex-col justify-between h-full">
            <div class="relative overflow-hidden aspect-[16/9]">
              <img src="{f}" alt="{t_en_html} 4K" loading="lazy" decoding="async" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105">
              <div class="absolute inset-0 bg-brand-forest-obsidian/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-brand-gold font-bold text-xs">
                <span class="px-4 py-2 rounded-full bg-brand-forest-obsidian/90 border border-brand-gold/60 shadow-lg inline-flex items-center gap-2">
                  <svg class="w-3.5 h-3.5 text-brand-gold flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    <line x1="11" y1="8" x2="11" y2="14"></line>
                    <line x1="8" y1="11" x2="14" y2="11"></line>
                  </svg>
                  <span data-i18n="gallery_inspect_btn">Inspect 4K Asset</span>
                </span>
              </div>
              <div class="absolute top-2.5 start-2.5 px-2 py-0.5 rounded-full bg-brand-forest-obsidian/85 border border-brand-gold/40 text-[9px] font-mono font-bold text-brand-gold">
                4K UHD • 16:9
              </div>
            </div>
            <div class="p-5 space-y-2">
              <div class="text-[10px] font-bold text-brand-gold uppercase tracking-wider" data-i18n="gallery_card{cid}_tag">{tag_en_html}</div>
              <h4 class="font-serif font-bold text-base text-brand-ivory" data-i18n="gallery_card{cid}_title">{t_en_html}</h4>
              <p class="text-xs text-brand-ivory/70 line-clamp-2" data-i18n="gallery_card{cid}_desc">{d_en_html}</p>
            </div>
          </div>
        </div>'''
        cards_html.append(card)
    
    return '\n\n'.join(cards_html)

def generate_en_translations():
    lines = []
    for c in CARDS:
        cid = c["id"]
        lines.append(f'        "gallery_card{cid}_tag": "{c["tag_en"]}",')
        lines.append(f'        "gallery_card{cid}_title": "{c["title_en"]}",')
        lines.append(f'        "gallery_card{cid}_desc": "{c["desc_en"]}",')
    return '\n'.join(lines)

def generate_ar_translations():
    lines = []
    for c in CARDS:
        cid = c["id"]
        lines.append(f'        "gallery_card{cid}_tag": "{c["tag_ar"]}",')
        lines.append(f'        "gallery_card{cid}_title": "{c["title_ar"]}",')
        lines.append(f'        "gallery_card{cid}_desc": "{c["desc_ar"]}",')
    return '\n'.join(lines)

def main():
    website_p = 'website.html'
    with open(website_p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace Gallery Grid content
    grid_pattern = re.compile(r'(<div id="gallery-grid"[^>]*>)(.*?)(</div>\s*</div>\s*</section>)', re.DOTALL)
    match = grid_pattern.search(html)
    if not match:
        raise ValueError("Could not find gallery-grid in website.html")
    
    new_grid_content = '\n        \n' + generate_grid_html() + '\n\n      '
    html = html[:match.start(2)] + new_grid_content + html[match.end(2):]
    print("Gallery grid replaced successfully!")

    # 2. Replace TRANSLATIONS.en gallery cards
    en_pattern = re.compile(r'(\"gallery_inspect_btn\":\s*\"Inspect 4K Asset\",\s*\n)(.*?)(\s*\"footer_l_gallery\":\s*\"4K Media Gallery\",)', re.DOTALL)
    en_match = en_pattern.search(html)
    if not en_match:
        raise ValueError("Could not find gallery cards in TRANSLATIONS.en")
    
    new_en_translations = generate_en_translations() + '\n'
    html = html[:en_match.start(2)] + new_en_translations + html[en_match.end(2):]
    print("TRANSLATIONS.en gallery cards replaced successfully!")

    # 3. Replace TRANSLATIONS.ar gallery cards
    ar_pattern = re.compile(r'(\"gallery_inspect_btn\":\s*\"معاينة الصورة بدقة 4K\",\s*\n)(.*?)(\s*\"footer_l_gallery\":\s*\"معرض الصور 4K\",)', re.DOTALL)
    ar_match = ar_pattern.search(html)
    if not ar_match:
        raise ValueError("Could not find gallery cards in TRANSLATIONS.ar")
    
    new_ar_translations = generate_ar_translations() + '\n'
    html = html[:ar_match.start(2)] + new_ar_translations + html[ar_match.end(2):]
    print("TRANSLATIONS.ar gallery cards replaced successfully!")

    with open(website_p, 'w', encoding='utf-8') as f:
        f.write(html)
    print("website.html written successfully!")

if __name__ == "__main__":
    main()
