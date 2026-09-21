# tests/test_honey_catalog.py
import json
import os
import unittest

class TestMariamHoneyCatalog(unittest.TestCase):
    def setUp(self):
        self.catalog_path = "data/mariam_honey_catalog.json"

    def test_catalog_file_exists_and_valid_json(self):
        self.assertTrue(os.path.exists(self.catalog_path), "Catalog file does not exist")
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("brand", data)
        self.assertEqual(data["brand"], "Mariam")
        self.assertEqual(data["category"], "Natural Honey & Superfoods")
        self.assertIn("families", data)

    def test_core_launch_skus_present(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        skus = {item["sku"]: item for family in data["families"] for item in family["items"]}
        required_skus = ["SKU-SF01", "SKU-H03", "SKU-H01", "SKU-H02", "SKU-H05", "SKU-H06", "SKU-SF02", "SKU-FN01", "SKU-GF01", "SKU-GF02"]
        for r in required_skus:
            self.assertIn(r, skus, f"Missing required launch SKU: {r}")

    def test_royal_mix_contains_zero_peanuts(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        skus = {item["sku"]: item for family in data["families"] for item in family["items"]}
        royal_mix = skus["SKU-SF01"]
        for ingredient in royal_mix["ingredients"]:
            self.assertNotIn("peanut", ingredient.lower(), "Royal Mix must have 0% peanuts")

    def test_standard_sizes_include_500g_and_1kg(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        skus = {item["sku"]: item for family in data["families"] for item in family["items"]}
        clover = skus["SKU-H01"]
        self.assertIn("500g", clover["sizes"])
        self.assertIn("1kg", clover["sizes"])

    def test_all_six_families_and_sku_count(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["families"]), 6, "Must have exactly 6 product families")
        
        family_ids = [f["family_id"] for f in data["families"]]
        expected_families = [
            "pure_honey",
            "superfood_nut_blends",
            "functional_infusions",
            "breakfast_spreads",
            "mariam_go",
            "luxury_gift_vaults"
        ]
        for ef in expected_families:
            self.assertIn(ef, family_ids, f"Missing product family: {ef}")

        all_skus = [item["sku"] for family in data["families"] for item in family["items"]]
        self.assertGreaterEqual(len(all_skus), 25, f"Expected 25+ SKUs, found {len(all_skus)}")

    def test_sku_schema_attributes(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for family in data["families"]:
            for item in family["items"]:
                self.assertIn("sku", item)
                self.assertIn("name_en", item)
                self.assertIn("name_ar", item)
                self.assertIn("sizes", item)
                self.assertIn("ingredients", item)
                self.assertIn("flavor_profile", item)
                self.assertIsInstance(item["sizes"], list)
                self.assertIsInstance(item["ingredients"], list)

if __name__ == "__main__":
    unittest.main()
