import io
with io.open('album.html', 'r', encoding='utf-8') as f:
    content = f.read()

with io.open('new_pages.html', 'r', encoding='utf-8') as f:
    new_pages = f.read()

content = content.replace('<!-- BÌA SAU (Bìa cứng) -->', new_pages + '<!-- BÌA SAU (Bìa cứng) -->')

with io.open('album.html', 'w', encoding='utf-8') as f:
    f.write(content)

