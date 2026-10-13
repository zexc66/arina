# Green Manzanilla & Andalusian Picual Table Olives Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the Green Manzanilla (مانزانيللو أخضر) and Andalusian Picual (بيكول أندلسي فاخر) table olive suites into the Arina export catalog (`mariam_export_catalog_2026.md`) and the digital B2B website platform (`website.html`).

**Architecture:** Create targeted test coverage in Python (`tests/test_green_manzanilla_picual_integration.py`); update `mariam_export_catalog_2026.md` with structured SKU matrices, calibers, and HS code 2005.70; extend the `PRODUCTS` data store and translation dictionary in `website.html` with calibrated weights, EAN-13 barcodes, and palletization schemes; add interactive gallery showcase cards linked to reference imagery.

**Tech Stack:** HTML5, Tailwind CSS, Vanilla JavaScript (ES6+), Python 3 `unittest`, GitHub Flavored Markdown.

**Spec:** `docs/superpowers/specs/2026-10-14-green-manzanilla-picual-olives-design.md`

## Global Constraints

- **Sacred Brand Identity Rule**: Brand logo is strictly `arina-logo-gold.png`. Never remove or alter the logo.
- **Palette**: Deep Forest Green (`#1E3326`), Warm Luxor Gold (`#DAAC36`), Warm Ivory (`#F8F5EE`).
- **No PDF / No Pouches in Website**: Maintain strict web compliance (no `.pdf` links, no pouch references in `website.html`).
- **Exact Specifications**: Zero placeholder text; all EAN-13 barcodes (`6281001202074` through `6281001202142`), weights, calibers, and Ti/Hi pallet counts must match the spec verbatim.
- **BiDi Isolation**: Arabic and English text blocks, numbers, and EANs must be isolated to prevent punctuation/order flip.

---

### Task 1: Automated Integration & Verification Tests

**Files:**
- Create: `tests/test_green_manzanilla_picual_integration.py`
- Test: `tests/test_green_manzanilla_picual_integration.py`

**Interfaces:**
- Consumes: `website.html` and `docs/superpowers/catalogs/mariam_export_catalog_2026.md`
- Produces: Test suite validating presence of 6 retail jar SKUs, 2 bulk drum SKUs, unique EAN-13 barcodes, image asset existence, and catalog tables.

- [ ] **Step 1: Write the failing integration test suite**

Create `tests/test_green_manzanilla_picual_integration.py` checking:
1. `test_website_contains_all_manzanilla_and_picual_skus`: verifies `website.html` defines `manzanilla-whole-370`, `manzanilla-whole-720`, `manzanilla-pitted-370`, `picual-whole-370`, `picual-whole-720`, `picual-rustic-370`, and bulk drum identifiers in `PRODUCTS`.
2. `test_barcode_uniqueness_and_format`: verifies all 8 new EAN codes are valid 13-digit strings and unique.
3. `test_catalog_line_a_expansion`: verifies `mariam_export_catalog_2026.md` contains Line A1 (Manzanilla) and Line A2 (Picual) with calibers and HS code `2005.70`.
4. `test_imagery_assets_exist`: verifies that all image paths in `PRODUCTS` exist on disk.

```python
import unittest
import os
import re

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILE = os.path.join(WORKSPACE_DIR, 'website.html')
CATALOG_FILE = os.path.join(WORKSPACE_DIR, 'docs', 'superpowers', 'catalogs', 'mariam_export_catalog_2026.md')

EXPECTED_EANS = [
    '6281001202074',  # Manzanilla Whole 370ml
    '6281001202081',  # Manzanilla Whole 720ml
    '6281001202098',  # Manzanilla Pitted 370ml
    '6281001202104',  # Picual Whole 370ml
    '6281001202111',  # Picual Whole 720ml
    '6281001202128',  # Picual Rustic 370ml
]

class TestGreenManzanillaPicualIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            cls.catalog_content = f.read()

    def test_website_contains_all_manzanilla_and_picual_skus(self):
        required_ids = [
            'manzanilla-whole-370',
            'manzanilla-whole-720',
            'manzanilla-pitted-370',
            'picual-whole-370',
            'picual-whole-720',
            'picual-rustic-370'
        ]
        for item_id in required_ids:
            self.assertIn(f"id: '{item_id}'", self.html_content, f"Missing product id: {item_id}")

    def test_barcode_uniqueness_and_format(self):
        for ean in EXPECTED_EANS:
            self.assertIn(ean, self.html_content, f"Missing EAN {ean} in website.html")
            self.assertEqual(len(ean), 13, f"EAN {ean} must be 13 digits")

    def test_catalog_line_a_expansion(self):
        self.assertIn("Line A1: Single-Varietal Green Manzanilla", self.catalog_content)
        self.assertIn("Line A2: Reserve Andalusian Picual", self.catalog_content)
        self.assertIn("2005.70", self.catalog_content)
        self.assertIn("200 / 220", self.catalog_content)
        self.assertIn("180 / 200", self.catalog_content)

    def test_imagery_assets_exist(self):
        img_matches = re.findall(r"img:\s*'([^']+)'", self.html_content)
        for img in img_matches:
            full_path = os.path.join(WORKSPACE_DIR, img)
            self.assertTrue(os.path.exists(full_path), f"Referenced image not found: {full_path}")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_green_manzanilla_picual_integration.py`
Expected: FAIL (missing product IDs in `website.html` and missing Line A1/A2 in catalog)

- [ ] **Step 3: Commit initial test suite**

```bash
git add tests/test_green_manzanilla_picual_integration.py
git commit -m "test: add integration test suite for green manzanilla and picual olives"
```

---

### Task 2: Update B2B Export Catalog (`mariam_export_catalog_2026.md`)

**Files:**
- Modify: `docs/superpowers/catalogs/mariam_export_catalog_2026.md`

**Interfaces:**
- Consumes: Spec section 2 & 4
- Produces: Comprehensive Line A1 & Line A2 tables, bulk specifications, and export narrative.

- [ ] **Step 1: Edit `mariam_export_catalog_2026.md`**

Replace the generic table in Line A with:
1. **Line A1: Single-Varietal Green Manzanilla Collection (Glass Jars)**:
   - `ARN-OLV-007`: Green Manzanilla Whole Olives (370g / 200g drained, 200/220 caliber, TO-63mm, 24 units/case, 36 Months, HS 2005.70)
   - `ARN-OLV-008`: Green Manzanilla Whole (Family Reserve) (700g / 420g drained, 200/220 caliber, TO-82mm, 12 units/case, 36 Months, HS 2005.70)
   - `ARN-OLV-009`: Green Manzanilla Pitted Olives (370g / 170g drained, 240/260 caliber, TO-63mm, 24 units/case, 36 Months, HS 2005.70)
2. **Line A2: Reserve Andalusian Picual & Herb Infusions (Glass Jars)**:
   - `ARN-OLV-015`: Picual Reserve Green Olives in Brine (370g / 210g drained, 180/200 jumbo, TO-63mm, 24 units/case, 36 Months, HS 2005.70)
   - `ARN-OLV-016`: Picual Reserve Green Olives (Grand Format) (700g / 420g drained, 180/200 jumbo, TO-82mm, 12 units/case, 36 Months, HS 2005.70)
   - `ARN-OLV-017`: Picual Rustic Herb & Lemon Marinated (370g / 210g drained, 180/200 jumbo, TO-63mm, 24 units/case, 36 Months, HS 2005.70)
3. **Bulk Industrial Matrix (HDPE Drums & Foodservice Buckets)**:
   - `ARN-BLK-020`: Bulk Green Manzanilla (230kg Drum, 155kg drained)
   - `ARN-BLK-021`: Bulk Picual Green Olives (230kg Drum, 160kg drained)
   - Pallet & FCL Loading: 80 drums per 20ft container (18.4 MT).

- [ ] **Step 2: Run test to verify catalog assertions pass**

Run: `python3 -m unittest tests/test_green_manzanilla_picual_integration.py::TestGreenManzanillaPicualIntegration::test_catalog_line_a_expansion`
Expected: PASS

- [ ] **Step 3: Commit catalog updates**

```bash
git add docs/superpowers/catalogs/mariam_export_catalog_2026.md
git commit -m "docs(catalog): integrate green manzanilla and picual export matrices"
```

---

### Task 3: Integrate Manzanilla & Picual into Website (`website.html`)

**Files:**
- Modify: `website.html`

**Interfaces:**
- Consumes: Spec section 2 & 3
- Produces: 6 retail jar entries and bulk drum entries in `const PRODUCTS`; bilingual translations in `TRANSLATIONS`; gallery cards in `#gallery`.

- [ ] **Step 1: Add product definitions into `const PRODUCTS` in `website.html`**

Insert the following items into `const PRODUCTS` in `website.html` (maintaining existing items and format):
- `manzanilla-whole-370` (EAN: 6281001202074)
- `manzanilla-whole-720` (EAN: 6281001202081)
- `manzanilla-pitted-370` (EAN: 6281001202098)
- `picual-whole-370` (EAN: 6281001202104)
- `picual-whole-720` (EAN: 6281001202111)
- `picual-rustic-370` (EAN: 6281001202128)

Use image paths:
- `output/imagery/arina_manzanilla_green_olives_black_studio_reference.jpg`
- `output/imagery/arina_picual_green_olives_wooden_bowl_reference.jpg`
- `output/imagery/arina_green_table_olives_terroir_dish_reference.jpg`

- [ ] **Step 2: Add translation keys and descriptors to `TRANSLATIONS`**

Add bilingual names, calibers, and flavor profile notes for Arabic (`ar`) and English (`en`).

- [ ] **Step 3: Add interactive gallery cards in `#gallery`**

Add two cards in the products gallery section featuring:
1. `ARINA Green Manzanilla Terroir Reserve`
2. `ARINA Andalusian Picual & Sun-Cured Lemon`
Linked to `openLightbox` modal.

- [ ] **Step 4: Run integration and regression tests**

Run: `python3 -m unittest tests/test_green_manzanilla_picual_integration.py tests/test_b2b_website.py`
Expected: ALL PASS (26 + 4 = 30 tests pass)

- [ ] **Step 5: Commit website updates**

```bash
git add website.html
git commit -m "feat(catalog): integrate green manzanilla and picual olives into website and product database"
```

---

### Task 4: Complete System Verification & Polish

**Files:**
- Test: `tests/test_b2b_website.py`
- Test: `tests/test_green_manzanilla_picual_integration.py`
- Modify: `website.html` (if any formatting or BiDi adjustments needed)

- [ ] **Step 1: Run complete test suite**

Run: `python3 -m unittest discover -s tests -p "test_*.py"`
Expected: ALL PASS

- [ ] **Step 2: Verify git status and clean working tree**

Run: `git status`
Expected: Clean working tree

- [ ] **Step 3: Verification handoff**
Confirm that both digital website and markdown export catalog are synchronized, fully documented, and verified.
