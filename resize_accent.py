from PIL import Image
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "profile-accent.jpeg")
img = Image.open(path)

# Target 3:4 ratio
W = img.width
H = int(W * 4 / 3)

# Crop center if original is wider, or extend canvas if taller needed
orig_w, orig_h = img.size
target_ratio = 4 / 3  # height/width

if orig_h / orig_w < target_ratio:
    # original too wide for 3:4 — crop width
    new_w = int(orig_h / target_ratio)
    left = (orig_w - new_w) // 2
    img = img.crop((left, 0, left + new_w, orig_h))
else:
    # original too tall — crop height
    new_h = int(orig_w * target_ratio)
    top = (orig_h - new_h) // 2
    img = img.crop((0, top, orig_w, top + new_h))

# Resize to clean 3:4 output (300x400)
img = img.resize((300, 400), Image.LANCZOS)
img.save(path, quality=95)
print(f"Done: {img.size}")
