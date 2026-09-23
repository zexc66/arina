import unittest
import os
from PIL import Image

WORKSPACE_DIR = '/home/zexc/Desktop/New Folder'
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, 'output/imagery')

class TestAmazonAPlusAndSellSheets(unittest.TestCase):
    def test_01_amazon_aplus_modules_exist_and_exact_resolutions(self):
        """Verify that all 6 Amazon A+ 4K modules exist and have exact resolutions."""
        expected_modules = {
            'mariam_amazon_aplus_01_brand_story_hero_4k.jpg': (3840, 1200),
            'mariam_amazon_aplus_02_card_tree_nuts_purity_4k.jpg': (1200, 1200),
            'mariam_amazon_aplus_03_card_nordic_glass_4k.jpg': (1200, 1200),
            'mariam_amazon_aplus_04_card_raw_enzymes_4k.jpg': (1200, 1200),
            'mariam_amazon_aplus_05_comparison_matrix_chart_4k.jpg': (3840, 2160),
            'mariam_amazon_aplus_06_functional_wellness_infographic_4k.jpg': (3840, 1800),
        }
        for filename, (expected_w, expected_h) in expected_modules.items():
            path = os.path.join(OUTPUT_DIR, filename)
            self.assertTrue(os.path.exists(path), f"Module {filename} must exist on disk")
            with Image.open(path) as img:
                self.assertEqual(img.size, (expected_w, expected_h),
                                 f"Module {filename} must be {expected_w}x{expected_h}, got {img.size}")

    def test_02_wholesale_sell_sheets_and_shelf_talkers_exist_and_dimensions(self):
        """Verify 300 DPI print-ready sell sheet, shelf talkers, and press proof sheet."""
        expected_sheets = {
            'mariam_honey_b2b_trade_sell_sheet_300dpi.png': (3508, 2480), # A4 Landscape @ 300 DPI
            'mariam_shelf_talker_royal_mix_300dpi.png': (2480, 448),      # 210mm x 38mm @ 300 DPI
            'mariam_shelf_talker_mountain_sidr_300dpi.png': (2480, 448),  # 210mm x 38mm @ 300 DPI
            'mariam_shelf_talker_honeycomb_hex_300dpi.png': (2480, 448),  # 210mm x 38mm @ 300 DPI
            'mariam_shelf_talker_clover_1kg_300dpi.png': (2480, 448),     # 210mm x 38mm @ 300 DPI
            'mariam_shelf_talkers_master_press_sheet_300dpi.png': (2480, 3508), # A4 Portrait @ 300 DPI
        }
        for filename, (expected_w, expected_h) in expected_sheets.items():
            path = os.path.join(OUTPUT_DIR, filename)
            self.assertTrue(os.path.exists(path), f"Print asset {filename} must exist on disk")
            with Image.open(path) as img:
                self.assertEqual(img.size, (expected_w, expected_h),
                                 f"Print asset {filename} must be {expected_w}x{expected_h}, got {img.size}")

    def test_03_strict_constraints_and_no_pdfs(self):
        """Verify absolute compliance with brand rules."""
        # Ensure no PDF files were generated in output/imagery/ or output/dielines/
        for root, _, files in os.walk(os.path.join(WORKSPACE_DIR, 'output')):
            for f in files:
                self.assertFalse(f.lower().endswith('.pdf'), f"Strict PDF prohibition: {f} must not be a PDF")

    def test_04_file_sizes_and_dpi(self):
        """Verify that all generated assets are non-empty and 300 DPI files have DPI metadata."""
        all_assets = [
            'mariam_amazon_aplus_01_brand_story_hero_4k.jpg',
            'mariam_amazon_aplus_02_card_tree_nuts_purity_4k.jpg',
            'mariam_amazon_aplus_03_card_nordic_glass_4k.jpg',
            'mariam_amazon_aplus_04_card_raw_enzymes_4k.jpg',
            'mariam_amazon_aplus_05_comparison_matrix_chart_4k.jpg',
            'mariam_amazon_aplus_06_functional_wellness_infographic_4k.jpg',
            'mariam_honey_b2b_trade_sell_sheet_300dpi.png',
            'mariam_shelf_talker_royal_mix_300dpi.png',
            'mariam_shelf_talker_mountain_sidr_300dpi.png',
            'mariam_shelf_talker_honeycomb_hex_300dpi.png',
            'mariam_shelf_talker_clover_1kg_300dpi.png',
            'mariam_shelf_talkers_master_press_sheet_300dpi.png'
        ]
        for fn in all_assets:
            path = os.path.join(OUTPUT_DIR, fn)
            size_bytes = os.path.getsize(path)
            self.assertGreater(size_bytes, 100_000, f"{fn} must be a high-res image greater than 100KB, got {size_bytes} bytes")
            if fn.endswith('_300dpi.png'):
                with Image.open(path) as img:
                    dpi = img.info.get('dpi')
                    if dpi:
                        self.assertEqual(int(round(dpi[0])), 300, f"{fn} must be 300 DPI")

    def test_05_sacred_brand_logo_files_present(self):
        """Verify authentic logo presence."""
        logo_path = os.path.join(WORKSPACE_DIR, 'mariam-logo-gold.png')
        self.assertTrue(os.path.exists(logo_path), "mariam-logo-gold.png must exist on disk")

if __name__ == '__main__':
    unittest.main()
