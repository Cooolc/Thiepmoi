import io
import os
import re

with io.open('album.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_styles = """
        /* --- NEW EDITORIAL LAYOUT STYLES --- */
        .layout-full {
            padding: 0 !important;
        }
        .layout-full img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .layout-collage {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 30px 20px;
            height: 100%;
            background-color: #fffaf0;
        }
        .collage-header {
            text-align: left;
            margin-bottom: 10px;
        }
        .font-vibes {
            font-family: 'Great Vibes', cursive;
            font-size: 2.5em;
            line-height: 1.1;
            color: #333;
            margin: 0;
            font-weight: normal;
        }
        .date-text {
            font-family: 'Playfair Display', serif;
            font-size: 0.9em;
            color: #555;
            letter-spacing: 2px;
            margin-top: 10px;
        }
        .collage-images {
            flex-grow: 1;
            position: relative;
            margin: 15px 0;
        }
        .img-wrapper {
            position: absolute;
            background: #fff;
            padding: 6px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .img-wrapper img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .img-1 {
            top: 0;
            right: 0;
            width: 60%;
            height: 65%;
            z-index: 2;
        }
        .img-2 {
            bottom: 0;
            left: 0;
            width: 55%;
            height: 60%;
            z-index: 1;
        }
        .collage-footer {
            text-align: right;
        }
        .collage-footer p {
            font-size: 0.8em;
            color: #555;
            line-height: 1.6;
            font-style: italic;
            margin: 0;
            font-family: 'Playfair Display', serif;
        }

        .layout-split {
            display: flex;
            flex-direction: column;
            gap: 15px;
            padding: 20px;
            height: 100%;
        }
        .split-img {
            flex: 1;
            background: #fff;
            padding: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        .split-img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* Cập nhật lại khung ảnh cũ cho đẹp hơn */
        .photo-frame {
            width: 90%;
            height: 70%;
            background: #fff;
            padding: 12px 12px 40px 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border: 1px solid #e0d8c3;
            box-sizing: border-box;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            margin: auto;
            margin-top: 5%;
        }
        .photo-frame img {
            width: 100%;
            height: 100%;
            object-fit: cover; /* Cover để không có viền thừa */
        }
"""

if "/* --- NEW EDITORIAL LAYOUT STYLES --- */" not in content:
    content = content.replace("</style>", new_styles + "\n    </style>")
    with io.open('album.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added styles")
else:
    print("Styles already present")


