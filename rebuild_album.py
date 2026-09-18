import io
import os
import re

with io.open('album.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the header (up to <!-- Trang 1 --> or the end of BÌA TRƯỚC)
header_match = re.search(r'(.*?<!-- BÌA TRƯỚC .*?</div>\s*</div>\s*)<!-- Trang 1 -->', content, flags=re.DOTALL)
if not header_match:
    print("Could not find header boundary")
    exit(1)
header = header_match.group(1)

# Extract the footer (from <!-- BÌA SAU)
footer_match = re.search(r'(<!-- BÌA SAU.*)', content, flags=re.DOTALL)
if not footer_match:
    print("Could not find footer boundary")
    exit(1)
footer = footer_match.group(1)

files = [f for f in os.listdir('./album_img/hinhcuoi') if f.endswith('.jpg') or f.endswith('.png')]

pages_html = ""
page = 1
for f in files:
    pages_html += f"""            <!-- Trang {page} -->
            <div class="page">
                <div class="page-content">
                    <div class="photo-frame">
                        <img src="./album_img/hinhcuoi/{f}" alt="Ảnh cưới {page}" loading="lazy">
                        <div class="photo-caption">Kỷ niệm</div>
                    </div>
                    <div class="page-number">{page}</div>
                </div>
            </div>
"""
    page += 1

new_content = header + pages_html + "            " + footer

with io.open('album.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated album.html successfully")

