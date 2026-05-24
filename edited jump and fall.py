import pygame
import random
import math

pygame.init()

# ── Screen ───────────────────────────────────────────────
SW, SH = 480, 800
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Sky Jumper")
clock = pygame.time.Clock()
FPS = 60

# ── Colors ───────────────────────────────────────────────
SKY1    = (20,  20,  60)
SKY2    = (60,  20, 100)
WHITE   = (255, 255, 255)
YELLOW  = (255, 220,  50)
RED     = (220,  50,  50)
GREEN   = ( 60, 200,  80)
DKGREEN = ( 30, 140,  50)
BLUE    = ( 60, 120, 255)
ORANGE  = (255, 140,  30)
PINK    = (255,  80, 160)
GRAY    = (120, 120, 140)
DKGRAY  = ( 60,  60,  80)
BLACK   = (  0,   0,   0)
COIN_C  = (255, 210,  30)
STAR_C  = (200, 200, 255)

# ── Fonts ────────────────────────────────────────────────
font_big  = pygame.font.SysFont("monospace", 52, bold=True)
font_med  = pygame.font.SysFont("monospace", 32, bold=True)
font_sm   = pygame.font.SysFont("monospace", 22)

# ── Stars (background) ───────────────────────────────────
stars = [(random.randint(0, SW), random.randint(0, SH),
          random.uniform(0.5, 2.0)) for _ in range(120)]

# ── Button layout ────────────────────────────────────────
BTN_Y  = SH - 110
BTNS = {
    "left":  pygame.Rect(20,  BTN_Y, 100, 90),
    "right": pygame.Rect(130, BTN_Y, 100, 90),
    "jump":  pygame.Rect(SW - 130, BTN_Y, 110, 90),
}

def draw_buttons(held):
    for name, rect in BTNS.items():
        col = (100, 100, 160) if name not in held else (180, 180, 80)
        pygame.draw.rect(screen, col, rect, border_radius=18)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=18)
        label = {"left": "◀", "right": "▶", "jump": "▲"}[name]
        t = font_med.render(label, True, WHITE)
        screen.blit(t, (rect.centerx - t.get_width()//2,
                        rect.centery - t.get_height()//2))

def btn_hit(pos):
    for name, rect in BTNS.items():
        if rect.collidepoint(pos):
            return name
    return None

# ── Draw helpers ─────────────────────────────────────────
def draw_text(txt, font, color, x, y, center=False):
    s = font.render(txt, True, color)
    if center:
        screen.blit(s, (x - s.get_width()//2, y))
    else:
        screen.blit(s, (x, y))

def draw_bg():
    screen.fill(SKY1)
    for x, y, r in stars:
        pygame.draw.circle(screen, STAR_C, (int(x), int(y)), int(r))

# ── Platform ─────────────────────────────────────────────
class Platform:
    def __init__(self, x, y, w, moving=False, has_coin=False, has_enemy=False):
        self.rect   = pygame.Rect(x, y, w, 18)
        self.moving = moving
        self.dir    = 1
        self.speed  = random.randint(1, 3)
        self.left   = x - random.randint(30, 80)
        self.right  = x + w + random.randint(30, 80)
        self.color  = random.choice([GREEN, BLUE, ORANGE, PINK])
        self.has_coin   = has_coin
        self.has_enemy  = has_enemy
        self.coin_collected = False

    def update(self):
        if self.moving:
            self.rect.x += self.speed * self.dir
            if self.rect.right > self.right or self.rect.left < self.left:
                self.dir *= -1

    def draw(self, cam_y):
        r = self.rect.move(0, -cam_y)
        pygame.draw.rect(screen, self.color,  r, border_radius=6)
        pygame.draw.rect(screen, WHITE, r, 2, border_radius=6)
        if self.has_coin and not self.coin_collected:
            cx = r.centerx
            cy = r.top - 18
            pygame.draw.circle(screen, COIN_C, (cx, cy), 10)
            pygame.draw.circle(screen, YELLOW, (cx, cy), 7)
            draw_text("$", font_sm, BLACK, cx - 5, cy - 9)

# ── Enemy ────────────────────────────────────────────────
class Enemy:
    def __init__(self, platform):
        self.plat  = platform
        self.x     = float(platform.rect.centerx)
        self.y     = float(platform.rect.top - 28)
        self.dir   = 1
        self.speed = random.uniform(1.2, 2.5)
        self.w, self.h = 28, 28
        self.alive = True
        self.anim  = 0

    def update(self):
        self.anim += 0.15
        self.x += self.speed * self.dir
        pr = self.plat.rect
        if self.x < pr.left + 14 or self.x > pr.right - 14:
            self.dir *= -1
        self.y = float(self.plat.rect.top - 28)

    def rect(self):
        return pygame.Rect(int(self.x) - 14, int(self.y), self.w, self.h)

    def draw(self, cam_y):
        if not self.alive:
            return
        ox = int(self.x)
        oy = int(self.y) - cam_y
        pygame.draw.circle(screen, RED, (ox, oy + 14), 14)
        ex = 5 if self.dir > 0 else -5
        pygame.draw.circle(screen, WHITE, (ox + ex - 3, oy + 10), 4)
        pygame.draw.circle(screen, WHITE, (ox + ex + 3, oy + 10), 4)
        pygame.draw.circle(screen, BLACK, (ox + ex - 3, oy + 10), 2)
        pygame.draw.circle(screen, BLACK, (ox + ex + 3, oy + 10), 2)
        leg = int(math.sin(self.anim) * 6)
        pygame.draw.line(screen, RED, (ox - 5, oy + 26), (ox - 10, oy + 28 + leg), 3)
        pygame.draw.line(screen, RED, (ox + 5, oy + 26), (ox + 10, oy + 28 - leg), 3)

# ── Player ───────────────────────────────────────────────
class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x     = SW // 2
        self.y     = SH - 200.0
        self.vx    = 0.0
        self.vy    = 0.0
        self.on_ground = False
        self.alive  = True
        self.anim   = 0
        self.facing = 1
        self.invincible = 0
        self.w, self.h = 32, 44

    def rect(self):
        return pygame.Rect(int(self.x) - 16, int(self.y) - self.h, self.w, self.h)

    def draw(self, cam_y):
        ox = int(self.x)
        oy = int(self.y) - cam_y
        blink = self.invincible > 0 and (self.invincible // 4) % 2 == 0
        if blink:
            return
        self.anim += 0.18 if abs(self.vx) > 0.5 else 0.05
        pygame.draw.rect(screen, BLUE, (ox - 12, oy - 30, 24, 24), border_radius=5)
        pygame.draw.circle(screen, (255, 210, 170), (ox, oy - 40), 14)
        ex = 4 * self.facing
        pygame.draw.circle(screen, BLACK, (ox + ex, oy - 42), 3)
        pygame.draw.arc(screen, BLACK, (ox + ex - 5, oy - 38, 10, 6), 3.14, 0, 2)
        leg = int(math.sin(self.anim) * 7)
        pygame.draw.line(screen, DKGRAY, (ox - 5, oy - 7), (ox - 8, oy + leg), 5)
        pygame.draw.line(screen, DKGRAY, (ox + 5, oy - 7), (ox + 8, oy - leg), 5)
        pygame.draw.line(screen, (255, 210, 170), (ox - 12, oy - 25), (ox - 20, oy - 16), 4)
        pygame.draw.line(screen, (255, 210, 170), (ox + 12, oy - 25), (ox + 20, oy - 16), 4)

# ── Level generator ──────────────────────────────────────
def generate_platforms(start_y, count, level):
    plats = []
    y = start_y
    for i in range(count):
        w = random.randint(max(50, 120 - level * 6), max(80, 180 - level * 4))
        x = random.randint(10, SW - w - 10)
        moving   = random.random() < min(0.15 + level * 0.04, 0.5)
        has_coin = random.random() < 0.45
        has_enemy= random.random() < min(0.08 + level * 0.04, 0.4)
        plats.append(Platform(x, y, w, moving, has_coin, has_enemy))
        y -= random.randint(80, 130)
    return plats

# ── Particles ────────────────────────────────────────────
particles = []

def spawn_particles(x, y, color, n=10):
    for _ in range(n):
        particles.append([float(x), float(y),
                          random.uniform(-3, 3),
                          random.uniform(-5, -1),
                          random.randint(4, 10), color])

def update_draw_particles(cam_y):
    for p in particles[:]:
        p[0] += p[2]; p[1] += p[3]; p[3] += 0.2; p[4] -= 0.3
        if p[4] <= 0:
            particles.remove(p)
            continue
        pygame.draw.circle(screen, p[5], (int(p[0]), int(p[1]) - cam_y), int(p[4]))

# ── Main game function ───────────────────────────────────
def game():
    player   = Player()
    score    = 0
    lives    = 3
    level    = 1
    cam_y    = 0
    high_y   = player.y

    # ── Music ────────────────────────────────────────────
    try:
        pygame.mixer.music.load("/storage/emulated/0/Xender/audio/mustard.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        pass
    # ─────────────────────────────────────────────────────

    ground = Platform(0, SH - 60, SW)
    ground.color = DKGREEN
    platforms = [ground] + generate_platforms(SH - 160, 40, level)
    enemies   = [Enemy(p) for p in platforms if p.has_enemy]

    held = set()
    touch_map = {}

    JUMP_FORCE  = -17
    GRAVITY     = 0.7
    ACCEL       = 1.2
    FRICTION    = 0.75
    MAX_VX      = 6

    def respawn():
        player.reset()
        nonlocal cam_y
        cam_y = 0

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit", 0

            if event.type == pygame.FINGERDOWN:
                mx = int(event.x * SW); my = int(event.y * SH)
                b  = btn_hit((mx, my))
                if b: touch_map[event.finger_id] = b; held.add(b)

            if event.type == pygame.FINGERUP:
                b = touch_map.pop(event.finger_id, None)
                if b: held.discard(b)

            if event.type == pygame.FINGERMOTION:
                mx = int(event.x * SW); my = int(event.y * SH)
                old = touch_map.get(event.finger_id)
                new = btn_hit((mx, my))
                if old != new:
                    if old: held.discard(old)
                    if new: held.add(new)
                    touch_map[event.finger_id] = new

            if event.type == pygame.MOUSEBUTTONDOWN:
                b = btn_hit(event.pos)
                if b: held.add(b)
            if event.type == pygame.MOUSEBUTTONUP:
                held.clear()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT,  pygame.K_a): held.add("left")
                if event.key in (pygame.K_RIGHT, pygame.K_d): held.add("right")
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE): held.add("jump")
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT,  pygame.K_a): held.discard("left")
                if event.key in (pygame.K_RIGHT, pygame.K_d): held.discard("right")
                if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE): held.discard("jump")

        if "left"  in held: player.vx -= ACCEL; player.facing = -1
        if "right" in held: player.vx += ACCEL; player.facing =  1
        if "jump"  in held and player.on_ground:
            player.vy = JUMP_FORCE
            player.on_ground = False
            spawn_particles(player.x, player.y, GRAY, 6)

        player.vx = max(-MAX_VX, min(MAX_VX, player.vx))
        if "left" not in held and "right" not in held:
            player.vx *= FRICTION
        player.vy += GRAVITY
        player.x  += player.vx
        player.y  += player.vy

        if player.x < 0:  player.x = SW
        if player.x > SW: player.x = 0

        player.on_ground = False
        pr = player.rect()
        for plat in platforms:
            r = plat.rect
            if (pr.bottom >= r.top and pr.bottom <= r.top + 20 and
                pr.right > r.left and pr.left < r.right and player.vy >= 0):
                player.y = float(r.top)
                player.vy = 0
                player.on_ground = True
                if plat.has_coin and not plat.coin_collected:
                    if r.left < pr.centerx < r.right:
                        plat.coin_collected = True
                        score += 10
                        spawn_particles(plat.rect.centerx, plat.rect.top - 18, COIN_C, 8)

        target_cam = int(player.y) - SH // 2
        cam_y += (target_cam - cam_y) * 0.1
        if player.y < high_y:
            high_y = player.y
            score  += 1

        top_plat_y = min(p.rect.y for p in platforms)
        if top_plat_y - cam_y > -200:
            new = generate_platforms(top_plat_y - 100, 15, level)
            platforms.extend(new)
            enemies.extend([Enemy(p) for p in new if p.has_enemy])

        platforms = [p for p in platforms if p.rect.y - cam_y < SH + 200]
        enemies   = [e for e in enemies if e.plat in platforms and e.alive]

        for p in platforms: p.update()
        for e in enemies:   e.update()

        if player.invincible == 0:
            for e in enemies:
                if not e.alive: continue
                er = e.rect(); pr = player.rect()
                if pr.colliderect(er):
                    if player.vy > 0 and pr.bottom < er.centery + 10:
                        e.alive = False
                        player.vy = -10
                        score += 25
                        spawn_particles(e.x, e.y, RED, 12)
                    else:
                        lives -= 1
                        player.invincible = 90
                        spawn_particles(player.x, player.y, ORANGE, 15)
                        if lives <= 0:
                            pygame.mixer.music.stop()
                            return "dead", score

        if player.invincible > 0:
            player.invincible -= 1

        if player.y - cam_y > SH + 50:
            lives -= 1
            spawn_particles(player.x, SH - 100, RED, 20)
            if lives <= 0:
                pygame.mixer.music.stop()
                return "dead", score
            respawn()

        if score > level * 300:
            level += 1

        draw_bg()
        for p in platforms: p.draw(int(cam_y))
        update_draw_particles(int(cam_y))
        for e in enemies:   e.draw(int(cam_y))
        player.draw(int(cam_y))

        draw_text(f"Score: {score}", font_sm, WHITE, 10, 10)
        draw_text(f"Lv {level}", font_sm, YELLOW, SW//2 - 30, 10)
        hearts = "♥ " * lives + "♡ " * (3 - lives)
        draw_text(hearts, font_sm, RED, SW - 130, 10)
        draw_buttons(held)
        pygame.display.update()

    return "quit", score

# ── Screens ──────────────────────────────────────────────
def title_screen():
    t = 0
    while True:
        clock.tick(FPS)
        draw_bg(); t += 1
        bob = int(math.sin(t * 0.05) * 6)
        draw_text("SKY",    font_big, YELLOW, SW//2, 160 + bob, center=True)
        draw_text("JUMPER", font_big, PINK,   SW//2, 220 + bob, center=True)
        draw_text("Collect coins  ●  Stomp enemies", font_sm, WHITE,  SW//2, 320, center=True)
        draw_text("Don't fall off screen!",          font_sm, GRAY,   SW//2, 355, center=True)
        pulse = int(abs(math.sin(t * 0.06)) * 60) + 160
        draw_text("TAP TO PLAY", font_med, (pulse, pulse, 255), SW//2, 430, center=True)
        draw_text("◀  Move   ▶  Move   ▲  Jump", font_sm, WHITE, SW//2, 540, center=True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                return True

def game_over_screen(score):
    t = 0
    while True:
        clock.tick(FPS)
        draw_bg(); t += 1
        draw_text("GAME OVER",    font_big, RED,    SW//2, 200, center=True)
        draw_text(f"Score: {score}", font_med, YELLOW, SW//2, 290, center=True)
        pulse = int(abs(math.sin(t * 0.06)) * 60) + 160
        draw_text("TAP TO RETRY", font_med, (pulse, 255, pulse), SW//2, 380, center=True)
        draw_text("or press Q to quit", font_sm, GRAY, SW//2, 430, center=True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                return event.key != pygame.K_q
            if event.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
                return True

# ── Entry point ──────────────────────────────────────────
if not title_screen():
    pygame.quit()
    exit()

while True:
    result, score = game()
    if result == "quit": break
    if not game_over_screen(score): break

pygame.quit()