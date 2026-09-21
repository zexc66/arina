# Mariam Natural Honey & Superfoods Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, calibrate, and verify the packaging dieline generation engine, structured catalog data layer, and automated test suite for the new Mariam Natural Honey & Superfoods product portfolio (featuring 500g & 1kg standards and the Hero Royal Mix).

**Architecture:** A Python-driven graphic compositing engine (using Pillow with antialiasing and exact mechanical millimeters-to-pixel calibration) that generates print-ready packaging label dielines across all honey and superfood formats, backed by a validated JSON catalog data layer and an automated pytest test suite.

**Tech Stack:** Python 3.10+, Pillow (PIL), Pytest, JSON.

**Spec:** `docs/superpowers/specs/2026-09-21-mariam-honey-and-superfoods-design.md`

## Global Constraints

- Primary Brand Logo: Strictly the authentic cursive gold logo `mariam-logo-gold.png` (`#DAAC36`).
- Sub-Brand Descriptor: `NATURAL HONEY & SUPERFOODS`.
- Tamper Ribbon Standard: Width 18mm, length 45mm, Mariam Blush Pink (`#E8C5C8`), with embossed Luxor Gold Crown Seal (`#DAAC36`).
- Core Packaging Standard: **500g (Standard Primary)** and **1kg (Family/Commercial)** across honey and superfood lines.
- Master Palette:
  - Blush Pink: `(232, 197, 200)` / `#E8C5C8`
  - Imperial Burgundy: `(105, 22, 48)` / `#691630`
  - Luxor Gold: `(218, 172, 54)` / `#DAAC36`
  - Warm Ivory: `(248, 245, 238)` / `#F8F5EE`
- PDF Prohibition: Under no circumstances generate or modify PDF files.

---

## File Structure Map

```
New Folder/
├── data/
│   └── mariam_honey_catalog.json           # Task 1: Complete 25+ SKU metadata, formulas & weights
├── scripts/
│   └── generate_honey_dielines.py          # Task 2: High-resolution packaging dieline generator
├── tests/
│   ├── test_honey_catalog.py               # Task 1: Validation of catalog formulas & constraints
│   └── test_honey_dielines.py              # Task 3: Mechanical dimensions and color calibration tests
└── output/
    └── dielines/
        ├── dieline_honey_500g_standard.png  # Task 2: 500g Cylindrical Honey Jar Dieline
        ├── dieline_honey_1kg_family.png     # Task 2: 1kg Family Bulk Honey Jar Dieline
        ├── dieline_royal_mix_500g_wide.png  # Task 2: Royal Mix 500g Wide-Mouth Heavy Base Dieline
        ├── dieline_honeycomb_500g_hex.png   # Task 2: 500g Hexagonal Comb Jar Dieline
        ├── dieline_tamper_ribbon_crown.png  # Task 2: Blush Pink 18x45mm Tamper Ribbon with Crown
        └── dieline_discovery_flight_50g.png # Task 2: 50g Petite Tasting Flight Belly-Band
```

---

### Task 1: Structured Product Catalog Data Model & Validation

**Files:**
- Create: `data/mariam_honey_catalog.json`
- Create: `tests/test_honey_catalog.py`

**Interfaces:**
- Consumes: Specifications from `docs/superpowers/specs/2026-09-21-mariam-honey-and-superfoods-design.md`.
- Produces: `data/mariam_honey_catalog.json` consumed by dieline scripts, website, and commercial sheets.

- [ ] **Step 1: Write the failing test for catalog schema and constraints**

```python
# tests/test_honey_catalog.py
import json
import os
import unittest

class TestMariamHoneyCatalog(unittest.TestCase):
    def setUp(self):
        self.catalog_path = "data/mariam_honey_catalog.json"

    def test_catalog_file_exists_and_valid_json(self):
        self.assertTrue(os.path.exists(self.catalog_path), "Catalog file does not exist")
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("brand", data)
        self.assertEqual(data["brand"], "Mariam")
        self.assertEqual(data["category"], "Natural Honey & Superfoods")
        self.assertIn("families", data)

    def test_core_launch_skus_present(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        skus = {item["sku"]: item for family in data["families"] for item in family["items"]}
        required_skus = ["SKU-SF01", "SKU-H03", "SKU-H01", "SKU-H02", "SKU-H05", "SKU-H06", "SKU-SF02", "SKU-FN01", "SKU-GF01", "SKU-GF02"]
        for r in required_skus:
            self.assertIn(r, skus, f"Missing required launch SKU: {r}")

    def test_royal_mix_contains_zero_peanuts(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        skus = {item["sku"]: item for family in data["families"] for item in family["items"]}
        royal_mix = skus["SKU-SF01"]
        for ingredient in royal_mix["ingredients"]:
            self.assertNotIn("peanut", ingredient.lower(), "Royal Mix must have 0% peanuts")

    def test_standard_sizes_include_500g_and_1kg(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        skus = {item["sku"]: item for family in data["families"] for item in family["items"]}
        clover = skus["SKU-H01"]
        self.assertIn("500g", clover["sizes"])
        self.assertIn("1kg", clover["sizes"])

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_honey_catalog.py`
Expected: FAIL (File not found `data/mariam_honey_catalog.json`)

- [ ] **Step 3: Implement `data/mariam_honey_catalog.json`**

Create `data/mariam_honey_catalog.json` populated with all 6 product families and detailed metadata for the 25+ SKUs, explicitly including `500g` and `1kg` size arrays, ingredients, allergens, and flavor profiles.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_honey_catalog.py`
Expected: PASS (4 tests passed)

- [ ] **Step 5: Commit**

```bash
git add data/mariam_honey_catalog.json tests/test_honey_catalog.py
git commit -m "feat(catalog): add Mariam Natural Honey & Superfoods catalog data model and tests"
```

---

### Task 2: Master Packaging Dieline Generator for Honey & Superfoods

**Files:**
- Create: `scripts/generate_honey_dielines.py`
- Outputs: `output/dielines/dieline_honey_*.png`

**Interfaces:**
- Consumes: `mariam-logo-gold.png`, `data/mariam_honey_catalog.json`.
- Produces: 6 print-calibrated PNG dieline blueprints with registration crosshairs, mechanical dimensions, zones, and authentic cursive logo.

- [ ] **Step 1: Write `scripts/generate_honey_dielines.py`**

Implement Python script using Pillow to generate:
1. `dieline_honey_500g_standard.png` (2200 × 900 px @ 254 DPI, physical 220mm × 90mm).
2. `dieline_honey_1kg_family.png` (2600 × 1100 px @ 254 DPI, physical 260mm × 110mm).
3. `dieline_royal_mix_500g_wide.png` (2400 × 850 px @ 254 DPI, physical 240mm × 85mm).
4. `dieline_honeycomb_500g_hex.png` (1800 × 900 px @ 254 DPI, physical 180mm × 90mm).
5. `dieline_tamper_ribbon_crown.png` (450 × 1125 px @ 254 DPI, physical 18mm × 45mm Blush Pink with Crown).
6. `dieline_discovery_flight_50g.png` (1200 × 400 px @ 254 DPI, physical 120mm × 40mm).

Includes:
- Warm Ivory / Blush Pink / Imperial Burgundy palettes.
- Genuine `mariam-logo-gold.png` scaled with antialiasing.
- Mechanical guides: Cut line, Safe margin (30px inset), Zone dividers, and Registration crosshairs.

- [ ] **Step 2: Run script to generate all dielines**

Run: `python3 scripts/generate_honey_dielines.py`
Expected: 6 PNG files generated in `output/dielines/`.

- [ ] **Step 3: Commit**

```bash
git add scripts/generate_honey_dielines.py
git commit -m "feat(dielines): implement honey and superfood packaging dieline generator"
```

---

### Task 3: Automated Packaging Dieline Test Suite

**Files:**
- Create: `tests/test_honey_dielines.py`

**Interfaces:**
- Consumes: `output/dielines/dieline_honey_*.png`, `dieline_royal_mix_*.png`, `dieline_tamper_ribbon_crown.png`.
- Produces: Test results verifying resolution, aspect ratios, and brand color presence.

- [ ] **Step 1: Write `tests/test_honey_dielines.py`**

```python
# tests/test_honey_dielines.py
import os
import unittest
from PIL import Image

class TestHoneyDielines(unittest.TestCase):
    def setUp(self):
        self.output_dir = "output/dielines"
        self.expected_formats = [
            ("dieline_honey_500g_standard.png", (2200, 900)),
            ("dieline_honey_1kg_family.png", (2600, 1100)),
            ("dieline_royal_mix_500g_wide.png", (2400, 850)),
            ("dieline_honeycomb_500g_hex.png", (1800, 900)),
            ("dieline_tamper_ribbon_crown.png", (450, 1125)),
            ("dieline_discovery_flight_50g.png", (1200, 400)),
        ]
        self.blush_pink = (232, 197, 200)
        self.burgundy = (105, 22, 48)
        self.gold_foil = (218, 172, 54)

    def test_dielines_exist_and_match_dimensions(self):
        for filename, expected_size in self.expected_formats:
            path = os.path.join(self.output_dir, filename)
            self.assertTrue(os.path.exists(path), f"Missing dieline: {filename}")
            with Image.open(path) as im:
                self.assertEqual(im.size, expected_size, f"{filename} size mismatch: {im.size} vs {expected_size}")

    def test_brand_colors_present_in_tamper_ribbon(self):
        ribbon_path = os.path.join(self.output_dir, "dieline_tamper_ribbon_crown.png")
        with Image.open(ribbon_path) as im:
            rgb_im = im.convert("RGB")
            colors = rgb_im.getcolors(maxcolors=im.width * im.height)
            unique_rgb = {c[1] for c in colors}
            # Check Blush Pink background
            self.assertIn(self.blush_pink, unique_rgb, "Blush Pink missing from tamper ribbon")
            # Check Gold Foil crown seal
            self.assertIn(self.gold_foil, unique_rgb, "Luxor Gold missing from tamper ribbon")

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python3 -m unittest tests/test_honey_dielines.py`
Expected: PASS (All assertions pass)

- [ ] **Step 3: Commit**

```bash
git add tests/test_honey_dielines.py output/dielines/
git commit -m "test(dielines): add automated verification suite for honey and superfood dielines"
```

---

### Task 4: Showcase Integration in Mariam Catalog Web Page

**Files:**
- Modify: `mariam.html` (or dedicated section component)

**Interfaces:**
- Consumes: Catalog items from `data/mariam_honey_catalog.json`.
- Produces: Rendered interactive Honey & Superfoods section with 500g and 1kg toggle and Hero Royal Mix spotlight.

- [ ] **Step 1: Write test for web page containing Honey & Superfoods section**

Create a test in `tests/test_web_catalog.py` that verifies `mariam.html` contains:
- `MARIAM ROYAL MIX`
- `Natural Honey & Superfoods`
- `500g` & `1kg` size indicators
- The authentic logo reference `mariam-logo-gold.png`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_web_catalog.py`
Expected: FAIL

- [ ] **Step 3: Add Honey & Superfoods suite to `mariam.html`**

Insert the luxury presentation cards for the new product family, featuring:
- Hero banner for Mariam Royal Mix.
- Product grid with 500g / 1kg switcher.
- Blush and burgundy styling matching the master palette.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_web_catalog.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add mariam.html tests/test_web_catalog.py
git commit -m "feat(web): integrate Natural Honey & Superfoods collection into Mariam catalog"
```

---

## Execution Handoff Choice

Plan complete and saved to `docs/superpowers/plans/2026-09-21-mariam-honey-and-superfoods-implementation.md`.
