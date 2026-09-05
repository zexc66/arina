# Mariam Foods B2B Sales Deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an executive-tier, interactive B2B sales presentation deck (`index.html`) featuring high-resolution facility and product photography, comprehensive technical specifications, and a dedicated print-to-PDF engine for Mariam Food Industries (Cairo, Egypt).

**Architecture:** Standalone, responsive 16:9 widescreen presentation canvas built with HTML5, Tailwind CSS, and vanilla JavaScript. Features keyboard/touch slide navigation, interactive modal image inspection for procurement buyers, and strict `@media print` CSS rules for clean PDF export.

**Tech Stack:** HTML5, CSS3, Tailwind CSS (via CDN), Vanilla JS, Lucide Icons (SVG), Print-to-PDF stylesheets.

**Spec:** `docs/superpowers/specs/2026-09-05-mariam-foods-sales-deck-design.md`

## Global Constraints
- Company Name: Mariam Food Industries
- Headquarters: Cairo, Egypt
- Direct Line / WhatsApp: `+20 10 08716714`
- Certifications Highlighted: ISO 22000, HACCP, FDA Registered (US FSMA), Halal, ISO 9001
- Primary Color Scheme: Deep Mediterranean Olive (`#1E3A2F`, `#142720`), Amber Gold (`#C89D3C`), Slate Charcoal (`#0F172A`)
- Canvas Ratio: 16:9 widescreen presentation format (`1920x1080` scaling)
- Fully Self-Contained: Operates offline by opening `index.html` directly in any web browser

---

## Tasks

### Task 1: Presentation Shell, Responsive 16:9 Canvas & Navigation Engine

**Files:**
- Create: `index.html`
- Create: `tests/test_deck_structure.py`

**Interfaces:**
- Produces: Base HTML DOM, Tailwind configuration, Slide state manager (`currentSlide`, `goToSlide(n)`, `nextSlide()`, `prevSlide()`), keyboard event listeners (`ArrowRight`, `ArrowLeft`, `Space`, `f`), and floating navigation dock (`#nav-dock`).

- [ ] **Step 1: Write test to verify presentation deck structure and navigation handlers**

```python
# tests/test_deck_structure.py
import os
import re

def test_index_file_exists():
    assert os.path.exists("index.html"), "index.html must exist"

def test_deck_contains_9_slides_and_nav():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    slides = re.findall(r'<section[^>]+class="[^"]*slide[^"]*"', html)
    assert len(slides) == 9, f"Expected 9 slides, found {len(slides)}"
    assert 'id="nav-dock"' in html, "Navigation dock must be present"
    assert '+20 10 08716714' in html, "Contact number must be present"
    assert 'Mariam Food Industries' in html, "Company name must be present"
```

- [ ] **Step 2: Run test to verify it fails initially**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: FAIL (`AssertionError: index.html must exist`)

- [ ] **Step 3: Scaffold `index.html` with Tailwind, 16:9 viewport container, and navigation JavaScript**

Implement the master HTML skeleton with:
- Tailwind CSS via CDN
- Custom styles for slide transitions, `@media print` rules, and 16:9 aspect ratio management
- Core JS state machine (`showSlide(index)`, `nextSlide()`, `prevSlide()`, keyboard shortcuts, full-screen toggle)
- Skeleton containers for all 9 slides

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: scaffold presentation shell, 16:9 canvas and slide navigation"
```

---

### Task 2: Implement Slide 1 (Cover), Slide 2 (Egyptian Agro Advantage), and Slide 3 (Infrastructure & Certifications)

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: Slide state engine from Task 1
- Produces: Slide 1 (Cover / Hero), Slide 2 (Geographic & Trade Advantage), Slide 3 (Industrial Processing Lines, Autoclave Pasteurization, and Food Safety Certifications).

- [ ] **Step 1: Write automated check for Slides 1-3 content and assets**

Add to `tests/test_deck_structure.py`:
```python
def test_slides_1_to_3_content():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "ISO 22000" in html and "HACCP" in html and "FDA" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg" in html, "Autoclave photo must be in slide 3"
    assert "Alexandria" in html and "Damietta" in html, "Ports must be referenced in slide 2"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: FAIL

- [ ] **Step 3: Implement Slides 1, 2, and 3 in `index.html`**

- **Slide 1:** Executive cover with Mariam Food Industries branding, Cairo location, gold badge trust markers, and high-impact hero composition.
- **Slide 2:** Interactive 3-column layout highlighting Egyptian agro terroir, strategic maritime routes (Alexandria, Damietta, Port Said with transit days), and tariff-free trade agreements (GAFTA, COMESA, Agadir, EU).
- **Slide 3:** Facility floor showcase: high-throughput stone pitting, rotary slicing lines, and autoclave retort crate (`WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg`), stacked A10 inventory (`WhatsApp Image 2026-09-05 at 12.52.17 PM.jpeg`), and the 5 certified compliance badges (ISO 22000, HACCP, FDA Registered, Halal, ISO 9001).

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: complete slide 1 (cover), slide 2 (supply advantage), and slide 3 (infrastructure)"
```

---

### Task 3: Implement Slide 4 (Table Olives Showcase) and Slide 5 (Pickled Specialties Showcase)

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: Navigation framework and image layout patterns
- Produces: Detailed product cards, caliber badges, slice uniformity callouts, and macro photography integration for Olives and Pickled Specialties.

- [ ] **Step 1: Write test for Slides 4-5 product lines and assets**

Add to `tests/test_deck_structure.py`:
```python
def test_slides_4_and_5_products():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "Picual" in html
    assert "Pimento" in html
    assert "Pepperoncini" in html
    assert "Turshi" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.20 PM.jpeg" in html, "Sliced black olives image required"
    assert "WhatsApp Image 2026-09-05 at 12.52.17 PM (5).jpeg" in html, "Pimento stuffed olives image required"
    assert "WhatsApp Image 2026-09-05 at 12.52.16 PM (2).jpeg" in html, "Mixed pickle jar image required"
```

- [ ] **Step 2: Run test to verify failure**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: FAIL

- [ ] **Step 3: Implement Slides 4 and 5 in `index.html`**

- **Slide 4 (Table Olives Portfolio):**
  - Grid featuring Sliced Black Olives (`12.52.20 PM.jpeg`, `12.52.15 PM (2).jpeg`), Pitted Black Olives (`12.52.16 PM (5).jpeg`), Whole Green Olives (`12.52.17 PM (6).jpeg`), Sliced Green Olives (`12.52.17 PM (1).jpeg`), and Pimento-Stuffed Green Olives (`12.52.17 PM (5).jpeg`).
  - Spec tags: Calibers (200/220, 240/260, 280/300), Ring thickness (3.2mm $\pm$0.2mm), Drained weight yield ($\ge 52\%$), Salinity (4.5%–6.0%).
- **Slide 5 (Pickled Vegetables & Specialty Peppers):**
  - Showcase for Golden Pepperoncini/Yellow Peppers (`12.52.18 PM (2).jpeg`), Whole Red Chili Peppers (`12.52.19 PM.jpeg`), Traditional Mixed Turshi (`12.52.16 PM (2).jpeg`), and Pickled Cucumbers/Gherkins.
  - Spec tags: Texture rating (crisp snap), acidity/pH ($3.2 - 3.6$), heat profiles, and aromatic brine formulation.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: complete slide 4 (olives showcase) and slide 5 (pickled specialties)"
```

---

### Task 4: Implement Slide 6 (Packaging Formats) and Slide 7 (Private Label & OEM Solutions)

**Files:**
- Modify: `index.html`

**Interfaces:**
- Produces: 3-tier packaging comparison (Foodservice Cans, Bulk Barrels, Retail Jars) and contract packaging / OEM capabilities.

- [ ] **Step 1: Write test for Slides 6-7 packaging specifications**

Add to `tests/test_deck_structure.py`:
```python
def test_slides_6_and_7_packaging_and_oem():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "A10" in html, "A10 foodservice can format required"
    assert "150kg" in html or "220kg" in html, "Bulk drum specs required"
    assert "Private Label" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.17 PM (7).jpeg" in html, "Open can photo required"
    assert "WhatsApp Image 2026-09-05 at 12.52.17 PM (4).jpeg" in html, "Bulk barrel photo required"
    assert "WhatsApp Image 2026-09-05 at 12.52.15 PM (5).jpeg" in html, "Pallet photo required"
```

- [ ] **Step 2: Run test to verify failure**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: FAIL

- [ ] **Step 3: Implement Slides 6 and 7 in `index.html`**

- **Slide 6 (Multi-Tier Packaging Architecture):**
  - Section A: Foodservice / Catering **A10 metal cans** (`12.52.17 PM (7).jpeg`, `12.52.16 PM (3).jpeg`). Stackable, high-yield, 36-month shelf life.
  - Section B: Industrial Bulk **150kg–220kg food-grade brine barrels/drums** (`12.52.17 PM (4).jpeg`, `12.52.17 PM (9).jpeg`).
  - Section C: Retail Supermarket **Glass Jars (370ml, 500ml, 720ml, 1000ml)** (`12.52.16 PM (4).jpeg`) with export palletization display (`12.52.15 PM (5).jpeg`).
- **Slide 7 (Private Label & Turnkey OEM):**
  - Turnkey OEM workflow: recipe custom brine, custom cuts (2mm–4mm), label design compliance (FDA, EU FIC, GSO, SFDA), barcode registration, and master carton packing.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: complete slide 6 (packaging architecture) and slide 7 (private label/OEM)"
```

---

### Task 5: Implement Slide 8 (Technical Spec Matrix & Logistics) and Slide 9 (Commercial Terms & Direct Contact)

**Files:**
- Modify: `index.html`

**Interfaces:**
- Produces: High-contrast technical data table, 20ft/40ft FCL container calculations, and high-converting CTA contact page with direct phone/WhatsApp link.

- [ ] **Step 1: Write test for Slides 8-9 specs and contact information**

Add to `tests/test_deck_structure.py`:
```python
def test_slides_8_and_9_specs_and_contact():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "FCL" in html, "Container loading specs required"
    assert "Drained Weight" in html
    assert "tel:+201008716714" in html or "wa.me/201008716714" in html, "Direct clickable link required"
    assert "Cairo, Egypt" in html
```

- [ ] **Step 2: Run test to verify failure**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: FAIL

- [ ] **Step 3: Implement Slides 8 and 9 in `index.html`**

- **Slide 8 (Technical Specifications & Freight Matrix):**
  - Full tabular breakdown of Drained Weight ratios, pH limits, Salinity percentages, Defect tolerances, and Shelf life across all 4 product families.
  - Shipping economics: 20ft FCL and 40ft FCL pallet capacities, carton counts, and sea-freight protection standards.
- **Slide 9 (Commercial Partnership & Direct Line):**
  - Mariam Food Industries executive closing card.
  - Direct Phone & WhatsApp: `+20 10 08716714` with active `https://wa.me/201008716714` quick-connect button.
  - Step-by-step buyer guide: Sample kit request (via DHL/FedEx), quotation parameters (FOB Egyptian Ports / CIF Global Ports), and L/C & T/T terms.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: complete slide 8 (spec matrix) and slide 9 (commercial terms and contact)"
```

---

### Task 6: Interactive Image Lightbox Modal, Print-to-PDF Stylesheet & End-to-End Verification

**Files:**
- Modify: `index.html`

**Interfaces:**
- Produces: Interactive click-to-zoom modal for all images, dedicated `@media print` CSS engine for generating clean 9-page landscape PDF decks, and slide jump drawer.

- [ ] **Step 1: Write test for modal and print engine**

Add to `tests/test_deck_structure.py`:
```python
def test_lightbox_modal_and_print_rules():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="image-modal"' in html, "Image lightbox modal element required"
    assert '@media print' in html, "Dedicated print media query required"
    assert 'break-after: page' in html or 'page-break-after: always' in html, "Page break rules required"
```

- [ ] **Step 2: Run test to verify failure**

Run: `python3 -m unittest tests/test_deck_structure.py`  
Expected: FAIL

- [ ] **Step 3: Implement Lightbox Modal & Print-to-PDF CSS in `index.html`**

- Add high-resolution image zoom modal with smooth backdrop blur, keyboard `Escape` to close, and responsive image scaling.
- Add slide overview drawer (click menu icon to view all 9 slide cards in a grid and jump directly).
- Refine `@media print` rules:
  - Force page size to `A4 landscape` / `Letter landscape`.
  - Ensure background colors, borders, and badges print faithfully with `-webkit-print-color-adjust: exact`.
  - Automatically display all 9 slides sequentially on print, hiding interactive buttons and navigation chrome.
- Add keyboard shortcuts hint modal (`?` key).

- [ ] **Step 4: Run the full test suite**

Run: `python3 -m unittest tests/test_deck_structure.py -v`  
Expected: ALL 6 TESTS PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_deck_structure.py
git commit -m "feat: add image modal lightbox, slide overview drawer, and print-to-pdf engine"
```
