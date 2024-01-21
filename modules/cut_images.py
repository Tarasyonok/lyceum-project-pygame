from PIL import Image

im_org = Image.open("Mage-Red.png")

x, y = im_org.size
s_w = 64
s_h = 64

x_names = ['idle1', 'idle2', 'move1', 'move2', 'sword1', 'sword2', 'sword3', 'sword4', 'bow1', 'bow2', 'bow3', 'bow4', 'magic1', 'magic2', 'magic3', 'magic4', '_', '_', 'hit1', 'hit2', '_', 'die1', 'die2', 'die3']
print(len(x_names))
y_names = ['down', 'downright', 'right', 'upright', 'up', 'upleft', 'left', 'downleft']

for i in range(24):
    for j in range(8):
        im = im_org.crop((s_w * i, s_h * j, s_w * i + s_w, s_h * j + s_h))
        im.save(f'images/{y_names[j]}{x_names[i]}.png')


for n in range(24):
    for m in range(8):
        im = Image.open(f"images/{y_names[m]}{x_names[n]}.png")
        pixels = im.load()
        x, y = im.size

        back = pixels[0, 0]

        top = 0

        top = 0
        for j in range(y):
            for i in range(x):
                if pixels[i, j] != back:
                    # print('top', i, j)
                    top = j
                    break
            if top != 0:
                break

        left = 0
        for i in range(x):
            for j in range(y):
                if pixels[i, j] != back:
                    left = i
                    break
            if left != 0:
                break

        right = x
        for i in range(x - 1, -1, -1):
            for j in range(y - 1, -1, -1):
                if pixels[i, j] != back:
                    right = i
                    break
            if right != x:
                break

        bottom = y
        for j in range(y - 1, -1, -1):
            for i in range(x - 1, -1, -1):
                if pixels[i, j] != back:
                    bottom = j
                    break
            if bottom != y:
                break

        ans = im.crop((left, top, right + 1, bottom + 1))

        ans.save(f"images/{y_names[m]}{x_names[n]}.png")