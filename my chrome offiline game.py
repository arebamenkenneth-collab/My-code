import pygame
import random
import math
import sys

pygame.init()

# ── Screen ──────────────────────────────────────────────────────────────────
W, H = 800, 400
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dino Rush – CodeWithKenneth")
clock = pygame.time.Clock()
FPS = 60

# ── Palette ─────────────────────────────────────────────────────────────────
SKY_DAY   = (200, 230, 255)
SKY_DUSK  = (255, 180, 120)
SKY_NIGHT = (15,  20,  50)
GROUND_TOP    = (180, 140, 90)
GROUND_SHADOW = (140, 100, 60)
SAND_COLOR    = (210, 175, 110)
DINO_COLOR    = (60,  80,  60)
DINO_DARK     = (30,  50,  30)
CACTUS_COLOR  = (50,  110, 50)
CACTUS_DARK   = (30,  75,  30)
CLOUD_COLOR   = (255, 255, 255)
STAR_COLOR    = (255, 255, 200)
DUST_COLOR    = (200, 170, 100)
WHITE         = (255, 255, 255)
BLACK         = (0,   0,   0)
RED           = (220, 60,  60)
GOLD          = (255, 200, 50)

# ── Fonts ────────────────────────────────────────────────────────────────────
try:
    font_big   = pygame.font.SysFont("monospace", 48, bold=True)
    font_mid   = pygame.font.SysFont("monospace", 28, bold=True)
    font_small = pygame.font.SysFont("monospace", 20)
except Exception:
    font_big   = pygame.font.Font(None, 48)
    font_mid   = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 20)

GROUND_Y = 300

# ══════════════════════════════════════════════════════════════════════════════
# DRAWING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_sky(surf, phase):
    if phase < 0.5:
        top = lerp_color(SKY_DAY, SKY_DUSK, phase * 2)
    else:
        top = lerp_color(SKY_DUSK, SKY_NIGHT, (phase - 0.5) * 2)
    surf.fill(top)

def draw_stars(surf, stars, alpha):
    if alpha <= 0:
        return
    for (sx, sy, sr) in stars:
        col = (min(255, STAR_COLOR[0]), min(255, STAR_COLOR[1]), min(255, STAR_COLOR[2]))
        pygame.draw.circle(surf, col, (sx, sy), sr)

def draw_moon(surf, alpha, x=680, y=60):
    if alpha <= 0:
        return
    r = 28
    pygame.draw.circle(surf, (230, 230, 200), (x, y), r)
    pygame.draw.circle(surf, lerp_color(SKY_NIGHT, (230, 230, 200), 0.3), (x - 8, y - 5), r - 6)

def draw_ground(surf, scroll):
    pygame.draw.rect(surf, GROUND_TOP,    (0, GROUND_Y,      W, 18))
    pygame.draw.rect(surf, GROUND_SHADOW, (0, GROUND_Y + 18, W, 8))
    pygame.draw.rect(surf, SAND_COLOR, (0, GROUND_Y + 26, W, H - GROUND_Y - 26))
    ox = int(scroll) % 40
    for x in range(-40, W + 40, 40):
        rx = (x - ox) % W
        pygame.draw.circle(surf, GROUND_SHADOW, (rx, GROUND_Y + 4), 2)
    ox2 = int(scroll * 0.6) % 60
    for x in range(-60, W + 60, 60):
        rx = (x - ox2) % W
        pygame.draw.circle(surf, GROUND_SHADOW, (rx, GROUND_Y + 10), 1)

# ══════════════════════════════════════════════════════════════════════════════
# DINO
# ══════════════════════════════════════════════════════════════════════════════

def draw_dino(surf, x, y, frame, ducking=False):
    s = 2
    c  = DINO_COLOR
    cd = DINO_DARK

    if ducking:
        parts = [
            (0, 4, 32, 10, c),
            (28, -2, 12, 8, c),
            (36, 0, 6, 4, c),
        ]
        for (px, py, pw, ph, col) in parts:
            pygame.draw.rect(surf, col, (x + px*s, y + py*s, pw*s, ph*s))
            pygame.draw.rect(surf, cd,  (x + px*s + s, y + py*s + s, pw*s - s, ph*s - s), 1)
        leg_ox = [0, 6] if frame % 2 == 0 else [4, 2]
        for lx in leg_ox:
            pygame.draw.rect(surf, c,  (x + (8 + lx)*s, y + 12*s, 4*s, 6*s))
        return

    pygame.draw.rect(surf, c,  (x,          y + 6*s,  22*s, 14*s))
    pygame.draw.rect(surf, cd, (x + s,      y + 7*s,  20*s, 12*s), 1)
    pygame.draw.rect(surf, c,  (x - 2*s,    y + 10*s, 6*s,  6*s))
    pygame.draw.rect(surf, c,  (x + 16*s,   y,        8*s,  10*s))
    pygame.draw.rect(surf, c,  (x + 20*s,   y - 6*s,  14*s, 12*s))
    pygame.draw.rect(surf, cd, (x + 21*s,   y - 5*s,  12*s, 10*s), 1)
    pygame.draw.rect(surf, BLACK, (x + 28*s, y - 4*s, 3*s, 3*s))
    pygame.draw.rect(surf, WHITE, (x + 29*s, y - 4*s, s,   s))
    pygame.draw.rect(surf, cd, (x + 28*s,   y + 4*s,  8*s,  3*s))
    pygame.draw.rect(surf, c,  (x + 14*s,   y + 12*s, 6*s,  4*s))

    if frame % 2 == 0:
        pygame.draw.rect(surf, c, (x + 6*s,  y + 18*s, 5*s, 8*s))
        pygame.draw.rect(surf, c, (x + 14*s, y + 18*s, 5*s, 6*s))
    else:
        pygame.draw.rect(surf, c, (x + 6*s,  y + 18*s, 5*s, 6*s))
        pygame.draw.rect(surf, c, (x + 14*s, y + 18*s, 5*s, 8*s))

DINO_W = 70
DINO_H = 50

# ══════════════════════════════════════════════════════════════════════════════
# CACTUS
# ══════════════════════════════════════════════════════════════════════════════

def draw_cactus(surf, x, y, kind):
    c  = CACTUS_COLOR
    cd = CACTUS_DARK
    s  = 3
    if kind == 0:
        pygame.draw.rect(surf, c,  (x + 4*s, y,       4*s, 20*s))
        pygame.draw.rect(surf, c,  (x,       y + 6*s, 4*s, 6*s))
        pygame.draw.rect(surf, c,  (x + 8*s, y + 8*s, 4*s, 5*s))
        pygame.draw.rect(surf, cd, (x + 5*s, y + s,   2*s, 18*s))
    elif kind == 1:
        for ox in (0, 14*s):
            pygame.draw.rect(surf, c,  (x + ox + 3*s, y + 5*s,  4*s, 15*s))
            pygame.draw.rect(surf, c,  (x + ox,       y + 8*s,  3*s, 5*s))
            pygame.draw.rect(surf, c,  (x + ox + 7*s, y + 9*s,  3*s, 4*s))
            pygame.draw.rect(surf, cd, (x + ox + 4*s, y + 6*s,  2*s, 13*s))
    else:
        for i, (ox, oh) in enumerate([(0, 0), (10*s, -4*s), (20*s, -2*s)]):
            pygame.draw.rect(surf, c,  (x + ox + 3*s, y + oh + 4*s, 4*s, 16*s))
            pygame.draw.rect(surf, c,  (x + ox,       y + oh + 7*s, 3*s, 5*s))
            pygame.draw.rect(surf, c,  (x + ox + 7*s, y + oh + 8*s, 3*s, 4*s))
            pygame.draw.rect(surf, cd, (x + ox + 4*s, y + oh + 5*s, 2*s, 14*s))

CACTUS_WIDTHS = [36, 66, 96]

# ══════════════════════════════════════════════════════════════════════════════
# CLOUD
# ══════════════════════════════════════════════════════════════════════════════

def draw_cloud(surf, x, y):
    c = CLOUD_COLOR
    pygame.draw.ellipse(surf, c, (x,      y + 10, 50, 20))
    pygame.draw.ellipse(surf, c, (x + 10, y,      30, 24))
    pygame.draw.ellipse(surf, c, (x + 30, y + 5,  30, 20))

# ══════════════════════════════════════════════════════════════════════════════
# DUST
# ══════════════════════════════════════════════════════════════════════════════

class Dust:
    def __init__(self, x, y):
        self.x = x + random.randint(-5, 5)
        self.y = y + random.randint(-3, 3)
        self.vx = random.uniform(-1.5, -0.5)
        self.vy = random.uniform(-1.5, 0.5)
        self.life = random.randint(10, 20)
        self.max_life = self.life
        self.r = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surf):
        alpha = self.life / self.max_life
        col = lerp_color(GROUND_TOP, SAND_COLOR, alpha)
        r = max(1, int(self.r * alpha))
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), r)

# ══════════════════════════════════════════════════════════════════════════════
# OBSTACLE
# ══════════════════════════════════════════════════════════════════════════════

class Obstacle:
    def __init__(self, speed):
        self.kind = random.randint(0, 2)
        self.w = CACTUS_WIDTHS[self.kind]
        self.h = 60
        self.x = W + 20
        self.y = GROUND_Y - self.h + 12
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self, surf):
        draw_cactus(surf, self.x, self.y, self.kind)

    def rect(self):
        return pygame.Rect(self.x + 6, self.y + 4, self.w - 12, self.h - 4)

    def off_screen(self):
        return self.x + self.w < 0

# ══════════════════════════════════════════════════════════════════════════════
# CLOUD ENTITY
# ══════════════════════════════════════════════════════════════════════════════

class Cloud:
    def __init__(self):
        self.x = W + random.randint(0, 100)
        self.y = random.randint(40, 160)
        self.speed = random.uniform(0.8, 1.5)

    def update(self):
        self.x -= self.speed

    def draw(self, surf):
        draw_cloud(surf, int(self.x), int(self.y))

    def off_screen(self):
        return self.x < -80

# ══════════════════════════════════════════════════════════════════════════════
# GAME
# ══════════════════════════════════════════════════════════════════════════════

class Game:
    def __init__(self):
        self.reset()
        self.hi_score = 0
        self.stars = [(random.randint(0, W), random.randint(20, GROUND_Y - 40), random.randint(1, 2))
                      for _ in range(60)]

    def reset(self):
        self.score      = 0
        self.speed      = 6.0
        self.scroll     = 0.0
        self.alive      = True
        self.started    = False
        self.phase      = 0.0
        self.phase_dir  = 1

        self.dx     = 80
        self.dy     = float(GROUND_Y - DINO_H)
        self.vy     = 0.0
        self.on_gnd = True
        self.ducking= False
        self.frame  = 0
        self.frame_t= 0

        self.obstacles  = []
        self.clouds     = [Cloud() for _ in range(3)]
        self.dusts      = []
        self.next_obs   = random.randint(60, 120)
        self.flash      = 0

    def jump(self):
        if self.on_gnd:
            self.vy = -16
            self.on_gnd = False
            for _ in range(8):
                self.dusts.append(Dust(self.dx + 30, int(self.dy) + DINO_H))

    def duck(self, holding):
        self.ducking = holding and self.on_gnd

    def update(self):
        if not self.started or not self.alive:
            return

        self.score += 1
        self.speed = 6.0 + self.score * 0.003
        self.scroll += self.speed

        self.phase += 0.0003 * self.phase_dir
        if self.phase >= 1.0:
            self.phase = 1.0; self.phase_dir = -1
        elif self.phase <= 0.0:
            self.phase = 0.0; self.phase_dir = 1

        self.vy += 0.85
        self.dy += self.vy
        land_y = float(GROUND_Y - DINO_H)
        if self.dy >= land_y:
            self.dy = land_y
            self.vy = 0
            self.on_gnd = True

        if self.on_gnd and not self.ducking:
            self.frame_t += 1
            if self.frame_t > max(4, int(10 - self.speed * 0.5)):
                self.frame_t = 0
                self.frame ^= 1
            if self.frame_t == 0:
                self.dusts.append(Dust(self.dx + 10, int(self.dy) + DINO_H - 2))

        self.next_obs -= 1
        if self.next_obs <= 0:
            self.obstacles.append(Obstacle(self.speed))
            gap = random.randint(int(70 - self.speed * 3), int(130 - self.speed * 2))
            self.next_obs = max(45, gap)

        for obs in self.obstacles:
            obs.speed = self.speed
            obs.update()

        self.obstacles = [o for o in self.obstacles if not o.off_screen()]

        for c in self.clouds:
            c.update()
        self.clouds = [c for c in self.clouds if not c.off_screen()]
        if random.random() < 0.005:
            self.clouds.append(Cloud())

        for d in self.dusts:
            d.update()
        self.dusts = [d for d in self.dusts if d.life > 0]

        dino_rect = pygame.Rect(self.dx + 8, int(self.dy) + 6, DINO_W - 20, DINO_H - 10)
        for obs in self.obstacles:
            if dino_rect.colliderect(obs.rect()):
                self.alive = False
                self.hi_score = max(self.hi_score, self.score // 10)
                self.flash = 8
                return

    def draw(self, surf):
        draw_sky(surf, self.phase)

        star_alpha = max(0.0, (self.phase - 0.5) * 2)
        draw_stars(surf, self.stars, star_alpha)
        draw_moon(surf, star_alpha)

        for c in self.clouds:
            c.draw(surf)

        draw_ground(surf, self.scroll)

        for d in self.dusts:
            d.draw(surf)

        for obs in self.obstacles:
            obs.draw(surf)

        draw_dino(surf, self.dx, int(self.dy), self.frame, self.ducking)

        if self.flash > 0:
            fsurf = pygame.Surface((W, H), pygame.SRCALPHA)
            fsurf.fill((255, 60, 60, int(120 * self.flash / 8)))
            surf.blit(fsurf, (0, 0))
            self.flash -= 1

        score_str = f"SCORE  {self.score // 10:05d}"
        hi_str    = f"HI  {self.hi_score:05d}"
        surf.blit(font_small.render(hi_str,    True, BLACK), (W - 180, 14))
        surf.blit(font_small.render(score_str, True, BLACK), (W - 180, 36))
        spd_txt = font_small.render(f"SPD x{self.speed:.1f}", True, (80, 80, 80))
        surf.blit(spd_txt, (14, 14))

        if not self.started:
            self._draw_start(surf)
        elif not self.alive:
            self._draw_gameover(surf)

    def _draw_start(self, surf):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surf.blit(overlay, (0, 0))
        title = font_big.render("DINO RUSH", True, WHITE)
        surf.blit(title, (W // 2 - title.get_width() // 2, 120))
        sub = font_mid.render("TAP / SPACE to start", True, GOLD)
        surf.blit(sub, (W // 2 - sub.get_width() // 2, 185))
        brand = font_small.render("CodeWithKenneth", True, (180, 220, 255))
        surf.blit(brand, (W // 2 - brand.get_width() // 2, 340))

    def _draw_gameover(self, surf):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surf.blit(overlay, (0, 0))
        go = font_big.render("GAME OVER", True, RED)
        surf.blit(go, (W // 2 - go.get_width() // 2, 110))
        sc = font_mid.render(f"Score: {self.score // 10}", True, WHITE)
        surf.blit(sc, (W // 2 - sc.get_width() // 2, 175))
        hi = font_mid.render(f"Best:  {self.hi_score}", True, GOLD)
        surf.blit(hi, (W // 2 - hi.get_width() // 2, 215))
        restart = font_small.render("TAP / SPACE / R  to restart", True, (200, 200, 200))
        surf.blit(restart, (W // 2 - restart.get_width() // 2, 275))

# ══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    game = Game()
    duck_held = False

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if not game.started:
                        game.started = True
                    elif not game.alive:
                        game.reset(); game.started = True
                    else:
                        game.jump()
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    duck_held = True
                if event.key == pygame.K_r and not game.alive:
                    game.reset(); game.started = True

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    duck_held = False

            if event.type == pygame.FINGERDOWN:
                fx = event.x * W
                fy = event.y * H
                if not game.started:
                    game.started = True
                elif not game.alive:
                    game.reset(); game.started = True
                elif fy > H * 0.6:
                    duck_held = True
                else:
                    game.jump()

            if event.type == pygame.FINGERUP:
                duck_held = False

        game.duck(duck_held)
        game.update()
        game.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()