from PIL import Image

im = Image.open("image.png")

x, y = im.size
s_w = x // 4
s_h = y // 4

for i in range(4):
    for j in range(4):
        if i != 3 or j != 3:
            im2 = im.crop((s_w * i, s_h * j, s_w * i + s_w, s_h * j + s_h))
            im2.save(f'image{j + 1}{i + 1}.png')
