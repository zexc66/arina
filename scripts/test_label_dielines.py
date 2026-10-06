import os
import unittest
from PIL import Image

class TestLabelDielines(unittest.TestCase):
    def setUp(self):
        self.output_dir = "output/dielines"
        self.expected_formats = [
            ("dieline_370g_jar.png", (2200, 850)),
            ("dieline_500ml_evoo.png", (750, 1400)),
            ("dieline_200ml_spray.png", (1300, 1100)),
            ("dieline_190g_tapenade.png", (1900, 450)),
            ("dieline_50g_pouch.png", (1100, 1600)),
        ]
        self.forest_green = (30, 51, 38)
        self.gold_foil = (212, 175, 55)
        self.warm_ivory = (234, 230, 223)

    def test_dieline_outputs_exist_and_calibrated(self):
        for filename, expected_size in self.expected_formats:
            path = os.path.join(self.output_dir, filename)
            self.assertTrue(os.path.exists(path), f"Missing dieline file: {filename}")
            
            with Image.open(path) as im:
                # Validate exact dimensions match specification
                self.assertEqual(
                    im.size,
                    expected_size,
                    f"{filename} dimensions {im.size} do not match expected {expected_size}"
                )
                self.assertGreaterEqual(im.width, expected_size[0] // 2)
                self.assertGreaterEqual(im.height, expected_size[1] // 2)
                
                # Convert to RGB to verify color standards
                rgb_im = im.convert("RGB")
                colors = rgb_im.getcolors(maxcolors=im.width * im.height)
                unique_rgb = {c[1] for c in colors}
                
                # Check that Deep Forest Green background color is present
                self.assertIn(
                    self.forest_green,
                    unique_rgb,
                    f"{filename} is missing Deep Forest Green (30, 51, 38)"
                )
                # Check that Gold Foil accent color is present
                self.assertIn(
                    self.gold_foil,
                    unique_rgb,
                    f"{filename} is missing Gold Foil (212, 175, 55)"
                )
                # Check that Warm Ivory guide/text color is present
                self.assertIn(
                    self.warm_ivory,
                    unique_rgb,
                    f"{filename} is missing Warm Ivory (234, 230, 223)"
                )

if __name__ == "__main__":
    unittest.main()
