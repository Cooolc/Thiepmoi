import io
import os
import re
import struct

def get_image_size(fname):
    with open(fname, 'rb') as f:
        head = f.read(24)
        if len(head) != 24: return None
        if head.startswith(b'\x89PNG\r\n\x1a\n'):
            return struct.unpack('>ii', head[16:24])
        elif head[:2] == b'\xff\xd8':
            f.seek(0)
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf or ftype in [0xc4, 0xc8, 0xcc]:
                f.seek(size, 1)
                byte = f.read(1)
                while ord(byte) == 0xff: byte = f.read(1)
                ftype = ord(byte)
                size = struct.unpack('>H', f.read(2))[0] - 2
            f.seek(1, 1)
            h, w = struct.unpack('>HH', f.read(4))
            return w, h
    return None

with io.open('album.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add layout-landscape CSS if missing
css_addition = """
        .layout-landscape {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background-color: #fffaf0;
            height: 100%;
            box-sizing: border-box;
        }
        .layout-landscape img {
            width: 100%;
            height: auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            border: 5px solid #fff;
        }
"""
if ".layout-landscape {" not in content:
    content = content.replace("</style>", css_addition + "\n    </style>")

# Extract header
header_match = re.search(r'(.*?<!-- BÌA TRƯỚC .*?</div>\s*</div>\s*)<!-- Trang 1 -->', content, flags=re.DOTALL)
header = header_match.group(1)

# Extract footer
footer_match = re.search(r'(<!-- BÌA SAU.*)', content, flags=re.DOTALL)
footer = footer_match.group(1)

# Sort images into Portrait and Landscape
portraits = []
landscapes = []

for f in os.listdir('./album_img/hinhcuoi'):
    if f.endswith('.jpg') or f.endswith('.png'):
        path = os.path.join('./album_img/hinhcuoi', f)
        size = get_image_size(path)
        if size:
            w, h = size
            if w >= h:
                landscapes.append(f)
            else:
                portraits.append(f)
        else:
            portraits.append(f) # Default to portrait

pages_html = ""
page_num = 1

def add_full(img):
    global pages_html, page_num
    pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-full">
                    <img src="./album_img/hinhcuoi/{img}" loading="lazy">
                </div>
            </div>\n"""
    page_num += 1

def add_collage(img1, img2):
    global pages_html, page_num
    pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-collage">
                    <div class="collage-header">
                        <h3 class="font-vibes">Chấn Cơ<br>&amp; Hảo Nghi</h3>
                        <p class="date-text">11 - 10 - 2026</p>
                    </div>
                    <div class="collage-images">
                        <div class="img-wrapper img-1">
                            <img src="./album_img/hinhcuoi/{img1}" loading="lazy">
                        </div>
                        <div class="img-wrapper img-2">
                            <img src="./album_img/hinhcuoi/{img2}" loading="lazy">
                        </div>
                    </div>
                    <div class="collage-footer">
                        <p>Mỗi ánh nhìn, mỗi nụ cười đều kể một câu chuyện.<br>Một hành trình bắt đầu từ yêu thương<br>và được lưu giữ bằng những khoảnh khắc đẹp nhất.</p>
                    </div>
                </div>
            </div>\n"""
    page_num += 1

def add_landscape(img):
    global pages_html, page_num
    pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-landscape">
                    <img src="./album_img/hinhcuoi/{img}" loading="lazy">
                </div>
            </div>\n"""
    page_num += 1

def add_polaroid(img):
    global pages_html, page_num
    pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content">
                    <div class="photo-frame">
                        <img src="./album_img/hinhcuoi/{img}" loading="lazy">
                        <div class="photo-caption">Kỷ niệm</div>
                    </div>
                    <div class="page-number">{page_num}</div>
                </div>
            </div>\n"""
    page_num += 1

import random
# Generate spreads
while portraits or landscapes:
    for _ in range(2): # 2 pages per spread
        if not portraits and not landscapes: break
        
        # Decide what to place
        # If we have landscapes, interleave them
        if landscapes and random.random() < 0.4:
            add_landscape(landscapes.pop(0))
        elif portraits:
            if len(portraits) >= 2 and random.random() < 0.3:
                # Use collage for 2 portraits
                add_collage(portraits.pop(0), portraits.pop(0))
            else:
                # Use full or polaroid
                if random.random() < 0.5:
                    add_full(portraits.pop(0))
                else:
                    add_polaroid(portraits.pop(0))
        elif landscapes:
            add_landscape(landscapes.pop(0))

# Ensure even pages
if (page_num - 1) % 2 != 0:
    pages_html += f"""            <!-- Trang {page_num} (Trang trắng để chẵn trang) -->
            <div class="page">
                <div class="page-content"></div>
            </div>\n"""
    page_num += 1

new_content = header + pages_html + "            " + footer

with io.open('album.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"Generated {page_num - 1} safe pages successfully")

