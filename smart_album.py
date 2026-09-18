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

# Make sure CSS has layout-split-vert
css_addition = """
        .layout-split-vert {
            display: flex;
            flex-direction: row;
            align-items: stretch;
            gap: 15px;
            padding: 20px;
            height: 100%;
            box-sizing: border-box;
        }
        .split-vert-img {
            flex: 1;
            height: 100%;
            background: #fff;
            padding: 6px;
            box-sizing: border-box;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            overflow: hidden;
            position: relative;
        }
        .split-vert-img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
"""
if ".layout-split-vert" not in content:
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

print(f"Found {len(portraits)} Portraits and {len(landscapes)} Landscapes.")

pages_html = ""
page_num = 1

def pop_img(is_landscape=False):
    if is_landscape and landscapes:
        return landscapes.pop(0)
    elif not is_landscape and portraits:
        return portraits.pop(0)
    # Fallback to whatever is available
    if landscapes: return landscapes.pop(0)
    if portraits: return portraits.pop(0)
    return None

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

def add_split_horiz(img1, img2):
    # Stacked top/bottom, good for Landscape images
    global pages_html, page_num
    pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-split">
                    <div class="split-img"><img src="./album_img/hinhcuoi/{img1}" loading="lazy"></div>
                    <div class="split-img"><img src="./album_img/hinhcuoi/{img2}" loading="lazy"></div>
                </div>
            </div>\n"""
    page_num += 1

def add_split_vert(img1, img2):
    # Side by side, good for Portrait images
    global pages_html, page_num
    pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-split-vert">
                    <div class="split-vert-img"><img src="./album_img/hinhcuoi/{img1}" loading="lazy"></div>
                    <div class="split-vert-img"><img src="./album_img/hinhcuoi/{img2}" loading="lazy"></div>
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

# Generate spreads
while portraits or landscapes:
    # Try to make a spread depending on what we have most of
    
    # Need 2 layouts for a spread (left and right)
    for _ in range(2):
        if not portraits and not landscapes: break
        
        # Decide layout
        if len(landscapes) >= 2 and len(portraits) < len(landscapes):
            # Do a horizontal split (uses 2 L)
            i1 = pop_img(True)
            i2 = pop_img(True)
            if i1 and i2: add_split_horiz(i1, i2)
            else: add_full(i1 or i2)
        elif len(portraits) >= 2:
            import random
            choice = random.choice(['collage', 'vert_split', 'polaroid'])
            if choice == 'collage':
                i1 = pop_img(False)
                i2 = pop_img(False)
                add_collage(i1, i2)
            elif choice == 'vert_split':
                i1 = pop_img(False)
                i2 = pop_img(False)
                add_split_vert(i1, i2)
            else:
                add_polaroid(pop_img(False))
        else:
            # Just do full pages
            img = pop_img(len(landscapes) > 0)
            if img: add_full(img)

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
print(f"Generated {page_num - 1} smart pages successfully")

