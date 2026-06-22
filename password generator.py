import pygame
import random
import string
import sys

pygame.init()
info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption("Password Generator")

# Colors
BG = (10, 14, 26)
CARD = (20, 25, 45)
ACCENT = (99, 102, 241)
ACCENT2 = (139, 92, 246)
GREEN = (52, 211, 153)
RED = (239, 68, 68)
TEXT = (226, 232, 240)
MUTED = (100, 116, 139)
WHITE = (255, 255, 255)
TOGGLE_ON = (99, 102, 241)
TOGGLE_OFF = (50, 60, 80)

# Fonts
BIG = pygame.font.SysFont("monospace", int(H * 0.045), bold=True)
MED = pygame.font.SysFont("monospace", int(H * 0.032))
SML = pygame.font.SysFont("monospace", int(H * 0.025))
TINY = pygame.font.SysFont("monospace", int(H * 0.02))

# State
length = 16
use_upper = True
use_lower = True
use_digits = True
use_symbols = True
password = ""
copied = False
copy_timer = 0
strength = ""
strength_color = WHITE

def generate_password():
    global password, strength, strength_color
    charset = ""
    if use_upper: charset += string.ascii_uppercase
    if use_lower: charset += string.ascii_lowercase
    if use_digits: charset += string.digits
    if use_symbols: charset += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    if not charset:
        password = "Enable at least one!"
        strength = ""
        return
    password = "".join(random.choices(charset, k=length))
    # Strength
    types = sum([use_upper, use_lower, use_digits, use_symbols])
    if length >= 16 and types >= 3:
        strength, strength_color = "STRONG 💪", GREEN
    elif length >= 10 and types >= 2:
        strength, strength_color = "MEDIUM ⚡", (251, 191, 36)
    else:
        strength, strength_color = "WEAK ⚠️", RED

generate_password()

def draw_rounded_rect(surf, color, rect, r=18):
    pygame.draw.rect(surf, color, rect, border_radius=r)

def draw_toggle(x, y, w, h, state):
    color = TOGGLE_ON if state else TOGGLE_OFF
    draw_rounded_rect(screen, color, (x, y, w, h), h // 2)
    cx = x + w - h // 2 - 4 if state else x + h // 2 + 4
    cy = y + h // 2
    pygame.draw.circle(screen, WHITE, (cx, cy), h // 2 - 4)

def wrap_text(text, font, max_w):
    words = text
    lines = []
    line = ""
    for ch in words:
        test = line + ch
        if font.size(test)[0] > max_w:
            lines.append(line)
            line = ch
        else:
            line = test
    if line:
        lines.append(line)
    return lines

# Layout
pad = int(W * 0.05)
card_w = W - pad * 2
cy = int(H * 0.04)

# Password display area
pw_box = pygame.Rect(pad, cy, card_w, int(H * 0.13))
cy += pw_box.height + int(H * 0.015)

# Strength bar
str_y = cy
cy += int(H * 0.04)

# Length control
len_y = cy
cy += int(H * 0.07)

# Toggles
tog_y = cy
tog_h = int(H * 0.06)
tog_w = int(W * 0.13)
tog_x = W - pad - tog_w

toggle_rects = [
    pygame.Rect(tog_x, tog_y, tog_w, int(tog_h * 0.6)),
    pygame.Rect(tog_x, tog_y + tog_h, tog_w, int(tog_h * 0.6)),
    pygame.Rect(tog_x, tog_y + tog_h * 2, tog_w, int(tog_h * 0.6)),
    pygame.Rect(tog_x, tog_y + tog_h * 3, tog_w, int(tog_h * 0.6)),
]
cy += tog_h * 4 + int(H * 0.02)

# Buttons
btn_h = int(H * 0.085)
btn_gap = int(W * 0.04)
btn_w = (card_w - btn_gap) // 2
gen_btn = pygame.Rect(pad, cy, btn_w, btn_h)
copy_btn = pygame.Rect(pad + btn_w + btn_gap, cy, btn_w, btn_h)

# Length minus/plus
minus_btn = pygame.Rect(pad, len_y + int(H * 0.008), int(W * 0.1), int(H * 0.05))
plus_btn = pygame.Rect(pad + int(W * 0.1) + int(W * 0.5), len_y + int(H * 0.008), int(W * 0.1), int(H * 0.05))

finger_down = {}

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    if copied:
        copy_timer -= dt
        if copy_timer <= 0:
            copied = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        tap_pos = None

        if event.type == pygame.FINGERDOWN:
            tx, ty = int(event.x * W), int(event.y * H)
            finger_down[event.finger_id] = (tx, ty)
            tap_pos = (tx, ty)

        if event.type == pygame.MOUSEBUTTONDOWN and not finger_down:
            tap_pos = event.pos

        if tap_pos:
            x, y = tap_pos

            if gen_btn.collidepoint(x, y):
                generate_password()

            elif copy_btn.collidepoint(x, y) and password and "Enable" not in password:
                try:
                    import subprocess
                    subprocess.run(['termux-clipboard-set', password])
                    copied = True
                    copy_timer = 2000
                except:
                    copied = True
                    copy_timer = 2000

            elif minus_btn.collidepoint(x, y):
                if length > 4:
                    length -= 1
                    generate_password()

            elif plus_btn.collidepoint(x, y):
                if length < 64:
                    length += 1
                    generate_password()

            else:
                for i, tr in enumerate(toggle_rects):
                    if tr.collidepoint(x, y):
                        if i == 0: use_upper = not use_upper
                        elif i == 1: use_lower = not use_lower
                        elif i == 2: use_digits = not use_digits
                        elif i == 3: use_symbols = not use_symbols
                        generate_password()

        if event.type == pygame.FINGERUP:
            finger_down.pop(event.finger_id, None)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Draw
    screen.fill(BG)

    # Password box
    draw_rounded_rect(screen, CARD, pw_box)
    pygame.draw.rect(screen, ACCENT, pw_box, 2, border_radius=18)
    pw_lines = wrap_text(password, MED, card_w - int(W * 0.06))
    line_h = MED.get_height()
    total_h = len(pw_lines) * line_h
    start_y = pw_box.centery - total_h // 2
    for i, line in enumerate(pw_lines):
        surf = MED.render(line, True, GREEN if "Enable" not in password else RED)
        screen.blit(surf, (pw_box.x + int(W * 0.03), start_y + i * line_h))

    # Strength
    if strength:
        s_surf = SML.render(f"Strength: {strength}", True, strength_color)
        screen.blit(s_surf, (pad, str_y + int(H * 0.005)))

    # Length
    l_label = MED.render(f"Length:", True, MUTED)
    screen.blit(l_label, (pad, len_y))
    draw_rounded_rect(screen, CARD, minus_btn, 12)
    m_surf = BIG.render("-", True, ACCENT2)
    screen.blit(m_surf, (minus_btn.centerx - m_surf.get_width() // 2, minus_btn.centery - m_surf.get_height() // 2))

    # Length number
    lnum_surf = BIG.render(str(length), True, WHITE)
    lnum_x = pad + int(W * 0.1) + int((int(W * 0.5) - lnum_surf.get_width()) // 2)
    screen.blit(lnum_surf, (lnum_x, len_y + int(H * 0.008)))

    draw_rounded_rect(screen, CARD, plus_btn, 12)
    p_surf = BIG.render("+", True, ACCENT2)
    screen.blit(p_surf, (plus_btn.centerx - p_surf.get_width() // 2, plus_btn.centery - p_surf.get_height() // 2))

    # Toggles
    labels = ["Uppercase  A-Z", "Lowercase  a-z", "Numbers   0-9", "Symbols  !@#$"]
    states = [use_upper, use_lower, use_digits, use_symbols]
    for i, (tr, lbl, st) in enumerate(zip(toggle_rects, labels, states)):
        l_surf = SML.render(lbl, True, TEXT if st else MUTED)
        screen.blit(l_surf, (pad, tr.centery - l_surf.get_height() // 2))
        draw_toggle(tr.x, tr.y, tr.width, tr.height, st)

    # Buttons
    draw_rounded_rect(screen, ACCENT, gen_btn)
    g_surf = MED.render("🔄 Generate", True, WHITE)
    screen.blit(g_surf, (gen_btn.centerx - g_surf.get_width() // 2, gen_btn.centery - g_surf.get_height() // 2))

    copy_color = GREEN if copied else ACCENT2
    draw_rounded_rect(screen, copy_color, copy_btn)
    c_text = "✅ Copied!" if copied else "📋 Copy"
    c_surf = MED.render(c_text, True, WHITE)
    screen.blit(c_surf, (copy_btn.centerx - c_surf.get_width() // 2, copy_btn.centery - c_surf.get_height() // 2))

    # Title
    title = TINY.render("🔐 CodeWithKenneth — Password Generator", True, MUTED)
    screen.blit(title, (W // 2 - title.get_width() // 2, H - int(H * 0.04)))

    pygame.display.flip()

pygame.quit()
sys.exit()