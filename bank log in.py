import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
W, H = screen.get_width(), screen.get_height()
pygame.display.set_caption("SecureBank")

BG        = (10,  14,  30)
CARD      = (18,  24,  48)
ACCENT    = (0,  168, 232)
WHITE     = (255, 255, 255)
GREY      = (140, 150, 170)
DARK_GREY = (60,  70,  90)
ERROR_RED = (220,  60,  60)
SUCCESS   = (50,  210, 120)
BLACK     = (0,    0,   0)

F_TITLE  = pygame.font.SysFont("monospace", int(H * 0.05),  bold=True)
F_LABEL  = pygame.font.SysFont("monospace", int(H * 0.025))
F_INPUT  = pygame.font.SysFont("monospace", int(H * 0.03))
F_BTN    = pygame.font.SysFont("monospace", int(H * 0.03),  bold=True)
F_SMALL  = pygame.font.SysFont("monospace", int(H * 0.02))
F_BANK   = pygame.font.SysFont("monospace", int(H * 0.07),  bold=True)

USERS = {
    "kenneth": "1234",
    "admin":   "pass",
}

STATE        = "login"
username_str = ""
password_str = ""
active_field = "username"
show_pw      = False
error_msg    = ""
attempts     = 0
MAX_ATTEMPTS = 3

KB_ROWS = [
    list("qwertyuiop"),
    list("asdfghjkl"),
    list("zxcvbnm"),
    ["123", "SPACE", "⌫"],
]
NUM_ROWS = [
    list("789"),
    list("456"),
    list("123"),
    ["0", "⌫"],
]
kb_mode = "alpha"

PAD    = int(W * 0.05)
CW     = W - PAD * 2
card_x = PAD

def draw_rounded_rect(surf, color, rect, radius=16, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def draw_text_center(surf, text, font, color, cx, cy):
    s = font.render(text, True, color)
    surf.blit(s, (cx - s.get_width() // 2, cy - s.get_height() // 2))

def draw_text(surf, text, font, color, x, y):
    s = font.render(text, True, color)
    surf.blit(s, (x, y))
    return s.get_width(), s.get_height()

def build_kb_rects(rows, start_y):
    keys  = []
    row_h = int(H * 0.065)
    gap   = int(W * 0.015)
    for r, row in enumerate(rows):
        n     = len(row)
        key_w = (W - gap * (n + 1)) // n
        for c, ch in enumerate(row):
            x = gap + c * (key_w + gap)
            y = start_y + r * (row_h + gap)
            keys.append((pygame.Rect(x, y, key_w, row_h), ch))
    return keys

KB_START_Y = int(H * 0.55)
alpha_keys = build_kb_rects(KB_ROWS, KB_START_Y)
num_keys   = build_kb_rects(NUM_ROWS, KB_START_Y)

FIELD_H      = int(H * 0.065)
field_y_user = int(H * 0.30)
field_y_pass = int(H * 0.42)
user_rect    = pygame.Rect(card_x, field_y_user, CW, FIELD_H)
pass_rect    = pygame.Rect(card_x, field_y_pass, CW, FIELD_H)

BTN_H    = int(H * 0.07)
btn_rect = pygame.Rect(card_x, int(H * 0.515), CW, BTN_H)
eye_rect = pygame.Rect(card_x + CW - int(W * 0.12), field_y_pass, int(W * 0.12), FIELD_H)
mode_rect = pygame.Rect(PAD, KB_START_Y - int(H * 0.055), int(W * 0.28), int(H * 0.045))

pulse = 0

def attempt_login():
    global STATE, error_msg, attempts
    u = username_str.strip().lower()
    p = password_str.strip()
    if u in USERS and USERS[u] == p:
        STATE     = "success"
        error_msg = ""
    else:
        attempts += 1
        if attempts >= MAX_ATTEMPTS:
            STATE = "locked"
        else:
            error_msg = f"Invalid credentials  ({MAX_ATTEMPTS - attempts} tries left)"

def draw_login():
    global pulse
    import math
    pulse = (pulse + 2) % 360
    glow  = int(abs(math.sin(math.radians(pulse))) * 60)

    screen.fill(BG)
    for gx in range(0, W, int(W * 0.1)):
        pygame.draw.line(screen, (20, 28, 55), (gx, 0), (gx, H))
    for gy in range(0, H, int(H * 0.08)):
        pygame.draw.line(screen, (20, 28, 55), (0, gy), (W, gy))

    draw_text_center(screen, "SECUREBANK", F_BANK,
                     (ACCENT[0], ACCENT[1], max(0, ACCENT[2] - glow)),
                     W // 2, int(H * 0.08))
    draw_text_center(screen, "Digital Banking Portal", F_SMALL, GREY,
                     W // 2, int(H * 0.135))

    # Username
    draw_text(screen, "USERNAME", F_LABEL, GREY, card_x, field_y_user - int(H * 0.03))
    draw_rounded_rect(screen, CARD, user_rect, 12, 2,
                      ACCENT if active_field == "username" else DARK_GREY)
    txt_u = username_str if username_str else "tap to type..."
    draw_text(screen, txt_u, F_INPUT, WHITE if username_str else GREY,
              user_rect.x + int(W * 0.03),
              user_rect.y + (FIELD_H - F_INPUT.get_height()) // 2)

    # Password
    draw_text(screen, "PASSWORD", F_LABEL, GREY, card_x, field_y_pass - int(H * 0.03))
    draw_rounded_rect(screen, CARD, pass_rect, 12, 2,
                      ACCENT if active_field == "password" else DARK_GREY)
    if password_str:
        display_p = password_str if show_pw else "●" * len(password_str)
    else:
        display_p = "tap to type..."
    draw_text(screen, display_p, F_INPUT, WHITE if password_str else GREY,
              pass_rect.x + int(W * 0.03),
              pass_rect.y + (FIELD_H - F_INPUT.get_height()) // 2)
    draw_text_center(screen, "HIDE" if show_pw else "SHOW", F_SMALL, ACCENT,
                     eye_rect.centerx, eye_rect.centery)

    if error_msg:
        draw_text_center(screen, error_msg, F_SMALL, ERROR_RED, W // 2, int(H * 0.50))

    draw_rounded_rect(screen, ACCENT, btn_rect, 14)
    draw_text_center(screen, "LOG IN", F_BTN, BLACK, btn_rect.centerx, btn_rect.centery)

    draw_rounded_rect(screen, DARK_GREY, mode_rect, 10)
    draw_text_center(screen, "→ 123" if kb_mode == "alpha" else "→ ABC",
                     F_SMALL, WHITE, mode_rect.centerx, mode_rect.centery)

    keys = alpha_keys if kb_mode == "alpha" else num_keys
    for rect, ch in keys:
        draw_rounded_rect(screen, (30, 40, 70), rect, 8)
        draw_rounded_rect(screen, BLACK, rect, 8, 1, (50, 60, 90))
        draw_text_center(screen, " " if ch == "SPACE" else ch.upper(),
                         F_SMALL, WHITE, rect.centerx, rect.centery)

def draw_success():
    screen.fill(BG)
    draw_text_center(screen, "SUCCESS", F_BANK, SUCCESS, W // 2, int(H * 0.3))
    draw_text_center(screen, "Welcome back,", F_LABEL, GREY, W // 2, int(H * 0.48))
    draw_text_center(screen, username_str.upper(), F_TITLE, WHITE, W // 2, int(H * 0.55))
    draw_text_center(screen, "Login successful", F_SMALL, SUCCESS, W // 2, int(H * 0.63))
    out_rect = pygame.Rect(PAD, int(H * 0.75), CW, BTN_H)
    draw_rounded_rect(screen, DARK_GREY, out_rect, 14)
    draw_text_center(screen, "LOG OUT", F_BTN, WHITE, out_rect.centerx, out_rect.centery)
    return out_rect

def draw_locked():
    screen.fill(BG)
    draw_text_center(screen, "LOCKED", F_BANK, ERROR_RED, W // 2, int(H * 0.3))
    draw_text_center(screen, "ACCOUNT LOCKED", F_TITLE, ERROR_RED, W // 2, int(H * 0.48))
    draw_text_center(screen, "Too many failed attempts", F_SMALL, GREY, W // 2, int(H * 0.56))
    draw_text_center(screen, "Contact support to unlock", F_SMALL, GREY, W // 2, int(H * 0.62))
    reset_rect = pygame.Rect(PAD, int(H * 0.75), CW, BTN_H)
    draw_rounded_rect(screen, DARK_GREY, reset_rect, 14)
    draw_text_center(screen, "RESET (DEMO)", F_BTN, WHITE,
                     reset_rect.centerx, reset_rect.centery)
    return reset_rect

def handle_key(ch):
    global username_str, password_str, kb_mode
    val = username_str if active_field == "username" else password_str

    if ch == "⌫":
        val = val[:-1]
    elif ch == "SPACE":
        val += " "
    elif ch == "123":
        kb_mode = "num";  return
    elif ch == "ABC":
        kb_mode = "alpha"; return
    else:
        val += ch.lower()

    if active_field == "username":
        username_str = val
    else:
        password_str = val

def reset():
    global STATE, username_str, password_str, error_msg, attempts, active_field, show_pw
    STATE = "login"; username_str = ""; password_str = ""
    error_msg = ""; attempts = 0; active_field = "username"; show_pw = False

clock = pygame.time.Clock()

while True:
    clock.tick(60)

    if STATE == "login":
        draw_login()
    elif STATE == "success":
        logout_rect = draw_success()
    else:
        reset_rect = draw_locked()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # ── ONLY FINGERDOWN — fixes double-input bug on Pydroid 3 ──
        tap_pos = None
        if event.type == pygame.FINGERDOWN:
            tap_pos = (int(event.x * W), int(event.y * H))

        if tap_pos is None:
            continue

        tx, ty = tap_pos

        if STATE == "login":
            if user_rect.collidepoint(tx, ty):
                active_field = "username"
            elif pass_rect.collidepoint(tx, ty):
                active_field = "password"
            elif eye_rect.collidepoint(tx, ty):
                show_pw = not show_pw
            elif btn_rect.collidepoint(tx, ty):
                attempt_login()
            elif mode_rect.collidepoint(tx, ty):
                kb_mode = "num" if kb_mode == "alpha" else "alpha"
            else:
                keys = alpha_keys if kb_mode == "alpha" else num_keys
                for rect, ch in keys:
                    if rect.collidepoint(tx, ty):
                        handle_key(ch); break

        elif STATE == "success":
            if logout_rect.collidepoint(tx, ty):
                reset()

        elif STATE == "locked":
            if reset_rect.collidepoint(tx, ty):
                reset()