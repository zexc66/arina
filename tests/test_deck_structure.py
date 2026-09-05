import os
import re
import unittest

def test_index_file_exists():
    assert os.path.exists("index.html"), "index.html must exist"

def test_deck_contains_9_slides_and_nav():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    slides = re.findall(r'<section[^>]+class="[^"]*slide[^"]*"', html)
    assert len(slides) == 9, f"Expected 9 slides, found {len(slides)}"
    assert 'id="nav-dock"' in html, "Navigation dock must be present"
    assert '+20 10 08716714' in html, "Contact number must be present"
    assert 'Mariam Food Industries' in html, "Company name must be present"

def test_slides_1_to_3_content():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "ISO 22000" in html and "HACCP" in html and "FDA" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.18 PM.jpeg" in html, "Autoclave photo must be in slide 3"
    assert "Alexandria" in html and "Damietta" in html, "Ports must be referenced in slide 2"

def test_slides_4_and_5_products():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "Picual" in html
    assert "Pimento" in html
    assert "Pepperoncini" in html
    assert "Turshi" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.20 PM.jpeg" in html, "Sliced black olives image required"
    assert "WhatsApp Image 2026-09-05 at 12.52.17 PM (5).jpeg" in html, "Pimento stuffed olives image required"
    assert "WhatsApp Image 2026-09-05 at 12.52.16 PM (2).jpeg" in html, "Mixed pickle jar image required"

class TestDeckStructure(unittest.TestCase):
    def test_index_file_exists(self):
        test_index_file_exists()

    def test_deck_contains_9_slides_and_nav(self):
        test_deck_contains_9_slides_and_nav()

    def test_slides_1_to_3_content(self):
        test_slides_1_to_3_content()

    def test_slides_4_and_5_products(self):
        test_slides_4_and_5_products()

if __name__ == '__main__':
    unittest.main()
