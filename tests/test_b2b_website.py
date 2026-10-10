import unittest
import os
import re
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILE = os.path.join(WORKSPACE_DIR, 'website.html' if os.path.exists(os.path.join(WORKSPACE_DIR, 'website.html')) else 'index.html')

class SimpleDOMParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = {}
        self.ids = {}
        self.images = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tags.setdefault(tag, []).append(attr_dict)
        if 'id' in attr_dict:
            self.ids[attr_dict['id']] = (tag, attr_dict)
        if tag == 'img' and 'src' in attr_dict:
            self.images.append(attr_dict['src'])

class TestMariamB2BWebsite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists(HTML_FILE):
            with open(HTML_FILE, 'r', encoding='utf-8') as f:
                cls.html_content = f.read()
            cls.parser = SimpleDOMParser()
            cls.parser.feed(cls.html_content)
        else:
            cls.html_content = ""
            cls.parser = SimpleDOMParser()

    def test_01_index_html_exists_and_valid(self):
        self.assertTrue(os.path.exists(HTML_FILE), "index.html must exist in workspace")
        self.assertGreater(len(self.html_content), 1000, "index.html must be populated with content")

    def test_02_sacred_brand_logo_present(self):
        # Logo must reference arina-logo-gold.png or mariam-logo-gold.png
        has_logo = any('arina-logo-gold.png' in src or 'mariam-logo-gold.png' in src for src in self.parser.images) or 'arina-logo-gold.png' in self.html_content or 'mariam-logo-gold.png' in self.html_content
        self.assertTrue(has_logo, "Must contain authentic brand logo (arina-logo-gold.png)")

    def test_03_no_forbidden_packaging_or_pdfs(self):
        lower = self.html_content.lower()
        self.assertNotIn(".pdf", lower, "Strict PDF prohibition: No PDF references allowed")
        self.assertNotIn("pouch", lower, "Jars only: No pouches allowed")
        self.assertNotIn("spray can", lower, "Jars only: No spray cans allowed")

    def test_04_core_sections_present(self):
        self.assertIn('header', self.parser.tags, "Must have header element")
        self.assertIn('hero', self.parser.ids, "Must have #hero section")
        self.assertIn('catalog', self.parser.ids, "Must have #catalog section")
        self.assertIn('calculator', self.parser.ids, "Must have #calculator section")
        self.assertIn('planograms', self.parser.ids, "Must have #planograms section")
        self.assertNotIn('videos', self.parser.ids, "Must not have #videos section per user directive")
        self.assertNotIn('honey-showcase', self.parser.ids, "Must not have #honey-showcase per zero-honey directive")
        self.assertIn('rfq-modal', self.parser.ids, "Must have #rfq-modal element")
        self.assertIn('footer', self.parser.tags, "Must have footer element")

    def test_05_bilingual_support(self):
        self.assertIn("switchLanguage", self.html_content, "Must have switchLanguage function")
        self.assertTrue(any(ord(c) > 127 for c in self.html_content), "Must contain Arabic text")
        self.assertIn("Tajawal", self.html_content, "Must import and use Tajawal font for Arabic typography")
        # Ensure data-i18n elements are present and covered
        i18n_keys = re.findall(r'data-i18n=[\"\']([^\"\']+)[\"\']', self.html_content)
        self.assertGreater(len(i18n_keys), 200, "Must have comprehensive data-i18n tags across all sections")
        self.assertIn("TRANSLATIONS", self.html_content, "Must define TRANSLATIONS dictionary")

    def test_06_sku_catalog_database(self):
        for sku_ean in ['6281001201015', '6281001201022', '6281001202012', '6281001204016', '6281001203026', '6281001202067']:
            self.assertIn(sku_ean, self.html_content, f"EAN {sku_ean} must be present in catalog")
        # Ensure 14 SKU objects are defined
        id_matches = re.findall(r"id:\s*'([a-z0-9\-]+)'", self.html_content)
        self.assertEqual(len(id_matches), 14, "Must contain exactly 14 SKUs in catalog")
        # Ensure every media path referenced in the file exists on disk
        media_paths = re.findall(r'[\"\']([a-zA-Z0-9_\-\./]+\.(?:jpg|png|mp4))[\"\']', self.html_content)
        for path in set(media_paths):
            full_path = os.path.join(WORKSPACE_DIR, path)
            self.assertTrue(os.path.exists(full_path), f"Media file {path} must exist on disk")

    def test_07_interactive_logistics_calculator(self):
        self.assertIn("calculateLogistics", self.html_content, "Must have calculateLogistics function")
        self.assertIn("20ft", self.html_content, "Must calculate 20ft container capacity")
        self.assertIn("40ft", self.html_content, "Must calculate 40ft container capacity")

    def test_08_strict_zero_video_directive(self):
        self.assertNotIn(".mp4", self.html_content, "Must have zero .mp4 video files per user directive")
        self.assertNotIn("<video", self.html_content, "Must have zero video tags per user directive")

    def test_09_rfq_modal_form(self):
        self.assertIn("rfq-company", self.parser.ids, "Must have rfq-company input")
        self.assertIn("rfq-email", self.parser.ids, "Must have rfq-email input")

    def test_10_mobile_experience(self):
        self.assertIn("mobile-bottom-bar", self.parser.ids, "Must have sticky mobile bottom quick action bar")
        self.assertIn("mobile-backdrop", self.parser.ids, "Must have mobile drawer backdrop overlay")
        self.assertIn("width=device-width", self.html_content, "Must have responsive viewport meta tag")
        self.assertIn("whitespace-nowrap", self.html_content, "Must prevent navigation links from wrapping and overlapping")
        self.assertIn("hidden 2xl:inline", self.html_content, "Must hide sample basket text on intermediate viewports to prevent navbar protrusion")

    def test_11_terroir_and_seasonal_harvest_timeline(self):
        self.assertIn('terroir', self.parser.ids, "Must have #terroir section")
        self.assertIn('Baby Cornichons & Dill', self.html_content, "Must describe Spring harvest cycle")
        self.assertIn('Mountain Garlic Curing', self.html_content, "Must describe Summer garlic harvest")
        self.assertIn('Kalamata & Ruby Turnips', self.html_content, "Must describe Autumn olive and turnip harvest")
        self.assertIn('Flint Glass Sea-Salt Brine', self.html_content, "Must describe Winter slow brine fermentation")

    def test_12_global_maritime_shipping_estimator(self):
        self.assertIn('shipping', self.parser.ids, "Must have #shipping section")
        self.assertIn('selectShippingPort', self.html_content, "Must have selectShippingPort function")
        self.assertIn('SHIPPING_ROUTES', self.html_content, "Must define SHIPPING_ROUTES object")
        for port in ['jeddah', 'jebel_ali', 'rotterdam', 'hamburg', 'new_york']:
            self.assertIn(port, self.html_content, f"Must include shipping route for {port}")

    def test_13_multi_currency_converter(self):
        self.assertIn('currency-dropdown', self.parser.ids, "Must have #currency-dropdown element")
        self.assertIn('setCurrency', self.html_content, "Must have setCurrency function")
        self.assertIn('CURRENCIES', self.html_content, "Must define CURRENCIES dictionary")
        for curr in ['USD', 'EUR', 'SAR', 'AED', 'GBP']:
            self.assertIn(curr, self.html_content, f"Must support currency {curr}")

    def test_14_commercial_proforma_invoice_modal(self):
        self.assertIn('proforma-modal', self.parser.ids, "Must have #proforma-modal element")
        self.assertIn('proforma-print-area', self.parser.ids, "Must have #proforma-print-area for high-contrast printing")
        self.assertIn('printProforma', self.html_content, "Must have printProforma function")
        self.assertIn('updateProformaLineItems', self.html_content, "Must have updateProformaLineItems function")
        self.assertIn('2001.10.00', self.html_content, "Must include official HS code 2001.10.00 for Pickles")
        self.assertIn('2005.70.00', self.html_content, "Must include official HS code 2005.70.00 for Olives")

    def test_15_interactive_360_turntable_viewer(self):
        self.assertIn('turntable-modal', self.parser.ids, "Must have #turntable-modal element")
        self.assertIn('openTurntableModal', self.html_content, "Must have openTurntableModal function")
        self.assertIn('setTurntableAngle', self.html_content, "Must have setTurntableAngle function")
        self.assertIn('TURNTABLE_PRODUCTS', self.html_content, "Must define TURNTABLE_PRODUCTS database")

    def test_16_zero_emojis_and_vector_svg_compliance(self):
        emoji_pattern = re.compile(
            r"[\U0001F600-\U0001F64F]"
            r"|[\U0001F300-\U0001F5FF]"
            r"|[\U0001F680-\U0001F6FF]"
            r"|[\U0001F1E0-\U0001F1FF]"
            r"|[\U00002702-\U000027B0]"
            r"|[\U0001F900-\U0001F9FF]"
            r"|[\U0001FA70-\U0001FAFF]"
        )
        matches = emoji_pattern.findall(self.html_content)
        self.assertEqual(len(matches), 0, f"No emojis permitted in luxury B2B website; found: {matches}")

    def test_17_customs_and_tariff_explorer(self):
        self.assertIn('shipping-customs-container', self.parser.ids, "Must have #shipping-customs-container element")
        self.assertIn('switchShippingTab', self.html_content, "Must define switchShippingTab function")
        self.assertIn('selectCustomsCountry', self.html_content, "Must define selectCustomsCountry function")
        self.assertIn('applyCustomsToRFQ', self.html_content, "Must define applyCustomsToRFQ function")
        self.assertIn('CUSTOMS_REGULATIONS', self.html_content, "Must define CUSTOMS_REGULATIONS database")
        for country in ['ksa', 'uae', 'germany', 'netherlands', 'usa', 'uk']:
            self.assertIn(f"customs-btn-{country}", self.parser.ids, f"Must have customs selector button for {country}")
        for hs in ['2001.10.00', '2001.90.90', '2005.70.00', '2103.90.90']:
            self.assertIn(hs, self.html_content, f"Must include HS code {hs}")
        self.assertIn("GAFTA", self.html_content, "Must reference GAFTA preferential duty agreement")
        self.assertIn("EUR.1", self.html_content, "Must reference EUR.1 preferential movement framework")
        self.assertIn("FASAH", self.html_content, "Must reference FASAH clearance portal")
        self.assertIn("FoodWatch", self.html_content, "Must reference Dubai FoodWatch portal")
    def test_18_english_purity_and_zero_arabic_leaks(self):
        # 1. Ensure TRANSLATIONS.en has 0 Arabic characters
        en_match = re.search(r'en:\s*\{(.*?)\n\s*\},', self.html_content, re.DOTALL)
        self.assertIsNotNone(en_match, "TRANSLATIONS.en block must exist")
        en_text = en_match.group(1)
        arabic_in_en = re.findall(r'[\u0600-\u06FF]+', en_text)
        self.assertEqual(len(arabic_in_en), 0, f"TRANSLATIONS.en must contain zero Arabic characters, found: {arabic_in_en}")

        # 2. Subtitle elements must not have hardcoded dir="rtl" or font-arabic
        sub_ids = ['hero_subtitle', 'terroir_subtitle', 'catalog_subtitle', 'calc_subtitle', 'shipping_subtitle', 'plano_subtitle']
        for sub_key in sub_ids:
            # Check data-i18n is present in html
            self.assertIn(f'data-i18n="{sub_key}"', self.html_content, f"Must have element with data-i18n='{sub_key}'")

        # 3. No HTML element tags outside <style> should have hardcoded dir="rtl" attributes
        html_outside_style = re.sub(r'<style[\s\S]*?</style>', '', self.html_content)
        html_outside_script = re.sub(r'<script[\s\S]*?</script>', '', html_outside_style)
        html_outside_comments = re.sub(r'<!--[\s\S]*?-->', '', html_outside_script)
        rtl_tag_matches = re.findall(r'<[a-zA-Z0-9_-]+[^>]*\bdir=["\']rtl["\']', html_outside_comments)
        self.assertEqual(len(rtl_tag_matches), 0, f"No HTML tags should have hardcoded dir='rtl'; direction must be dynamic, found: {rtl_tag_matches}")
        self.assertNotIn('font-arabic', html_outside_comments, "No HTML tags should have static font-arabic class")

        # 4. DOMContentLoaded must initialize with switchLanguage('en')
        self.assertIn("switchLanguage('en')", self.html_content, "DOMContentLoaded must initialize page with switchLanguage('en')")

        # 5. Lightbox function must support bilingual parameters
        self.assertIn("function openLightbox(imgSrc, titleEn, titleAr, descEn, descAr)", self.html_content)

        # 6. WhatsApp must dynamically construct inquiry text based on language
        self.assertIn("Hello, I am reaching out on behalf of", self.html_content, "Must have English WhatsApp export inquiry text")

    def test_19_factory_certified_matrix_and_logistics_calibration(self):
        # 1. Official Factory Formats & Dimensions
        formats = [
            "Ø 7 cm × H 12 cm",   # Format 1: Table Jar
            "Ø 9 cm × H 16 cm",   # Format 2: Supermarket Shelf Jar
            "Ø 12 cm × H 22 cm",  # Format 3: Club & Deli Jar
            "15 × 15 × 25 cm",    # Format 4: HORECA Box
            "Ø 22 cm × H 25 cm",  # Format 5: Sealed Pail
            "Ø 30 cm × H 38 cm",  # Format 6: Commissary Pail
            "Ø 48 cm × H 75 cm",  # Format 7: Processing Drum
            "Ø 58 cm × H 95 cm",  # Format 8: Export Standard Drum
        ]
        for fmt in formats:
            self.assertIn(fmt, self.html_content, f"Must include certified factory format dimension {fmt}")

        # 2. Certified 20ft / 40ft Container Limits & Capacities
        self.assertIn("1,200 Cases Standard (5.9m × 2.35m • 21-28T)", self.html_content, "Must specify 1,200 Cases for 20ft container")
        self.assertIn("2,400 Cases Standard (12.0m × 2.35m • 26.5T)", self.html_content, "Must specify 2,400 Cases for 40ft container")
        self.assertIn("maxCapacityCases = 1200", self.html_content, "Logistics engine must use 1,200 cases base for 20ft FCL")
        self.assertIn("maxCapacityCases = 2400", self.html_content, "Logistics engine must use 2,400 cases base for 40ft FCL")

        # 3. Pallet Tare Weight Accounting
        self.assertIn("palletTareKg", self.html_content, "Must calculate Euro Pallet tare weight in logistics engine")

        # 4. Critical Logistics Advisories
        self.assertIn("5.90m (L) × 2.35m (W) × 2.39m (H)", self.html_content, "Must detail 20ft container dimensions")
        self.assertIn("12.00m (L) × 2.35m (W) × 2.39m (H)", self.html_content, "Must detail 40ft container dimensions")
        self.assertIn("Direct Floor-Loading for Bulk Drums", self.html_content, "Must include floor-loading advisory")
        self.assertIn("Climate-Controlled Reefer Dispatch Option", self.html_content, "Must include reefer cold-chain advisory")

    def test_20_performance_optimization_standards(self):
        # 1. GSAP deferred loading
        self.assertIn('gsap.min.js" defer', self.html_content, "GSAP CDN script must have defer attribute")
        self.assertIn('ScrollTrigger.min.js" defer', self.html_content, "ScrollTrigger CDN script must have defer attribute")

        # 2. Hero and brand logo prioritized loading
        self.assertIn('fetchpriority="high"', self.html_content, "Hero and header logos must have fetchpriority='high' for LCP")

        # 3. Catalog cards and planograms lazy loading
        self.assertIn('loading="lazy" decoding="async"', self.html_content, "Below-the-fold media must have loading='lazy' and decoding='async'")
        self.assertIn('product.img}" alt="${name}" loading="lazy" decoding="async"', self.html_content, "Dynamic catalog card images must be lazy-loaded")

        # 5. INP (Interaction to Next Paint) Language Switcher & DOM Batching Standards
        self.assertIn('el.textContent = trans[key]', self.html_content, "switchLanguage must use textContent to eliminate layout thrashing")
        self.assertIn('createDocumentFragment', self.html_content, "renderProducts and renderMatrix must batch DOM mutations with DocumentFragment")
        self.assertIn('requestAnimationFrame', self.html_content, "switchLanguage must yield secondary below-the-fold updates to next animation frame")

    def test_21_container_3d_simulator_and_theme_engine(self):
        # 1. 3D Container Stacking Simulator Elements
        self.assertIn('id="container-3d-viewport"', self.html_content, "Must have 3D container visualizer stage")
        self.assertIn('id="sim-axle-ratio"', self.html_content, "Must have real-time axle balance ratio meter")
        self.assertIn('id="sim-btn-3d"', self.html_content, "Must have 3D isometric view mode button")
        self.assertIn('id="sim-btn-2d"', self.html_content, "Must have 2D planogram view mode button")
        self.assertIn('id="sim-hover-hud"', self.html_content, "Must have interactive pallet HUD tooltip")
        self.assertIn('function renderContainer3D', self.html_content, "Must define renderContainer3D engine")
        self.assertIn('function setSimulatorView', self.html_content, "Must define setSimulatorView function")
        self.assertIn('function buildIsometricSvg', self.html_content, "Must generate isometric 3D SVG projection")
        self.assertIn('function buildPlanogramSvg', self.html_content, "Must generate 2D planogram SVG layout")

        # 2. Dual Ambience Theme Mode Engine Elements
        self.assertIn('id="theme-toggle-btn"', self.html_content, "Must have desktop header theme toggle button")
        self.assertIn('id="mob-theme-toggle-btn"', self.html_content, "Must have mobile drawer theme toggle button")
        self.assertIn('theme-daylight', self.html_content, "Must define theme-daylight CSS class styles")
        self.assertIn('function toggleTheme', self.html_content, "Must define toggleTheme function")
        self.assertIn('function initTheme', self.html_content, "Must define initTheme function")
        self.assertIn("localStorage.getItem('mariam_theme')", self.html_content, "Theme engine must persist choice to localStorage")

        # 3. Bilingual Key Symmetry & Prohibitions
        self.assertIn('"sim_title"', self.html_content, "Must have sim_title in translation dictionary")
        self.assertIn('"theme_obsidian_label"', self.html_content, "Must have theme_obsidian_label in translation dictionary")
        self.assertIn('"theme_daylight_label"', self.html_content, "Must have theme_daylight_label in translation dictionary")
        lower = self.html_content.lower()
        self.assertNotIn(".pdf", lower, "Strict PDF prohibition: zero PDF files allowed")
        self.assertNotIn("pouch", lower, "Strict glass-only packaging directive")
        self.assertNotIn("spray can", lower, "Strict glass-only packaging directive")

    def test_22_retail_roi_margin_calculator_and_daylight_perfection(self):
        # 1. Interactive Dual Mode Switcher in #calculator
        self.assertIn('id="calc-tab-logistics"', self.html_content, "Must have Logistics Calculator Mode tab")
        self.assertIn('id="calc-tab-roi"', self.html_content, "Must have Retail ROI Simulator Mode tab")
        self.assertIn('id="logistics-calculator-container"', self.html_content, "Must have container for logistics mode")
        self.assertIn('id="roi-simulator-container"', self.html_content, "Must have container for retail ROI simulator")

        # 2. Retail ROI Simulator Inputs & Controls
        self.assertIn('id="roi-market"', self.html_content, "Must have destination export market dropdown")
        self.assertIn('id="roi-sku"', self.html_content, "Must have product SKU selector")
        self.assertIn('id="roi-srp"', self.html_content, "Must have target consumer shelf price (SRP) input")
        self.assertIn('id="roi-srp-range"', self.html_content, "Must have target SRP slider")
        self.assertIn('id="roi-stores"', self.html_content, "Must have supermarket chain store count input")
        self.assertIn('id="roi-stores-range"', self.html_content, "Must have chain store count slider")
        self.assertIn('id="roi-facings"', self.html_content, "Must have shelf facings input")
        self.assertIn('id="roi-facings-range"', self.html_content, "Must have shelf facings slider")

        # 3. Commercial Profitability Cockpit & Financial KPI Outputs
        self.assertIn('id="out-roi-landed"', self.html_content, "Must have estimated CIF landed cost output")
        self.assertIn('id="out-roi-margin"', self.html_content, "Must have gross retail margin percentage output")
        self.assertIn('id="out-roi-margin-badge"', self.html_content, "Must have dynamic margin tier badge")
        self.assertIn('id="out-roi-annual-store"', self.html_content, "Must have annual profit per store output")
        self.assertIn('id="out-roi-annual-chain"', self.html_content, "Must have total chain annual profit output")
        self.assertIn('id="roi-margin-bar"', self.html_content, "Must have visual margin progress meter")

        # 4. Unit Economics Waterfall Breakdown Table
        self.assertIn('id="out-roi-fob"', self.html_content, "Must display base FOB price")
        self.assertIn('id="out-roi-freight"', self.html_content, "Must display ocean freight allocation")
        self.assertIn('id="out-roi-duty"', self.html_content, "Must display customs duty rate")
        self.assertIn('id="out-roi-landed-detail"', self.html_content, "Must display landed CIF unit breakdown")
        self.assertIn('id="out-roi-srp-exvat"', self.html_content, "Must display consumer price excluding VAT")
        self.assertIn('id="out-roi-profit-jar"', self.html_content, "Must display net retailer gross profit per jar")
        self.assertIn('id="out-roi-annual-units"', self.html_content, "Must display projected annual chain volume")

        # 5. Core JavaScript Financial Modeling Functions
        self.assertIn('function switchCalculatorMode', self.html_content, "Must define switchCalculatorMode function")
        self.assertIn('function calculateRetailROI', self.html_content, "Must define calculateRetailROI calculation engine")
        self.assertIn('function transferROIToRFQ', self.html_content, "Must define transferROIToRFQ function")
        self.assertIn('function copyROISummary', self.html_content, "Must define copyROISummary export function")

        # 6. Daylight Theme Mode Perfection CSS
        self.assertIn('html.theme-daylight section#terroir', self.html_content, "Daylight theme must override #terroir gradient")
        self.assertIn('html.theme-daylight section#catalog', self.html_content, "Daylight theme must override #catalog gradient")
        self.assertIn('html.theme-daylight section#calculator', self.html_content, "Daylight theme must override #calculator gradient")
        self.assertIn('html.theme-daylight section#shipping', self.html_content, "Daylight theme must override #shipping gradient")
        self.assertIn('html.theme-daylight section#rfq', self.html_content, "Daylight theme must override #rfq gradient")
        self.assertIn('html.theme-daylight .glass-card-shell', self.html_content, "Daylight theme must calibrate glass card shells")
        self.assertIn('html.theme-daylight .glass-card-core', self.html_content, "Daylight theme must calibrate glass card cores")
        self.assertIn('html.theme-daylight .hero-vignette', self.html_content, "Daylight theme must suppress hero vignette to keep 4K photo visible")
        self.assertIn('html.theme-daylight .hero-caption-plate', self.html_content, "Daylight theme must style hero caption plate as porcelain card")
        self.assertIn('class="hero-caption-plate', self.html_content, "Hero caption plate must have semantic class")
        self.assertIn('class="hero-vignette', self.html_content, "Hero vignette must have semantic class")

        # 7. Bilingual Translation Parity & Sacred Directives
        self.assertIn('"calc_tab_logistics"', self.html_content, "Must translate calc_tab_logistics")
        self.assertIn('"calc_tab_roi"', self.html_content, "Must translate calc_tab_roi")
        self.assertIn('"roi_title"', self.html_content, "Must translate roi_title")
        self.assertIn('"roi_gross_margin"', self.html_content, "Must translate roi_gross_margin")
        self.assertIn('"roi_annual_chain"', self.html_content, "Must translate roi_annual_chain")
        lower = self.html_content.lower()
        self.assertNotIn(".pdf", lower, "Strict PDF prohibition: zero PDF files allowed")
        self.assertNotIn("pouch", lower, "Strict glass-only packaging directive")
        self.assertNotIn("spray can", lower, "Strict glass-only packaging directive")

    def test_23_luxury_interactive_dock_and_motion_engines(self):
        # 1. 3D Gyro-Tilt and Specular Gold Sheen Architecture
        self.assertIn('.tilt-card', self.html_content, "Must define .tilt-card CSS class for 3D perspective")
        self.assertIn('.specular-sheen-layer', self.html_content, "Must define .specular-sheen-layer CSS class for dynamic gold sheen")
        self.assertIn('function init3DTiltEngine', self.html_content, "Must define init3DTiltEngine function")
        self.assertIn('matchMedia', self.html_content, "Must check matchMedia hover capability for touch device performance")
        self.assertIn('perspective(1000px)', self.html_content, "Must apply CSS perspective transform matrix")
        self.assertIn('radial-gradient', self.html_content, "Must apply dynamic radial gradient specular highlight")

        # 2. Ambient Chiaroscuro Cursor Spotlight
        self.assertIn('id="ambient-cursor-spotlight"', self.html_content, "Must have #ambient-cursor-spotlight element in DOM")
        self.assertIn('function initAmbientCursorSpotlight', self.html_content, "Must define initAmbientCursorSpotlight function")
        self.assertIn('pointer-events-none', self.html_content, "Spotlight must be non-blocking for user interactions")

        # 3. Executive Floating Glass Command Dock (Dynamic Island)
        self.assertIn('id="floating-command-dock"', self.html_content, "Must have #floating-command-dock element in DOM")
        self.assertIn('.dock-glass-pill', self.html_content, "Must style dock pills with .dock-glass-pill glassmorphic treatment")
        self.assertIn('id="dock-sample-count-badge"', self.html_content, "Must have #dock-sample-count-badge for real-time RFQ counter")
        self.assertIn('id="dock-current-currency"', self.html_content, "Must have #dock-current-currency for instant currency switch")
        self.assertIn('id="dock-theme-icon-sun"', self.html_content, "Must have #dock-theme-icon-sun in floating dock")
        self.assertIn('id="dock-theme-icon-moon"', self.html_content, "Must have #dock-theme-icon-moon in floating dock")
        self.assertIn('id="dock-lang-label"', self.html_content, "Must have #dock-lang-label in floating dock")
        self.assertIn('function initDockScrollBehavior', self.html_content, "Must define initDockScrollBehavior function")
        self.assertIn('dock-hidden', self.html_content, "Must define dock-hidden class for scroll velocity concealment")

        # 4. Rolling Odometer Engine (Cubic Easing)
        self.assertIn('function animateOdometer', self.html_content, "Must define animateOdometer choreography engine")
        self.assertIn('out-total-cases', self.html_content, "Must update out-total-cases with odometer")
        self.assertIn('out-total-jars', self.html_content, "Must update out-total-jars with odometer")
        self.assertIn('out-roi-annual-chain', self.html_content, "Must update out-roi-annual-chain with odometer")
        self.assertIn('out-roi-annual-store', self.html_content, "Must update out-roi-annual-store with odometer")

        # 5. Bilingual Symmetry & Sacred Brand Rules
        self.assertIn('"dock_rfq_label"', self.html_content, "Must include dock_rfq_label in translation dictionary")
        has_logo = any('arina-logo-gold.png' in src or 'mariam-logo-gold.png' in src for src in self.parser.images) or 'arina-logo-gold.png' in self.html_content or 'mariam-logo-gold.png' in self.html_content
        self.assertTrue(has_logo, "Must preserve sacred brand logo arina-logo-gold.png")
        lower = self.html_content.lower()
        self.assertNotIn(".pdf", lower, "Strict PDF prohibition: zero PDF files allowed")
        self.assertNotIn("pouch", lower, "Strict glass-only packaging directive")
        self.assertNotIn("spray can", lower, "Strict glass-only packaging directive")

    def test_24_strict_zero_honey_directive(self):
        """Verify honey has been completely removed from the project per user directive."""
        self.assertNotIn('honey-showcase', self.parser.ids, "Must not have #honey-showcase section")
        self.assertNotIn("honey", self.html_content.lower(), "Must have zero occurrences of 'honey' in website.html")
        self.assertNotIn("عسل", self.html_content, "Must have zero occurrences of 'عسل' in website.html")
        self.assertNotIn("switchWebHoneyProduct", self.html_content)
        self.assertNotIn("WEB_HONEY_DATA", self.html_content)

    def test_25_spain_madrid_office_whatsapp_integration(self):
        """Verify Spain Madrid Office WhatsApp desk (+34 641 648 681) integration across the portal."""
        # 1. Phone number & wa.me link presence
        self.assertIn("+34 641 648 681", self.html_content, "Must display Spain Madrid WhatsApp number +34 641 648 681")
        self.assertIn("wa.me/34641648681", self.html_content, "Must link to official Spain WhatsApp wa.me/34641648681")
        
        # 2. Key Interactive IDs for Spain Madrid desk
        self.assertIn("whatsapp-rfq-spain-link", self.html_content, "Must have #whatsapp-rfq-spain-link")
        self.assertIn("whatsapp-form-spain-btn", self.html_content, "Must have #whatsapp-form-spain-btn")
        self.assertIn("whatsapp-modal-spain-btn", self.html_content, "Must have #whatsapp-modal-spain-btn")
        
        # 3. Dynamic JS updater for Spain desk
        self.assertIn("waSpainIds", self.html_content, "Must have waSpainIds array in updateProforma")
        
        # 4. Translation keys
        self.assertIn('"btn_whatsapp_spain"', self.html_content, "Must have btn_whatsapp_spain translation key")
        self.assertIn('"rfq_form_whatsapp_spain_btn"', self.html_content, "Must have rfq_form_whatsapp_spain_btn translation key")
        self.assertIn('"modal_whatsapp_spain_btn"', self.html_content, "Must have modal_whatsapp_spain_btn translation key")
        self.assertIn('"footer_wa_madrid"', self.html_content, "Must have footer_wa_madrid translation key")
        self.assertIn('"mob_menu_whatsapp_spain"', self.html_content, "Must have mob_menu_whatsapp_spain translation key")

    def test_26_upper_page_whatsapp_desks_integration(self):
        """Verify upper page (Header & Hero) dual WhatsApp desks integration."""
        # 1. Header WhatsApp Pill and Popover Dropdown
        self.assertIn('id="whatsapp-header-btn"', self.html_content, "Must have #whatsapp-header-btn in header")
        self.assertIn('id="whatsapp-header-dropdown"', self.html_content, "Must have #whatsapp-header-dropdown in header")
        self.assertIn('toggleWhatsAppHeaderDropdown', self.html_content, "Must define toggleWhatsAppHeaderDropdown function")
        
        # 2. Both Egypt and Spain desks in Header dropdown
        self.assertIn('wa.me/201008716714', self.html_content, "Must link to Egypt WhatsApp wa.me/201008716714")
        self.assertIn('wa.me/34641648681', self.html_content, "Must link to Spain WhatsApp wa.me/34641648681")
        
        # 3. Hero Section Fast-Connect Chips
        self.assertIn('hero-wa-chip', self.html_content, "Must have .hero-wa-chip in Hero section")
        self.assertIn('data-i18n="hero_wa_direct"', self.html_content, "Must have hero_wa_direct translation anchor")
        self.assertIn('data-i18n="hero_wa_cairo"', self.html_content, "Must have hero_wa_cairo translation anchor")
        self.assertIn('data-i18n="hero_wa_madrid"', self.html_content, "Must have hero_wa_madrid translation anchor")
        
        # 4. Translation keys in English and Arabic dictionaries
        for key in ['nav_wa_desks', 'nav_wa_dropdown_title', 'nav_wa_cairo_title', 'nav_wa_madrid_title', 'hero_wa_direct', 'hero_wa_cairo', 'hero_wa_madrid']:
            self.assertIn(f'"{key}"', self.html_content, f"Must define translation key {key}")
            
        # 5. Daylight Theme calibration
        self.assertIn('html.theme-daylight #whatsapp-header-dropdown', self.html_content, "Must have daylight theme style for whatsapp dropdown")
        self.assertIn('html.theme-daylight .hero-wa-chip', self.html_content, "Must have daylight theme style for hero chips")

        # 6. BiDi isolation for phone numbers across RTL contexts
        self.assertIn('<bdi dir="ltr">+20 10 08716714</bdi>', self.html_content, "Egypt phone number must be wrapped in bdi dir=ltr")
        self.assertIn('<bdi dir="ltr">+34 641 648 681</bdi>', self.html_content, "Spain phone number must be wrapped in bdi dir=ltr")

if __name__ == '__main__':
    unittest.main()




