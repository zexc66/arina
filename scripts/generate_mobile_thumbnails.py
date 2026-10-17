#!/usr/bin/env python3
"""
Generates responsive mobile thumbnails in output/imagery/mobile/ for all 4K JPEGs
referenced across website.html, index.html, and arina.html, and optimizes progressive
encoding on 4K Arina imagery while preserving exact 4K dimensions for Lightbox & zoom.
"""

import os
import re
from PIL import Image

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGERY_DIR = os.path.join(WORKSPACE_DIR, 'output', 'imagery')
MOBILE_DIR = os.path.join(IMAGERY_DIR, 'mobile')


def main():
    os.makedirs(MOBILE_DIR, exist_ok=True)

    referenced_jpgs = set()
    for html_name in ('website.html', 'index.html', 'arina.html'):
        html_path = os.path.join(WORKSPACE_DIR, html_name)
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            matches = re.findall(r'output/imagery/([a-zA-Z0-9_\-\.]+\.jpg)', content)
            referenced_jpgs.update(matches)

    total_orig_bytes = 0
    total_mobile_bytes = 0
    generated_count = 0

    for fname in sorted(referenced_jpgs):
        src_path = os.path.join(IMAGERY_DIR, fname)
        if not os.path.exists(src_path):
            continue

        orig_size = os.path.getsize(src_path)
        total_orig_bytes += orig_size

        with Image.open(src_path) as img:
            rgb = img.convert('RGB')
            w, h = rgb.size

            # Generate responsive mobile/card thumbnail (800px wide)
            target_w = 800
            if w > target_w:
                target_h = int(round(h * (target_w / float(w))))
                thumb = rgb.resize((target_w, target_h), Image.Resampling.LANCZOS)
            else:
                thumb = rgb.copy()

            mob_path = os.path.join(MOBILE_DIR, fname)
            q = 78
            thumb.save(mob_path, 'JPEG', quality=q, optimize=True, progressive=True)
            while os.path.getsize(mob_path) > 150_000 and q > 55:
                q -= 5
                thumb.save(mob_path, 'JPEG', quality=q, optimize=True, progressive=True)

            mob_size = os.path.getsize(mob_path)
            total_mobile_bytes += mob_size
            generated_count += 1

            # Also optimize progressive 4K original if it's an oversized arina_* file (> 1.4 MB)
            if fname.startswith('arina_') and orig_size > 1_400_000:
                tmp_path = src_path + '.opt.jpg'
                rgb.save(tmp_path, 'JPEG', quality=84, optimize=True, progressive=True)
                if os.path.getsize(tmp_path) < orig_size:
                    os.replace(tmp_path, src_path)
                else:
                    os.remove(tmp_path)

    print(
        f"Generated {generated_count} mobile thumbnails in output/imagery/mobile/ "
        f"({total_orig_bytes / (1024 * 1024):.2f} MB -> {total_mobile_bytes / (1024 * 1024):.2f} MB, "
        f"{(1 - total_mobile_bytes / max(1, total_orig_bytes)) * 100:.1f}% reduction)"
    )


if __name__ == '__main__':
    main()
