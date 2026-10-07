from PIL import Image, ImageDraw, ImageFilter
import math, os

import os as _os
OUT = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "public")

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def gradient(draw, w, h, top, bottom):
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=lerp_color(top, bottom, t))

def add_noise(img, amount=8):
    import random
    px = img.load()
    w, h = img.size
    for _ in range(w * h // 3):
        x, y = random.randint(0, w-1), random.randint(0, h-1)
        r, g, b = px[x, y]
        n = random.randint(-amount, amount)
        px[x, y] = (max(0,min(255,r+n)), max(0,min(255,g+n)), max(0,min(255,b+n)))
    return img

def draw_leaf(draw, cx, cy, size, color, angle=0):
    """Draw a simple leaf shape"""
    points = []
    for i in range(20):
        t = i / 19
        # leaf curve
        x = cx + math.sin(math.pi * t) * size * 0.5
        y = cy - size * 0.5 + size * t
        # rotate
        rx = cx + (x-cx)*math.cos(angle) - (y-cy)*math.sin(angle)
        ry = cy + (x-cx)*math.sin(angle) + (y-cy)*math.cos(angle)
        points.append((rx, ry))
    for i in range(20):
        t = (19-i) / 19
        x = cx - math.sin(math.pi * t) * size * 0.25
        y = cy - size * 0.5 + size * t
        rx = cx + (x-cx)*math.cos(angle) - (y-cy)*math.sin(angle)
        ry = cy + (x-cx)*math.sin(angle) + (y-cy)*math.cos(angle)
        points.append((rx, ry))
    if len(points) >= 3:
        draw.polygon(points, fill=color)

def draw_circle_accent(draw, cx, cy, r, color, width=2):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=width)

# ──────────────────────────────────────────────
# 1. PROFILE MAIN — portrait (480x600)
#    Warm ivory background, abstract human silhouette hint,
#    botanical decorations, very aesthetic
# ──────────────────────────────────────────────
def make_profile_main():
    W, H = 480, 600
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Background gradient: ivory to soft green
    gradient(draw, W, H, (245, 246, 238), (220, 235, 220))

    # Decorative large circle — top right
    draw_circle_accent(draw, W-60, 60, 80, (168,188,168,), 1)
    draw_circle_accent(draw, W-60, 60, 55, (168,188,168), 1)

    # Decorative small circles — bottom left
    draw_circle_accent(draw, 50, H-80, 40, (168,188,168), 1)
    draw_circle_accent(draw, 50, H-80, 22, (168,188,168), 1)

    # Abstract silhouette — shoulder/neck oval (soft sage fill)
    # body oval
    body_color = (180, 200, 180)
    draw.ellipse([W//2-90, H//2-20, W//2+90, H-40], fill=body_color)
    # head oval
    head_color = (195, 210, 192)
    draw.ellipse([W//2-70, 80, W//2+70, 280], fill=head_color)
    # neck
    draw.rectangle([W//2-22, 255, W//2+22, 310], fill=head_color)

    # Soft inner glow on face
    for r in range(60, 0, -4):
        alpha = int(60 * (1 - r/60))
        glow_color = (215, 228, 210)
        draw.ellipse([W//2-r, 140-r//2, W//2+r, 220+r//2], fill=glow_color)

    # Hair hint — dark rounded top
    hair_color = (80, 55, 40)
    draw.ellipse([W//2-72, 72, W//2+72, 210], fill=hair_color)
    # re-draw face on top of hair
    draw.ellipse([W//2-60, 105, W//2+60, 270], fill=head_color)

    # Eyes (simple dots)
    eye_color = (40, 30, 20)
    draw.ellipse([W//2-22, 168, W//2-12, 180], fill=eye_color)
    draw.ellipse([W//2+12, 168, W//2+22, 180], fill=eye_color)
    # Nose
    draw.ellipse([W//2-4, 200, W//2+4, 210], fill=(160,140,130))
    # Lips
    draw.arc([W//2-16, 218, W//2+16, 235], start=0, end=180, fill=(180,100,90), width=3)

    # Botanical leaves — various positions
    leaf_green = (90, 140, 95)
    leaf_light = (140, 180, 130)
    # top left cluster
    draw_leaf(draw, 40, 120, 70, leaf_green, angle=-0.4)
    draw_leaf(draw, 70, 90, 55, leaf_light, angle=-0.8)
    draw_leaf(draw, 20, 80, 45, leaf_green, angle=0.3)
    # bottom right cluster
    draw_leaf(draw, W-50, H-150, 80, leaf_green, angle=0.5)
    draw_leaf(draw, W-80, H-120, 60, leaf_light, angle=0.2)
    draw_leaf(draw, W-30, H-100, 50, leaf_green, angle=1.0)
    # bottom left
    draw_leaf(draw, 80, H-60, 55, leaf_light, angle=-0.3)

    # Scattered dots
    dot_color = (168, 188, 168)
    for pos in [(120,50),(350,70),(400,400),(60,350),(200,560),(380,500)]:
        draw.ellipse([pos[0]-4, pos[1]-4, pos[0]+4, pos[1]+4], fill=dot_color)
    for pos in [(140,500),(320,40),(450,350)]:
        draw.ellipse([pos[0]-2, pos[1]-2, pos[0]+2, pos[1]+2], fill=dot_color)

    # Thin horizontal line accent at bottom area
    draw.line([(60, H-30), (W-60, H-30)], fill=(168,188,168), width=1)

    # Small ✦ stars text approximation using circles+lines
    for (sx, sy) in [(W-100, H-50), (30, 40), (W//2+120, 70)]:
        sz = 5
        draw.line([sx-sz, sy, sx+sz, sy], fill=(11,77,43), width=1)
        draw.line([sx, sy-sz, sx, sy+sz], fill=(11,77,43), width=1)
        draw.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(11,77,43))

    # Subtle noise
    img = add_noise(img, 6)

    # Slight vignette
    vignette = Image.new("RGBA", (W, H), (0,0,0,0))
    vd = ImageDraw.Draw(vignette)
    for r in range(max(W,H)//2, 0, -3):
        alpha = int(60 * max(0, 1 - r / (max(W,H)*0.6)))
        vd.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], fill=(0,0,0,alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, vignette).convert("RGB")

    img.save(os.path.join(OUT, "profile-main.jpg"), quality=95)
    print("✓ profile-main.jpg")

# ──────────────────────────────────────────────
# 2. PROFILE ACCENT — square (400x400)
#    BTS / candid feel — green tones, botanical overlay
# ──────────────────────────────────────────────
def make_profile_accent():
    W, H = 400, 500
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Background gradient: soft forest green
    gradient(draw, W, H, (195, 218, 195), (245, 246, 238))

    # Large organic blob in center
    blob_color = (160, 195, 160)
    draw.ellipse([40, 60, W-40, H-60], fill=blob_color)

    # Inner lighter blob
    inner_color = (210, 228, 208)
    draw.ellipse([80, 110, W-80, H-110], fill=inner_color)

    # Silhouette — person holding phone / camera
    body_c = (100, 145, 100)
    # torso
    draw.ellipse([W//2-55, H//2-20, W//2+55, H-60], fill=body_c)
    # head
    head_c = (185, 208, 183)
    draw.ellipse([W//2-50, 100, W//2+50, 230], fill=head_c)
    draw.rectangle([W//2-18, 215, W//2+18, 260], fill=head_c)
    # hair
    draw.ellipse([W//2-52, 92, W//2+52, 215], fill=(65, 45, 35))
    draw.ellipse([W//2-45, 115, W//2+45, 235], fill=head_c)

    # camera/phone in hands
    cam_color = (50, 50, 50)
    draw.rectangle([W//2-30, H//2+20, W//2+30, H//2+65], fill=cam_color, outline=(80,80,80), width=2)
    draw.ellipse([W//2-12, H//2+28, W//2+12, H//2+58], outline=(120,120,120), width=2)

    # Arms
    arm_c = (170, 195, 165)
    draw.ellipse([W//2-90, H//2+10, W//2-30, H//2+80], fill=arm_c)
    draw.ellipse([W//2+30, H//2+10, W//2+90, H//2+80], fill=arm_c)

    # Botanical frame
    leaf_dark = (60, 110, 65)
    leaf_med = (90, 145, 88)
    leaf_light = (135, 175, 128)
    # top cluster
    draw_leaf(draw, 30, 60, 90, leaf_dark, angle=-0.6)
    draw_leaf(draw, 70, 30, 75, leaf_med, angle=-1.1)
    draw_leaf(draw, 10, 30, 65, leaf_light, angle=0.2)
    # top right
    draw_leaf(draw, W-30, 50, 80, leaf_dark, angle=0.7)
    draw_leaf(draw, W-70, 25, 65, leaf_med, angle=1.2)
    # bottom
    draw_leaf(draw, 30, H-40, 70, leaf_med, angle=-0.4)
    draw_leaf(draw, W-40, H-40, 70, leaf_dark, angle=0.6)
    draw_leaf(draw, W//2, H-20, 60, leaf_light, angle=0.0)

    # Dots
    for pos in [(50,200),(350,200),(200,30),(30,H//2),(W-30,H//2)]:
        draw.ellipse([pos[0]-5, pos[1]-5, pos[0]+5, pos[1]+5], fill=(168,188,168))

    img = add_noise(img, 5)
    img.save(os.path.join(OUT, "profile-accent.jpg"), quality=95)
    print("✓ profile-accent.jpg")

# ──────────────────────────────────────────────
# 3. DECORATION — wide banner (1200x400)
#    Used as strip/banner image — moody forest green
# ──────────────────────────────────────────────
def make_decoration():
    W, H = 1200, 400
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Dark forest background
    gradient(draw, W, H, (8, 40, 22), (20, 65, 38))

    # Large soft circles (bokeh feel)
    bokeh_positions = [
        (200, 100, 120), (500, 300, 90), (800, 80, 110),
        (1050, 250, 100), (100, 320, 80), (650, 200, 140),
        (1150, 100, 70), (350, 50, 60), (900, 350, 85)
    ]
    for (bx, by, br) in bokeh_positions:
        for r in range(br, 0, -8):
            t = r / br
            alpha_val = int(30 * (1-t))
            c = lerp_color((30, 90, 50), (80, 150, 90), 1-t)
            draw.ellipse([bx-r, by-r, bx+r, by+r], fill=c)

    # Botanical silhouettes across width
    leaf_colors = [(25, 80, 40), (40, 100, 55), (55, 120, 65), (70, 140, 75)]
    leaf_positions = [
        (0, H, 180, -0.3), (100, H+20, 200, -0.6), (50, H//2, 150, -0.9),
        (300, H, 160, 0.1), (250, H+10, 140, -0.4),
        (500, H, 190, 0.2), (450, H//2+50, 130, -0.7),
        (700, H+20, 175, -0.2), (650, H//2, 120, 0.5),
        (900, H, 185, 0.1), (850, H//2+30, 145, -0.5),
        (1100, H, 170, -0.3), (1050, H//2, 130, 0.4),
        (1180, H//2+50, 150, 0.6), (W, H//2-20, 160, 0.9),
    ]
    for (lx, ly, ls, la) in leaf_positions:
        idx = int(abs(lx)) % len(leaf_colors)
        draw_leaf(draw, lx, ly, ls, leaf_colors[idx], angle=la)

    # Top leaf silhouettes
    for (lx, ls, la) in [(50,120,-2.8),(200,100,-2.5),(400,130,-2.9),(600,110,-2.6),(800,125,-2.8),(1000,115,-2.7),(1150,105,-2.9)]:
        draw_leaf(draw, lx, 0, ls, leaf_colors[1], angle=la)

    # Subtle horizontal lines (light)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(255,255,255), width=1)
    # Overlay to reduce line visibility
    overlay = Image.new("RGBA", (W, H), (8, 40, 22, 200))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay).convert("RGB")

    # Re-draw leaves on top of overlay
    img2 = img.copy()
    draw2 = ImageDraw.Draw(img2)
    for (lx, ly, ls, la) in leaf_positions[:8]:
        idx = int(abs(lx)) % len(leaf_colors)
        c = leaf_colors[idx]
        bright = tuple(min(255, v+30) for v in c)
        draw_leaf(draw2, lx, ly, ls, bright, angle=la)

    # Light rays
    for i in range(5):
        x = int(W * i / 4)
        ray_color = (60, 130, 70)
        pts = [(x-20, 0), (x+20, 0), (x+80, H), (x-80, H)]
        draw2.polygon(pts, fill=ray_color)

    final = img2.filter(ImageFilter.GaussianBlur(radius=1))
    add_noise(final, 10)
    final.save(os.path.join(OUT, "decoration.jpg"), quality=93)
    print("✓ decoration.jpg")

make_profile_main()
make_profile_accent()
make_decoration()
print("\nAll images generated!")
