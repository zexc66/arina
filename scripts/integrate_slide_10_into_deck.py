import os
import re

def integrate():
    workspace = '/home/zexc/Desktop/New Folder'
    index_path = os.path.join(workspace, 'index.html')
    mariam_path = os.path.join(workspace, 'mariam.html')

    with open(index_path, 'r', encoding='utf-8') as f:
        idx_content = f.read()

    with open(mariam_path, 'r', encoding='utf-8') as f:
        m_content = f.read()

    # 1. Extract Slide 10 from mariam.html
    s10_match = re.search(r'(<!-- Slide 10: Mariam Natural Honey & Superfoods Collection -->.*?)(?=</main>)', m_content, re.DOTALL)
    if not s10_match:
        print("Error: Could not find Slide 10 in mariam.html")
        return
    slide_10_html = s10_match.group(1).strip()

    # Update Slide 10 Header to have Khaeer Alwadi producer emblem + bilingual text
    new_header = """        <!-- Header -->
        <header class="flex items-center justify-between border-b border-white/10 pb-2 relative z-10">
          <div class="flex items-center gap-3 lg:gap-4">
            <img src="khaeer-alwadi-logo.png" alt="Khaeer Alwadi" class="h-8 w-auto object-contain hidden sm:block opacity-90">
            <div class="h-7 w-px bg-white/15 hidden sm:block"></div>
            <img src="mariam-logo-gold.png" alt="Mariam - made with love" class="h-7 lg:h-8 w-auto object-contain">
            <div class="h-6 w-px bg-white/15 hidden md:block"></div>
            <div>
              <div class="flex items-center gap-2">
                <h2 class="text-lg lg:text-xl font-bold tracking-tight text-white">
                  <span class="lang-en font-sans">Natural Honey &amp; Superfoods</span>
                  <span class="lang-ar font-cairo">عسل مريم الطبيعي والخلطات الملكية</span>
                </h2>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-[#76122E]/60 text-[#F5B7C2] border border-[#F5B7C2]/30">
                  <span class="lang-en">Artisanal Superfood Suite</span>
                  <span class="lang-ar font-cairo">باقة السوبرفود الحرفية</span>
                </span>
              </div>
              <p class="text-[11px] font-medium text-[#DAAC36]/90 mt-0.5">
                <span class="lang-en">Section 10 // Raw Unpasteurized Monoflorals • Tree Nut &amp; Super Seed Blends • 0% Peanuts Policy</span>
                <span class="lang-ar font-cairo">القسم 10 // أعسال أحادية الزهرة نقية • خلطات المكسرات والغذاء الملكي • خلو تام 100% من الفول السوداني</span>
              </p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <!-- Tamper Ribbon Mini-Badge -->
            <div class="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#76122E]/40 border border-[#F5B7C2]/30 text-[10px] font-mono text-[#F5B7C2]">
              <span class="w-1.5 h-1.5 rounded-full bg-[#DAAC36] animate-pulse"></span>
              <span class="lang-en">Crown Seal Tamper Ribbon</span>
              <span class="lang-ar font-cairo">شريط التويج الملكي</span>
            </div>
            <!-- Standard Badge -->
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-mono text-[#DAAC36]">
              <span>CODEX STAN 12-1981</span>
            </span>
          </div>
        </header>"""

    # Replace header inside slide_10_html
    slide_10_html = re.sub(r'<!-- Header -->.*?<!-- Executive Banner', new_header + '\n\n        <!-- Executive Banner', slide_10_html, flags=re.DOTALL)

    # 2. Extract Slide 10 JavaScript from mariam.html
    js_match = re.search(r'(// Interactive Honey & Superfoods Packaging Switcher \(Slide 10\).*?)(?=// Interactive Freight Container Switcher|// Navigation engine|\Z)', m_content, re.DOTALL)
    if not js_match:
        print("Error: Could not extract Slide 10 JS from mariam.html")
        return
    slide_10_js = js_match.group(1).strip()

    # 3. Update totalSlides in index.html to 10
    idx_content = re.sub(r'const totalSlides = 9;', 'const totalSlides = 10;', idx_content)

    # 4. Insert slide_10_html before </main>
    if 'id="slide-10"' not in idx_content:
        idx_content = idx_content.replace('</main>', slide_10_html + '\n\n    </main>')

    # 5. Add Slide 10 to slideTitles
    s10_title_entry = """,
      {
        num: '10',
        category_en: 'Superfood Reserve',
        category_ar: 'عسل وسوبرفود فاخر',
        title_en: 'Mariam Natural Honey & Connoisseur Superfood Blends',
        title_ar: 'عسل مريم الطبيعي وخلطات السوبرفود الملكية الفاخرة'
      }"""
    if "num: '10'" not in idx_content:
        idx_content = re.sub(r'(num:\s*[\'"]09[\'"].*?title_ar:\s*[\'"].*?[\'"]\s*\})', r'\1' + s10_title_entry, idx_content, flags=re.DOTALL)

    # 6. Add Slide 10 JS to index.html before window.addEventListener
    if 'switchHoneySize' not in idx_content:
        idx_content = idx_content.replace('document.addEventListener(\'DOMContentLoaded\'', slide_10_js + '\n\n    document.addEventListener(\'DOMContentLoaded\'')

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(idx_content)

    print("Successfully integrated Slide 10 into index.html!")

if __name__ == '__main__':
    integrate()
