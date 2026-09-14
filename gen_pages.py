import os
html = ''
page = 26
files = [f for f in os.listdir('./album_img/hinhcuoi') if f.endswith('.jpg') or f.endswith('.png')]
for f in files:
    html += f"""            <!-- Trang {page} -->
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

with open('new_pages.html', 'w', encoding='utf-8') as f:
    f.write(html)
