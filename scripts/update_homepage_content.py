#!/usr/bin/env python3
"""
Updates website.html homepage content cleanly and robustly:
1. Elevates Hero headline, kicker, subtitle, and procurement narrative.
2. Inserts executive B2B Metrics & Credentials Ribbon (#hero-metrics-ribbon).
3. Updates TRANSLATIONS.en and TRANSLATIONS.ar in strictly separated blocks.
4. Strictly asserts zero Arabic characters in TRANSLATIONS.en before saving.
"""

import re
import os

METRICS_RIBBON_HTML = '''  <!-- ========================================================================= -->
  <!-- 2B. EXECUTIVE B2B METRICS & EXPORT CREDENTIALS RIBBON -->
  <!-- ========================================================================= -->
  <div id="hero-metrics-ribbon" class="relative z-20 -mt-10 sm:-mt-14 mb-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="glass-card-shell rounded-2xl sm:rounded-3xl p-1.5 shadow-[0_20px_50px_rgba(0,0,0,0.5)] border border-brand-gold/30 backdrop-blur-xl">
      <div class="glass-card-core rounded-[calc(1rem-0.125rem)] sm:rounded-[calc(1.5rem-0.125rem)] p-4 sm:p-6 grid grid-cols-2 lg:grid-cols-5 gap-4 sm:gap-6 divide-y lg:divide-y-0 lg:divide-x divide-brand-gold/15 rtl:lg:divide-x-reverse">
        
        <!-- Metric 1: Master SKUs -->
        <div class="flex items-center gap-3.5 pt-3 first:pt-0 lg:pt-0 px-2 sm:px-4">
          <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-brand-gold/20 to-brand-forest-obsidian/80 border border-brand-gold/35 flex items-center justify-center text-brand-gold flex-shrink-0 shadow-[0_0_15px_rgba(218,172,54,0.2)]">
            <svg class="w-5 h-5 text-brand-gold" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
          </div>
          <div>
            <div class="text-2xl sm:text-3xl font-serif font-bold text-brand-ivory tracking-tight leading-none" data-i18n="metric_1_val">14 SKUs</div>
            <div class="text-xs font-bold text-brand-gold uppercase tracking-wider mt-1" data-i18n="metric_1_title">Export Portfolio</div>
            <div class="text-[10px] text-brand-ivory/60 leading-tight mt-0.5" data-i18n="metric_1_sub">Olives, Pickles &amp; Toum</div>
          </div>
        </div>

        <!-- Metric 2: Retail Margin -->
        <div class="flex items-center gap-3.5 pt-3 lg:pt-0 px-2 sm:px-4">
          <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-brand-gold/20 to-brand-forest-obsidian/80 border border-brand-gold/35 flex items-center justify-center text-brand-gold flex-shrink-0 shadow-[0_0_15px_rgba(218,172,54,0.2)]">
            <svg class="w-5 h-5 text-brand-gold" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
            </svg>
          </div>
          <div>
            <div class="text-2xl sm:text-3xl font-serif font-bold text-brand-ivory tracking-tight leading-none" data-i18n="metric_2_val">35%–48%</div>
            <div class="text-xs font-bold text-brand-gold uppercase tracking-wider mt-1" data-i18n="metric_2_title">Retailer Margin</div>
            <div class="text-[10px] text-brand-ivory/60 leading-tight mt-0.5" data-i18n="metric_2_sub">High Consumer Velocity</div>
          </div>
        </div>

        <!-- Metric 3: 0% Tariff (GAFTA / EUR.1) -->
        <div class="flex items-center gap-3.5 pt-3 lg:pt-0 px-2 sm:px-4">
          <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-brand-gold/20 to-brand-forest-obsidian/80 border border-brand-gold/35 flex items-center justify-center text-brand-gold flex-shrink-0 shadow-[0_0_15px_rgba(218,172,54,0.2)]">
            <svg class="w-5 h-5 text-brand-gold" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <div>
            <div class="text-2xl sm:text-3xl font-serif font-bold text-brand-ivory tracking-tight leading-none" data-i18n="metric_3_val">0% Tariff</div>
            <div class="text-xs font-bold text-brand-gold uppercase tracking-wider mt-1" data-i18n="metric_3_title">GAFTA &amp; EUR.1</div>
            <div class="text-[10px] text-brand-ivory/60 leading-tight mt-0.5" data-i18n="metric_3_sub">GCC &amp; EU Duty-Free</div>
          </div>
        </div>

        <!-- Metric 4: Ambient Shelf Life -->
        <div class="flex items-center gap-3.5 pt-3 lg:pt-0 px-2 sm:px-4">
          <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-brand-gold/20 to-brand-forest-obsidian/80 border border-brand-gold/35 flex items-center justify-center text-brand-gold flex-shrink-0 shadow-[0_0_15px_rgba(218,172,54,0.2)]">
            <svg class="w-5 h-5 text-brand-gold" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6l4 2"/>
            </svg>
          </div>
          <div>
            <div class="text-2xl sm:text-3xl font-serif font-bold text-brand-ivory tracking-tight leading-none" data-i18n="metric_4_val">24 Months</div>
            <div class="text-xs font-bold text-brand-gold uppercase tracking-wider mt-1" data-i18n="metric_4_title">Ambient Stable</div>
            <div class="text-[10px] text-brand-ivory/60 leading-tight mt-0.5" data-i18n="metric_4_sub">Hermetic Vacuum Sealed</div>
          </div>
        </div>

        <!-- Metric 5: 48h Express Dispatch -->
        <div class="col-span-2 lg:col-span-1 flex items-center gap-3.5 pt-3 lg:pt-0 px-2 sm:px-4">
          <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-brand-gold/20 to-brand-forest-obsidian/80 border border-brand-gold/35 flex items-center justify-center text-brand-gold flex-shrink-0 shadow-[0_0_15px_rgba(218,172,54,0.2)]">
            <svg class="w-5 h-5 text-brand-gold" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
          </div>
          <div>
            <div class="text-2xl sm:text-3xl font-serif font-bold text-brand-ivory tracking-tight leading-none" data-i18n="metric_5_val">48 Hours</div>
            <div class="text-xs font-bold text-brand-gold uppercase tracking-wider mt-1" data-i18n="metric_5_title">Sample Dispatch</div>
            <div class="text-[10px] text-brand-ivory/60 leading-tight mt-0.5" data-i18n="metric_5_sub">DHL/FedEx Air to Buyers</div>
          </div>
        </div>

      </div>
    </div>
  </div>
'''

def update_homepage():
    website_p = 'website.html'
    with open(website_p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Hero Left Column in HTML
    old_kicker = re.search(r'(<span data-i18n="hero_kicker"[^>]*>)(.*?)(</span>)', html, re.DOTALL)
    assert old_kicker, "hero_kicker not found in html"
    html = html[:old_kicker.start(2)] + '\n              SINGLE-ESTATE EGYPTIAN EXPORT • DIRECT FACTORY-TO-SHELF SUPPLY\n            ' + html[old_kicker.end(2):]

    old_titles = re.search(r'(<h1[^>]*>)(.*?)(</h1>)', html, re.DOTALL)
    assert old_titles, "h1 not found in html"
    new_h1_inner = '''
            <span data-i18n="hero_title_1" class="block">Single-Estate Table Olives &amp; Heritage Artisanal Pickles.</span>
            <span class="gold-gradient-text italic font-medium block mt-1.5 sm:mt-2.5" data-i18n="hero_title_2">Direct Factory Supply for Tier-1 Supermarkets &amp; Global Importers.</span>
          '''
    html = html[:old_titles.start(2)] + new_h1_inner + html[old_titles.end(2):]

    old_subtitle = re.search(r'(<p class="text-lg sm:text-2xl text-brand-gold-light font-bold leading-relaxed" data-i18n="hero_subtitle">)(.*?)(</p>)', html, re.DOTALL)
    assert old_subtitle, "hero_subtitle not found in html"
    new_sub = '\n              100% Pure Flint Glass • 24-Month Ambient Shelf Stability • 35%–48% Retail Margin Architecture\n            '
    html = html[:old_subtitle.start(2)] + new_sub + html[old_subtitle.end(2):]

    old_desc = re.search(r'(<p class="text-brand-ivory/85 text-sm sm:text-base lg:text-lg leading-relaxed max-w-2xl font-normal font-sans tracking-wide" data-i18n="hero_desc">)(.*?)(</p>)', html, re.DOTALL)
    assert old_desc, "hero_desc not found in html"
    new_desc = '\n            Direct estate-to-shelf supply for Tier-1 Supermarket Chains, Gourmet Delicatessens, and Global Foodservice Distributors. Preserved strictly in iconic 100% recyclable glass jars with 24-month ambient shelf life, high retail velocity, and automated FMCG case pack logistics. Zero intermediary markups, ISO 22000/HACCP certified, and 0% preferential tariffs under GAFTA &amp; EUR.1.\n          '
    html = html[:old_desc.start(2)] + new_desc + html[old_desc.end(2):]

    # 2. Insert Metrics Ribbon between </section> (hero) and <!-- 2.5. SINGLE-ESTATE TERROIR -->
    if 'id="hero-metrics-ribbon"' not in html:
        m = re.search(r'(</section>\s*)(<!--\s*=+\s*-->\s*<!--\s*2\.5\.\s*SINGLE-ESTATE\s*TERROIR)', html)
        assert m, "Transition between hero and terroir not found"
        html = html[:m.start(1)] + '</section>\n\n' + METRICS_RIBBON_HTML + '\n' + html[m.start(2):]
        print("Metrics ribbon inserted successfully!")
    else:
        print("Metrics ribbon already present!")

    # 3. Carefully isolate en: { ... } and ar: { ... }
    en_idx = html.find('en: {')
    ar_idx = html.find('ar: {')
    assert en_idx != -1 and ar_idx != -1 and en_idx < ar_idx, "Could not find en: and ar: blocks"

    prefix = html[:en_idx]
    en_part = html[en_idx:ar_idx]
    ar_part = html[ar_idx:]

    # --- Update English block ---
    old_en_hero = re.search(
        r'(\"hero_kicker\":\s*\")(.*?)(\",\s*\n\s*\"hero_title_1\":\s*\")(.*?)(\",\s*\n\s*\"hero_title_2\":\s*\")(.*?)(\",\s*\n\s*\"hero_subtitle\":\s*\")(.*?)(\",\s*\n\s*\"hero_subtitle_ar\":\s*\")(.*?)(\",\s*\n\s*\"hero_desc\":\s*\")(.*?)(\",)',
        en_part, re.DOTALL
    )
    assert old_en_hero, "Hero block in en_part not found"

    new_en_replacement = '''"hero_kicker": "SINGLE-ESTATE EGYPTIAN EXPORT • DIRECT FACTORY-TO-SHELF SUPPLY",
        "hero_title_1": "Single-Estate Table Olives & Heritage Artisanal Pickles.",
        "hero_title_2": "Direct Factory Supply for Tier-1 Supermarkets & Global Importers.",
        "hero_subtitle": "100% Pure Flint Glass • 24-Month Ambient Shelf Stability • 35%–48% Retail Margin Architecture",
        "hero_subtitle_ar": "100% Pure Flint Glass • 24-Month Ambient Shelf Stability • 35%–48% Retail Margin Architecture",
        "hero_desc": "Direct estate-to-shelf supply for Tier-1 Supermarket Chains, Gourmet Delicatessens, and Global Foodservice Distributors. Preserved strictly in iconic 100% recyclable glass jars with 24-month ambient shelf life, high retail velocity, and automated FMCG case pack logistics. Zero intermediary markups, ISO 22000/HACCP certified, and 0% preferential tariffs under GAFTA & EUR.1.",
        "metric_1_val": "14 SKUs",
        "metric_1_title": "Export Portfolio",
        "metric_1_sub": "Olives, Pickles & Toum",
        "metric_2_val": "35%–48%",
        "metric_2_title": "Retailer Margin",
        "metric_2_sub": "High Consumer Velocity",
        "metric_3_val": "0% Tariff",
        "metric_3_title": "GAFTA & EUR.1",
        "metric_3_sub": "GCC & EU Duty-Free",
        "metric_4_val": "24 Months",
        "metric_4_title": "Ambient Stable",
        "metric_4_sub": "Hermetic Vacuum Sealed",
        "metric_5_val": "48 Hours",
        "metric_5_title": "Sample Dispatch",
        "metric_5_sub": "DHL/FedEx Air to Buyers",'''

    en_part = en_part[:old_en_hero.start(1)] + new_en_replacement + en_part[old_en_hero.end(13):]

    # Verify zero Arabic characters in en_part
    arabic_in_en = re.findall(r'[\u0600-\u06FF]+', en_part)
    assert len(arabic_in_en) == 0, f"FATAL: Arabic characters found in en_part: {arabic_in_en}"
    print("en_part verified with 0 Arabic characters!")

    # --- Update Arabic block ---
    old_ar_hero = re.search(
        r'(\"hero_kicker\":\s*\")(.*?)(\",\s*\n\s*\"hero_title_1\":\s*\")(.*?)(\",\s*\n\s*\"hero_title_2\":\s*\")(.*?)(\",\s*\n\s*\"hero_subtitle\":\s*\")(.*?)(\",\s*\n\s*\"hero_subtitle_ar\":\s*\")(.*?)(\",\s*\n\s*\"hero_desc\":\s*\")(.*?)(\",)',
        ar_part, re.DOTALL
    )
    assert old_ar_hero, "Hero block in ar_part not found"

    new_ar_replacement = '''"hero_kicker": "تصدير معتمد من المزارع المصرية مباشرة • توريد مصنعي لأرقى منافذ التجزئة",
        "hero_title_1": "زيتون المائدة الفاخر ومخللات التراث المصري الأصيل.",
        "hero_title_2": "توريد مصنعي مباشر لكبرى سلاسل الهايبرماركت والمستوردين الدوليين.",
        "hero_subtitle": "برطمانات زجاجية نقية 100% • صلاحية 24 شهراً بدرجة حرارة الغرفة • هوامش ربحية للتجزئة بين 35% و 48%",
        "hero_subtitle_ar": "برطمانات زجاجية نقية 100% • صلاحية 24 شهراً بدرجة حرارة الغرفة • هوامش ربحية للتجزئة بين 35% و 48%",
        "hero_desc": "توريد تصديري مباشر بدون وسطاء من محطات تعبئة علامة أرينا إلى أرفف كبرى سلاسل الهايبرماركت وموزعي الأغذية الدوليين. معبأة حصرياً في برطمانات زجاجية نقية قابلة للتدوير بنسبة 100%، صلاحية 24 شهراً في درجة حرارة الغرفة، أعلى معدل دوران بيعي، وكراتين معيارية مؤتمتة. معتمدة بشهادات ISO 22000 وHACCP وتخضع لتعريفة جمركية 0% بموجب اتفاقيات التجارة الحرة GAFTA وEUR.1.",
        "metric_1_val": "14 صنفاً",
        "metric_1_title": "المحفظة التصديرية",
        "metric_1_sub": "زيتون ومخللات وثومية",
        "metric_2_val": "35%–48%",
        "metric_2_title": "هامش ربح التجزئة",
        "metric_2_sub": "دوران استهلاكي فائق",
        "metric_3_val": "0% جمارك",
        "metric_3_title": "اتفاقيات GAFTA وEUR.1",
        "metric_3_sub": "إعفاء بالخليج وأوروبا",
        "metric_4_val": "24 شهراً",
        "metric_4_title": "استقرار بالحرارة العادية",
        "metric_4_sub": "إغلاق مفرغ من الهواء",
        "metric_5_val": "48 ساعة",
        "metric_5_title": "شحن عينات مجانية",
        "metric_5_sub": "شحن جوي سريع للمشترين",'''

    ar_part = ar_part[:old_ar_hero.start(1)] + new_ar_replacement + ar_part[old_ar_hero.end(13):]
    print("ar_part updated successfully!")

    # Reassemble
    html = prefix + en_part + ar_part

    with open(website_p, 'w', encoding='utf-8') as f:
        f.write(html)
    print("website.html written successfully!")

if __name__ == "__main__":
    update_homepage()
