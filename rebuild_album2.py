import io
import os
import re

with io.open('album.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract header
header_match = re.search(r'(.*?<!-- BÌA TRƯỚC .*?</div>\s*</div>\s*)<!-- Trang 1 -->', content, flags=re.DOTALL)
if not header_match:
    print("Could not find header boundary")
    exit(1)
header = header_match.group(1)

# Extract footer
footer_match = re.search(r'(<!-- BÌA SAU.*)', content, flags=re.DOTALL)
if not footer_match:
    print("Could not find footer boundary")
    exit(1)
footer = footer_match.group(1)

files = [f for f in os.listdir('./album_img/hinhcuoi') if f.endswith('.jpg') or f.endswith('.png')]

# Layout templates
def layout_full(img_path, page_num):
    return f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-full">
                    <img src="{img_path}" loading="lazy">
                </div>
            </div>\n"""

def layout_collage(img1, img2, page_num):
    return f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-collage">
                    <div class="collage-header">
                        <h3 class="font-vibes">Chấn Cơ<br>&amp; Hảo Nghi</h3>
                        <p class="date-text">11 - 10 - 2026</p>
                    </div>
                    <div class="collage-images">
                        <div class="img-wrapper img-1">
                            <img src="{img1}" loading="lazy">
                        </div>
                        <div class="img-wrapper img-2">
                            <img src="{img2}" loading="lazy">
                        </div>
                    </div>
                    <div class="collage-footer">
                        <p>Mỗi ánh nhìn, mỗi nụ cười đều kể một câu chuyện.<br>Một hành trình bắt đầu từ yêu thương<br>và được lưu giữ bằng những khoảnh khắc đẹp nhất.</p>
                    </div>
                </div>
            </div>\n"""

def layout_split(img1, img2, page_num):
    return f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-split">
                    <div class="split-img"><img src="{img1}" loading="lazy"></div>
                    <div class="split-img"><img src="{img2}" loading="lazy"></div>
                </div>
            </div>\n"""

def layout_polaroid(img_path, page_num):
    return f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content">
                    <div class="photo-frame">
                        <img src="{img_path}" loading="lazy">
                        <div class="photo-caption">Kỷ niệm</div>
                    </div>
                    <div class="page-number">{page_num}</div>
                </div>
            </div>\n"""

pages_html = ""
page_num = 1
idx = 0

# We have 36 files. Let's consume them.
# Spread patterns:
# 1: Full (1) + Collage (2) = 3 photos
# 2: Split (2) + Full (1) = 3 photos
# 3: Polaroid (1) + Polaroid (1) = 2 photos
# 4: Full (1) + Full (1) = 2 photos
# 5: Collage (2) + Full (1) = 3 photos
# Total: 13 photos per 5 spreads.
# Let's just loop these patterns.

patterns = [
    # (Left layout func, num_imgs, Right layout func, num_imgs)
    (layout_full, 1, layout_collage, 2),
    (layout_split, 2, layout_full, 1),
    (layout_full, 1, layout_full, 1),
    (layout_polaroid, 1, layout_polaroid, 1),
    (layout_collage, 2, layout_full, 1),
    (layout_split, 2, layout_split, 2),
]

pattern_idx = 0
while idx < len(files):
    pat = patterns[pattern_idx % len(patterns)]
    
    # Left page
    left_imgs_needed = pat[1]
    if idx + left_imgs_needed <= len(files):
        if left_imgs_needed == 1:
            pages_html += pat[0](f"./album_img/hinhcuoi/{files[idx]}", page_num)
        else:
            pages_html += pat[0](f"./album_img/hinhcuoi/{files[idx]}", f"./album_img/hinhcuoi/{files[idx+1]}", page_num)
        idx += left_imgs_needed
        page_num += 1
    else:
        # Fallback to polaroids if not enough images
        while idx < len(files):
            pages_html += layout_polaroid(f"./album_img/hinhcuoi/{files[idx]}", page_num)
            idx += 1
            page_num += 1
        break

    # Right page
    right_imgs_needed = pat[3]
    if idx + right_imgs_needed <= len(files):
        if right_imgs_needed == 1:
            pages_html += pat[2](f"./album_img/hinhcuoi/{files[idx]}", page_num)
        else:
            pages_html += pat[2](f"./album_img/hinhcuoi/{files[idx]}", f"./album_img/hinhcuoi/{files[idx+1]}", page_num)
        idx += right_imgs_needed
        page_num += 1
    else:
        while idx < len(files):
            pages_html += layout_polaroid(f"./album_img/hinhcuoi/{files[idx]}", page_num)
            idx += 1
            page_num += 1
        break
    
    pattern_idx += 1

# If total pages is odd, we need to add an empty page to make the back cover right.
# PageFlip usually expects an even number of pages (including covers) so that the back cover is on the outside.
# Front Cover (1), Pages (N), Back Cover (1). Total = N + 2. N should be even.
# Wait, page_num is currently N + 1. So N = page_num - 1.
if (page_num - 1) % 2 != 0:
    pages_html += f"""            <!-- Trang {page_num} (Trang trắng để chẵn trang) -->
            <div class="page">
                <div class="page-content"></div>
            </div>\n"""
    page_num += 1

new_content = header + pages_html + "            " + footer

with io.open('album.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"Generated {page_num - 1} pages with dynamic layouts successfully")

