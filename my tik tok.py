import pygame
import math
import random

# ── Init ────────────────────────────────────────────────────────────────────
pygame.init()
info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption("TikFeed")
clock = pygame.time.Clock()

# ── Colours ─────────────────────────────────────────────────────────────────
BLACK      = (0, 0, 0)
WHITE      = (255, 255, 255)
PINK       = (255, 20, 100)
CYAN       = (0, 242, 234)
GREY_DARK  = (18, 18, 18)
GREY_MID   = (40, 40, 40)
GREY_LIGHT = (180, 180, 180)
OVERLAY    = (0, 0, 0, 160)

# ── Fonts ────────────────────────────────────────────────────────────────────
def font(size, bold=False):
    return pygame.font.SysFont("sans", size, bold=bold)

F_BIG   = font(28, bold=True)
F_MED   = font(22)
F_SMALL = font(18)
F_TINY  = font(15)

# ── Posts data ───────────────────────────────────────────────────────────────
POSTS = [
    {
        "user":    "@kenneth_codes",
        "caption": "Building a full game on Android 🐍🎮 #Python #Pygame #MobileDev",
        "likes":   "14.2K",
        "comments":"832",
        "shares":  "1.1K",
        "color_a": (20, 10, 60),
        "color_b": (80, 0, 120),
        "anim":    "wave",
    },
    {
        "user":    "@pygame_daily",
        "caption": "Smooth parallax scrolling in 30 lines of code 👀 #GameDev",
        "likes":   "9.7K",
        "comments":"415",
        "shares":  "670",
        "color_a": (0, 30, 60),
        "color_b": (0, 100, 140),
        "anim":    "circles",
    },
    {
        "user":    "@codewithtunde",
        "caption": "Python is NOT hard. Watch this 👇 #LearnPython #Beginners",
        "likes":   "31K",
        "comments":"2.3K",
        "shares":  "5.8K",
        "color_a": (60, 10, 10),
        "color_b": (160, 40, 0),
        "anim":    "matrix",
    },
    {
        "user":    "@snakegamemaster",
        "caption": "Snake game from scratch in Pygame – full tutorial 🐍",
        "likes":   "22.4K",
        "comments":"1.9K",
        "shares":  "3.2K",
        "color_a": (0, 50, 20),
        "color_b": (0, 130, 60),
        "anim":    "pulse",
    },
    {
        "user":    "@afrotech_ng",
        "caption": "Nigerian coders are taking over 🇳🇬🔥 #TechAfrica #Coding",
        "likes":   "48K",
        "comments":"4.1K",
        "shares":  "9.9K",
        "color_a": (50, 30, 0),
        "color_b": (180, 100, 0),
        "anim":    "wave",
    },
]

# ── Animation helpers ─────────────────────────────────────────────────────────
def draw_wave(surf, rect, t, ca, cb):
    surf.fill(ca, rect)
    for y in range(rect.top, rect.bottom, 4):
        progress = (y - rect.top) / rect.height
        wave = math.sin(progress * 6 + t * 0.05) * 0.3 + 0.5
        r = int(ca[0] + (cb[0] - ca[0]) * wave)
        g = int(ca[1] + (cb[1] - ca[1]) * wave)
        b = int(ca[2] + (cb[2] - ca[2]) * wave)
        pygame.draw.line(surf, (r, g, b), (rect.left, y), (rect.right, y))

def draw_circles(surf, rect, t, ca, cb):
    surf.fill(ca, rect)
    cx, cy = rect.centerx, rect.centery
    for i in range(7):
        r = int(30 + i * 35 + math.sin(t * 0.04 + i) * 15)
        alpha_val = max(0, 180 - i * 25)
        c = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(c, (*cb, alpha_val), (r, r), r, 2)
        surf.blit(c, (cx - r, cy - r))

def draw_matrix(surf, rect, t, ca, cb):
    surf.fill(ca, rect)
    cols = rect.width // 14
    for col in range(cols):
        x = rect.left + col * 14 + 7
        offset = (col * 37 + int(t * 0.3)) % rect.height
        for row in range(8):
            y = rect.top + (offset + row * 22) % rect.height
            digit = str((col + row + int(t * 0.1)) % 10)
            alpha = 255 - row * 28
            alpha = max(0, alpha)
            color = (0, min(255, alpha), 0)
            txt = F_SMALL.render(digit, True, color)
            surf.blit(txt, (x - 5, y))

def draw_pulse(surf, rect, t, ca, cb):
    surf.fill(ca, rect)
    cx, cy = rect.centerx, rect.centery
    for i in range(6):
        size = int(40 + i * 45 + math.sin(t * 0.04 + i * 1.2) * 20)
        alpha_val = max(0, 160 - i * 25)
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.rect(s, (*cb, alpha_val), (0, 0, size * 2, size * 2),
                         3, border_radius=16)
        surf.blit(s, (cx - size, cy - size))

ANIM_FN = {
    "wave":    draw_wave,
    "circles": draw_circles,
    "matrix":  draw_matrix,
    "pulse":   draw_pulse,
}

# ── Like heart helper ─────────────────────────────────────────────────────────
def draw_heart(surf, cx, cy, size, color):
    pts = []
    for angle in range(360):
        rad = math.radians(angle)
        x = 16 * (math.sin(rad) ** 3)
        y = 13 * math.cos(rad) - 5 * math.cos(2 * rad) - \
            2 * math.cos(3 * rad) - math.cos(4 * rad)
        pts.append((cx + x * size / 16, cy - y * size / 16))
    if len(pts) > 2:
        pygame.draw.polygon(surf, color, pts)

# ── Right sidebar icons ───────────────────────────────────────────────────────
def draw_sidebar(surf, post, liked, like_scale, t):
    icon_x = W - 48
    icon_size = 38
    items = [
        ("heart",   post["likes"],    H // 2 - 80),
        ("comment", post["comments"], H // 2),
        ("share",   post["shares"],   H // 2 + 80),
        ("music",   "Sound",          H // 2 + 160),
    ]
    for kind, label, iy in items:
        if kind == "heart":
            scale = like_scale
            s = int(icon_size * scale)
            color = PINK if liked else WHITE
            draw_heart(surf, icon_x, iy, s, color)
        elif kind == "comment":
            pygame.draw.circle(surf, WHITE, (icon_x, iy), 18, 3)
            pygame.draw.polygon(surf, WHITE,
                [(icon_x - 8, iy + 14), (icon_x - 4, iy + 22),
                 (icon_x + 6, iy + 14)])
        elif kind == "share":
            pygame.draw.line(surf, WHITE, (icon_x - 14, iy + 8),
                             (icon_x + 14, iy - 8), 3)
            pygame.draw.polygon(surf, WHITE,
                [(icon_x + 14, iy - 8),
                 (icon_x + 2, iy - 16),
                 (icon_x + 20, iy - 18)])
        elif kind == "music":
            angle = t * 2
            pygame.draw.circle(surf, GREY_MID, (icon_x, iy), 18)
            pygame.draw.circle(surf, WHITE, (icon_x, iy), 18, 2)
            pygame.draw.circle(surf, CYAN, (icon_x, iy), 5)
            end_x = icon_x + int(math.cos(math.radians(angle)) * 14)
            end_y = iy + int(math.sin(math.radians(angle)) * 14)
            pygame.draw.line(surf, WHITE, (icon_x, iy), (end_x, end_y), 2)

        lbl = F_TINY.render(label, True, WHITE)
        surf.blit(lbl, (icon_x - lbl.get_width() // 2, iy + 24))

# ── Bottom overlay ────────────────────────────────────────────────────────────
def draw_bottom(surf, post):
    oy = H - 160
    ow = W - 80
    panel = pygame.Surface((ow, 140), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 0))
    for row in range(140):
        a = int(180 * row / 140)
        pygame.draw.line(panel, (0, 0, 0, a), (0, row), (ow, row))
    surf.blit(panel, (0, oy))
    name = F_BIG.render(post["user"], True, WHITE)
    surf.blit(name, (16, oy + 8))
    words = post["caption"].split()
    line, lines = "", []
    for w in words:
        test = line + w + " "
        if F_MED.size(test)[0] > ow - 16:
            lines.append(line)
            line = w + " "
        else:
            line = test
    lines.append(line)
    for i, ln in enumerate(lines[:3]):
        txt = F_MED.render(ln.strip(), True, GREY_LIGHT)
        surf.blit(txt, (16, oy + 44 + i * 26))

# ── Top bar ───────────────────────────────────────────────────────────────────
def draw_topbar(surf, tab):
    tabs = ["Following", "For You"]
    spacing = W // 3
    for i, name in enumerate(tabs):
        x = spacing + i * spacing
        col = WHITE if tab == i else GREY_LIGHT
        lbl = F_MED.render(name, True, col)
        surf.blit(lbl, (x - lbl.get_width() // 2, 12))
        if tab == i:
            bar_w = lbl.get_width() + 12
            pygame.draw.rect(surf, WHITE,
                             (x - bar_w // 2, 42, bar_w, 3), border_radius=2)
    pygame.draw.circle(surf, PINK, (W - 36, 26), 6)
    live = F_TINY.render("LIVE", True, WHITE)
    surf.blit(live, (W - 28, 19))

# ── Swipe hint ────────────────────────────────────────────────────────────────
def draw_hint(surf, alpha):
    if alpha <= 0:
        return
    arr = F_BIG.render("▲  swipe up", True, WHITE)
    s = pygame.Surface(arr.get_size(), pygame.SRCALPHA)
    s.blit(arr, (0, 0))
    s.set_alpha(max(0, min(255, alpha)))
    surf.blit(s, (W // 2 - arr.get_width() // 2, H - 220))

# ── Main loop ─────────────────────────────────────────────────────────────────
current      = 0
offset       = 0.0
dragging     = False
drag_start_y = 0
drag_cur_y   = 0
t            = 0
liked        = [False] * len(POSTS)
like_scale   = [1.0]  * len(POSTS)
hint_alpha   = 255
tab          = 1

running = True
while running:
    dt = clock.tick(60)
    t += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
            if event.type == pygame.FINGERDOWN:
                px, py = int(event.x * W), int(event.y * H)
            else:
                px, py = event.pos
            dragging = True
            drag_start_y = py
            drag_cur_y   = py

            # Tap like
            icon_x = W - 48
            like_y = H // 2 - 80
            if abs(px - icon_x) < 30 and abs(py - like_y) < 30:
                liked[current] = not liked[current]
                like_scale[current] = 1.4
                dragging = False

            # Tap tab
            if py < 52:
                for i, tx in enumerate([W // 3, W * 2 // 3]):
                    if abs(px - tx) < 60:
                        tab = i
                dragging = False

        if event.type in (pygame.FINGERMOTION, pygame.MOUSEMOTION):
            if dragging:
                if event.type == pygame.FINGERMOTION:
                    drag_cur_y = int(event.y * H)
                else:
                    drag_cur_y = event.pos[1]
                offset = drag_cur_y - drag_start_y

        if event.type in (pygame.FINGERUP, pygame.MOUSEBUTTONUP):
            if dragging:
                dragging = False
                threshold = H * 0.25
                if offset < -threshold and current < len(POSTS) - 1:
                    current += 1
                    hint_alpha = 0
                elif offset > threshold and current > 0:
                    current -= 1
                offset = 0

    # Animate like bounce
    for i in range(len(POSTS)):
        if like_scale[i] > 1.0:
            like_scale[i] = max(1.0, like_scale[i] - 0.06)

    # Ease offset back
    if not dragging and offset != 0:
        offset *= 0.75
        if abs(offset) < 1:
            offset = 0

    # Draw
    screen.fill(BLACK)
    post = POSTS[current]
    rect = pygame.Rect(0, int(offset), W, H)
    fn = ANIM_FN.get(post["anim"], draw_wave)
    fn(screen, rect, t, post["color_a"], post["color_b"])

    # Peek adjacent post while dragging
    if offset < -10 and current < len(POSTS) - 1:
        peek_rect = pygame.Rect(0, int(H + offset), W, H)
        np = POSTS[current + 1]
        ANIM_FN.get(np["anim"], draw_wave)(screen, peek_rect, t, np["color_a"], np["color_b"])
    elif offset > 10 and current > 0:
        peek_rect = pygame.Rect(0, int(-H + offset), W, H)
        pp = POSTS[current - 1]
        ANIM_FN.get(pp["anim"], draw_wave)(screen, peek_rect, t, pp["color_a"], pp["color_b"])

    draw_bottom(screen, post)
    draw_sidebar(screen, post, liked[current], like_scale[current], t)
    draw_topbar(screen, tab)
    draw_hint(screen, hint_alpha)

    # Progress dots
    for i in range(len(POSTS)):
        color = WHITE if i == current else GREY_MID
        pygame.draw.circle(screen, color, (W - 6, H // 2 - len(POSTS) * 10 + i * 20), 4)

    pygame.display.flip()

pygame.quit()