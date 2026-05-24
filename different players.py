import pygame
import random
import math
import sys

pygame.init()

# ── Screen ───────────────────────────────────────────────────────────────────
info = pygame.display.Info()
WIDTH  = info.current_w
HEIGHT = info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Duel")
clock = pygame.time.Clock()
FPS = 60
HALF = WIDTH // 2

# ── Colours ──────────────────────────────────────────────────────────────────
WHITE  = (255, 255, 255)
RED    = (255,  50,  50)
GREEN  = (50,  255, 100)
YELLOW = (255, 220,  50)
CYAN   = (50,  220, 255)
ORANGE = (255, 140,  30)
GREY   = (180, 180, 180)
DARK   = (10,   10,  30)
DKGREY = (60,   60,  60)

# ── Fonts ────────────────────────────────────────────────────────────────────
FS = max(14, WIDTH // 50)
font_sm  = pygame.font.SysFont("monospace", FS,      bold=True)
font_med = pygame.font.SysFont("monospace", FS + 6,  bold=True)
font_big = pygame.font.SysFont("monospace", FS + 20, bold=True)

# ── Stars ────────────────────────────────────────────────────────────────────
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT),
          random.uniform(0.5, 2.5)) for _ in range(140)]

def update_stars():
    global stars
    out = []
    for x, y, s in stars:
        y += s * 0.5
        if y > HEIGHT:
            y = 0; x = random.randint(0, WIDTH)
        out.append((x, y, s))
    stars = out

def draw_stars(surf):
    for x, y, s in stars:
        r = max(1, int(s * 0.6))
        b = int(150 + s * 40)
        pygame.draw.circle(surf, (b, b, b), (int(x), int(y)), r)

# ── Pixel ship ───────────────────────────────────────────────────────────────
SHIP = ["  XXX  ", " XXXXX ", "XXXXXXX", " X X X ", "X     X"]
P1C  = [None, CYAN,   (30,100,200), WHITE, YELLOW, ORANGE]
P2C  = [None, ORANGE, RED,          WHITE, YELLOW, CYAN  ]

def draw_ship(surf, cx, cy, cmap, scale=3):
    pw = len(SHIP[0]) * scale
    ph = len(SHIP)    * scale
    ox, oy = cx - pw//2, cy - ph//2
    for ri, row in enumerate(SHIP):
        for ci, ch in enumerate(row):
            if ch == 'X':
                idx = (ri + ci) % (len(cmap)-1) + 1
                pygame.draw.rect(surf, cmap[idx],
                                 (ox+ci*scale, oy+ri*scale, scale, scale))

# ── Bullet ───────────────────────────────────────────────────────────────────
class Bullet:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.r = max(4, WIDTH // 120)

    def update(self):   self.y -= 12
    def dead(self):     return self.y < -10
    def draw(self, surf, ox=0):
        pygame.draw.circle(surf, self.color, (int(self.x)+ox, int(self.y)), self.r)

# ── Particle ──────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        a = random.uniform(0, math.tau); sp = random.uniform(1,5)
        self.vx, self.vy = math.cos(a)*sp, math.sin(a)*sp
        self.life = random.randint(20,45)
        self.color = color
        self.r = random.randint(2,5)

    def update(self):
        self.x += self.vx; self.y += self.vy
        self.vy += 0.1;    self.life -= 1

    def draw(self, surf, ox=0):
        if self.life > 0:
            pygame.draw.circle(surf, self.color,
                               (int(self.x)+ox, int(self.y)), self.r)

# ── Enemy ─────────────────────────────────────────────────────────────────────
class Enemy:
    def __init__(self, side):
        self.side = side
        self.x  = random.randint(20, HALF-20)
        self.y  = random.randint(-80, -20)
        self.dy = random.uniform(1.5, 3.2)
        self.r  = random.randint(12, 24)
        self.color = random.choice([RED, ORANGE, (180,60,180), GREY])
        self.hp = 1 if self.r < 18 else 2
        self.alive = True
        self.pts = [(math.cos(i*math.tau/8)*self.r*random.uniform(.7,1.3),
                     math.sin(i*math.tau/8)*self.r*random.uniform(.7,1.3))
                    for i in range(8)]

    def update(self): self.y += self.dy
    def off(self):    return self.y > HEIGHT+30

    def draw(self, surf):
        ox = 0 if self.side==1 else HALF
        pts = [(int(self.x+ox+dx), int(self.y+dy)) for dx,dy in self.pts]
        pygame.draw.polygon(surf, self.color, pts)
        pygame.draw.polygon(surf, WHITE, pts, 1)

# ── Touch Button ──────────────────────────────────────────────────────────────
class Button:
    def __init__(self, x, y, w, h, label, color):
        self.rect  = pygame.Rect(x, y, w, h)
        self.label = label
        self.color = color
        self.held  = False

    def draw(self, surf):
        alpha = 180 if self.held else 110
        s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        surf.blit(s, self.rect.topleft)
        pygame.draw.rect(surf, (*self.color, 230), self.rect, 2, border_radius=8)
        lbl = font_sm.render(self.label, True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def touch(self, pos): return self.rect.collidepoint(pos)

# ── Player ────────────────────────────────────────────────────────────────────
class Player:
    def __init__(self, side):
        self.side  = side
        self.x     = HALF // 2
        self.y     = HEIGHT - int(HEIGHT * 0.18)
        self.speed = max(4, WIDTH // 180)
        self.max_hp= 10
        self.hp    = self.max_hp
        self.bullets   = []
        self.particles = []
        self.shoot_cd  = 0
        self.invinc    = 0
        self.alive     = True
        self.cmap      = P1C if side==1 else P2C
        self.bcol      = CYAN if side==1 else ORANGE
        self.move_left = self.move_right = self.move_up = self.move_down = False
        self.firing    = False

    def update(self):
        if self.move_left:  self.x -= self.speed
        if self.move_right: self.x += self.speed
        if self.move_up:    self.y -= self.speed
        if self.move_down:  self.y += self.speed
        self.x = max(20, min(HALF-20, self.x))
        self.y = max(20, min(HEIGHT-20, self.y))
        if self.shoot_cd > 0: self.shoot_cd -= 1
        if self.invinc  > 0: self.invinc  -= 1
        if self.firing and self.shoot_cd == 0:
            self.bullets.append(Bullet(self.x, self.y-15, self.bcol))
            self.shoot_cd = 18
        for b in self.bullets: b.update()
        self.bullets = [b for b in self.bullets if not b.dead()]
        for p in self.particles: p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def hit(self):
        if self.invinc > 0: return
        self.hp -= 1
        self.invinc = 40
        for _ in range(20):
            self.particles.append(Particle(self.x, self.y, self.bcol))
        if self.hp <= 0:
            self.alive = False
            for _ in range(60):
                self.particles.append(Particle(self.x, self.y, self.bcol))

    def draw(self, surf):
        ox = 0 if self.side==1 else HALF
        for p in self.particles: p.draw(surf, ox)
        for b in self.bullets:   b.draw(surf, ox)
        if self.alive and (self.invinc==0 or self.invinc%6<3):
            draw_ship(surf, self.x+ox, self.y, self.cmap,
                      scale=max(2, WIDTH//200))

# ── Build touch controls ──────────────────────────────────────────────────────
def make_controls():
    BW  = max(60, WIDTH // 14)
    BH  = max(55, HEIGHT // 10)
    PAD = 8
    BY  = HEIGHT - BH - PAD

    p1_left  = Button(PAD,                  BY,        BW, BH, "◀", CYAN)
    p1_right = Button(PAD+BW+PAD,           BY,        BW, BH, "▶", CYAN)
    p1_up    = Button(PAD+BW//2,            BY-BH-PAD, BW, BH, "▲", CYAN)
    p1_down  = Button(PAD+BW//2,            BY,        BW, BH, "▼", CYAN)
    p1_fire  = Button(HALF - BW - PAD,      BY,        BW, BH, "FIRE", RED)

    ox = HALF
    p2_left  = Button(ox+PAD,               BY,        BW, BH, "◀", ORANGE)
    p2_right = Button(ox+PAD+BW+PAD,        BY,        BW, BH, "▶", ORANGE)
    p2_up    = Button(ox+PAD+BW//2,         BY-BH-PAD, BW, BH, "▲", ORANGE)
    p2_down  = Button(ox+PAD+BW//2,         BY,        BW, BH, "▼", ORANGE)
    p2_fire  = Button(ox+HALF-BW-PAD,       BY,        BW, BH, "FIRE", RED)

    p1_btns = {"left":p1_left,"right":p1_right,"up":p1_up,"down":p1_down,"fire":p1_fire}
    p2_btns = {"left":p2_left,"right":p2_right,"up":p2_up,"down":p2_down,"fire":p2_fire}
    return p1_btns, p2_btns

def draw_controls(surf, btns):
    for b in btns.values(): b.draw(surf)

def process_touches(touches, p1_btns, p2_btns, p1, p2):
    for pl in (p1, p2):
        pl.move_left=pl.move_right=pl.move_up=pl.move_down=pl.firing=False
    for btn in list(p1_btns.values())+list(p2_btns.values()):
        btn.held = False
    for pos in touches:
        for name, btn in p1_btns.items():
            if btn.touch(pos):
                btn.held = True
                if name=="left":  p1.move_left  = True
                if name=="right": p1.move_right = True
                if name=="up":    p1.move_up    = True
                if name=="down":  p1.move_down  = True
                if name=="fire":  p1.firing     = True
        for name, btn in p2_btns.items():
            if btn.touch(pos):
                btn.held = True
                if name=="left":  p2.move_left  = True
                if name=="right": p2.move_right = True
                if name=="up":    p2.move_up    = True
                if name=="down":  p2.move_down  = True
                if name=="fire":  p2.firing     = True

# ── HUD ───────────────────────────────────────────────────────────────────────
def draw_hud(surf, player, score):
    ox = 8 if player.side==1 else HALF+8
    bw, bh = 100, 12
    filled = int(bw * player.hp / player.max_hp)
    bc = GREEN if player.hp>3 else (YELLOW if player.hp>1 else RED)
    pygame.draw.rect(surf, DKGREY, (ox+52, 8, bw, bh))
    if filled>0:
        pygame.draw.rect(surf, bc, (ox+52, 8, filled, bh))
    pygame.draw.rect(surf, WHITE,  (ox+52, 8, bw, bh), 1)
    surf.blit(font_sm.render(f"HP:{player.hp}", True, WHITE), (ox, 6))
    surf.blit(font_sm.render(f"Score:{score}",  True,
              CYAN if player.side==1 else ORANGE), (ox, 6+FS+2))

# ── Main ──────────────────────────────────────────────────────────────────────
active_fingers = {}

def main_touch():
    MENU, PLAY, OVER = "menu","play","over"
    state = MENU
    p1=p2=None; e1=[]; e2=[]
    spawn_t=0; winner=0; sc1=sc2=0
    p1_btns, p2_btns = make_controls()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

            if event.type == pygame.FINGERDOWN:
                fx = int(event.x * WIDTH); fy = int(event.y * HEIGHT)
                active_fingers[event.finger_id] = (fx, fy)
                if state == MENU:
                    state=PLAY; p1=Player(1); p2=Player(2)
                    e1=[]; e2=[]; spawn_t=0; sc1=sc2=0
                elif state == OVER:
                    state = MENU

            elif event.type == pygame.FINGERMOTION:
                active_fingers[event.finger_id] = (int(event.x*WIDTH), int(event.y*HEIGHT))

            elif event.type == pygame.FINGERUP:
                active_fingers.pop(event.finger_id, None)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                active_fingers[-1] = event.pos
                if state == MENU:
                    state=PLAY; p1=Player(1); p2=Player(2)
                    e1=[]; e2=[]; spawn_t=0; sc1=sc2=0
                elif state == OVER:
                    state = MENU

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    active_fingers[-1] = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                active_fingers.pop(-1, None)

        update_stars()
        touches = list(active_fingers.values())

        if state == PLAY:
            process_touches(touches, p1_btns, p2_btns, p1, p2)
            p1.update(); p2.update()
            spawn_t += 1
            if spawn_t >= 55:
                spawn_t=0; e1.append(Enemy(1)); e2.append(Enemy(2))
            for e in e1: e.update()
            for e in e2: e.update()
            e1 = [e for e in e1 if not e.off() and e.alive]
            e2 = [e for e in e2 if not e.off() and e.alive]

            for b in list(p1.bullets):
                for e in list(e1):
                    if math.hypot(b.x-e.x, b.y-e.y) < e.r+b.r:
                        if b in p1.bullets: p1.bullets.remove(b)
                        e.hp-=1
                        if e.hp<=0: e.alive=False; sc1+=1
                        break
            for b in list(p2.bullets):
                for e in list(e2):
                    if math.hypot(b.x-e.x, b.y-e.y) < e.r+b.r:
                        if b in p2.bullets: p2.bullets.remove(b)
                        e.hp-=1
                        if e.hp<=0: e.alive=False; sc2+=1
                        break

            for e in e1:
                if math.hypot(p1.x-e.x, p1.y-e.y) < e.r+14: p1.hit(); e.alive=False
            for e in e2:
                if math.hypot(p2.x-e.x, p2.y-e.y) < e.r+14: p2.hit(); e.alive=False

            if not p1.alive and not p2.alive: winner=0; state=OVER
            elif not p1.alive: winner=2; state=OVER
            elif not p2.alive: winner=1; state=OVER

        # ── Draw ─────────────────────────────────────────────────────────
        screen.fill(DARK)
        draw_stars(screen)

        if state in (PLAY, OVER):
            for e in e1: e.draw(screen)
            for e in e2: e.draw(screen)
            if p1: p1.draw(screen)
            if p2: p2.draw(screen)
            pygame.draw.line(screen, WHITE, (HALF,0), (HALF,HEIGHT), 2)
            draw_hud(screen, p1, sc1)
            draw_hud(screen, p2, sc2)
            draw_controls(screen, p1_btns)
            draw_controls(screen, p2_btns)

        if state == MENU:
            screen.fill(DARK)
            draw_stars(screen)
            t1 = font_big.render("SPACE DUEL", True, CYAN)
            t2 = font_med.render("2 Players | Split Screen", True, GREY)
            t3 = font_med.render("Tap anywhere to Start", True, YELLOW)
            screen.blit(t1, t1.get_rect(center=(WIDTH//2, HEIGHT//3)))
            screen.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//3+60)))
            screen.blit(t3, t3.get_rect(center=(WIDTH//2, HEIGHT//3+110)))
            draw_controls(screen, p1_btns)
            draw_controls(screen, p2_btns)

        elif state == OVER:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((0,0,0,150)); screen.blit(ov, (0,0))
            if winner==0:
                t = font_big.render("DRAW!", True, YELLOW)
            else:
                col = CYAN if winner==1 else ORANGE
                t = font_big.render(f"PLAYER {winner} WINS!", True, col)
            t2 = font_med.render(f"P1: {sc1} pts    P2: {sc2} pts", True, WHITE)
            t3 = font_sm.render("Tap to return to menu", True, GREY)
            screen.blit(t,  t.get_rect(center=(WIDTH//2, HEIGHT//2-60)))
            screen.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//2)))
            screen.blit(t3, t3.get_rect(center=(WIDTH//2, HEIGHT//2+50)))

        pygame.display.flip()

main_touch()