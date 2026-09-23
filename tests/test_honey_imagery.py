import os
import unittest
from PIL import Image

class TestHoneyImagery(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.imagery_dir = os.path.join(base_dir, "output", "imagery")
        self.expected_images = [
            # Macro & Lifestyle Gastronomy
            ("mariam_honey_sidr_macro_dipper_drizzle_4k.jpg", (3000, 3000)),
            ("mariam_honey_honeycomb_hex_artisan_lifestyle_4k.jpg", (3840, 2160)),
            ("mariam_honey_afternoon_tea_ricotta_figs_lifestyle_4k.jpg", (3840, 2160)),
            ("mariam_honey_gift_flight_box_unboxing_editorial_4k.jpg", (3840, 2160)),
            ("mariam_honey_royal_mix_ingredients_flatlay_4k.jpg", (3000, 3000)),
            ("mariam_honey_luxury_boutique_shelf_display_4k.jpg", (3840, 2160)),
            ("mariam_honey_mountain_sidr_terroir_lifestyle_4k.jpg", (3840, 2160)),
            ("mariam_honey_wellness_breakfast_lifestyle_4k.jpg", (3840, 2160)),
            ("mariam_honey_royal_mix_macro_spoon_drizzle_4k.jpg", (3000, 3000)),
            ("mariam_honey_royal_mix_hero_commercial_4k.jpg", (3000, 3000)),
            # Multi-Packshots White Studio
            ("mariam_honey_golden_nectars_duo_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_connoisseur_duo_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_six_jar_regal_panorama_white_studio_4k.jpg", (3840, 2160)),
            ("mariam_honey_master_collection_white_studio_hero_4k.jpg", (3840, 2160)),
            ("mariam_honey_flagship_quartet_white_studio_4k.jpg", (3840, 2160)),
            ("mariam_honey_pure_reserves_trio_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_superfood_duo_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_size_comparison_500g_vs_1kg_white_studio_4k.jpg", (3000, 3000)),
            # Individual 4K PDP Packshots
            ("mariam_honey_royal_mix_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_mountain_sidr_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_clover_blossom_1kg_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_raw_honeycomb_hex_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_royal_jelly_elixir_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_discovery_flight_box_white_studio_hero_4k.jpg", (3000, 3000)),
            # New E-Commerce Multi-Angle & Open Jar Packshots (Pure White #FFFFFF)
            ("mariam_honey_sidr_500g_open_jar_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_royal_mix_500g_open_jar_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_raw_honeycomb_hex_500g_open_jar_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_cap_seal_and_ribbon_macro_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_royal_mix_500g_back_label_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_black_seed_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_citrus_blossom_500g_white_studio_hero_4k.jpg", (3000, 3000)),
            ("mariam_honey_sidr_500g_45deg_angle_white_studio_4k.jpg", (3000, 3000)),
            # New E-Commerce Curated Bundles (Pure White #FFFFFF)
            ("mariam_honey_open_jars_connoisseur_duo_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_functional_wellness_trio_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_breakfast_spreads_duo_white_studio_4k.jpg", (3000, 3000)),
            ("mariam_honey_master_ecommerce_lineup_white_studio_4k.jpg", (3840, 2160)),
        ]

    def test_all_honey_imagery_exists_and_matches_resolution(self):
        self.assertTrue(os.path.isdir(self.imagery_dir))
        for filename, expected_size in self.expected_images:
            path = os.path.join(self.imagery_dir, filename)
            self.assertTrue(os.path.exists(path), f"Missing honey image: {filename}")
            with Image.open(path) as im:
                self.assertEqual(im.size, expected_size, f"{filename} size mismatch: {im.size} vs {expected_size}")
                # Verify minimum file size (at least 200KB for high-res JPEG)
                fsize = os.path.getsize(path)
                self.assertGreater(fsize, 200 * 1024, f"{filename} file size too small: {fsize} bytes")

    def test_white_studio_corners_pure_white(self):
        white_studio_imgs = [fname for fname, _ in self.expected_images if "white_studio" in fname]
        for fname in white_studio_imgs:
            path = os.path.join(self.imagery_dir, fname)
            with Image.open(path) as im:
                corners = [
                    im.getpixel((10, 10))[:3],
                    im.getpixel((im.width - 10, 10))[:3],
                    im.getpixel((10, im.height - 10))[:3],
                    im.getpixel((im.width - 10, im.height - 10))[:3],
                ]
                for idx, c in enumerate(corners):
                    # Verify pure white within JPEG DCT quantization tolerance (>= 253)
                    self.assertGreaterEqual(min(c), 253, f"{fname} corner {idx+1} is not pure white: {c}")
                    # Verify neutral white balance (R, G, B within 2 levels of each other)
                    self.assertLessEqual(max(c) - min(c), 2, f"{fname} corner {idx+1} not neutral white: {c}")

if __name__ == "__main__":
    unittest.main()
