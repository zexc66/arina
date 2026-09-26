import os
import unittest
from PIL import Image

class TestUltraSharpHoneyImagery(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.imagery_dir = os.path.join(base_dir, "output", "imagery")
        self.expected_packshots = [
            ("mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_black_seed_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_citrus_blossom_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_sidr_500g_open_jar_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_cap_seal_and_ribbon_macro_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_master_ecommerce_lineup_white_studio_4k.jpg", (3840, 2160)),
        ]

    def test_all_packshots_exist_and_match_dimensions(self):
        for fname, size in self.expected_packshots:
            p = os.path.join(self.imagery_dir, fname)
            self.assertTrue(os.path.exists(p), f"Missing: {fname}")
            with Image.open(p) as im:
                self.assertEqual(im.size, size, f"{fname} size mismatch: {im.size} vs {size}")

    def test_white_studio_corners_pure_white(self):
        for fname, _ in self.expected_packshots:
            p = os.path.join(self.imagery_dir, fname)
            with Image.open(p) as im:
                corners = [
                    im.getpixel((10, 10))[:3],
                    im.getpixel((im.width - 10, 10))[:3],
                    im.getpixel((10, im.height - 10))[:3],
                    im.getpixel((im.width - 10, im.height - 10))[:3],
                ]
                for idx, c in enumerate(corners):
                    self.assertGreaterEqual(min(c), 253, f"{fname} corner {idx+1} not pure white: {c}")

    def test_logo_is_strictly_luxor_gold_and_no_burgundy(self):
        for fname, _ in self.expected_packshots:
            if "lineup" in fname:
                continue
            p = os.path.join(self.imagery_dir, fname)
            with Image.open(p) as im:
                w, h = im.size
                pixels = [im.getpixel((x, y)) for x in range(w//3, 2*w//3, 15) for y in range(h//3, 2*h//3, 15)]
                gold = [px for px in pixels if px[0] > 180 and px[1] > 140 and px[2] < 100]
                exact_burgundy = [px for px in pixels if abs(px[0]-118) < 6 and abs(px[1]-18) < 6 and abs(px[2]-46) < 6]
                self.assertGreater(len(gold), 50, f"{fname} lacks Luxor Gold logo pixels: {len(gold)}")
                self.assertEqual(len(exact_burgundy), 0, f"{fname} contains unauthorized burgundy logo pixels!")

if __name__ == "__main__":
    unittest.main()
