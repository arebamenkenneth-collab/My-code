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
clock  = pygame.time.Clock()
FPS    = 60
HALF   = WIDTH // 2

# ── Colours ──────────────────────────────────────────────────────────────────
WHITE  = (255, 255, 255)
RED    = (255,  50,  50)
GREEN  = (50,  255, 100)
YELLOW = (255, 220,  50)
CYAN   = (50,  220, 255)
ORANGE = (255, 140,  30)
GREY   = (180, 180, 180)
DARK   = (10,   10,  30)
DKGREY = (40,   40,  60)

# ── Fonts ────────────────────────────────────────────────────────────────────
FS       = max(14, WIDTH // 45)
font_sm  = pygame.font.SysFont("monospace", FS,      bold=True)
font_med = pygame.font.SysFont("monospace", FS+6,    bold=True)
font_big = pygame.font.SysFont("monospace", FS+22,   bold=True)

# ── Stars ────────────────────────────────────────────────────────────────────
stars = [(random.randint(0,WIDTH), random.randint(0,HEIGHT),
          random.uniform(0.5,2.5)) for _ in range(150)]

def update_stars():
    global stars
    out = []
    for x,y,s in stars:
        y += s*0.4
        if y > HEIGHT: y=0; x=random.randint(0,WIDTH)
        out.append((x,y,s))
    stars = out

def draw_stars(surf):
    for x,y,s in stars:
        r = max(1,int(s*0.6))
        b = int(140+s*45)
        pygame.draw.circle(surf,(b,b,b),(int(x),int(y)),r)

# ── Pixel ship ───────────────────────────────────────────────────────────────
SHIP = ["  XXX  "," XXXXX ","XXXXXXX"," X X X ","X     X"]
P1C  = [None, CYAN,   (30,100,220), WHITE, YELLOW, (0,180,255)]
P2C  = [None, ORANGE, RED,          WHITE, YELLOW, (255,80,0) ]

def draw_ship(surf, cx, cy, cmap, scale, flipped=False):
    rows = SHIP[::-1] if flipped else SHIP
    pw   = len(rows[0])*scale
    ph   = len(rows)  *scale
    ox   = cx - pw//2
    oy   = cy - ph//2
    for ri,row in enumerate(rows):
        for ci,ch in enumerate(row):
            if ch=='X':
                idx = (ri+ci)%(len(cmap)-1)+1
                pygame.draw.rect(surf, cmap[idx],
                                 (ox+ci*scale, oy+ri*scale, scale, scale))

# ── Bullet ───────────────────────────────────────────────────────────────────
class Bullet:
    def __init__(self, x, y, vx, vy, color):
        self.x, self.y   = float(x), float(y)
        self.vx, self.vy = vx, vy
        self.color        = color
        self.r            = max(4, WIDTH//130)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def dead(self):
        return (self.x < 0 or self.x > WIDTH or
                self.y < 0 or self.y > HEIGHT)

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x),int(self.y)), self.r)
        # small glow
        gx, gy = int(self.x), int(self.y)
        gs = pygame.Surface((self.r*4, self.r*4), pygame.SRCALPHA)
        pygame.draw.circle(gs, (*self.color, 60), (self.r*2,self.r*2), self.r*2)
        surf.blit(gs, (gx-self.r*2, gy-self.r*2))

# ── Particle ─────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = float(x), float(y)
        a  = random.uniform(0, math.tau)
        sp = random.uniform(2, 7)
        self.vx = math.cos(a)*sp
        self.vy = math.sin(a)*sp
        self.life  = random.randint(25, 55)
        self.color = color
        self.r     = random.randint(2, 6)

    def update(self):
        self.x += self.vx; self.y += self.vy
        self.vy += 0.15;   self.life -= 1

    def draw(self, surf):
        if self.life > 0:
            pygame.draw.circle(surf, self.color,
                               (int(self.x), int(self.y)), self.r)

# ── Touch Button ─────────────────────────────────────────────────────────────
class Button:
    def __init__(self, x, y, w, h, label, color):
        self.rect  = pygame.Rect(x, y, w, h)
        self.label = label
        self.color = color
        self.held  = False

    def draw(self, surf):
        alp = 200 if self.held else 120
        s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        s.fill((*self.color, alp))
        surf.blit(s, self.rect.topleft)
        pygame.draw.rect(surf, (*self.color, 240), self.rect, 2, border_radius=10)
        lbl = font_sm.render(self.label, True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def hit(self, pos): return self.rect.collidepoint(pos)

# ── Player ───────────────────────────────────────────────────────────────────
class Player:
    def __init__(self, side):
        self.side   = side
        # each player lives in full-screen coords
        # P1 starts left half, P2 starts right half
        if side == 1:
            self.x = HALF // 2
        else:
            self.x = HALF + HALF // 2
        self.y      = HEIGHT // 2
        self.spd    = max(5, WIDTH//160)
        self.max_hp = 5
        self.hp     = self.max_hp
        self.bullets    = []
        self.particles  = []
        self.shoot_cd   = 0
        self.invinc     = 0
        self.alive      = True
        self.cmap       = P1C if side==1 else P2C
        self.bcol       = CYAN if side==1 else ORANGE
        # movement flags
        self.ml=self.mr=self.mu=self.md=self.firing=False
        self.scale = max(3, WIDTH//120)

    def shoot_toward(self, target_x, target_y):
        """Fire a bullet aimed at the opponent."""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy) or 1
        spd  = 14
        vx   = dx/dist * spd
        vy   = dy/dist * spd
        self.bullets.append(Bullet(self.x, self.y, vx, vy, self.bcol))
        self.shoot_cd = 22

    def update(self, opp_x, opp_y):
        if self.ml: self.x -= self.spd
        if self.mr: self.x += self.spd
        if self.mu: self.y -= self.spd
        if self.md: self.y += self.spd

        # keep inside own half
        if self.side == 1:
            self.x = max(30, min(HALF-30, self.x))
        else:
            self.x = max(HALF+30, min(WIDTH-30, self.x))
        self.y = max(30, min(HEIGHT-30, self.y))

        if self.shoot_cd > 0: self.shoot_cd -= 1
        if self.invinc  > 0: self.invinc  -= 1

        if self.firing and self.shoot_cd == 0:
            self.shoot_toward(opp_x, opp_y)

        for b in self.bullets: b.update()
        self.bullets = [b for b in self.bullets if not b.dead()]
        for p in self.particles: p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def take_hit(self):
        if self.invinc > 0: return False
        self.hp     -= 1
        self.invinc  = 50
        for _ in range(25):
            self.particles.append(Particle(self.x, self.y, self.bcol))
        if self.hp <= 0:
            self.alive = False
            for _ in range(80):
                self.particles.append(Particle(self.x, self.y, self.bcol))
        return True

    def draw(self, surf):
        for p in self.particles: p.draw(surf)
        for b in self.bullets:   b.draw(surf)
        if self.alive and (self.invinc==0 or self.invinc%6<3):
            # P1 faces right, P2 faces left (flipped)
            draw_ship(surf, int(self.x), int(self.y),
                      self.cmap, self.scale, flipped=(self.side==2))

# ── Controls layout ───────────────────────────────────────────────────────────
def make_controls():
    BW  = max(65, WIDTH//13)
    BH  = max(60, HEIGHT//10)
    PAD = 10
    BY  = HEIGHT - BH - PAD

    # Player 1 — bottom-left area
    p1_up    = Button(PAD + BW,          BY-BH-PAD, BW, BH, "▲", CYAN)
    p1_left  = Button(PAD,               BY,        BW, BH, "◀", CYAN)
    p1_down  = Button(PAD + BW,          BY,        BW, BH, "▼", CYAN)
    p1_right = Button(PAD + BW*2,        BY,        BW, BH, "▶", CYAN)
    p1_fire  = Button(HALF - BW - PAD,   BY,        BW, BH, "FIRE", RED)

    # Player 2 — bottom-right area (mirrored)
    ox = HALF
    p2_up    = Button(ox + PAD + BW,           BY-BH-PAD, BW, BH, "▲", ORANGE)
    p2_left  = Button(ox + PAD,                BY,        BW, BH, "◀", ORANGE)
    p2_down  = Button(ox + PAD + BW,           BY,        BW, BH, "▼", ORANGE)
    p2_right = Button(ox + PAD + BW*2,         BY,        BW, BH, "▶", ORANGE)
    p2_fire  = Button(WIDTH - BW - PAD,        BY,        BW, BH, "FIRE", RED)

    p1b = {"up":p1_up,"left":p1_left,"down":p1_down,"right":p1_right,"fire":p1_fire}
    p2b = {"up":p2_up,"left":p2_left,"down":p2_down,"right":p2_right,"fire":p2_fire}
    return p1b, p2b

def draw_controls(surf, btns):
    for b in btns.values(): b.draw(surf)

def process_touches(touches, p1b, p2b, p1, p2):
    for pl in (p1,p2):
        pl.ml=pl.mr=pl.mu=pl.md=pl.firing=False
    for btn in list(p1b.values())+list(p2b.values()):
        btn.held = False
    for pos in touches:
        for name,btn in p1b.items():
            if btn.hit(pos):
                btn.held=True
                if name=="left":  p1.ml=True
                if name=="right": p1.mr=True
                if name=="up":    p1.mu=True
                if name=="down":  p1.md=True
                if name=="fire":  p1.firing=True
        for name,btn in p2b.items():
            if btn.hit(pos):
                btn.held=True
                if name=="left":  p2.ml=True
                if name=="right": p2.mr=True
                if name=="up":    p2.mu=True
                if name=="down":  p2.md=True
                if name=="fire":  p2.firing=True

# ── HUD ───────────────────────────────────────────────────────────────────────
def draw_hud(surf, player, wins):
    ox  = 8 if player.side==1 else HALF+8
    bw, bh = 110, 14
    filled = int(bw * max(0,player.hp) / player.max_hp)
    bc = GREEN if player.hp > 2 else (YELLOW if player.hp==2 else RED)
    pygame.draw.rect(surf, DKGREY, (ox, 8, bw, bh))
    if filled > 0:
        pygame.draw.rect(surf, bc, (ox, 8, filled, bh))
    pygame.draw.rect(surf, WHITE, (ox, 8, bw, bh), 1)
    label = "P1" if player.side==1 else "P2"
    col   = CYAN if player.side==1 else ORANGE
    surf.blit(font_sm.render(f"{label} HP:{player.hp}", True, col), (ox, 26))
    surf.blit(font_sm.render(f"Wins:{wins}", True, WHITE), (ox, 26+FS+2))

# ── Draw arena divider ────────────────────────────────────────────────────────
def draw_divider(surf):
    # dashed line
    dash = 18
    for y in range(0, HEIGHT, dash*2):
        pygame.draw.line(surf, (100,100,140), (HALF, y), (HALF, min(y+dash, HEIGHT)), 2)

# ── Main ─────────────────────────────────────────────────────────────────────
active_fingers = {}

def main():
    MENU, PLAY, OVER = "menu","play","over"
    state   = MENU
    p1=p2   = None
    wins1=wins2 = 0
    winner  = 0
    particles_global = []   # big bang on death
    p1b, p2b = make_controls()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

            if event.type == pygame.FINGERDOWN:
                fx=int(event.x*WIDTH); fy=int(event.y*HEIGHT)
                active_fingers[event.finger_id]=(fx,fy)
                if state==MENU:
                    state=PLAY; p1=Player(1); p2=Player(2); particles_global.clear()
                elif state==OVER:
                    state=PLAY; p1=Player(1); p2=Player(2); particles_global.clear()

            elif event.type==pygame.FINGERMOTION:
                active_fingers[event.finger_id]=(int(event.x*WIDTH),int(event.y*HEIGHT))
            elif event.type==pygame.FINGERUP:
                active_fingers.pop(event.finger_id,None)

            elif event.type==pygame.MOUSEBUTTONDOWN:
                active_fingers[-1]=event.pos
                if state==MENU:
                    state=PLAY; p1=Player(1); p2=Player(2); particles_global.clear()
                elif state==OVER:
                    state=PLAY; p1=Player(1); p2=Player(2); particles_global.clear()
            elif event.type==pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    active_fingers[-1]=event.pos
            elif event.type==pygame.MOUSEBUTTONUP:
                active_fingers.pop(-1,None)

        update_stars()
        touches = list(active_fingers.values())

        if state==PLAY:
            process_touches(touches, p1b, p2b, p1, p2)
            p1.update(p2.x, p2.y)
            p2.update(p1.x, p1.y)

            # check bullets hitting opponent
            for b in list(p1.bullets):
                if math.hypot(b.x-p2.x, b.y-p2.y) < 20+p2.scale*2:
                    p1.bullets.remove(b)
                    p2.take_hit()
                    break
            for b in list(p2.bullets):
                if math.hypot(b.x-p1.x, b.y-p1.y) < 20+p1.scale*2:
                    p2.bullets.remove(b)
                    p1.take_hit()
                    break

            if not p1.alive:
                winner=2; wins2+=1; state=OVER
            elif not p2.alive:
                winner=1; wins1+=1; state=OVER

        # ── Draw ─────────────────────────────────────────────────────────
        screen.fill(DARK)
        draw_stars(screen)
        draw_divider(screen)

        if state in (PLAY,OVER):
            if p1: p1.draw(screen)
            if p2: p2.draw(screen)
            draw_hud(screen, p1, wins1)
            draw_hud(screen, p2, wins2)
            draw_controls(screen, p1b)
            draw_controls(screen, p2b)

        if state==MENU:
            screen.fill(DARK)
            draw_stars(screen)
            t1=font_big.render("SPACE DUEL", True, CYAN)
            t2=font_med.render("P1  vs  P2", True, WHITE)
            t3=font_med.render("Shoot across to win!", True, GREY)
            t4=font_sm.render("Tap anywhere to Start", True, YELLOW)
            screen.blit(t1, t1.get_rect(center=(WIDTH//2, HEIGHT//3-20)))
            screen.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//3+50)))
            screen.blit(t3, t3.get_rect(center=(WIDTH//2, HEIGHT//3+95)))
            screen.blit(t4, t4.get_rect(center=(WIDTH//2, HEIGHT//3+145)))
            draw_controls(screen, p1b)
            draw_controls(screen, p2b)

        elif state==OVER:
            ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            ov.fill((0,0,0,140)); screen.blit(ov,(0,0))
            col  = CYAN if winner==1 else ORANGE
            t1   = font_big.render(f"PLAYER {winner} WINS!", True, col)
            t2   = font_med.render(f"P1 Wins: {wins1}    P2 Wins: {wins2}", True, WHITE)
            t3   = font_sm.render("Tap to Play Again", True, GREY)
            screen.blit(t1, t1.get_rect(center=(WIDTH//2, HEIGHT//2-70)))
            screen.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//2)))
            screen.blit(t3, t3.get_rect(center=(WIDTH//2, HEIGHT//2+60)))

        pygame.display.flip()

main()