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

class TestDeckStructure(unittest.TestCase):
    def test_index_file_exists(self):
        test_index_file_exists()

    def test_deck_contains_9_slides_and_nav(self):
        test_deck_contains_9_slides_and_nav()

if __name__ == '__main__':
    unittest.main()
