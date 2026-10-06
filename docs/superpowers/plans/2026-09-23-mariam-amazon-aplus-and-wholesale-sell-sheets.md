# Mariam Amazon A+ Content & Wholesale Export Sell-Sheets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, render, calibrate, and verify the complete Amazon A+ Content & Infographic Suite (4K) and Wholesale Export Sell-Sheets & Shelf-Talker Blueprints (300 DPI Print-Ready) for Mariam Natural Honey & Superfoods, adhering strictly to authentic brand identity rules, 0% Peanuts policy, heavy glass packaging, and zero PDF prohibition.

**Architecture:** A Python-based graphic compositing and rendering engine (using Pillow with HarfBuzz/Pango text rendering, Lanczos supersampling, alpha masking, and mechanical millimeter-to-pixel calibration at 300 DPI and 4K) to output print-ready PNG/JPEG assets with mechanical crop marks and color bars.

**Tech Stack:** Python 3.10+, Pillow, Pango/HarfBuzz, Unittest.

**Spec:** `docs/superpowers/specs/2026-09-21-mariam-honey-and-superfoods-design.md`

## Global Constraints

- Primary Brand Logo: Strictly the authentic cursive gold logo `mariam-logo-gold.png` (`#DAAC36`).
- Corporate Producer Emblem: `khaeer-alwadi-logo-gold.png` (`#D4A836`).
- Master Palette:
  - Blush Pink: `(232, 197, 200)` / `#E8C5C8` / `#F5B7C2`
  - Wine Burgundy: `(105, 22, 48)` / `#691630` / `#76122E`
  - Luxor Gold: `(218, 172, 54)` / `#DAAC36`
  - Forest Green: `(30, 51, 38)` / `#1E3326`
  - Warm Ivory: `(248, 245, 238)` / `#F8F5EE`
- PDF Prohibition: Under no circumstances generate or modify PDF files. All printable assets must be 300 DPI PNG/JPEG.
- Packaging Constraint: Glass jars only (zero pouches, zero spray cans).
- Allergy Standard: 0% Peanuts certified guarantee prominently displayed on all Royal Mix assets.

---

## File Structure Map

```
New Folder/
├── scripts/
│   ├── build_amazon_aplus_suite.py            # Task 1: 4K Amazon A+ content & infographics
│   └── build_wholesale_sell_sheets.py          # Task 2: 300 DPI B2B trade sell-sheet & shelf-talkers
├── tests/
│   └── test_amazon_aplus_and_sell_sheets.py    # Task 3: Comprehensive automated validation
└── output/
    └── imagery/
        ├── mariam_amazon_aplus_01_brand_story_hero_4k.jpg
        ├── mariam_amazon_aplus_02_card_tree_nuts_purity_4k.jpg
        ├── mariam_amazon_aplus_03_card_nordic_glass_4k.jpg
        ├── mariam_amazon_aplus_04_card_raw_enzymes_4k.jpg
        ├── mariam_amazon_aplus_05_comparison_matrix_chart_4k.jpg
        ├── mariam_amazon_aplus_06_functional_wellness_infographic_4k.jpg
        ├── mariam_honey_b2b_trade_sell_sheet_300dpi.png
        ├── mariam_shelf_talker_royal_mix_300dpi.png
        ├── mariam_shelf_talker_mountain_sidr_300dpi.png
        ├── mariam_shelf_talker_honeycomb_hex_300dpi.png
        ├── mariam_shelf_talker_clover_1kg_300dpi.png
        └── mariam_shelf_talkers_master_press_sheet_300dpi.png
```

---

### Task 1: Amazon A+ Content & Infographic Suite Renderer (4K)

**Files:**
- Create: `scripts/build_amazon_aplus_suite.py`
- Test: `tests/test_amazon_aplus_and_sell_sheets.py`

**Interfaces:**
- Consumes: `output/imagery/mariam_honey_*_4k.jpg`, `mariam-logo-gold.png`.
- Produces: 6 high-converting Amazon A+ modules in Cinema 4K.

- [ ] **Step 1: Write test for Amazon A+ module dimensions and brand logo presence**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `scripts/build_amazon_aplus_suite.py`**
- [ ] **Step 4: Run script and verify 6 4K images are generated**
- [ ] **Step 5: Verify test passes**

---

### Task 2: Wholesale Export Sell-Sheets & Shelf-Talkers Generator (300 DPI)

**Files:**
- Create: `scripts/build_wholesale_sell_sheets.py`
- Test: `tests/test_amazon_aplus_and_sell_sheets.py`

**Interfaces:**
- Consumes: `data/mariam_honey_catalog.json`, `output/imagery/mariam_honey_*_4k.jpg`, `mariam-logo-gold.png`.
- Produces: 300 DPI A4 technical sell sheet and gondola shelf-talker strips with crop marks.

- [ ] **Step 1: Write test for sell-sheet dimensions (3508 × 2480 px @ 300 DPI) and shelf-talkers (2480 × 448 px @ 300 DPI)**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement `scripts/build_wholesale_sell_sheets.py`**
- [ ] **Step 4: Run script and verify all 300 DPI print-ready files exist**
- [ ] **Step 5: Verify test passes**

---

### Task 3: Full Automated Verification & Visual Review

**Files:**
- Modify/Extend: `tests/test_amazon_aplus_and_sell_sheets.py`

- [ ] **Step 1: Run complete test suite across all 47+ tests**
- [ ] **Step 2: Visually verify rendered print sheets and 4K Amazon banners**
- [ ] **Step 3: Commit and generate walkthrough**
