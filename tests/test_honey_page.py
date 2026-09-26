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
