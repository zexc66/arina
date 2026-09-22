import os
import unittest
from PIL import Image

class TestPrintMockups(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.mockups_dir = os.path.join(base_dir, "output", "mockups")
        self.expected_files = [
            ("mariam_honey_sidr_500g_printable_label_sheet_a4_300dpi.png", (3508, 2480)),
            ("mariam_honey_royal_mix_500g_printable_label_sheet_a4_300dpi.png", (3508, 2480)),
            ("mariam_honey_master_press_proof_sheet_a3_300dpi.png", (4960, 3508)),
            ("mariam_honey_sidr_500g_photorealistic_print_mockup_4k.jpg", (3840, 2160)),
            ("mariam_honey_packaging_evaluation_board_4k.jpg", (3840, 2160)),
            ("mariam_royal_mix_500g_printable_label_sheet_a4_300dpi.png", (3508, 2480)),
            ("mariam_packaging_press_proof_sheet_a3_300dpi.png", (4960, 3508)),
            ("mariam_royal_mix_500g_photorealistic_print_mockup_4k.jpg", (3840, 2160)),
            ("mariam_packaging_print_evaluation_board_4k.jpg", (3840, 2160)),
            ("mariam_olives_370g_printable_label_sheet_a4_300dpi.png", (3508, 2480)),
        ]
        self.blush_pink = (245, 183, 194)
        self.burgundy = (118, 18, 46)
        self.gold_foil = (218, 172, 54)

    def test_mockup_files_exist_and_match_dimensions(self):
        self.assertTrue(os.path.isdir(self.mockups_dir), f"Directory {self.mockups_dir} does not exist")
        for filename, expected_size in self.expected_files:
            path = os.path.join(self.mockups_dir, filename)
            self.assertTrue(os.path.exists(path), f"Missing mockup file: {filename}")
            with Image.open(path) as im:
                self.assertEqual(im.size, expected_size, f"{filename} size mismatch: {im.size} vs {expected_size}")

    def test_honey_brand_colors_in_printable_sheet(self):
        path = os.path.join(self.mockups_dir, "mariam_honey_sidr_500g_printable_label_sheet_a4_300dpi.png")
        self.assertTrue(os.path.exists(path))
        with Image.open(path) as im:
            rgb_im = im.convert("RGB")
            colors = rgb_im.getcolors(maxcolors=im.width * im.height)
            unique_rgb = {c[1] for c in colors}
            self.assertIn(self.blush_pink, unique_rgb, "Blush Pink missing from honey printable A4 sheet")
            self.assertIn(self.burgundy, unique_rgb, "Wine Burgundy missing from honey printable A4 sheet")
            self.assertIn(self.gold_foil, unique_rgb, "Luxor Gold missing from honey printable A4 sheet")

    def test_royal_mix_solid_pink_colors(self):
        path = os.path.join(self.mockups_dir, "mariam_honey_royal_mix_500g_printable_label_sheet_a4_300dpi.png")
        self.assertTrue(os.path.exists(path))
        with Image.open(path) as im:
            rgb_im = im.convert("RGB")
            colors = rgb_im.getcolors(maxcolors=im.width * im.height)
            unique_rgb = {c[1] for c in colors}
            self.assertIn(self.blush_pink, unique_rgb, "Blush Pink missing from royal mix pink sheet")
            self.assertIn(self.burgundy, unique_rgb, "Wine Burgundy missing from royal mix pink sheet")
            self.assertIn(self.gold_foil, unique_rgb, "Luxor Gold missing from royal mix pink sheet")

if __name__ == "__main__":
    unittest.main()
