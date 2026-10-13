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
        self.assertEqual(len(EXPECTED_EANS), len(set(EXPECTED_EANS)), "EAN codes must be unique")
        for ean in EXPECTED_EANS:
            self.assertIn(ean, self.html_content, f"Missing EAN {ean} in website.html")
            self.assertEqual(len(ean), 13, f"EAN {ean} must be 13 digits")
            self.assertTrue(ean.isdigit(), f"EAN {ean} must be numeric")

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

if __name__ == '__main__':
    unittest.main()
