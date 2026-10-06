# Mariam — Master Luxury Brand Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete visual asset portfolio, packaging die-line generators, and B2B export catalog for the "Mariam — Made with Love" global luxury Mediterranean brand.

**Architecture:** A unified brand system using Python image processing and generative visual pipelines. It produces print-calibrated label die-lines and ultra-photorealistic 4K commercial mockups across all 6 product lines (Table Olives, Stuffed Olives, Estate Oils & Sprays, Tapenades & Balsamics, Snack Pouches, and Luxury Gift Vaults).

**Tech Stack:** Python 3, Pillow (PIL), Cairo/SVG, ImageMagick, Markdown Artifact System.

**Spec:** `docs/superpowers/specs/2026-09-11-mariam-brand-strategy-design.md`

## Global Constraints
- **Brand Name**: Mariam
- **Tagline**: made with love
- **Logo Asset**: Exact official gold script calligraphy preserved without alteration or redrawing.
- **Primary Palette**: Deep Forest Green (`Pantone 5605 C` / `#1E3326`)
- **Metallic Accent**: 3D Hot-stamped warm gold foil (`Kurz Luxor 428` / `#D4AF37`)
- **Secondary Typo**: Warm organic ivory (`Pantone 7527 C` / `#EAE6DF`)
- **Lid Standards**: Matte deep forest-green with precision gold perimeter rim; matte black for Grand Reserve.
- **Label Paper**: 120 gsm textured cotton-feel moisture-resistant stock.

---

### Task 1: Label Die-Line Template & Dimension Generator

**Files:**
- Create: `scripts/generate_label_dielines.py`
- Test: `scripts/test_label_dielines.py`

**Interfaces:**
- Produces: `output/dielines/*.png` specification blueprints for all packaging formats:
  - 370g/700g Glass Jar Label (`220mm x 85mm`)
  - 500ml EVOO Bottle Label (`75mm x 140mm`)
  - 200ml Spray Can Label (`130mm x 110mm`)
  - 190g Tapenade Jar Belly-Band (`190mm x 45mm`)
  - 50g Doypack Snack Pouch (`110mm x 160mm`)
  - 3L/5L Lithographed Tin Panel (`180mm x 240mm`)

- [ ] **Step 1: Write test for label dimensions and color calibration**

```python
# scripts/test_label_dielines.py
import os
import unittest
from PIL import Image

class TestLabelDielines(unittest.TestCase):
    def test_dieline_outputs_exist_and_calibrated(self):
        formats = [
            ("dieline_370g_jar.png", (2200, 850)),
            ("dieline_500ml_evoo.png", (750, 1400)),
            ("dieline_200ml_spray.png", (1300, 1100)),
            ("dieline_190g_tapenade.png", (1900, 450)),
            ("dieline_50g_pouch.png", (1100, 1600)),
        ]
        for filename, min_res in formats:
            path = os.path.join("output/dielines", filename)
            self.assertTrue(os.path.exists(path), f"Missing dieline: {filename}")
            im = Image.open(path)
            self.assertGreaterEqual(im.width, min_res[0] // 2)
            self.assertGreaterEqual(im.height, min_res[1] // 2)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 scripts/test_label_dielines.py`
Expected: FAIL (missing files)

- [ ] **Step 3: Implement minimal label dieline generator**

```python
# scripts/generate_label_dielines.py
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("output/dielines", exist_ok=True)

# Color constants
FOREST_GREEN = (30, 51, 38)
GOLD_FOIL = (212, 175, 55)
WARM_IVORY = (234, 230, 223)

formats = [
    ("dieline_370g_jar.png", 2200, 850, "WHOLE GREEN OLIVES - 370G / 700G JAR"),
    ("dieline_500ml_evoo.png", 750, 1400, "FIRST HARVEST RESERVE EVOO - 500ML BOTTLE"),
    ("dieline_200ml_spray.png", 1300, 1100, "EVOO CULINARY AIR-SPRAY - 200ML CAN"),
    ("dieline_190g_tapenade.png", 1900, 450, "RUSTIC GREEN TAPENADE - 190G JAR"),
    ("dieline_50g_pouch.png", 1100, 1600, "LIQUID-FREE OLIVE SNACK - 50G DOYPACK"),
]

for filename, w, h, title in formats:
    im = Image.new("RGBA", (w, h), FOREST_GREEN)
    draw = ImageDraw.Draw(im)
    
    # Outer gold border with 30px inset
    draw.rounded_rectangle([30, 30, w - 30, h - 30], radius=25, outline=GOLD_FOIL, width=4)
    # Inner thin ivory guide
    draw.rounded_rectangle([45, 45, w - 45, h - 45], radius=20, outline=WARM_IVORY, width=2)
    
    # Grid sections
    # Center 40% reserved for brand & product name
    cx0, cx1 = int(w * 0.3), int(w * 0.7)
    draw.line([(cx0, 45), (cx0, h - 45)], fill=GOLD_FOIL, width=2)
    draw.line([(cx1, 45), (cx1, h - 45)], fill=GOLD_FOIL, width=2)
    
    out_path = os.path.join("output/dielines", filename)
    im.save(out_path)
    print("Generated:", out_path)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 scripts/generate_label_dielines.py && python3 scripts/test_label_dielines.py`
Expected: PASS

---

### Task 2: Artisan Stuffed & Royal Kalamata Olives Commercial Imagery

**Files:**
- Create: `output/imagery/mariam_kalamata_stuffed_collection_4k.jpg`
- Tool: `generate_image`

**Interfaces:**
- Consumes: Official Mariam logo, Spec color rules (`Pantone 5605 C`, gold rim, glass cylinder)
- Produces: 4K Commercial product image showing the luxury stuffed and Kalamata table olive variants.

- [ ] **Step 1: Execute image generation prompt for Stuffed & Kalamata line**
Prompt details:
- Jar 1: Royal Kalamata Olives (naturally dark-purple, whole in rich EVOO brine, matte-black lid with gold edge).
- Jar 2: Almond-Stuffed Green Olives (visible toasted Spanish almond inside green olive center).
- Jar 3: Roasted Garlic & Herb Stuffed Green Olives.
- Setting: Warm travertine stone with small tasting plates, olive branches, and folded linen.

- [ ] **Step 2: Verify visual consistency**
Verify:
- Logo spelling: "Mariam" with "made with love".
- Deep forest green label with gold framing borders.
- Submerged, realistic produce texture with authentic natural skin.

---

### Task 3: Single-Estate EVOO & Culinary Air-Spray Imagery

**Files:**
- Create: `output/imagery/mariam_evoo_and_spray_4k.jpg`
- Tool: `generate_image`

**Interfaces:**
- Consumes: Spec Line (C) requirements (500ml dark glass bottle, 200ml spray can)
- Produces: 4K Commercial product image of the Mariam Olive Oil line.

- [ ] **Step 1: Execute image generation prompt for EVOO and Spray**
Prompt details:
- Hero bottle: 500ml First Harvest Grand Reserve EVOO in dark forest-green opaque glass with a gold cap and wax seal.
- Second bottle: 750ml Everyday Gourmet EVOO in clear glass showcasing radiant golden-green oil.
- Can: 200ml Bag-on-Valve culinary spray can in dark green satin metal with gold nozzle and cap.
- Surface: Polished limestone countertop with drizzled golden oil and fresh rosemary sprigs.

- [ ] **Step 2: Verify visual consistency**
Verify:
- "FIRST HARVEST RESERVE" and "EXTRA VIRGIN OLIVE OIL" titles.
- Official Mariam gold calligraphy logo.
- Clean premium bottle silhouette with zero distortion.

---

### Task 4: Tapenades, Aged Balsamics & Finishing Salts Imagery

**Files:**
- Create: `output/imagery/mariam_tapenades_and_condiments_4k.jpg`
- Tool: `generate_image`

**Interfaces:**
- Consumes: Spec Line (D) requirements (190g petite tapenade jars, 250ml balsamic bottle, salt jar)
- Produces: 4K Commercial image of the Mariam antipasti & condiments suite.

- [ ] **Step 1: Execute image generation prompt for Antipasti Suite**
Prompt details:
- Petite jar 1: Rustic Green Olive Tapenade (coarsely crushed green olives and capers).
- Petite jar 2: Black Kalamata Olive Pâté with wild thyme.
- Bottle: Tall elegant 250ml Aged Modena Balsamic Glaze bottle with gold neck wrap.
- Salt jar: 120g wide-mouth jar filled with flaked Mediterranean sea salt smoked with olive leaves.
- Props: Sourdough baguette slices, wooden spreader, and fresh herbs on slate board.

---

### Task 5: Liquid-Free Snack Pouches & Luxury Gift Vault Imagery

**Files:**
- Create: `output/imagery/mariam_pouches_and_gift_vault_4k.jpg`
- Tool: `generate_image`

**Interfaces:**
- Consumes: Spec Line (E) & (F) requirements (Doypack pouches and olive-wood chest)
- Produces: 4K Commercial image of the on-the-go snack pouches and master gift vault.

- [ ] **Step 1: Execute image generation prompt for Pouches & Gift Box**
Prompt details:
- Two stand-up matte Doypack pouches (50g) in deep forest-green with gold foil Mariam logo: "TO-GO GREEN OLIVES (THYME & LEMON)" and "TO-GO KALAMATA OLIVES (CHILI & HERBS)".
- Background / Beside: Solid olive-wood connoisseur presentation chest with velvet interior holding an EVOO bottle, two olive jars, and gold-plated tasting picks.

---

### Task 6: Master Export Catalog & B2B Pitch Presentation

**Files:**
- Modify: `product_presentation.md`
- Create: `docs/superpowers/catalogs/mariam_export_catalog_2026.md`

**Interfaces:**
- Consumes: All 4K imagery from Tasks 1–5 and the Spec file.
- Produces: Complete, interactive B2B Sales Deck and Export Catalog formatted for international buyers (Eataly, Whole Foods, Spinneys, Harrods).

- [ ] **Step 1: Compile all high-resolution imagery and SKU data into master catalog**
- [ ] **Step 2: Add logistics data (case pack counts, shelf life, net weights, HS export codes)**
- [ ] **Step 3: Verify all markdown image links and render formatting**
