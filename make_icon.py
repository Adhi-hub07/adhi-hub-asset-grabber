from PIL import Image, ImageDraw, ImageFilter
import os

S = 256
img = Image.new("RGB", (S, S), "#0c1220")
draw = ImageDraw.Draw(img)

for y in range(S):
    t = y / S
    r = int(24 + (8 - 24) * t)
    g = int(40 + (20 - 40) * t)
    b = int(76 + (44 - 76) * t)
    draw.line([(0, y), (S, y)], fill=(r, g, b))

mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([8, 8, S - 8, S - 8], radius=52, fill=255)

glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-70, -70, 170, 170], fill=(77, 196, 255, 110))
gd.ellipse([110, 100, 330, 320], fill=(255, 111, 165, 70))
glow = glow.filter(ImageFilter.GaussianBlur(40))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
draw = ImageDraw.Draw(img)

c = S // 2
draw.rounded_rectangle([c - 58, 56, c + 58, 118], radius=16, fill="#7fd8ff")
draw.polygon([(c - 58, 118), (c + 58, 118), (c, 196)], fill="#7fd8ff")
draw.rounded_rectangle([c - 78, 150, c + 78, 172], radius=11, fill="#7fd8ff")

draw.ellipse([52, 40, 66, 54], fill="#ff9ec7")
draw.ellipse([192, 186, 206, 200], fill="#7fd8ff")

img = Image.composite(img, Image.new("RGB", (S, S), (0, 0, 0)), mask)
img = img.convert("RGBA")
img.putalpha(mask)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")
img.save(out, sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print("saved:", out)