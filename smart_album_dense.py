import io
import os
import re
import random
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

css_addition = """
        .layout-stacked {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background-color: #fffaf0;
            height: 100%;
            box-sizing: border-box;
            gap: 20px;
        }
        .layout-stacked img {
            width: 100%;
            height: auto;
            max-height: 45%;
            object-fit: cover;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border: 4px solid #fff;
        }
        .ornament-block {
            text-align: center;
            padding: 20px;
        }
        .ornament-block h3 {
            font-family: 'Great Vibes', cursive;
            font-size: 3em;
            color: #bfa57c;
            margin: 0;
            font-weight: normal;
        }
        .ornament-block p {
            font-family: 'Playfair Display', serif;
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
            font-style: italic;
        }
        .polaroid-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            background-color: #fffaf0;
            padding: 10px;
        }
"""
if ".layout-stacked {" not in content:
    content = content.replace("</style>", css_addition + "\n    </style>")

header_match = re.search(r'(.*?<!-- BÌA TRƯỚC .*?</div>\s*</div>\s*)<!-- Trang 1 -->', content, flags=re.DOTALL)
header = header_match.group(1)

footer_match = re.search(r'(<!-- BÌA SAU.*)', content, flags=re.DOTALL)
footer = footer_match.group(1)

portraits = []
landscapes = []

for f in os.listdir('./album_img/hinhcuoi'):
    if f.endswith('.jpg') or f.endswith('.png'):
        path = os.path.join('./album_img/hinhcuoi', f)
        size = get_image_size(path)
        if size:
            w, h = size
            if w >= h: landscapes.append(f)
            else: portraits.append(f)
        else:
            portraits.append(f)

pages_html = ""
page_num = 1

def add_full(img):
    global pages_html, page_num
    pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-full">
                    <img src="./album_img/hinhcuoi/{img}" loading="lazy" style="object-position: center 20%;">
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
                            <img src="./album_img/hinhcuoi/{img1}" loading="lazy" style="object-position: center 20%;">
                        </div>
                        <div class="img-wrapper img-2">
                            <img src="./album_img/hinhcuoi/{img2}" loading="lazy" style="object-position: center 20%;">
                        </div>
                    </div>
                    <div class="collage-footer">
                        <p>Mỗi ánh nhìn, mỗi nụ cười đều kể một câu chuyện.<br>Một hành trình bắt đầu từ yêu thương<br>và được lưu giữ bằng những khoảnh khắc đẹp nhất.</p>
                    </div>
                </div>
            </div>\n"""
    page_num += 1

quotes = [
    "Hạnh phúc không phải là đích đến, mà là hành trình chúng ta đi cùng nhau.",
    "Bên em, mỗi ngày đều là một ngày nắng đẹp.",
    "Tình yêu không phải là nhìn chằm chằm vào nhau, mà là cùng nhìn về một hướng.",
    "Cảm ơn vì đã đến và trở thành ngoại lệ của anh.",
    "Nắm tay nhau đi qua giông bão, để trân trọng những ngày nắng trong."
]

def add_stacked_landscapes(img1, img2=None):
    global pages_html, page_num
    q = random.choice(quotes)
    if img2:
        pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-stacked">
                    <img src="./album_img/hinhcuoi/{img1}" loading="lazy">
                    <img src="./album_img/hinhcuoi/{img2}" loading="lazy">
                </div>
            </div>\n"""
    else:
        pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content layout-stacked">
                    <div class="ornament-block">
                        <h3>Love Story</h3>
                    </div>
                    <img src="./album_img/hinhcuoi/{img1}" loading="lazy">
                    <div class="ornament-block" style="padding-top:0;">
                        <p>{q}</p>
                    </div>
                </div>
            </div>\n"""
    page_num += 1

def add_polaroid(img):
    global pages_html, page_num
    q = random.choice(quotes)
    pages_html += f"""            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content polaroid-container">
                    <div class="ornament-block" style="margin-bottom: -15px; z-index: 10;">
                        <h3 style="font-size: 2.2em;">Forever</h3>
                    </div>
                    <div class="photo-frame" style="margin-top: 0; height: 60%;">
                        <img src="./album_img/hinhcuoi/{img}" loading="lazy">
                        <div class="photo-caption">Kỷ niệm</div>
                    </div>
                    <div class="ornament-block">
                        <p>{q}</p>
                    </div>
                    <div class="page-number">{page_num}</div>
                </div>
            </div>\n"""
    page_num += 1

while portraits or landscapes:
    for _ in range(2):
        if not portraits and not landscapes: break
        
        if len(landscapes) >= 2:
            add_stacked_landscapes(landscapes.pop(0), landscapes.pop(0))
        elif len(landscapes) == 1:
            add_stacked_landscapes(landscapes.pop(0), None)
        elif len(portraits) >= 2:
            if random.random() < 0.4:
                add_collage(portraits.pop(0), portraits.pop(0))
            else:
                if random.random() < 0.5:
                    add_full(portraits.pop(0))
                else:
                    add_polaroid(portraits.pop(0))
        elif len(portraits) == 1:
            if random.random() < 0.5:
                add_full(portraits.pop(0))
            else:
                add_polaroid(portraits.pop(0))

if (page_num - 1) % 2 != 0:
    pages_html += f"""            <!-- Trang {page_num} (Trang trắng để chẵn trang) -->
            <div class="page">
                <div class="page-content layout-stacked">
                    <div class="ornament-block" style="margin: auto;">
                        <h3 style="font-size: 4em;">The End</h3>
                        <p>Cảm ơn bạn đã lật từng trang kỷ niệm.</p>
                    </div>
                </div>
            </div>\n"""
    page_num += 1

new_content = header + pages_html + "            " + footer

with io.open('album.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"Generated {page_num - 1} pages with dense layouts successfully")

