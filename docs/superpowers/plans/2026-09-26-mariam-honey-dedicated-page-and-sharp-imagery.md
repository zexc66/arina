# Mariam Honey Dedicated Page & Ultra-Sharp 4K Imagery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dedicated, standalone luxury boutique storefront for Mariam Natural Honey & Superfoods (`honey.html`), alongside an ultra-sharp 4K photography processing engine that guarantees razor-sharp packshots with strictly the authentic cursive Luxor Gold logo (`mariam-logo-gold.png` in `#DAAC36`).

**Architecture:** A standalone, responsive HTML5/Tailwind/Vanilla JS storefront (`honey.html`) connected to the platform navigation. A specialized Python image processing script (`scripts/render_ultra_sharp_honey_packshots.py`) applies unsharp masking, bicubic/Lanczos supersampling, seamless 2D inpainting, and pure-white clamping to produce crisp 3000 × 3000 studio imagery.

**Tech Stack:** Python 3 (PIL, OpenCV, NumPy), HTML5, Tailwind CSS, Vanilla JavaScript, Unittest.

**Spec:** `docs/superpowers/specs/2026-09-26-mariam-honey-dedicated-page-and-sharp-imagery-design.md`

## Global Constraints
- Primary Brand Logo: Strictly and exclusively `mariam-logo-gold.png` (`#DAAC36`). No AI typography, no standard fonts, no burgundy logos.
- Studio Background: 100% pure white (`#FFFFFF`) outside contact shadows ($RGB \ge 253$ at corners).
- Image Resolution: Square 4K (`3000 × 3000 px`) for individual packshots, Cinema 4K (`3840 × 2160 px`) for panoramic lineups, saved at JPEG Quality 98+.
- Allergy Policy: 100% Tree Nuts, Zero Peanuts in Mariam Royal Mix.
- Bilingual Support: Instant Arabic (RTL) and English (LTR) toggle without page reloads.
- PDF Prohibition: Under no circumstances generate or modify PDF files.

---

### Task 1: Ultra-Sharp 4K Photography Pipeline & Script

**Files:**
- Create: `scripts/render_ultra_sharp_honey_packshots.py`
- Test: `tests/test_ultra_sharp_honey_imagery.py`
- Output: `output/imagery/mariam_honey_*_4k.jpg`

**Interfaces:**
- Consumes: Raw studio files in brain dir `/home/zexc/.gemini/antigravity/brain/3d8927e4-3c48-4f4b-b899-e68bfea55e7d/` and `mariam-logo-gold.png`.
- Produces: 6 core packshots (3000×3000), 5 view angles for Royal Mix & Sidr, and 1 master panoramic lineup (3840×2160).

- [ ] **Step 1: Write the failing test for ultra-sharp honey packshots**

Create `tests/test_ultra_sharp_honey_imagery.py`:
```python
import os
import unittest
from PIL import Image

class TestUltraSharpHoneyImagery(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.imagery_dir = os.path.join(base_dir, "output", "imagery")
        self.expected_packshots = [
            ("mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_black_seed_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_citrus_blossom_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_sidr_500g_open_jar_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_cap_seal_and_ribbon_macro_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_master_ecommerce_lineup_white_studio_4k.jpg", (3840, 2160)),
        ]

    def test_all_packshots_exist_and_match_dimensions(self):
        for fname, size in self.expected_packshots:
            p = os.path.join(self.imagery_dir, fname)
            self.assertTrue(os.path.exists(p), f"Missing: {fname}")
            with Image.open(p) as im:
                self.assertEqual(im.size, size, f"{fname} size mismatch: {im.size} vs {size}")

    def test_white_studio_corners_pure_white(self):
        for fname, _ in self.expected_packshots:
            p = os.path.join(self.imagery_dir, fname)
            with Image.open(p) as im:
                corners = [
                    im.getpixel((10, 10))[:3],
                    im.getpixel((im.width - 10, 10))[:3],
                    im.getpixel((10, im.height - 10))[:3],
                    im.getpixel((im.width - 10, im.height - 10))[:3],
                ]
                for idx, c in enumerate(corners):
                    self.assertGreaterEqual(min(c), 253, f"{fname} corner {idx+1} not pure white: {c}")

    def test_logo_is_strictly_luxor_gold_and_no_burgundy(self):
        for fname, _ in self.expected_packshots:
            if "lineup" in fname:
                continue
            p = os.path.join(self.imagery_dir, fname)
            with Image.open(p) as im:
                w, h = im.size
                pixels = [im.getpixel((x, y)) for x in range(w//3, 2*w//3, 15) for y in range(h//3, 2*h//3, 15)]
                gold = [px for px in pixels if px[0] > 180 and px[1] > 140 and px[2] < 100]
                exact_burgundy = [px for px in pixels if abs(px[0]-118) < 6 and abs(px[1]-18) < 6 and abs(px[2]-46) < 6]
                self.assertGreater(len(gold), 50, f"{fname} lacks Luxor Gold logo pixels: {len(gold)}")
                self.assertEqual(len(exact_burgundy), 0, f"{fname} contains unauthorized burgundy logo pixels!")

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails or needs script generation**

Run: `python3 -m unittest tests/test_ultra_sharp_honey_imagery.py`

- [ ] **Step 3: Implement `scripts/render_ultra_sharp_honey_packshots.py`**

Write the complete script with:
1. High-frequency unsharp masking (`cv2.addWeighted` or PIL `ImageFilter.UnsharpMask(radius=1.2, percent=135, threshold=3)`).
2. Clean 2D inpainting for Sidr Open, Royal Open, Comb Open, Black Seed, Citrus, and Cap Macro.
3. Authentic Luxor Gold cursive logo (`mariam-logo-gold.png` in `#DAAC36`).
4. Micro-embossing shadow (`RGBA(75, 18, 30, 140)` blur 1.8).
5. Clamping pure white background with soft drop shadow.
6. Multi-packshot compilation.

- [ ] **Step 4: Execute script and verify tests pass**

Run: `python3 scripts/render_ultra_sharp_honey_packshots.py && python3 -m unittest tests/test_ultra_sharp_honey_imagery.py`
Expected: Ran 3 tests -> OK.

- [ ] **Step 5: Commit**

```bash
git add scripts/render_ultra_sharp_honey_packshots.py tests/test_ultra_sharp_honey_imagery.py
git commit -m "feat(imagery): implement ultra-sharp 4K honey photography rendering pipeline"
```

---

### Task 2: Dedicated Honey & Superfoods Storefront (`honey.html`)

**Files:**
- Create: `honey.html`
- Test: `tests/test_honey_page.py`

**Interfaces:**
- Consumes: `output/imagery/mariam_honey_*_4k.jpg`, `mariam-logo-gold.png`, `khaeer-alwadi-logo.png`.
- Produces: Standalone webpage accessible at `http://localhost:8080/honey.html`.

- [ ] **Step 1: Write the failing test for `honey.html`**

Create `tests/test_honey_page.py`:
```python
import os
import unittest

class TestHoneyPage(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.page_path = os.path.join(self.base_dir, "honey.html")

    def test_honey_page_exists_and_has_content(self):
        self.assertTrue(os.path.exists(self.page_path), "honey.html does not exist")
        with open(self.page_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertGreater(len(content), 10000, "honey.html too short")

    def test_required_branding_and_skus(self):
        with open(self.page_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("mariam-logo-gold.png", content)
        self.assertIn("SKU-SF01", content) # Royal Mix
        self.assertIn("SKU-H01", content)  # Sidr
        self.assertIn("SKU-H03", content)  # Honeycomb Hex
        self.assertIn("SKU-H04", content)  # Clover Family
        self.assertIn("SKU-H05", content)  # Black Seed
        self.assertIn("SKU-H02", content)  # Citrus Blossom

    def test_interactive_components_present(self):
        with open(self.page_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("selectHoneyProduct", content)
        self.assertIn("selectHoneyAngle", content)
        self.assertIn("toggleLanguage", content)
        self.assertIn("openSampleModal", content)

    def test_no_burgundy_logo_references(self):
        with open(self.page_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn("wine burgundy cursive", content.lower())

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_honey_page.py`
Expected: FAIL (File not found)

- [ ] **Step 3: Implement `honey.html`**

Build the comprehensive, standalone luxury storefront:
1. Luxury sticky navigation bar with authentic cursive gold logo, Khaeer Alwadi producer crest, links to other categories (`website.html`), and bilingual switch (AR/EN).
2. Hero section with Cinema 4K master panoramic banner and call to action.
3. Interactive 4K PDP Studio Stage: 6 products tabs, 5 view-angle pills, full-screen lightbox modal for zooming in at 3000x3000px.
4. Product Collection Bento Grid: 6 cards with SKU badges, flavor triads, packaging specs, and sample request buttons.
5. Purity & Standards Verification Section (Codex Stan 12-1981, 0% Peanuts, Nordic glass).
6. B2B Wholesale Sample Shipper Request Modal.
7. Footer with company links and cross-navigation.
8. Full bilingual JavaScript controller supporting seamless AR (RTL) / EN (LTR) toggling.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_honey_page.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add honey.html tests/test_honey_page.py
git commit -m "feat(storefront): implement dedicated luxury honey and superfoods storefront"
```

---

### Task 3: Cross-Navigation Integration & Platform Verification

**Files:**
- Modify: `website.html` (Add clear navigation link to `honey.html`)
- Modify: `index.html` (Add link to `honey.html` in Slide 10 and menu)
- Test: Full repository test suite (`tests/test_*.py`)

- [ ] **Step 1: Update navigation in `website.html` and `index.html`**

Add direct links pointing to the dedicated `honey.html` boutique storefront in the header navigation bars and slide 10 callouts.

- [ ] **Step 2: Run all test suites across the repository**

Run: `python3 -m unittest discover -s tests -p "test_*.py"`
Expected: All tests PASS.

- [ ] **Step 3: Verify live HTTP endpoints**

Run:
```bash
python3 -c "
import urllib.request
for url in ['http://localhost:8080/honey.html', 'http://localhost:8080/website.html', 'http://localhost:8080/index.html']:
    res = urllib.request.urlopen(url)
    assert res.status == 200, f'Failed {url}'
    print(f'PASS: {url} (Status {res.status})')
"
```

- [ ] **Step 4: Commit**

```bash
git add website.html index.html
git commit -m "feat(nav): integrate cross-category navigation to dedicated honey storefront"
```

---
