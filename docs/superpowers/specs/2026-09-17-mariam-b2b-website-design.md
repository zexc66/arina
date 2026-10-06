# MARIAM (مريم) — B2B & Export Wholesale Web Portal Design Specification

**Date:** 2026-09-17  
**Topic:** Luxury B2B & Export Wholesale Web Portal for Supermarkets, Distributors & Category Managers  
**Status:** Approved by Human Partner  
**Target Path:** `/home/zexc/Desktop/New Folder/index.html` (Standalone Modern Web App)

---

## 1. Executive Summary & Objectives

The goal is to engineer a world-class, responsive, standalone B2B & Export Wholesale Web Application for **Mariam (مريم)**. This portal bridges luxury Mediterranean food heritage with FMCG retail rigor, specifically built to convert supermarket retail buyers, FMCG category managers, institutional distributors, and HORECA procurement officers.

### Core Strategic Requirements:
1. **Sacred Brand Identity**: Prominently feature the authentic cursive gold brand logo (`mariam-logo-gold.png`) in Luxor Gold (`#DAAC36`). Never substitute with generic fonts or AI text.
2. **Glass Jars Exclusively**: 100% focused on premium glass jars across all 4 pillars. Strictly zero pouches, zero cans, zero bottles.
3. **Bilingual Real-Time Toggle**: Full English and Arabic support with dynamic BiDi/RTL switching, persistent language memory, and authentic typography.
4. **Interactive B2B Logistics Tooling**:
   - Live Pallet & Container Load Calculator (Carton count, gross weight, pallet Ti/Hi, 20ft & 40ft container capacity).
   - "Sample Request Basket" allowing buyers to select specific SKUs across sizes (500g, 370g, 210g, 190g, 100g) and generate a formal Request for Quotation (RFQ).
   - FMCG Merchandising & Planogram Viewer (Gondola shelf planograms, master shipper carton specs, FSDU floor stands, deli counter displays).
   - 4K Commercial Video Theater (Brand film, acoustic crunch hook, garlic spotlight).
5. **No PDF Generation**: In strict accordance with brand guidelines, zero PDF files will be generated or modified.

---

## 2. Technology Stack & Architecture

- **Format**: Single-Page Web Application (`index.html`) + modular asset structure.
- **Styling**: Tailwind CSS (via CDN) customized with Mariam's luxury palette (`#1E3326` Deep Forest Green, `#DAAC36` Luxor Gold, `#F8F5EE` Warm Ivory, `#691630` Imperial Ruby).
- **Typography**:
  - Latin: Cormorant Garamond / Playfair Display / Liberation Serif + Inter / Plus Jakarta Sans.
  - Arabic: Noto Sans Arabic + Cairo font families.
- **Motion & Interactions**: GSAP 3 (GreenSock) for smooth section transitions, scroll reveals, and modal animations.
- **Scripting**: Pure vanilla modern JavaScript (ES6+) with zero build dependencies, instantly runnable in any browser or deployable to Netlify, Vercel, or GitHub Pages.

---

## 3. Detailed UI/UX Layout & Sections

### Section 1: Top Navigation Bar (`<header>`)
- **Sticky Glassmorphism Header**: Deep forest green backdrop with blur and bottom gold hairline (`#DAAC36`).
- **Brand Logo (Center/Left)**: Authentic `mariam-logo-gold.png` scaled with crisp SVG/PNG rendering.
- **Navigation Links**:
  - Collections & Catalog (`#catalog`)
  - Retail Planograms (`#planograms`)
  - Container Calculator (`#calculator`)
  - Video Theater (`#videos`)
  - Wholesale RFQ (`#rfq`)
- **Interactive Controls (Right)**:
  - Language Toggle: `[ AR / EN ]` with instant text flip and `dir="rtl"` / `dir="ltr"` attribute switching.
  - Sample Request Cart Badge: `[ 🛒 Sample Basket (0) ]` with live counter badge opening the RFQ modal.

---

### Section 2: Executive B2B Hero Section (`<section id="hero">`)
- **Visual Staging**: Full-width atmospheric chiaroscuro on polished dark slate featuring the flagship jar trio (Baby Cucumbers 500g, Royal Kalamata 370g, Whipped Toum 210g) with authentic gold cursive logos.
- **Headline & Narrative**:
  - EN: *"PREMIUM MEDITERRANEAN HARVEST • WHOLESALE & EXPORT RESERVE"*
  - AR: *"أفخر خيرات الأرض المعتّقة بحب • بوابة التوزيع والبيع بالجملة لكبرى سلاسل التجزئة"*
  - Subhead: Commercial supply to Tier-1 Hypermarkets, Gourmet Food Halls, and Global Foodservice Distributors.
- **B2B CTA Buttons**:
  - Primary: `[ REQUEST WHOLESALE SAMPLES & PRICELIST ]` (Triggers RFQ modal)
  - Secondary: `[ LAUNCH CONTAINER LOGISTICS CALCULATOR ]` (Scrolls to calculator)
- **International Accreditation Badges**:
  - `ISO 22000 & HACCP Certified` | `100% Recyclable Flint Glass` | `Tier-1 FMCG Shelf Ready` | `Cold-Chain GCC Delivery`

---

### Section 3: Interactive B2B Product Catalog & Specification Matrix (`<section id="catalog">`)
- **Category Filter Tabs**:
  - `All Products` | `Artisanal Pickles (500g & 210g)` | `Table & Stuffed Olives (370g & 190g)` | `Garlic Pastes (210g & 100g)` | `Gourmet Tapenades (190g & 100g)`
- **Product Card Architecture (12 Flagship SKUs)**:
  - 4K transparent-cutout studio jar photo with contact shadow.
  - SKU Name in English & Arabic.
  - Format: Net Weight & Drained Weight (e.g., *Net: 500g | Drained: 260g*).
  - Secondary Packaging: *12 Jars per Master Shipper Carton*.
  - Logistics: *Pallet Ti/Hi (e.g. 12 × 6 = 72 Cases)*.
  - Shelf Life: *24 Months Ambient*.
  - Global EAN-13 Barcode.
  - Action Button: `[ + Add to Sample Request ]` (Increments sample basket).

---

### Section 4: Interactive Pallet & Container Logistics Calculator (`<section id="calculator">`)
A functional tool for procurement officers to model ordering economics:
- **Input Controls**:
  - Preset SKU selectors with quantity stepper for cases.
  - Container Type Selector: `[ 20ft Standard FCL (~1,400 Cases) ]` vs `[ 40ft High Cube FCL (~2,800 Cases) ]` vs `[ LCL Less-than-Container ]`.
- **Live Dynamic Outputs**:
  - Total Jars & Total Master Cartons.
  - Gross Metric Weight (kg / tonnes).
  - Standard Euro-Pallet Count (120 × 80 cm).
  - Container Volume Utilization Bar (e.g., *85% of 20ft Container capacity*).
  - Logistics Summary Generator: Button to copy order summary directly into the RFQ form.

---

### Section 5: FMCG Merchandising & Planogram Viewer (`<section id="planograms">`)
Dedicated to supermarket category managers evaluating shelf dominance:
- **Interactive Lightbox / Viewer** featuring:
  1. `mariam_fmcg_supermarket_shelf_planogram_4k.jpg`: 3-tier gondola planogram categorized by shelf hierarchy.
  2. `mariam_fmcg_category_manager_shelf_facing_panorama_4k.jpg`: Dual-facing (2 facings/SKU) shelf matrix with pricing channels.
  3. `mariam_fmcg_retail_fsdu_floor_display_stand_4k.jpg`: Corrugated FSDU floor stand with gold crown logo.
  4. `mariam_fmcg_master_carton_shipper_case_pack_4k.jpg`: 12-jar corrugated shipper box with anti-breakage cell dividers.
  5. `mariam_fmcg_countertop_delicatessen_pos_display_4k.jpg`: Natural oak countertop POS impulse display for Petite jars.
- **Specification Download Links**: Direct link to open/download each 4K full-resolution asset.

---

### Section 6: Commercial Video Theater (`<section id="videos">`)
- HTML5 Video Player with tabbed playlist:
  1. **Master Brand Film (Cinema 4K)**: `output/videos/mariam_master_brand_film_4k.mp4`
  2. **Social Hook Reel — The Royal Crunch**: `output/videos/mariam_social_reel_the_royal_crunch_9x16.mp4`
  3. **Garlic Spotlight Reel**: `output/videos/mariam_garlic_revolution_spotlight_9x16.mp4`
  4. **3D Pyramid Flythrough (4K)**: `output/videos/mariam_pyramid_exhibition_3d_flythrough_4k.mp4`
- Includes play/pause controls, theater mode, and full-screen support.

---

### Section 7: Interactive RFQ & Sample Request Modal (`<div id="rfq-modal">`)
- Triggered by header cart badge, hero CTA, or product cards.
- **Form Fields**:
  - Buyer Name, Corporate Email, Phone / WhatsApp (with country code).
  - Company Name & Business Category: (Hypermarket Chain / Food Distributor / Importer / HORECA & Hotel Group).
  - Target Destination Country & Port of Discharge (e.g. Jeddah Islamic Port, Jebel Ali, Dammam, Rotterdam, New York).
  - Selected Sample SKUs list (Pre-populated from basket, with ability to add notes).
  - Estimated Order Volume (Cases per month / Containers per quarter).
  - Submission handler: Instant validation with confirmation screen and mailto/WhatsApp link generator.

---

### Section 8: Global Footer & Legal Ribbon (`<footer>`)
- Mariam authentic gold logo + Khaeer Alwadi producer insignia.
- Terroir declaration: *"Bottled in 100% Recyclable Artisan Glass by Khaeer Alwadi"*.
- Quick navigation links, compliance credentials, and corporate copyright.

---

## 4. Verification & Testing Plan

1. **Brand Identity Verification**:
   - Confirm `mariam-logo-gold.png` is displayed in original vector/PNG fidelity at top navigation, hero, and footer.
   - Confirm zero generic font replacements for the Mariam brand name.
2. **Glass Only Enforcement**:
   - Verify every product card, image, and graphic depicts glass jars only.
3. **Bilingual & RTL Testing**:
   - Toggle language between English and Arabic.
   - Verify text changes, alignments flip from LTR to RTL, and fonts render properly without tofu boxes.
4. **Interactive Calculators**:
   - Enter carton quantities and verify that pallet counts, gross weights, and container load percentages update accurately in real time.
5. **Sample Basket & RFQ Modal**:
   - Add items to sample basket, open RFQ modal, verify pre-filled SKUs, and test form validation.
6. **Video Playback**:
   - Test that MP4 video files in `output/videos/` play smoothly with audio controls.
7. **Responsiveness**:
   - Verify layouts on desktop (4K/1080p), tablet, and mobile phone viewports.
