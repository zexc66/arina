#!/usr/bin/env python3
"""
Fixes the issues discovered by Chrome DevTools MCP:
1. Malformed WhatsApp SVG path in 3 locations (replace with standard valid SVG path).
2. Missing favicon link causing 404 error (add arina-logo-gold.png favicon).
3. Missing aria-labels on form inputs causing accessibility warnings.
"""

import re

WHATSAPP_CLEAN_PATH = 'M19.05 4.91A9.816 9.816 0 0 0 12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01zm-7.01 15.24c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.16 8.16 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.55-3.7 8.24-8.23 8.24zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.12-.15.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.44.06-.66.31-.23.25-.88.86-.88 2.1 0 1.23.9 2.43 1.03 2.6.12.17 1.77 2.7 4.28 3.79.6.26 1.07.41 1.43.53.6.19 1.15.16 1.58.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.15-1.18-.06-.11-.23-.17-.48-.3z'

def main():
    website_p = 'website.html'
    with open(website_p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix favicon 404: Add favicon link tag in <head> if not present
    if '<link rel="icon"' not in html:
        head_tag = '<meta charset="UTF-8">'
        assert head_tag in html
        html = html.replace(head_tag, head_tag + '\n  <link rel="icon" type="image/png" href="arina-logo-gold.png">')
        print("Favicon link tag added.")

    # 2. Fix malformed WhatsApp SVG path (3 occurrences)
    old_broken_path = re.compile(r'd="M12\.031 6\.172c-3\.181 0-5\.767 2\.586[\s\S]*?\.04\.387-\.105\.795z"')
    matches = old_broken_path.findall(html)
    print(f"Found {len(matches)} broken SVG path occurrences.")
    assert len(matches) == 3, f"Expected 3 occurrences, found {len(matches)}"
    html = old_broken_path.sub(f'd="{WHATSAPP_CLEAN_PATH}"', html)
    print("Replaced all broken SVG path occurrences with valid WhatsApp path.")

    # 3. Add aria-label to form elements missing accessibility labels
    aria_fixes = [
        ('id="catalog-search"', 'id="catalog-search" aria-label="Search product catalog"'),
        ('id="guide-search-input"', 'id="guide-search-input" aria-label="Search varieties guide"'),
        ('id="qty-cucumbers"', 'id="qty-cucumbers" aria-label="Quantity of pickled baby cucumbers cartons"'),
        ('id="qty-turnips"', 'id="qty-turnips" aria-label="Quantity of pickled turnips cartons"'),
        ('id="qty-kalamata"', 'id="qty-kalamata" aria-label="Quantity of Kalamata olives cartons"'),
        ('id="qty-toum"', 'id="qty-toum" aria-label="Quantity of whipped toum garlic cream cartons"'),
        ('id="roi-srp-range"', 'id="roi-srp-range" aria-label="Estimated retail selling price per jar slider"'),
        ('id="roi-stores-range"', 'id="roi-stores-range" aria-label="Number of retail store locations slider"'),
        ('id="roi-facings-range"', 'id="roi-facings-range" aria-label="Shelf facings per store slider"'),
        ('id="rfq-name"', 'id="rfq-name" aria-label="Full commercial buyer name"'),
        ('id="rfq-email"', 'id="rfq-email" aria-label="Corporate buyer email address"'),
        ('id="rfq-company"', 'id="rfq-company" aria-label="Company or supermarket chain name"'),
        ('id="rfq-type"', 'id="rfq-type" aria-label="Buyer organization business type"'),
        ('id="rfq-port"', 'id="rfq-port" aria-label="Destination ocean or dry port"'),
        ('id="rfq-incoterm"', 'id="rfq-incoterm" aria-label="Preferred Incoterm delivery basis"'),
        ('id="rfq-notes"', 'id="rfq-notes" aria-label="Additional container packing specifications or notes"'),
        ('id="turntable-scrub-slider"', 'id="turntable-scrub-slider" aria-label="3D turntable jar rotation scrub slider"'),
        ('value="20ft" checked', 'value="20ft" checked aria-label="20 foot Full Container Load"'),
        ('value="40ft"', 'value="40ft" aria-label="40 foot High Cube Container Load"'),
        ('value="lcl"', 'value="lcl" aria-label="Less than Container Load Pallet Dispatch"'),
    ]

    for old_str, new_str in aria_fixes:
        if old_str in html:
            html = html.replace(old_str, new_str, 1)

    print("Added aria-labels to all form inputs.")

    with open(website_p, 'w', encoding='utf-8') as f:
        f.write(html)
    print("website.html written successfully!")

if __name__ == "__main__":
    main()
