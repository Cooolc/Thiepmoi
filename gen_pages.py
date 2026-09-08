import os
import json

img_dir = r'd:\PROJECT\Thiepmoi\album_img'
files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
files.sort()

html_content = ''
page_num = 1

captions = ['Kỷ niệm', 'Yêu thương', 'Hạnh phúc', 'Bên nhau', 'Nụ cười', 'Khoảnh khắc', 'Tình yêu', 'Ánh mắt']

for idx, f in enumerate(files):
    caption = captions[idx % len(captions)]
    html_content += f'''
            <!-- Trang {page_num} -->
            <div class="page">
                <div class="page-content">
                    <div class="photo-frame">
                        <img src="./album_img/{f}" alt="Ảnh cưới {page_num}" loading="lazy">
                        <div class="photo-caption">{caption}</div>
                    </div>
                    <div class="page-number">{page_num}</div>
                </div>
            </div>'''
    page_num += 1

with open(r'd:\PROJECT\Thiepmoi\pages.txt', 'w', encoding='utf-8') as outfile:
    outfile.write(html_content)

print('Generated.')
