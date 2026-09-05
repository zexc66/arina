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

def test_slides_6_and_7_packaging_and_oem():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "A10" in html, "A10 foodservice can format required"
    assert "150kg" in html or "220kg" in html, "Bulk drum specs required"
    assert "Private Label" in html
    assert "WhatsApp Image 2026-09-05 at 12.52.17 PM (7).jpeg" in html, "Open can photo required"
    assert "WhatsApp Image 2026-09-05 at 12.52.17 PM (4).jpeg" in html, "Bulk barrel photo required"
    assert "WhatsApp Image 2026-09-05 at 12.52.15 PM (5).jpeg" in html, "Pallet photo required"

def test_slides_8_and_9_specs_and_contact():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "FCL" in html, "Container loading specs required"
    assert "Drained Weight" in html
    assert "tel:+201008716714" in html or "wa.me/201008716714" in html, "Direct clickable link required"
    assert "Cairo, Egypt" in html
    # Technical specs matrix checks
    assert "Salinity" in html, "Salinity specs required"
    assert "Defect Tolerance" in html, "Defect tolerance required"
    assert "ISPM-15" in html or "ISPM 15" in html, "Pallet specs required"
    # Commercial onboarding checks
    assert "DHL" in html or "FedEx" in html, "Sample dispatch carrier required"
    assert "Letter of Credit" in html or "L/C" in html, "Payment terms required"

class TestDeckStructure(unittest.TestCase):
    def test_index_file_exists(self):
        test_index_file_exists()

    def test_deck_contains_9_slides_and_nav(self):
        test_deck_contains_9_slides_and_nav()

    def test_slides_1_to_3_content(self):
        test_slides_1_to_3_content()

    def test_slides_4_and_5_products(self):
        test_slides_4_and_5_products()

    def test_slides_6_and_7_packaging_and_oem(self):
        test_slides_6_and_7_packaging_and_oem()

    def test_slides_8_and_9_specs_and_contact(self):
        test_slides_8_and_9_specs_and_contact()

if __name__ == '__main__':
    unittest.main()

