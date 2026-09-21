import os
import unittest
import re

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARIAM_HTML_PATH = os.path.join(WORKSPACE_DIR, 'mariam.html')

class TestWebCatalogHoneyShowcase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(MARIAM_HTML_PATH):
            raise unittest.SkipTest("mariam.html not found")
        with open(MARIAM_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()

    def test_01_honey_and_superfoods_collection_present(self):
        """Verify the core title and collection heading are present."""
        self.assertIn("Natural Honey & Superfoods", self.html_content,
                      "mariam.html must contain 'Natural Honey & Superfoods'")
        self.assertIn("MARIAM ROYAL MIX", self.html_content,
                      "mariam.html must feature hero product 'MARIAM ROYAL MIX'")

    def test_02_packaging_size_standards(self):
        """Verify 500g and 1kg packaging standards and size switcher."""
        self.assertIn("500g", self.html_content, "mariam.html must reference 500g packaging standard")
        self.assertIn("1kg", self.html_content, "mariam.html must reference 1kg packaging standard")

    def test_03_sacred_brand_logo_reference(self):
        """Verify authentic logo reference per Sacred Brand Identity Rule."""
        self.assertIn("mariam-logo-gold.png", self.html_content,
                      "mariam.html must reference authentic cursive gold logo 'mariam-logo-gold.png'")

    def test_04_dieline_blueprint_references(self):
        """Verify references to high-precision generated dielines."""
        self.assertIn("dieline_royal_mix_500g_wide.png", self.html_content,
                      "mariam.html must reference dieline_royal_mix_500g_wide.png")
        self.assertIn("dieline_tamper_ribbon_crown.png", self.html_content,
                      "mariam.html must reference dieline_tamper_ribbon_crown.png")

    def test_05_royal_mix_purity_and_ingredients(self):
        """Verify Hero Royal Mix guarantees: 0% peanuts, 100% tree nuts, super seeds, fresh royal jelly."""
        content = self.html_content
        self.assertTrue(re.search(r'0%\s*Peanuts', content, re.IGNORECASE),
                        "Must prominently display 0% Peanuts guarantee")
        self.assertTrue(re.search(r'Tree\s*Nuts', content, re.IGNORECASE),
                        "Must display Tree Nuts")
        self.assertTrue(re.search(r'Super\s*Seeds', content, re.IGNORECASE),
                        "Must display Super Seeds")
        self.assertTrue(re.search(r'Royal\s*Jelly', content, re.IGNORECASE),
                        "Must display Royal Jelly")

    def test_06_brand_color_palette_styling(self):
        """Verify Blush Pink (#E8C5C8), Imperial Burgundy (#691630), and Luxor Gold (#DAAC36)."""
        content_upper = self.html_content.upper()
        self.assertIn("#E8C5C8", content_upper, "Blush Pink (#E8C5C8) styling must be present in mariam.html")
        self.assertIn("#691630", content_upper, "Imperial Burgundy (#691630) styling must be present in mariam.html")
        self.assertTrue("#DAAC36" in content_upper or "#D4A836" in content_upper,
                        "Luxor Gold styling must be present in mariam.html")

    def test_07_tamper_ribbon_and_crown_seal(self):
        """Verify tamper-evident ribbon with royal crown seal is highlighted."""
        content_lower = self.html_content.lower()
        self.assertTrue("tamper" in content_lower or "ribbon" in content_lower,
                        "Tamper ribbon must be referenced")
        self.assertTrue("crown" in content_lower, "Crown seal must be referenced")

    def test_08_existing_sections_preserved(self):
        """Verify existing slide deck sections (slide-1 through slide-9) remain intact."""
        for i in range(1, 10):
            slide_id = f'id="slide-{i}"'
            self.assertIn(slide_id, self.html_content, f"Existing section {slide_id} must be preserved in mariam.html")
        self.assertIn("Mariam Food Industries", self.html_content,
                      "Mariam Food Industries company title must be preserved")

if __name__ == '__main__':
    unittest.main()
