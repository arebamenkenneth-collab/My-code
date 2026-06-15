import pygame
import sys
import time

pygame.init()

# ── Screen ──────────────────────────────────────────────────────────────
info = pygame.display.Info()
WIDTH  = min(500, info.current_w)
HEIGHT = min(860, info.current_h)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CodeWithKenneth")

# ── Colours ──────────────────────────────────────────────────────────────
BG          = (15,  15,  25)
CARD        = (28,  28,  45)
CARD2       = (38,  38,  58)
ACCENT      = (99, 102, 241)
ACCENT2     = (236, 72, 153)
GREEN       = (34, 197, 94)
RED         = (239, 68, 68)
YELLOW      = (250, 204, 21)
WHITE       = (255, 255, 255)
GRAY        = (160, 160, 180)
LIGHT_GRAY  = (210, 210, 230)
NAV_BG      = (20,  20,  35)
DIVIDER     = (45,  45,  65)

# ── Fonts ────────────────────────────────────────────────────────────────
f_big    = pygame.font.Font(None, 42)
f_med    = pygame.font.Font(None, 32)
f_small  = pygame.font.Font(None, 26)
f_tiny   = pygame.font.Font(None, 22)

# ── State ────────────────────────────────────────────────────────────────
page          = "home"
scroll_y      = 0
typing        = False
draft_text    = ""
finger_used   = False
notif_count   = 2

profile = {
    "name":      "Kenneth",
    "handle":    "@codewithkenneth",
    "bio":       "🐍 Teaching Python on mobile | Pygame lover | Nigeria 🇳🇬",
    "followers":  1_204,
    "following":  318,
}

posts = [
    {
        "author":   "Kenneth",
        "handle":   "@codewithkenneth",
        "time":     "2h ago",
        "body":     "Just built a calculator in Pygame with square root! 🧮🔥 Mobile Python is real, guys.",
        "likes":    47,
        "liked":    False,
        "comments": 12,
    },
    {
        "author":   "PyBeginner",
        "handle":   "@pythonnewbie",
        "time":     "4h ago",
        "body":     "Kenneth's Python group on WhatsApp changed my life. From zero to building games in 3 weeks! 💪",
        "likes":    83,
        "liked":    False,
        "comments": 9,
    },
    {
        "author":   "TechNaija",
        "handle":   "@technaija",
        "time":     "6h ago",
        "body":     "Pydroid 3 + Pygame = 🚀  No laptop needed. Nigerian coders are winning!",
        "likes":    124,
        "liked":    False,
        "comments": 21,
    },
    {
        "author":   "CodeQueen",
        "handle":   "@codequeenng",
        "time":     "1d ago",
        "body":     "Anyone else using CodeWithKenneth's free Python group? Best decision of 2025 👏",
        "likes":    56,
        "liked":    False,
        "comments": 7,
    },
]

notifications = [
    {"icon": "❤️",  "text": "PyBeginner liked your post",        "time": "2m ago"},
    {"icon": "💬",  "text": "TechNaija commented on your post",  "time": "15m ago"},
    {"icon": "👥",  "text": "CodeQueen started following you",   "time": "1h ago"},
    {"icon": "🔥",  "text": "Your post is trending in #Python",  "time": "3h ago"},
    {"icon": "⭐",  "text": "You hit 1,200 followers!",          "time": "5h ago"},
]

# ── Helpers ───────────────────────────────────────────────────────────────
NAV_H    = 70
HEADER_H = 60
INPUT_H  = 80

def draw_text(surf, text, font, color, x, y, max_width=None):
    if max_width is None:
        s = font.render(text, True, color)
        surf.blit(s, (x, y))
        return font.size(text)[1]
    words = text.split()
    line  = ""
    cy    = y
    lh    = font.size("A")[1] + 3
    for w in words:
        test = line + w + " "
        if font.size(test)[0] <= max_width:
            line = test
        else:
            surf.blit(font.render(line.strip(), True, color), (x, cy))
            cy  += lh
            line = w + " "
    if line.strip():
        surf.blit(font.render(line.strip(), True, color), (x, cy))
        cy += lh
    return cy - y

def draw_rounded_rect(surf, color, rect, r=12):
    pygame.draw.rect(surf, color, rect, border_radius=r)

def draw_avatar(surf, x, y, size, color, letter):
    pygame.draw.circle(surf, color, (x + size//2, y + size//2), size//2)
    lbl = f_med.render(letter, True, WHITE)
    surf.blit(lbl, (x + size//2 - lbl.get_width()//2,
                    y + size//2 - lbl.get_height()//2))

def avatar_color(name):
    colors = [ACCENT, ACCENT2, GREEN, (255, 165, 0), (0, 200, 200)]
    return colors[ord(name[0]) % len(colors)]

# ── Post card ─────────────────────────────────────────────────────────────
POST_RECTS = []

def draw_post(surf, post, idx, y, clip_top, clip_bot):
    pad   = 12
    aw    = WIDTH - 2*pad
    x     = pad
    ac    = avatar_color(post["author"])

    words     = post["body"].split()
    line      = ""
    lh        = f_small.size("A")[1] + 3
    max_w     = aw - 70
    body_lines = []
    for w in words:
        test = line + w + " "
        if f_small.size(test)[0] <= max_w:
            line = test
        else:
            body_lines.append(line.strip())
            line = w + " "
    if line.strip():
        body_lines.append(line.strip())

    body_h = len(body_lines) * lh
    card_h = 20 + 40 + 8 + body_h + 10 + 30 + 14
    rect   = pygame.Rect(x, y, aw, card_h)

    if y + card_h < clip_top or y > clip_bot:
        return y + card_h + 8

    draw_rounded_rect(surf, CARD, rect, 14)
    draw_avatar(surf, x+10, y+14, 38, ac, post["author"][0])
    surf.blit(f_med.render(post["author"], True, WHITE),  (x+56, y+14))
    surf.blit(f_tiny.render(post["handle"], True, GRAY),  (x+56, y+36))
    surf.blit(f_tiny.render(post["time"],   True, GRAY),
              (x + aw - f_tiny.size(post["time"])[0] - 10, y+14))

    by = y + 60
    for ln in body_lines:
        surf.blit(f_small.render(ln, True, LIGHT_GRAY), (x+10, by))
        by += lh

    action_y = by + 6
    like_col = GREEN if post["liked"] else GRAY
    surf.blit(f_small.render(f"❤  {post['likes']}",    True, like_col), (x+10,  action_y))
    surf.blit(f_small.render(f"💬  {post['comments']}", True, GRAY),     (x+100, action_y))

    like_rect = pygame.Rect(x+10, action_y, 80, 28)
    POST_RECTS.append((like_rect, idx))

    return y + card_h + 8

# ── Pages ─────────────────────────────────────────────────────────────────
def draw_header(title):
    pygame.draw.rect(screen, NAV_BG, (0, 0, WIDTH, HEADER_H))
    pygame.draw.line(screen, DIVIDER, (0, HEADER_H), (WIDTH, HEADER_H), 1)
    if title == "home":
        logo1 = f_big.render("Code",    True, ACCENT)
        logo2 = f_big.render("With",    True, ACCENT2)
        logo3 = f_big.render("Kenneth", True, WHITE)
        tx = 10
        screen.blit(logo1, (tx, 12)); tx += logo1.get_width()
        screen.blit(logo2, (tx, 12)); tx += logo2.get_width()
        screen.blit(logo3, (tx, 12))
    else:
        lbl = f_big.render(title.capitalize(), True, WHITE)
        screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, 14))

def draw_nav():
    pygame.draw.rect(screen, NAV_BG, (0, HEIGHT - NAV_H, WIDTH, NAV_H))
    pygame.draw.line(screen, DIVIDER, (0, HEIGHT - NAV_H), (WIDTH, HEIGHT - NAV_H), 1)
    tabs = [("🏠", "home"), ("👤", "profile"), ("🔔", "notifications")]
    w3   = WIDTH // 3
    for i, (icon, pg) in enumerate(tabs):
        cx  = i * w3 + w3 // 2
        cy  = HEIGHT - NAV_H + 14
        col = ACCENT if page == pg else GRAY
        lbl = f_med.render(icon, True, col)
        screen.blit(lbl, (cx - lbl.get_width()//2, cy))
        nm  = f_tiny.render(pg.capitalize(), True, col)
        screen.blit(nm,  (cx - nm.get_width()//2,  cy + 28))
        if pg == "notifications" and notif_count > 0:
            bx, by = cx + 10, cy - 4
            pygame.draw.circle(screen, RED, (bx, by), 9)
            nb = f_tiny.render(str(notif_count), True, WHITE)
            screen.blit(nb, (bx - nb.get_width()//2, by - nb.get_height()//2))

def draw_home():
    clip_top = HEADER_H
    clip_bot = HEIGHT - NAV_H - INPUT_H
    screen.fill(BG)
    draw_header("home")
    screen.set_clip(pygame.Rect(0, clip_top, WIDTH, clip_bot - clip_top))
    POST_RECTS.clear()
    y = clip_top + scroll_y + 8
    for i, p in enumerate(posts):
        y = draw_post(screen, p, i, y, clip_top, clip_bot)
    screen.set_clip(None)

    # Composer
    comp_y    = HEIGHT - NAV_H - INPUT_H
    pygame.draw.rect(screen, NAV_BG, (0, comp_y, WIDTH, INPUT_H))
    pygame.draw.line(screen, DIVIDER, (0, comp_y), (WIDTH, comp_y), 1)
    box_rect  = pygame.Rect(10, comp_y + 10, WIDTH - 90, 55)
    post_rect = pygame.Rect(WIDTH - 76, comp_y + 18, 66, 38)
    bord_col  = ACCENT if typing else CARD2
    draw_rounded_rect(screen, CARD2, box_rect, 10)
    pygame.draw.rect(screen, bord_col, box_rect, 2, border_radius=10)
    display  = draft_text if draft_text else "What's on your mind?"
    txt_col  = WHITE if draft_text else GRAY
    cursor   = "|" if typing and int(time.time() * 2) % 2 == 0 else ""
    txt_surf = f_small.render(display[:38] + cursor, True, txt_col)
    screen.blit(txt_surf, (box_rect.x + 10, box_rect.y + 18))
    draw_rounded_rect(screen, ACCENT, post_rect, 10)
    pl = f_small.render("Post", True, WHITE)
    screen.blit(pl, (post_rect.x + post_rect.width//2  - pl.get_width()//2,
                     post_rect.y + post_rect.height//2 - pl.get_height()//2))
    draw_nav()
    return box_rect, post_rect

def draw_profile():
    screen.fill(BG)
    draw_header("profile")
    y = HEADER_H + 20
    pygame.draw.rect(screen, ACCENT, (0, HEADER_H, WIDTH, 90))
    draw_avatar(screen, WIDTH//2 - 36, y + 30, 72, ACCENT2, profile["name"][0])
    y += 120
    nm = f_big.render(profile["name"], True, WHITE)
    screen.blit(nm, (WIDTH//2 - nm.get_width()//2, y)); y += nm.get_height() + 4
    hd = f_small.render(profile["handle"], True, GRAY)
    screen.blit(hd, (WIDTH//2 - hd.get_width()//2, y)); y += hd.get_height() + 10
    bio_h = draw_text(screen, profile["bio"], f_small, LIGHT_GRAY, 20, y, WIDTH - 40)
    y += bio_h + 18
    stats = [
        (str(len(posts)),           "Posts"),
        (f"{profile['followers']:,}", "Followers"),
        (str(profile["following"]),  "Following"),
    ]
    sw = WIDTH // 3
    for i, (val, lbl) in enumerate(stats):
        cx = i * sw + sw // 2
        vl = f_big.render(val, True, ACCENT)
        ll = f_tiny.render(lbl, True, GRAY)
        screen.blit(vl, (cx - vl.get_width()//2, y))
        screen.blit(ll, (cx - ll.get_width()//2, y + vl.get_height() + 2))
    y += 70
    pygame.draw.line(screen, DIVIDER, (0, y), (WIDTH, y), 1); y += 14
    lbl = f_med.render("My Posts", True, WHITE)
    screen.blit(lbl, (16, y)); y += lbl.get_height() + 8
    my = [p for p in posts if p["author"] == "Kenneth"]
    if not my:
        screen.blit(f_small.render("No posts yet. Share something!", True, GRAY), (16, y))
    else:
        for p in my[:2]:
            draw_rounded_rect(screen, CARD, pygame.Rect(10, y, WIDTH-20, 60), 10)
            preview = p["body"][:55] + ("…" if len(p["body"]) > 55 else "")
            screen.blit(f_small.render(preview, True, LIGHT_GRAY), (18, y+10))
            screen.blit(f_tiny.render(f"❤ {p['likes']}  💬 {p['comments']}", True, GRAY), (18, y+36))
            y += 70
    draw_nav()

def draw_notifications():
    screen.fill(BG)
    draw_header("notifications")
    y = HEADER_H + 12
    for n in notifications:
        draw_rounded_rect(screen, CARD, pygame.Rect(10, y, WIDTH-20, 60), 10)
        screen.blit(f_med.render(n["icon"],  True, WHITE),      (20, y+16))
        screen.blit(f_small.render(n["text"], True, LIGHT_GRAY), (56, y+10))
        screen.blit(f_tiny.render(n["time"],  True, GRAY),       (56, y+34))
        y += 68
    draw_nav()

# ── Input handling ────────────────────────────────────────────────────────
def nav_tab_hit(px, py):
    if py < HEIGHT - NAV_H:
        return None
    tabs = ["home", "profile", "notifications"]
    col  = px // (WIDTH // 3)
    return tabs[col] if col < len(tabs) else None

def handle_tap(px, py, box_rect, post_rect):
    global page, scroll_y, typing, draft_text, notif_count

    tab = nav_tab_hit(px, py)
    if tab:
        page     = tab
        scroll_y = 0
        if tab == "notifications":
            notif_count = 0
        typing = False
        return

    if page == "home":
        if box_rect and box_rect.collidepoint(px, py):
            typing = True
            return
        if post_rect and post_rect.collidepoint(px, py) and draft_text.strip():
            posts.insert(0, {
                "author":   "Kenneth",
                "handle":   "@codewithkenneth",
                "time":     "Just now",
                "body":     draft_text.strip(),
                "likes":    0,
                "liked":    False,
                "comments": 0,
            })
            draft_text = ""
            typing     = False
            return
        for lr, idx in POST_RECTS:
            if lr.collidepoint(px, py):
                if not posts[idx]["liked"]:
                    posts[idx]["likes"] += 1
                    posts[idx]["liked"]  = True
                else:
                    posts[idx]["likes"] -= 1
                    posts[idx]["liked"]  = False
                return
        typing = False

# ── Main loop ─────────────────────────────────────────────────────────────
clock     = pygame.time.Clock()
box_rect  = None
post_rect = None

running = True
while running:
    clock.tick(60)

    if page == "home":
        box_rect, post_rect = draw_home()
    elif page == "profile":
        draw_profile()
    elif page == "notifications":
        draw_notifications()

    finger_used = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and typing:
            if event.key == pygame.K_BACKSPACE:
                draft_text = draft_text[:-1]
            elif event.key == pygame.K_RETURN:
                typing = False
            else:
                draft_text += event.unicode

        if event.type == pygame.FINGERDOWN:
            finger_used = True
            handle_tap(int(event.x * WIDTH), int(event.y * HEIGHT),
                       box_rect, post_rect)

        if event.type == pygame.MOUSEBUTTONDOWN and not finger_used:
            handle_tap(event.pos[0], event.pos[1], box_rect, post_rect)

        if event.type == pygame.MOUSEWHEEL and page == "home":
            scroll_y = max(-500, min(0, scroll_y + event.y * 25))

    pygame.display.update()

pygame.quit()
sys.exit()