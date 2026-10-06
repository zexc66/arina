# Mariam (مريم) B2B & Export Wholesale Portal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a luxury, high-conversion, standalone B2B & Export Wholesale Web Application (`index.html`) for Mariam (مريم) targeted at supermarket buyers, FMCG distributors, and category managers.

**Architecture:** A standalone Single-Page Application (SPA) built with HTML5, Tailwind CSS, GSAP 3 for motion, and Vanilla JavaScript. Features an interactive bilingual engine (English/Arabic RTL), dynamic SKU catalog with sample request cart, interactive container/pallet calculator, FMCG planogram lightbox, 4K commercial video theater, and formal RFQ quotation modal.

**Tech Stack:** HTML5, Tailwind CSS (CDN with custom theme), GSAP 3, Vanilla JS (ES6+), Python unittest/BeautifulSoup for automated DOM & logic verification.

**Spec:** `/home/zexc/Desktop/New Folder/docs/superpowers/specs/2026-09-17-mariam-b2b-website-design.md`

## Global Constraints

- Authentic brand logo strictly `mariam-logo-gold.png` in Luxor Gold `#DAAC36`. Never replace with generic text or fonts.
- Exclusively glass jars only across all product representations. Zero pouches, zero cans, zero bottles.
- Zero PDF files modified, generated, or added.
- Pure standalone frontend: zero mandatory build steps, zero npm server dependencies, runnable directly in browser or static host.
- Full bilingual English and Arabic support with real-time RTL/LTR switching and zero missing glyphs / tofu boxes.

---

### Task 1: Project Scaffolding & Automated Test Suite

**Files:**
- Create: `tests/test_b2b_website.py`
- Create: `index.html` (initial scaffold)

**Interfaces:**
- Produces: HTML5 skeleton with Tailwind configuration, font imports, asset bindings, and a test suite validating DOM structure, brand guidelines, and script logic.

- [ ] **Step 1: Write the failing automated test in `tests/test_b2b_website.py`**
  - Verify existence of `index.html`.
  - Verify presence of `mariam-logo-gold.png`.
  - Verify presence of bilingual attributes, navigation links, and core sections (`#hero`, `#catalog`, `#calculator`, `#planograms`, `#videos`, `#rfq-modal`).
  - Verify absence of forbidden keywords (pouches, spray cans, plastic bottles, or PDF files).
- [ ] **Step 2: Run test to confirm failure**
- [ ] **Step 3: Create initial `index.html` skeleton with head, fonts, Tailwind palette, and GSAP**
- [ ] **Step 4: Run test to confirm scaffolding passes**
- [ ] **Step 5: Commit scaffolding**

---

### Task 2: Interactive Bilingual Engine (EN/AR) & Navigation Header

**Files:**
- Modify: `index.html`
- Modify: `tests/test_b2b_website.py`

**Interfaces:**
- Produces: `window.MariamI18n` bilingual data object, `switchLanguage(lang)` function, and sticky glassmorphic `<header>` with responsive mobile menu and sample basket counter badge.

- [ ] **Step 1: Add unit test for language toggle and translation key coverage**
- [ ] **Step 2: Implement `translations` dictionary for all site sections in EN and AR**
- [ ] **Step 3: Implement `switchLanguage(lang)` function updating DOM text, `dir="rtl"` / `dir="ltr"`, and `lang` attribute**
- [ ] **Step 4: Implement sticky glassmorphic navigation header with `mariam-logo-gold.png`, navigation anchors, language toggle, and sample basket trigger**
- [ ] **Step 5: Run tests and verify language switching in both directions**
- [ ] **Step 6: Commit Task 2**

---

### Task 3: Executive B2B Hero Section & Commercial Credentials

**Files:**
- Modify: `index.html`
- Modify: `tests/test_b2b_website.py`

**Interfaces:**
- Produces: `<section id="hero">` with chiaroscuro flagship jar trio, B2B call-to-actions, and international food safety badges.

- [ ] **Step 1: Add test asserting hero elements, CTA buttons, and accreditation badges**
- [ ] **Step 2: Build hero section markup with luxury typography, bilingual headline, subhead, and CTA buttons**
- [ ] **Step 3: Embed 4K flagship jar cutout visual with contact reflections**
- [ ] **Step 4: Build accreditation trust ticker (ISO 22000, HACCP, 100% Glass, Tier-1 FMCG Ready)**
- [ ] **Step 5: Run tests to verify hero structure and responsiveness**
- [ ] **Step 6: Commit Task 3**

---

### Task 4: Interactive B2B Product Catalog & Sample Request Basket

**Files:**
- Modify: `index.html`
- Modify: `tests/test_b2b_website.py`

**Interfaces:**
- Produces: Dynamic 12-SKU product catalog, category filter tabs, specification badges, and `addToSampleBasket(skuId)` functionality.

- [ ] **Step 1: Add test validating 12 SKUs, category tabs, and sample basket interaction**
- [ ] **Step 2: Define JavaScript catalog database with technical B2B specs (Net/drained weight, case pack 12 units, pallet Ti/Hi, EAN barcodes)**
- [ ] **Step 3: Implement category filter tabs (All, Pickles, Olives, Garlic, Tapenades)**
- [ ] **Step 4: Render responsive grid of 12 luxury product cards with 4K jar images and `+ Add to Sample Request` buttons**
- [ ] **Step 5: Implement `addToSampleBasket()` with live badge updates and toast notifications**
- [ ] **Step 6: Run tests and verify catalog rendering and filtering**
- [ ] **Step 7: Commit Task 4**

---

### Task 5: Interactive Pallet & Container Logistics Calculator

**Files:**
- Modify: `index.html`
- Modify: `tests/test_b2b_website.py`

**Interfaces:**
- Produces: `<section id="calculator">` with real-time mathematical calculations for gross case weights, Euro-pallet counts, and 20ft/40ft container capacity utilization.

- [ ] **Step 1: Add test for logistics mathematical formulas (case weight, pallet Ti/Hi, container utilization)**
- [ ] **Step 2: Build calculator UI with SKU case quantity inputs and container type radio selector (20ft FCL vs 40ft FCL vs LCL)**
- [ ] **Step 3: Implement JavaScript calculation engine calculating: Total Cartons, Total Jars, Gross Metric Tonnes, Euro-Pallets, and Volume %**
- [ ] **Step 4: Build dynamic progress bar and visual container graphic indicating fill percentage**
- [ ] **Step 5: Implement "Transfer Logistics Spec to RFQ" button linking calculator results to RFQ form**
- [ ] **Step 6: Run tests to verify calculation accuracy across edge cases**
- [ ] **Step 7: Commit Task 5**

---

### Task 6: FMCG Merchandising & Planogram Lightbox Viewer

**Files:**
- Modify: `index.html`
- Modify: `tests/test_b2b_website.py`

**Interfaces:**
- Produces: `<section id="planograms">` showcasing retail gondola planograms, master cartons, and display stands with an interactive zoom modal.

- [ ] **Step 1: Add test asserting planogram section and lightbox functionality**
- [ ] **Step 2: Build grid displaying the 5 FMCG retail assets (3-Tier Planogram, Dual-Facing Matrix, FSDU Floor Stand, Master Shipper Box, Deli Counter POS)**
- [ ] **Step 3: Implement full-screen modal image viewer with zoom, caption details, and download link**
- [ ] **Step 4: Run tests to verify modal open/close and keyboard escape accessibility**
- [ ] **Step 5: Commit Task 6**

---

### Task 7: 4K Commercial Video Theater

**Files:**
- Modify: `index.html`
- Modify: `tests/test_b2b_website.py`

**Interfaces:**
- Produces: `<section id="videos">` with HTML5 video player, custom play/pause overlay, and playlist tabs for all 4 commercial MP4 videos.

- [ ] **Step 1: Add test verifying video player elements and video playlist sources**
- [ ] **Step 2: Build responsive cinema player interface with play overlay and video title**
- [ ] **Step 3: Implement interactive video playlist switcher (Brand Film 4K, Royal Crunch 9:16 Reel, Garlic Spotlight 9:16 Reel, 3D Pyramid Flythrough 4K)**
- [ ] **Step 4: Run tests to verify video source switching and playback controls**
- [ ] **Step 5: Commit Task 7**

---

### Task 8: Sample Request Basket & Interactive RFQ Modal + Global Footer

**Files:**
- Modify: `index.html`
- Modify: `tests/test_b2b_website.py`

**Interfaces:**
- Produces: Complete slide-over / modal RFQ form with pre-filled sample items, validation, WhatsApp/Email quotation link generation, and luxury brand footer.

- [ ] **Step 1: Add test validating RFQ modal form inputs, validation logic, and footer links**
- [ ] **Step 2: Build RFQ modal with buyer fields (Name, Corporate Email, Phone, Company, Business Type, Destination Port, Delivery Term: FOB/CIF)**
- [ ] **Step 3: Connect sample basket items to RFQ modal with quantity adjustments and item deletion**
- [ ] **Step 4: Implement client-side form submission handler generating formatted inquiry for email/WhatsApp transmission**
- [ ] **Step 5: Implement luxury global footer with authentic gold logo, producer credentials, directory links, and copyright**
- [ ] **Step 6: Run tests and verify full end-to-end RFQ workflow**
- [ ] **Step 7: Commit Task 8**

---

### Task 9: End-to-End Verification, Accessibility & Browser Preview

**Files:**
- Modify: `index.html`
- Execute: `python3 tests/test_b2b_website.py`

**Interfaces:**
- Produces: Fully verified, production-ready B2B web application with 100% test coverage.

- [ ] **Step 1: Run comprehensive automated test suite and confirm 100% pass**
- [ ] **Step 2: Verify responsive layouts across 4K, 1440p, 1080p, iPad, and mobile viewports**
- [ ] **Step 3: Audit brand compliance: authentic logo present, jars only, zero PDFs**
- [ ] **Step 4: Create walkthrough documentation and deliver final web application**
