# Design Specification: Khaeer Alwadi Food Industries Bilingual B2B Sales Presentation Deck

**Date:** 2026-09-05  
**Brand:** Khaeer Alwadi Food Industries (خير الوادي للصناعات الغذائية)  
**Location:** Cairo, Egypt  
**Contact Desk:** Direct WhatsApp & Phone: `+20 10 08716714`  
**Target Files:**  
- Primary Bilingual Deck: `index.html`  
- Preserved Prior Deck: `mariam.html`  
- Extracted Logo Assets: `khaeer-alwadi-logo.png`, `khaeer-alwadi-logo-gold.png`  
- Test Suite: `tests/test_deck_structure.py`  

---

## 1. Executive Summary & Brand Identity

### 1.1 Brand Background
"Khaeer Alwadi" (خير الوادي - *Bounty of the Valley*) represents Egyptian agro-industrial excellence, specializing in contract-farmed Mediterranean table olives, pickled specialty peppers, and traditional artisan pickles (Turshi). The company serves international wholesale importers, foodservice chains, pizza commissaries, and supermarket private-label partners across Europe, the GCC, North America, and Africa.

### 1.2 Logo Analysis & Asset Matting
The official logo features:
- **Symbol:** A stylized Mediterranean olive twig bearing two-tone olive green leaves and a plump dark purple/black table olive with a warm golden oil reflection.
- **Arabic Typography:** Custom geometric Kufic script with soft rounded terminals and leaf-shaped dots for *"خير الوادي"*.
- **Latin Sub-brand:** Clean sans-serif set in golden brass brackets: `"- Khaeer Alwadi -"`.
- **Descriptor:** *"للصناعات الغذائية"* (For Food Industries).

**Logo Assets to Generate:**
1. `khaeer-alwadi-logo.png`: Full-color deconvolution with transparent alpha channel, retaining authentic leaf green, ripe olive purple-black, charcoal wordmark, and golden brass framing.
2. `khaeer-alwadi-logo-gold.png`: Royal gold metallic edition for dark executive cards and slide headers.

### 1.3 Calibrated Color Hierarchy
- **Valley Leaf Green:** `#2D5232` (DEFAULT), `#3D6B42` (light), `#1E3A24` (dark)
- **Harvest Brass & Gold:** `#D4A836` (amber-400), `#C29B44` (brass), `#E6C46E` (amber-300)
- **Kalamata Obsidian:** `#181116` / `#2C1A27`
- **Background OLED Canvas:** `linear-gradient(to bottom right, #091410, #0E1F17, #050907)`
- **Card Double-Bezel Surface:** `linear-gradient(145deg, rgba(16, 34, 26, 0.92), rgba(9, 18, 14, 0.97))` with `border-white/10` and gold hover reflection `rgba(212, 168, 54, 0.45)`.

### 1.4 Typography Stack
- **Arabic Display & Body:** `Cairo` (Google Fonts: 400, 600, 700, 800) paired with system fallbacks (`Segoe UI`, `Tahoma`, `sans-serif`).
- **English Display & Body:** `Plus Jakarta Sans` (Google Fonts: 400, 500, 600, 700, 800).
- **Technical Metrics & Freight Tables:** `JetBrains Mono` (Google Fonts: 400, 500, 600, 700).

---

## 2. Workspace & File Architecture

1. **Safety Backup of Mariam Deck:**
   - Copy existing `index.html` to `mariam.html`.
   - Ensure all assets in `mariam.html` continue to function 100% offline.
2. **Khaeer Alwadi as Primary Deck:**
   - Scaffold the new bilingual deck into `index.html`.
   - Incorporate the bilingual engine, responsive 16:9 widescreen presentation canvas, navigation dock, image lightbox, overview drawer, and print-to-PDF styles.
3. **Shared Photography Assets:**
   - Directly leverage the 35 real factory and product photographs already tracked in the repository (`WhatsApp Image 2026-09-05 at 12.52.*.jpeg`).
4. **Automated Test Suite (`tests/test_deck_structure.py`):**
   - Assert existence of `mariam.html` and `index.html`.
   - Assert Khaeer Alwadi brand presence in Arabic ("خير الوادي") and English ("Khaeer Alwadi").
   - Assert presence of bilingual language toggle mechanics and direction switching.
   - Assert all 9 slides, contact details, freight specs, and lightbox modals.

---

## 3. Bilingual Interaction & RTL Engine

### 3.1 Language Switching Architecture
- **Root State:** Controlled by `<html lang="ar" dir="rtl">` (or `lang="en" dir="ltr"`).
- **Nav Dock Toggle Pill:** A tactile pill button in `#nav-dock` showing `EN | عربي` with visual badge indicating the current active mode.
- **Keyboard Shortcut:** Pressing the `L` key (or `Lang` button) toggles the language instantly without page reload.
- **State Preservation:** When toggling language, the current active slide index (`currentSlide`) is preserved. The presenter never loses their place.

### 3.2 Dual-DOM Element Structure
- Text containers utilize dual child elements:
  ```html
  <span class="lang-en">Executive Procurement Desk</span>
  <span class="lang-ar">مكتب المشتريات والتصدير التنفيذي</span>
  ```
- CSS rules automatically hide/show based on the root language:
  ```css
  html[lang="en"] .lang-ar { display: none !important; }
  html[lang="ar"] .lang-en { display: none !important; }
  ```
- Directional logical spacing ensures mirrored paddings and borders without layout breaking:
  ```css
  html[dir="rtl"] body { font-family: 'Cairo', 'Plus Jakarta Sans', sans-serif; }
  html[dir="ltr"] body { font-family: 'Plus Jakarta Sans', sans-serif; }
  ```

### 3.3 Modal Localization
- **Image Lightbox Modal (`#image-modal`):** Captions and inspection labels update dynamically to match the active language.
- **Overview Drawer (`#overview-modal`):** All 9 slide thumbnail titles render in Arabic or English according to the active mode.
- **Shortcuts Modal (`#shortcuts-modal`):** Full Arabic translation of navigation keys.

### 3.4 Print-to-PDF Engine
- When `window.print()` is triggered (or via the print button in `#nav-dock` / `Ctrl+P`):
  - Prints all 9 slides sequentially in landscape A4.
  - Direction and typography correspond to the currently active language (prints full Arabic RTL presentation if Arabic is active, or full English LTR presentation if English is active).
  - Background graphics, badges, and colors print with `-webkit-print-color-adjust: exact`.

---

## 4. Slide-by-Slide Content Architecture

### Slide 1: الغلاف والملخص التنفيذي / Executive Cover & Introduction
- **Header:** `khaeer-alwadi-logo.png` alongside company name in Arabic ("خير الوادي للصناعات الغذائية") and English ("Khaeer Alwadi Food Industries"), with official B2B portfolio badge.
- **Title:**
  - EN: *Mediterranean Table Olives & Pickled Specialties — Industrial Processing, Direct Grove Sourcing & Turnkey Private Label Solutions*.
  - AR: *زيتون مائدة متوسطي فاخر ومخللات تخصصية — معالجة صناعية، توريد مباشر من المزارع، وحلول تصنيع للغير (Private Label)*.
- **4 Trust Pillars:**
  1. Direct Agro Terroir / التوريد الزراعي المباشر (15–25% cost edge over Southern Europe).
  2. Industrial Scale / الطاقة الصناعية المؤتمتة (Mechanical pitting, rotary slicing, autoclave sterilization).
  3. Rapid Port Logistics / لوجستيات موانئ سريعة (3–5 days to Southern Europe, 4–7 days to GCC).
  4. Global Certifications / اعتمادات ومطابقة دولية (ISO 22000, HACCP, FDA Registered, Halal, ISO 9001).
- **Direct Contact Strip:** WhatsApp `+20 10 08716714` with quick-chat button and 24-hr quotation guarantee.
- **Product Hero Card:** Multi-tier jar showcase (`WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg`).

### Slide 2: الميزة التنافسية للزراعة والتصدير المصري / The Egyptian Strategic Supply Advantage
- **Value Thesis:** 15%–25% landed cost advantage over Spanish, Greek, and Italian processors.
- **3 Strategic Corridors:**
  1. Nile Delta & Mediterranean Microclimate (Ismailia, Fayoum, Alexandria road groves; high fruit density).
  2. Tri-Port Maritime Corridors: Alexandria Port (2.5h), Damietta Port (2.5h), Port Said Port (2.0h).
  3. 0% Duty-Free Free Trade Accords: GAFTA (17 Arab countries), COMESA (580M+ consumers), Agadir Agreement, EU Association Agreement.

### Slide 3: البنية الصناعية والتقنية وضمان الجودة / Industrial Infrastructure, Technology & Compliance
- **4 Processing Highlights:**
  1. Mechanical Stone Pitting Line (`<0.1%` pit fragment tolerance).
  2. Rotary Ring Slicing Lines (3.0mm–3.5mm calibrated ring thickness).
  3. Automated A10 Can Seaming & Washing.
  4. High-Pressure Retort Autoclave Sterilization ($F_0 \ge 4.0$, 36-month ambient shelf life).
- **Compliance Badges:** ISO 22000:2018, HACCP Codex Alimentarius, FDA Registered (US FSMA), Halal Certified, ISO 9001:2015.
- **Real Plant Photos:** Autoclave crate with gold lid jars (`WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg`) and warehouse palletized floor (`WhatsApp Image 2026-09-05 at 12.52.17 PM.jpeg`).

### Slide 4: خط الإنتاج الأول: زيتون المائدة المتوسطي الفاخر / Core Line I: Table Olives Portfolio
- **5 Featured Olive Lines:**
  1. Sliced Black Olive Rings (Picual/Confection) — non-scorching pizza oven specs (`WhatsApp Image 2026-09-05 at 12.52.20 PM.jpeg`, `WhatsApp Image 2026-09-05 at 12.52.15 PM (2).jpeg`).
  2. Mechanically Pitted Black Olives — intact cylindrical geometry (`WhatsApp Image 2026-09-05 at 12.52.16 PM (5).jpeg`).
  3. Whole & Sliced Green Olives (Manzanilla & Picual) (`WhatsApp Image 2026-09-05 at 12.52.17 PM (6).jpeg`, `WhatsApp Image 2026-09-05 at 12.52.17 PM (1).jpeg`).
  4. Pimento-Stuffed Green Olives — sweet pimento paste flush with crown (`WhatsApp Image 2026-09-05 at 12.52.17 PM (5).jpeg`).
  5. Kalamata-Style Dark Olives — red wine vinegar & EVOO infusion (`WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg`).
- **Technical Spec Chips:** Calibers (200/220, 240/260, 280/300), ring thickness 3.2mm $\pm0.2$mm, drained weight $\ge 52\%$, salinity 4.5%–6.0%, shelf life 36 months.

### Slide 5: خط الإنتاج الثاني: المخللات التخصصية والفلفل الممتاز / Core Line II: Pickles & Specialty Peppers
- **4 Featured Pickled Specialties:**
  1. Golden Pepperoncini (Friggitello) — crisp snap, mild heat (100–500 SHU) (`WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg`).
  2. Whole Hot Red Chili Peppers (Egyptian Cayenne) (15,000–30,000 SHU) (`WhatsApp Image 2026-09-05 at 12.52.19 PM.jpeg`).
  3. Traditional Mixed Pickles (Turshi Baladi) — cauliflower, carrots, turnips, olives in spiced pink coriander brine (`WhatsApp Image 2026-09-05 at 12.52.16 PM (2).jpeg`).
  4. Pickled Snap Cucumbers & Gherkins — dill, garlic, and mustard seed brine (`WhatsApp Image 2026-09-05 at 12.52.18 PM (2).jpeg`).
- **Technical Spec Chips:** Natural lactic fermentation, crispness retention, pH 3.2–3.6, salinity 3.5%–5.0%, ambient shelf life 24 months.

### Slide 6: هندسة العبوات والتعبئة والتغليف متعددة المستويات / Multi-Tier Packaging Architecture
- **Tier 1 (Foodservice & HoReCa):** Heavy-gauge A10 metal cans (~3kg gross, drained weight $\ge 1,560$g, BPA-NI protective interior lacquer, 6 tins/case) (`WhatsApp Image 2026-09-05 at 12.52.17 PM (7).jpeg`, `WhatsApp Image 2026-09-05 at 12.52.16 PM (3).jpeg`).
- **Tier 2 (Industrial Bulk Processing):** 150kg & 220kg food-grade HDPE barrels with galvanized lever clamp rings (`WhatsApp Image 2026-09-05 at 12.52.17 PM (4).jpeg`, `WhatsApp Image 2026-09-05 at 12.52.17 PM (9).jpeg`).
- **Tier 3 (Retail Supermarket Tier):** High-clarity glass jars (370ml, 500ml, 720ml, 1,000ml) with tamper-evident safety vacuum button caps branded with Khaeer Alwadi or buyer label (`WhatsApp Image 2026-09-05 at 12.52.16 PM (4).jpeg`, `WhatsApp Image 2026-09-05 at 12.52.16 PM (6).jpeg`).
- **Tier 4 (Export Palletization):** ISPM-15 heat-treated timber pallets, 23µm stretch film, edge protectors (`WhatsApp Image 2026-09-05 at 12.52.15 PM (5).jpeg`).

### Slide 7: التصنيع للغير والحلول الجاهزة المتكاملة / Private Label & Turnkey OEM Solutions
- **6-Stage OEM Workflow:** 01 Sourcing $\rightarrow$ 02 Formulation $\rightarrow$ 03 Geometry $\rightarrow$ 04 Compliance $\rightarrow$ 05 Packing $\rightarrow$ 06 Dispatch.
- **Dual Brand Strategy:** Clients can import under the registered **Khaeer Alwadi** brand or deploy full-service turnkey **Private Label OEM**.
- **Regulatory Compliance:** US FDA (21 CFR Nutrition Facts), EU FIC (Reg 1169/2011 allergens), GSO, SFDA, and official GS1 EAN-13/GTIN-14 barcodes.

### Slide 8: مصفوفة المواصفات الفنية ولوجستيات شحن الحاويات / Technical Specifications & Freight Matrix
- **Quality Parameters Table:** Drained weight ratio, salt content, pH limits, defect tolerances ($<1.0\%$), organoleptic standards.
- **Ocean Freight Loading Math:**
  - 20ft FCL: 10–11 pallets, 1,000–1,200 cartons or 80–90 drums (~18–20.5 MT payload).
  - 40ft HC FCL: 20–22 pallets, 2,000–2,200 cartons or 120–140 drums (~24.5–26 MT payload).
  - Protection: Certified ISPM-15 pallets, desiccants, heavy shrink-wrap.

### Slide 9: الشراكة التجارية وبدء التعامل والاتصال المباشر / Commercial Partnership & Direct Line
- **Executive Procurement Desk:** Khaeer Alwadi Food Industries, Cairo, Egypt.
- **Active Clickable Channels:**
  - WhatsApp: `https://wa.me/201008716714` (`+20 10 08716714`)
  - Direct Dial: `tel:+201008716714`
- **4-Step Fast Buyer Onboarding Protocol:**
  1. Sample Dispatch via DHL Express / FedEx International Priority.
  2. 24-Hour Quotation Guarantee (FOB Alexandria / Damietta / Port Said, CIF Global Ports).
  3. Flexible Payment Terms: Irrevocable Letter of Credit (L/C at sight), T/T deposit/balance.
  4. Guaranteed Laycan & Production Scheduling.

---

## 5. Verification & Testing Strategy

1. **Automated Structural & Bilingual Tests (`tests/test_deck_structure.py`):**
   - Verify `mariam.html` exists and passes original assertions.
   - Verify `index.html` exists, contains 9 slides, and `#nav-dock`.
   - Verify Khaeer Alwadi branding in Arabic ("خير الوادي") and English ("Khaeer Alwadi").
   - Verify presence of bilingual classes (`.lang-en`, `.lang-ar`) and toggle button.
   - Verify contact number `+20 10 08716714` and active clickable links.
   - Verify all required product images and certificates (ISO 22000, HACCP, FDA, Halal, ISO 9001).
   - Verify lightbox modal and print rules.
2. **Interactive Manual Verification:**
   - Test keyboard navigation (`ArrowRight`, `ArrowLeft`, `Space`, `1`–`9`).
   - Test language toggle button and `L` shortcut.
   - Test image lightbox zoom and slide overview drawer.
   - Test browser print preview in both Arabic and English.
