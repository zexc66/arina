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

if __name__ == "__main__":
    unittest.main()
