# Design Specification: Mariam Honey & Superfoods Dedicated Storefront & Ultra-Sharp 4K Imagery Pipeline

## 1. Overview & Context

Mariam (مريم) is a premium Mediterranean food brand produced by Khaeer Alwadi (خير الوادي). The portfolio covers table olives, artisanal pickles, extra virgin olive oil, garlic pastes, and natural honey & superfoods.

Previously, honey products were embedded inside a monolithic, multi-category page alongside pickles and olives, creating product confusion. Furthermore, automated inpainting and resizing scripts resulted in soft/blurry packshots that did not match the pristine vector sharpness of the authentic brand logo, and occasional logo miscolorations (e.g. burgundy tints or AI font substitutions) occurred.

This design establishes:
1. A **dedicated, standalone boutique storefront** exclusively for **Mariam Natural Honey & Superfoods** located at `honey.html`.
2. An **ultra-sharp 4K photography processing engine** that renders photorealistic, razor-sharp white studio packshots (3000 × 3000 px @ JPEG Quality 98+) featuring strictly the authentic cursive Luxor Gold logo (`mariam-logo-gold.png` in `#DAAC36`).
3. An **interactive 5-angle studio inspection stage** (0° Front Hero, Open Jar Texture, 45° Depth, 180° Back Regulatory, Cap Macro Seal) with full-screen lightbox zoom.
4. Complete **bilingual support (Arabic & English)** with instant RTL/LTR toggle, B2B wholesale sample request modal, and export-compliant specifications.

---

## 2. Brand Identity & Visual Guidelines

### 2.1 Sacred Brand Identity Directives
- **Authentic Logo**: Strictly and exclusively `mariam-logo-gold.png` located in the root directory. Under NO circumstances should standard typography, AI text generators, or alternate colors (such as wine burgundy `#76122E`) be applied to the Mariam logo.
- **Logo Metallic Tint**: Warm Luxor Gold (`RGB: 218, 172, 54` / `#DAAC36`).
- **Logo Micro-Embossing**: A microscopic 1.5–2px soft contact shadow (`RGBA: 75, 18, 30, 140`) placed behind the gold cursive strokes to simulate physical hot-foil stamping on paper without degrading vector sharpness.
- **Packaging Background**: Petal Blush Pink (`RGB: 245, 183, 194` / `#F5B7C2`), Warm Ivory (`RGB: 255, 245, 247` / `#FFF5F7`), and Obsidian Emerald Black (`#0A1612`).
- **Studio Packshot Standard**: 100% pure white background (`RGB: 255, 255, 255` / `#FFFFFF`) outside natural contact drop shadows. Corner pixels must satisfy $RGB \ge 253$ with neutral color balance ($|R - G| \le 2, |G - B| \le 2$).

---

## 3. Product Portfolio & SKUs

The dedicated Honey & Superfoods storefront features 6 primary products organized across 3 curated families:

| Product Name (EN) | Product Name (AR) | SKU | Sizes | Description & Formula |
| :--- | :--- | :--- | :--- | :--- |
| **Mariam Royal Mix** | خلطة مريم الملكية الفاخرة | `SKU-SF01` | 500g Glass | Mountain Sidr Honey (65%), whole roasted cashews, California almonds, Turkish hazelnuts, golden pumpkin seeds, royal jelly. **0% Peanuts Policy.** |
| **Mountain Sidr Honey** | عسل السدر الجبلي الحر | `SKU-H01` | 500g & 1kg | Raw, unpasteurized, single-estate monofloral Sidr honey. Highly viscous, glowing amber tone. |
| **Raw Cut Honeycomb in Honey** | قرص شمع العسل في برطمان سداسي | `SKU-H03` | 500g Hex Glass | Natural geometric virgin beeswax comb suspended in crystal-clear acacia honey. |
| **Clover Blossom Honey** | عسل زهور البرسيم النقي | `SKU-H04` | 500g & 1kg Family | Cold-extracted floral honey, silky crystalline texture, delicate vanilla notes. |
| **Black Seed Blossom Honey** | عسل زهور حبة البركة | `SKU-H05` | 500g Glass | Rich dark monofloral honey from Nigella Sativa blossoms with earthy, warm undertones. |
| **Citrus Blossom Honey** | عسل زهور الحمضيات والموالح | `SKU-H02` | 500g Glass | Light, aromatic Mediterranean orange & lemon blossom honey rich in natural enzymes. |

---

## 4. Ultra-Sharp 4K Photography Pipeline

To ensure the images have the exact razor-sharp clarity of the authentic logo, a dedicated Python script `scripts/render_ultra_sharp_honey_packshots.py` will process and composite all packshots:

### 4.1 Processing Steps:
1. **Raw Component Sourcing**: Load high-resolution studio captures from the brain directory (`honey_sidr_open_white_*.jpg`, `honey_royal_pdp_*.jpg`, etc.).
2. **2D Seamless Inpainting**: Use 2D bilinear gradient modeling and column-profile reconstruction to cleanly erase placeholder text, eliminating rectangular patch artifacts and halos.
3. **High-Frequency Edge Enhancement**: Apply subtle Unsharp Masking (`radius=1.2, percent=135, threshold=3`) to enhance the crisp facets of Nordic glass, amber honey highlights, and paper texture.
4. **Precision Logo Compositing**: Resize `mariam-logo-gold.png` with Lanczos interpolation at exact scale, tint in `#DAAC36`, and composite with micro-embossing shadow.
5. **Pure White Background Clamping**: Apply background threshold clamping to guarantee `#FFFFFF` at borders while preserving soft Gaussian contact drop shadows directly underneath the glass base.
6. **Dual Destination Export**: Save final images to both `output/imagery/` and the active brain directory at JPEG Quality 98+.

---

## 5. Dedicated Storefront Architecture (`honey.html`)

### 5.1 Technology Stack & Structure
- **Framework**: Semantic HTML5, Tailwind CSS via CDN, Vanilla JavaScript (zero bulky external dependencies).
- **Typography**: Playfair Display / Cormorant Garamond for luxury serif headers, Outfit / Inter for clean sans-serif UI, Amiri / Noto Kufi Arabic for Arabic calligraphy.
- **Responsive Layout**: Full support from 375px mobile screens up to 4K desktop displays.

### 5.2 Page Sections:
1. **Global Header & Navigation**:
   - Producer Emblem: Khaeer Alwadi logo.
   - Primary Brand Script: Authentic cursive gold Mariam logo.
   - Navigation links:
     - Honey & Superfoods (Active indicator)
     - Table Olives (`website.html#olives`)
     - Royal Pickles (`website.html#pickles`)
     - Extra Virgin Olive Oil (`website.html#evoo`)
     - Brand Story (`index.html`)
   - Language Switcher (AR / EN).
2. **Hero Showcase**:
   - Grand editorial headline and brand narrative.
   - Cinema 4K master panoramic banner of the complete honey lineup.
   - Quick action buttons: "Explore Collection" & "Request B2B Sample Kit".
3. **Interactive 4K PDP Studio Stage**:
   - Central high-resolution display viewport with click-to-zoom (Lightbox modal).
   - Horizontal product switcher tabs (`Royal Mix`, `Sidr 500g`, `Honeycomb Hex`, `Clover 1kg`, `Black Seed`, `Citrus`).
   - 5 interactive view-angle buttons (`0° Front Hero`, `Open Jar Texture`, `45° Depth Perspective`, `180° Back Regulatory`, `Cap Macro Ribbon`).
   - Dynamic specifications readout: Net Weight, Ingredients, Allergen Alert, Case Pack, Pallet Tier.
4. **Product Collection Bento Grid**:
   - Dedicated luxury cards for each of the 6 core honey SKUs.
   - High-resolution hover-zoom packshot thumbnails.
   - Sensory triads and tasting notes (e.g. "Floral • Velvety • Herbal").
   - Direct sample request button on each card.
5. **Quality, Purity & Laboratory Verification Section**:
   - Codex Alimentarius (Codex Stan 12-1981) export compliance metrics.
   - Certified zero-peanuts facility protocol.
   - Nordic flint glass and royal crown tamper-evident security ribbon specifications.
6. **B2B Wholesale & Commercial Quotation Modal**:
   - Interactive pop-up form allowing importers, distributors, and hotel chefs to request sample shippers, MOQ details, and CIF/FOB export pricing.
7. **Footer**:
   - Company credentials, production facilities, social links, and cross-category site directory.

---

## 6. Testing & Quality Assurance Plan

1. **Automated Unit Tests (`tests/test_honey_page.py`)**:
   - Verify `honey.html` exists and is well-formed HTML.
   - Verify all 6 honey products and 5 view angles are wired with correct image paths.
   - Verify language toggle functions switch between Arabic and English without errors.
   - Verify zero references to unauthorized burgundy logos or generic placeholder text.
2. **Imagery Purity & Resolution Tests (`tests/test_honey_imagery.py`)**:
   - Verify all generated honey packshots exist at exact dimensions (`3000 × 3000` or `3840 × 2160`).
   - Verify all white-studio images pass corner pure-white checks ($RGB \ge 253$).
   - Verify all packshots contain Luxor Gold pixels (`#DAAC36`) and zero burgundy stroke pixels.
3. **HTTP Server & Live Browser Verification**:
   - Verify `http://localhost:8080/honey.html` returns HTTP 200 OK.
   - Verify cross-navigation links between `honey.html`, `website.html`, and `index.html`.
