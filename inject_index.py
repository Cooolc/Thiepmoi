import io
import os

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

files = [f for f in os.listdir('./album_img/hinhcuoi') if f.endswith('.jpg') or f.endswith('.png')]

injection = ""
for f in files:
    injection += f"            {{\n                src: 'album_img/hinhcuoi/{f}',\n            }},\n"

# The array ends with:
#             {
#                 src: 'album_img/vungtau.jpg',
#                 // caption: 'Từng ánh nhìn đong đầy yêu thương'
#             }
#         ];

target = """            {
                src: 'album_img/vungtau.jpg',
                // caption: 'Từng ánh nhìn đong đầy yêu thương'
            }
        ];"""

replacement = f"""            {{
                src: 'album_img/vungtau.jpg',
                // caption: 'Từng ánh nhìn đong đầy yêu thương'
            }},
{injection}        ];"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("Target not found!")

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

