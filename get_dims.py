import os, struct

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

for f in os.listdir('./album_img/hinhcuoi'):
    if f.endswith('.jpg') or f.endswith('.png'):
        print(f, get_image_size(os.path.join('./album_img/hinhcuoi', f)))

