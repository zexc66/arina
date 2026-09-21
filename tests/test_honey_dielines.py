# tests/test_honey_dielines.py
import os
import unittest
from PIL import Image

class TestHoneyDielines(unittest.TestCase):
    def setUp(self):
        # Path resilience: resolve output/dielines from either current working directory or relative to test file
        if os.path.isdir("output/dielines"):
            self.output_dir = "output/dielines"
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.output_dir = os.path.join(base_dir, "output", "dielines")

        self.expected_formats = [
            ("dieline_honey_500g_standard.png", (2200, 900)),
            ("dieline_honey_1kg_family.png", (2600, 1100)),
            ("dieline_royal_mix_500g_wide.png", (2400, 850)),
            ("dieline_honeycomb_500g_hex.png", (1800, 900)),
            ("dieline_tamper_ribbon_crown.png", (450, 1125)),
            ("dieline_discovery_flight_50g.png", (1200, 400)),
        ]
        self.blush_pink = (232, 197, 200)
        self.burgundy = (105, 22, 48)
        self.gold_foil = (218, 172, 54)

    def test_dielines_exist_and_match_dimensions(self):
        for filename, expected_size in self.expected_formats:
            path = os.path.join(self.output_dir, filename)
            self.assertTrue(os.path.exists(path), f"Missing dieline: {filename}")
            with Image.open(path) as im:
                self.assertEqual(im.size, expected_size, f"{filename} size mismatch: {im.size} vs {expected_size}")

    def test_brand_colors_present_in_tamper_ribbon(self):
        ribbon_path = os.path.join(self.output_dir, "dieline_tamper_ribbon_crown.png")
        self.assertTrue(os.path.exists(ribbon_path), f"Tamper ribbon missing: {ribbon_path}")
        with Image.open(ribbon_path) as im:
            rgb_im = im.convert("RGB")
            colors = rgb_im.getcolors(maxcolors=im.width * im.height)
            unique_rgb = {c[1] for c in colors}
            # Check Blush Pink background
            self.assertIn(self.blush_pink, unique_rgb, "Blush Pink missing from tamper ribbon")
            # Check Gold Foil crown seal
            self.assertIn(self.gold_foil, unique_rgb, "Luxor Gold missing from tamper ribbon")

    def test_path_resilience(self):
        """Verify that output/dielines resolves correctly both from cwd and relative to file."""
        self.assertTrue(os.path.isdir(self.output_dir), f"Directory {self.output_dir} does not exist")
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        expected_dir = os.path.join(root_dir, "output", "dielines")
        self.assertTrue(os.path.isdir(expected_dir), f"Directory {expected_dir} does not exist")

if __name__ == "__main__":
    unittest.main()
