import re
import os

def clean_index_html():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove Slide 10
    slide10_pattern = re.compile(
        r'\s*<!-- Slide 10: Arina Natural Honey & Superfoods Collection -->.*?</section>',
        re.DOTALL
    )
    assert slide10_pattern.search(content), "Slide 10 not found in index.html"
    content = slide10_pattern.sub('', content)

    # 2. Remove Boutique banner in overview modal
    overview_banner_pattern = re.compile(
        r'\s*<!-- Direct Boutique Storefront Banner -->.*?</a>\s*</div>',
        re.DOTALL
    )
    assert overview_banner_pattern.search(content), "Overview banner not found in index.html"
    content = overview_banner_pattern.sub('', content)

    # 3. Remove bottom nav link to honey.html
    nav_link_pattern = re.compile(
        r'\s*<!-- Direct Standalone Honey Boutique Link -->.*?</a>\s*<div class="w-px h-5 bg-white/20 mx-0.5"></div>',
        re.DOTALL
    )
    assert nav_link_pattern.search(content), "Nav link not found in index.html"
    content = nav_link_pattern.sub('', content)

    # 4. totalSlides = 10 -> totalSlides = 9
    assert 'const totalSlides = 10;' in content, "totalSlides = 10 not found"
    content = content.replace('const totalSlides = 10;', 'const totalSlides = 9;')

    # 5. Remove slide 10 from slideTitles
    slide10_titles_pattern = re.compile(
        r',\s*\{\s*num:\s*\'10\',\s*category_en:\s*\'Superfood Reserve\'.*?\}',
        re.DOTALL
    )
    assert slide10_titles_pattern.search(content), "Slide 10 in slideTitles not found"
    content = slide10_titles_pattern.sub('', content)

    # 6. Remove idx === 9 block in renderOverviewGrid
    idx9_pattern = re.compile(
        r'\s*\$\{idx === 9 \? `.*?` : \'\'\}',
        re.DOTALL
    )
    assert idx9_pattern.search(content), "idx === 9 not found in renderOverviewGrid"
    content = idx9_pattern.sub('', content)

    # 7. Remove HONEY_PDP_DATA and functions
    honey_pdp_pattern = re.compile(
        r'\s*// Honey & Superfoods Interactive PDP Viewer Data & Functions.*?window\.zoomCurrentHoneyPdp = zoomCurrentHoneyPdp;\n',
        re.DOTALL
    )
    assert honey_pdp_pattern.search(content), "HONEY_PDP_DATA not found in index.html"
    content = honey_pdp_pattern.sub('', content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html cleaned successfully.")

def clean_arina_html():
    path = "arina.html"
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Slide 9 footer: Slide 9 of 10 -> Slide 9 of 9
    content = content.replace("Slide 9 of 10", "Slide 9 of 9")

    # 2. Remove Slide 10
    slide10_pattern = re.compile(
        r'\s*<!-- Slide 10: Arina Natural Honey & Superfoods Collection -->.*?</section>',
        re.DOTALL
    )
    if slide10_pattern.search(content):
        content = slide10_pattern.sub('', content)
        print("Removed Slide 10 from arina.html")

    # 3. totalSlides = 10 -> totalSlides = 9
    content = content.replace('const totalSlides = 10;', 'const totalSlides = 9;')

    # 4. Remove slide 10 from slideTitles
    slide10_title = re.compile(
        r',\s*\{\s*num:\s*\'10\',\s*category:\s*\'Superfood Reserve\'.*?\}',
        re.DOTALL
    )
    if slide10_title.search(content):
        content = slide10_title.sub('', content)
        print("Removed slide 10 from slideTitles in arina.html")

    # 5. Remove HONEY_PDP_DATA and functions
    honey_pdp = re.compile(
        r'\s*// -------------------------------------------------------------------------\s*// Interactive 4K PDP Studio Viewer Engine \(Slide 10\).*?window\.zoomCurrentHoneyPdp = zoomCurrentHoneyPdp;\n',
        re.DOTALL
    )
    if honey_pdp.search(content):
        content = honey_pdp.sub('', content)
        print("Removed HONEY_PDP_DATA from arina.html")

    # 6. Remove honey color if present
    content = content.replace("honey: '#E5BA55',", "")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("arina.html cleaned successfully.")

if __name__ == "__main__":
    clean_index_html()
    clean_arina_html()
