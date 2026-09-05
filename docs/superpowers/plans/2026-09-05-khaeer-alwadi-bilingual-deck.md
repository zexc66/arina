# Khaeer Alwadi Bilingual B2B Sales Deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an executive, fully self-contained, interactive bilingual (Arabic RTL & English LTR) 16:9 B2B sales presentation deck for Khaeer Alwadi Food Industries (`index.html`), while preserving the Mariam deck in `mariam.html`.

**Architecture:** Dual-DOM declarative localization architecture with live directionality (`dir="rtl"` / `dir="ltr"`) toggled via `#nav-dock` pill and keyboard shortcut `L`. High-end agency aesthetic with double-bezel card geometry, tactile micro-physics, custom Cairo/Plus Jakarta typography, and landscape A4 print-to-PDF engine.

**Tech Stack:** HTML5, Tailwind CSS (via CDN), Lucide Icons, Google Fonts (`Cairo`, `Plus Jakarta Sans`, `JetBrains Mono`), Python Pillow for logo asset extraction, Python `unittest` for structural verification.

**Spec:** [`docs/superpowers/specs/2026-09-05-khaeer-alwadi-bilingual-deck-design.md`](file:///home/zexc/Desktop/New%20Folder/docs/superpowers/specs/2026-09-05-khaeer-alwadi-bilingual-deck-design.md)

## Global Constraints

- **Brand Names:** "خير الوادي للصناعات الغذائية" (Arabic) and "Khaeer Alwadi Food Industries" (English)
- **Headquarters Location:** Cairo, Egypt
- **Direct Procurement Desk / WhatsApp:** `+20 10 08716714` (active links `https://wa.me/201008716714` and `tel:+201008716714`)
- **Active Certifications:** ISO 22000, HACCP, FDA Registered (US FSMA), Halal, ISO 9001
- **Color Tokens:** Valley Green (`#2D5232`, `#3D6B42`), Harvest Gold (`#D4A836`, `#C29B44`), Kalamata Obsidian (`#181116`, `#2C1A27`), Background OLED Canvas (`#091410` via `#0E1F17` to `#050907`)
- **Canvas Ratio:** 16:9 widescreen presentation canvas (`aspectRatio: 16/9`) auto-scaling with viewport
- **Self-Contained & Offline:** Operates offline with local asset paths; zero network dependencies for core presentation

---

### Task 1: Preserve Mariam Deck and Extract Khaeer Alwadi Logo Assets

**Files:**
- Create: `mariam.html` (verbatim copy of current `index.html`)
- Create: `khaeer-alwadi-logo.png` (high-res 2x Retina transparent logo asset)
- Create: `khaeer-alwadi-logo-gold.png` (gold metallic silhouette/accent edition)
- Test: `tests/test_deck_structure.py`

**Interfaces:**
- Consumes: `/home/zexc/.gemini/antigravity/brain/11b18b7f-b6fc-44c3-b411-4191383aeaa1/.user_uploaded/media_1788619834322.jpg`
- Produces: `mariam.html`, `khaeer-alwadi-logo.png`, `khaeer-alwadi-logo-gold.png`

- [ ] **Step 1: Write test asserting existence of `mariam.html` and logo assets**

```python
# In tests/test_deck_structure.py
def test_mariam_deck_preserved():
    assert os.path.exists("mariam.html"), "mariam.html must exist as a preserved copy of the Mariam deck"
    with open("mariam.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "Mariam Food Industries" in html, "mariam.html must contain Mariam Food Industries branding"

def test_khaeer_alwadi_logo_assets():
    assert os.path.exists("khaeer-alwadi-logo.png"), "khaeer-alwadi-logo.png must exist"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: FAIL (`mariam.html` or `khaeer-alwadi-logo.png` does not exist)

- [ ] **Step 3: Copy `index.html` to `mariam.html` and extract logo via Python Pillow**

```bash
cp index.html mariam.html
```

Execute Python script to crop bounding box `(280, 330, 710, 680)` from `media_1788619834322.jpg`, deconvolve white background to clean alpha channel, and save `khaeer-alwadi-logo.png` and `khaeer-alwadi-logo-gold.png`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add mariam.html khaeer-alwadi-logo.png khaeer-alwadi-logo-gold.png tests/test_deck_structure.py
git commit -m "feat: preserve mariam.html and extract official Khaeer Alwadi logo assets"
```

---

### Task 2: Scaffold Bilingual Shell, RTL Engine & Updated Navigation Dock in `index.html`

**Files:**
- Modify: `index.html`
- Modify: `tests/test_deck_structure.py`

**Interfaces:**
- Consumes: `khaeer-alwadi-logo.png`, `khaeer-alwadi-logo-gold.png`
- Produces: Global functions `toggleLanguage()`, `setLanguage(lang)`, reactive bilingual CSS rules (`.lang-en`, `.lang-ar`, `html[dir="rtl"]`, `html[dir="ltr"]`), 16:9 canvas with Tailwind palette

- [ ] **Step 1: Write test for bilingual shell and RTL toggle**

```python
def test_bilingual_shell_and_branding():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "khaeer-alwadi-logo.png" in html, "Logo must be referenced in index.html"
    assert "خير الوادي" in html, "Arabic brand name must exist"
    assert "Khaeer Alwadi" in html, "English brand name must exist"
    assert 'id="nav-dock"' in html, "Navigation dock must exist"
    assert "toggleLanguage" in html, "toggleLanguage function must be defined in index.html"
    assert "lang-ar" in html and "lang-en" in html, "Bilingual CSS classes must exist"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: FAIL

- [ ] **Step 3: Implement bilingual shell and Tailwind configuration in `index.html`**

Configure Tailwind theme colors (`valley`, `gold`, `kalamata`, `charcoal`), embed Google Fonts (`Cairo`, `Plus Jakarta Sans`, `JetBrains Mono`), implement bilingual CSS hiding rules, and add the `EN | عربي` toggle pill to `#nav-dock`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: scaffold bilingual presentation shell and RTL engine for Khaeer Alwadi"
```

---

### Task 3: Implement Bilingual Slide 1 (Cover), Slide 2 (Supply Advantage) & Slide 3 (Infrastructure)

**Files:**
- Modify: `index.html`
- Modify: `tests/test_deck_structure.py`

**Interfaces:**
- Consumes: `khaeer-alwadi-logo.png`, `WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg`, `WhatsApp Image 2026-09-05 at 12.52.17 PM.jpeg`
- Produces: Fully translated Slide 1, Slide 2, and Slide 3 with dual English & Arabic markup

- [ ] **Step 1: Write test for Slides 1–3 bilingual content**

```python
def test_bilingual_slides_1_to_3():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "ISO 22000" in html and "HACCP" in html and "FDA" in html
    assert "Alexandria" in html and "الإسكندرية" in html
    assert "Damietta" in html and "دمياط" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: FAIL

- [ ] **Step 3: Implement Slides 1, 2, and 3 in `index.html`**

- **Slide 1:** Official logo, dual-language headings, 4 trust pillars, WhatsApp strip, and hero glass jar card.
- **Slide 2:** 15–25% landed cost advantage, Tri-Port proximity corridor (Alexandria, Damietta, Port Said), and free-trade pacts (GAFTA, COMESA, Agadir, EU).
- **Slide 3:** High-volume automated pitting lines, rotary slicing, autoclave retort sterilization ($F_0 \ge 4.0$), and 5 international compliance badges.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: implement bilingual slides 1, 2, and 3 for Khaeer Alwadi"
```

---

### Task 4: Implement Bilingual Slide 4 (Table Olives) & Slide 5 (Pickles & Specialty Peppers)

**Files:**
- Modify: `index.html`
- Modify: `tests/test_deck_structure.py`

**Interfaces:**
- Consumes: Macro olive & pickle photography (`12.52.20 PM.jpeg`, `12.52.17 PM (5).jpeg`, `12.52.16 PM (2).jpeg`, `12.52.18 PM (2).jpeg`, etc.)
- Produces: Bilingual product cards with dual-language technical chips (calibers, salinity, pH, drained weight)

- [ ] **Step 1: Write test for Slides 4 & 5 bilingual products**

```python
def test_bilingual_slides_4_and_5():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "Picual" in html or "بيكوال" in html
    assert "Pimento" in html or "بيمنتو" in html
    assert "Pepperoncini" in html or "بيبرونشيني" in html
    assert "Turshi" in html or "طرشي" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.20 PM.jpeg" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: FAIL

- [ ] **Step 3: Implement Slides 4 and 5 in `index.html`**

- **Slide 4 (Olives):** Sliced black olives, mechanically pitted olives, green olives, pimento-stuffed olives, and Kalamata dark olives. Calibers 200/220, 240/260, 280/300, drained weight $\ge 52\%$.
- **Slide 5 (Pickles):** Golden pepperoncini, red hot chilis, traditional Turshi Baladi, and crunchy cucumbers. Acidity pH 3.2–3.6, salinity 3.5%–5.0%.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: implement bilingual slides 4 and 5 for Khaeer Alwadi"
```

---

### Task 5: Implement Bilingual Slide 6 (Packaging Architecture) & Slide 7 (Private Label & OEM)

**Files:**
- Modify: `index.html`
- Modify: `tests/test_deck_structure.py`

**Interfaces:**
- Consumes: Packaging photography (`12.52.17 PM (7).jpeg`, `12.52.17 PM (4).jpeg`, `12.52.15 PM (5).jpeg`, etc.)
- Produces: 4 packaging tier cards and 6-stage turnkey OEM contract manufacturing workflow

- [ ] **Step 1: Write test for Slides 6 & 7 packaging and OEM**

```python
def test_bilingual_slides_6_and_7():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "A10" in html
    assert "150kg" in html or "220kg" in html
    assert "Private Label" in html or "التصنيع للغير" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.17 PM (7).jpeg" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: FAIL

- [ ] **Step 3: Implement Slides 6 and 7 in `index.html`**

- **Slide 6:** Institutional A10 metal cans, 150kg–220kg polymer drums, crystal glass jars (370–1,000ml), and export pallets.
- **Slide 7:** 6-stage turnkey OEM engineering workflow (Sourcing $\rightarrow$ Formulation $\rightarrow$ Geometry $\rightarrow$ Compliance $\rightarrow$ Packing $\rightarrow$ Dispatch) and dual brand strategy.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: implement bilingual slides 6 and 7 for Khaeer Alwadi"
```

---

### Task 6: Implement Bilingual Slide 8 (Freight Matrix) & Slide 9 (Commercial Contact Desk)

**Files:**
- Modify: `index.html`
- Modify: `tests/test_deck_structure.py`

**Interfaces:**
- Consumes: Logistics math (20ft FCL, 40ft HC FCL), contact credentials
- Produces: Bilingual Quality Specification Matrix, 4-step buyer onboarding guide, and executive WhatsApp quick-connect card

- [ ] **Step 1: Write test for Slides 8 & 9 specs and contact**

```python
def test_bilingual_slides_8_and_9():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "FCL" in html
    assert "+20 10 08716714" in html
    assert "wa.me/201008716714" in html
    assert "Cairo, Egypt" in html or "القاهرة، مصر" in html
    assert "DHL" in html or "FedEx" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: FAIL

- [ ] **Step 3: Implement Slides 8 and 9 in `index.html`**

- **Slide 8:** Technical specification matrix table, chemical/microbiological thresholds, and container payload calculations.
- **Slide 9:** 4-step buyer onboarding protocol (Sample dispatch, 24-hr quote, flexible payment terms, production laycan) and Khaeer Alwadi Executive Procurement card with WhatsApp button.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: implement bilingual slides 8 and 9 for Khaeer Alwadi"
```

---

### Task 7: Implement Bilingual Lightbox, Overview Drawer, Shortcuts Modal & Print-to-PDF Engine

**Files:**
- Modify: `index.html`
- Modify: `tests/test_deck_structure.py`

**Interfaces:**
- Consumes: `#image-modal`, `#overview-modal`, `#shortcuts-modal`, `@media print`
- Produces: Dynamic bilingual modal rendering and landscape A4 print styling

- [ ] **Step 1: Write test for bilingual modals and print rules**

```python
def test_bilingual_modals_and_print():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="image-modal"' in html
    assert 'id="overview-modal"' in html
    assert 'id="shortcuts-modal"' in html
    assert '@media print' in html
    assert 'break-after: page' in html or 'page-break-after: always' in html
    assert 'print-color-adjust: exact' in html or '-webkit-print-color-adjust: exact' in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: FAIL

- [ ] **Step 3: Implement bilingual modals and print engine in `index.html`**

- Localize `#image-modal` title and caption according to active language.
- Localize `#overview-modal` grid cards dynamically in Arabic and English.
- Localize `#shortcuts-modal` with Arabic key descriptions.
- Ensure `@media print` respects the currently selected language orientation (`dir="rtl"` or `dir="ltr"`).

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: add bilingual modals, dynamic slide drawer, and print engine"
```

---

### Task 8: End-to-End Verification, Full Test Suite Execution & Documentation

**Files:**
- Modify: `tests/test_deck_structure.py`
- Modify: `walkthrough.md`

**Interfaces:**
- Consumes: Complete `index.html` and `mariam.html`
- Produces: 100% passing test suite and comprehensive walkthrough documentation

- [ ] **Step 1: Run full test suite**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: All tests pass with exit code 0.

- [ ] **Step 2: Update `walkthrough.md` with Khaeer Alwadi bilingual deck documentation**

Document file structure, bilingual toggle controls, keyboard shortcuts, print-to-PDF procedures, and brand assets.

- [ ] **Step 3: Commit and review git status**

```bash
git add tests/test_deck_structure.py walkthrough.md
git commit -m "chore: complete end-to-end verification and documentation for Khaeer Alwadi bilingual deck"
```
