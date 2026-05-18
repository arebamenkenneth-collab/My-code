import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System - Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn")

clock = pygame.time.Clock()

font_small  = pygame.font.SysFont("monospace", 11)
font_medium = pygame.font.SysFont("monospace", 13, bold=True)
font_title  = pygame.font.SysFont("monospace", 15, bold=True)

stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT),
          random.choice([1, 1, 1, 2])) for _ in range(280)]

PLANETS = [
    {"name": "Mercury", "orbit": 70,  "size": 5,  "color": (169,169,169), "speed": 4.74,  "angle": 20},
    {"name": "Venus",   "orbit": 105, "size": 8,  "color": (255,198,100), "speed": 1.86,  "angle": 80},
    {"name": "Earth",   "orbit": 145, "size": 9,  "color": ( 70,130,220), "speed": 1.14,  "angle": 160},
    {"name": "Mars",    "orbit": 190, "size": 7,  "color": (200, 80, 40), "speed": 0.61,  "angle": 240},
    {"name": "Jupiter", "orbit": 265, "size": 22, "color": (210,160,100), "speed": 0.096, "angle": 310},
    {"name": "Saturn",  "orbit": 340, "size": 17, "color": (220,190,120), "speed": 0.039, "angle": 50},
]

moon = {"name": "Moon", "orbit": 20, "size": 3, "color": (200,200,200), "speed": 13.17, "angle": 0}

angles     = {p["name"]: p["angle"] for p in PLANETS}
moon_angle = moon["angle"]

paused      = False
show_orbits = True
show_names  = True
speed_mult  = 1.0
zoom        = 1.0
selected    = None

PANEL_X, PANEL_Y = 10, 50
PANEL_W, PANEL_H = 175, 265

def draw_glow(surface, color, cx, cy, radius, layers=4):
    for i in range(layers, 0, -1):
        alpha = int(60 / i)
        r = max(0, min(255, color[0]))
        g = max(0, min(255, color[1]))
        b = max(0, min(255, color[2]))
        glow_surf = pygame.Surface((radius*2 + i*8, radius*2 + i*8), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (r, g, b, alpha),
                           (radius + i*4, radius + i*4), radius + i*4)
        surface.blit(glow_surf, (cx - radius - i*4, cy - radius - i*4))

def draw_saturn_rings(surface, cx, cy, planet_r, zoom):
    rw = int((planet_r + 14) * zoom)
    rh = int(6 * zoom)
    ring_surf = pygame.Surface((rw*2+4, rh*2+4), pygame.SRCALPHA)
    pygame.draw.ellipse(ring_surf, (180,155,90,130), (0, rh//2, rw*2+4, rh*2), 3)
    surface.blit(ring_surf, (cx - rw - 2, cy - rh - 2))

def draw_sun(surface, cx, cy, zoom):
    r = int(38 * zoom)
    for i in [5, 4, 3, 2, 1]:
        alpha = 18 * i
        gs = pygame.Surface(((r + i*12)*2, (r + i*12)*2), pygame.SRCALPHA)
        pygame.draw.circle(gs, (255, 140, 0, alpha),
                           (r + i*12, r + i*12), r + i*12)
        surface.blit(gs, (cx - r - i*12, cy - r - i*12))
    pygame.draw.circle(surface, (255, 220, 60), (cx, cy), r)
    pygame.draw.circle(surface, (255, 170, 20), (cx, cy), int(r * 0.75))
    pygame.draw.circle(surface, (255, 100,  0), (cx, cy), int(r * 0.45))

def draw_panel():
    panel_surf = pygame.Surface((PANEL_W, PANEL_H), pygame.SRCALPHA)
    panel_surf.fill((10, 10, 30, 200))
    screen.blit(panel_surf, (PANEL_X, PANEL_Y))
    pygame.draw.rect(screen, (80, 120, 200), (PANEL_X, PANEL_Y, PANEL_W, PANEL_H), 1)

    y = PANEL_Y + 8
    lbl = font_title.render("Control Panel", True, (180, 210, 255))
    screen.blit(lbl, (PANEL_X + 8, y)); y += 22

    col = (100, 220, 100) if paused else (220, 100, 100)
    txt = "► Resume" if paused else "‖ Pause"
    pygame.draw.rect(screen, col, (PANEL_X+8, y, PANEL_W-16, 22), border_radius=4)
    lbl = font_medium.render(txt, True, (0,0,0))
    screen.blit(lbl, (PANEL_X + 8 + (PANEL_W-16)//2 - lbl.get_width()//2, y+3))
    global btn_pause_rect
    btn_pause_rect = pygame.Rect(PANEL_X+8, y, PANEL_W-16, 22)
    y += 30

    col2 = (80,180,255) if show_orbits else (80,80,100)
    pygame.draw.rect(screen, col2, (PANEL_X+8, y, PANEL_W-16, 22), border_radius=4)
    lbl = font_medium.render("Show Orbits: " + ("ON" if show_orbits else "OFF"), True, (0,0,0))
    screen.blit(lbl, (PANEL_X + 8 + (PANEL_W-16)//2 - lbl.get_width()//2, y+3))
    global btn_orbit_rect
    btn_orbit_rect = pygame.Rect(PANEL_X+8, y, PANEL_W-16, 22)
    y += 30

    col3 = (80,180,255) if show_names else (80,80,100)
    pygame.draw.rect(screen, col3, (PANEL_X+8, y, PANEL_W-16, 22), border_radius=4)
    lbl = font_medium.render("Show Names: " + ("ON" if show_names else "OFF"), True, (0,0,0))
    screen.blit(lbl, (PANEL_X + 8 + (PANEL_W-16)//2 - lbl.get_width()//2, y+3))
    global btn_names_rect
    btn_names_rect = pygame.Rect(PANEL_X+8, y, PANEL_W-16, 22)
    y += 30

    lbl = font_small.render(f"Sim Speed: x{speed_mult:.1f}", True, (200, 220, 255))
    screen.blit(lbl, (PANEL_X+8, y)); y += 16
    bar_x = PANEL_X + 12
    bar_w = PANEL_W - 24
    pygame.draw.rect(screen, (60,60,100), (bar_x, y, bar_w, 8), border_radius=4)
    fill_w = int((speed_mult / 5.0) * bar_w)
    pygame.draw.rect(screen, (100,160,255), (bar_x, y, fill_w, 8), border_radius=4)
    hx = bar_x + fill_w
    pygame.draw.circle(screen, (200,220,255), (hx, y+4), 7)
    global slider_rect, slider_bar_x, slider_bar_w
    slider_rect  = pygame.Rect(bar_x-5, y-5, bar_w+10, 18)
    slider_bar_x = bar_x
    slider_bar_w = bar_w
    y += 22

    lbl = font_small.render(f"Zoom: x{zoom:.2f}", True, (200,220,255))
    screen.blit(lbl, (PANEL_X+8, y)); y += 16
    bar_x2 = PANEL_X + 12
    bar_w2 = PANEL_W - 24
    pygame.draw.rect(screen, (60,60,100), (bar_x2, y, bar_w2, 8), border_radius=4)
    fill_w2 = int(((zoom - 0.4) / 1.6) * bar_w2)
    fill_w2 = max(0, min(bar_w2, fill_w2))
    pygame.draw.rect(screen, (100,220,160), (bar_x2, y, fill_w2, 8), border_radius=4)
    hx2 = bar_x2 + fill_w2
    pygame.draw.circle(screen, (180,255,200), (hx2, y+4), 7)
    global zoom_rect, zoom_bar_x, zoom_bar_w
    zoom_rect  = pygame.Rect(bar_x2-5, y-5, bar_w2+10, 18)
    zoom_bar_x = bar_x2
    zoom_bar_w = bar_w2
    y += 22

    if selected:
        lbl = font_small.render(f"Selected: {selected}", True, (255,220,100))
        screen.blit(lbl, (PANEL_X+8, y)); y += 14
        for p in PLANETS:
            if p["name"] == selected:
                au = p["orbit"] / 145
                lbl2 = font_small.render(f"Earth-Sun(AU): {au:.2f}", True, (200,200,200))
                screen.blit(lbl2, (PANEL_X+8, y))

    y = PANEL_Y + PANEL_H - 30
    pygame.draw.rect(screen, (50,50,80), (PANEL_X+8, y, PANEL_W-16, 22), border_radius=4)
    lbl = font_medium.render("Show Description", True, (180,200,255))
    screen.blit(lbl, (PANEL_X + 8 + (PANEL_W-16)//2 - lbl.get_width()//2, y+3))

def planet_pos(cx, cy, orbit, angle_deg, zoom):
    rad = math.radians(angle_deg)
    x = cx + int(orbit * zoom * math.cos(rad))
    y = cy + int(orbit * zoom * math.sin(rad))
    return x, y

btn_pause_rect = pygame.Rect(0,0,0,0)
btn_orbit_rect = pygame.Rect(0,0,0,0)
btn_names_rect = pygame.Rect(0,0,0,0)
slider_rect    = pygame.Rect(0,0,0,0)
slider_bar_x   = 0; slider_bar_w = 1
zoom_rect      = pygame.Rect(0,0,0,0)
zoom_bar_x     = 0; zoom_bar_w   = 1

dragging_speed = False
dragging_zoom  = False

CX, CY = WIDTH // 2 + 50, HEIGHT // 2

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_o:
                show_orbits = not show_orbits
            elif event.key == pygame.K_n:
                show_names = not show_names

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if btn_pause_rect.collidepoint(mx, my):
                paused = not paused
            elif btn_orbit_rect.collidepoint(mx, my):
                show_orbits = not show_orbits
            elif btn_names_rect.collidepoint(mx, my):
                show_names = not show_names
            elif slider_rect.collidepoint(mx, my):
                dragging_speed = True
                frac = max(0.0, min(1.0, (mx - slider_bar_x) / slider_bar_w))
                speed_mult = max(0.1, round(frac * 5.0, 1))
            elif zoom_rect.collidepoint(mx, my):
                dragging_zoom = True
                frac = max(0.0, min(1.0, (mx - zoom_bar_x) / zoom_bar_w))
                zoom = round(0.4 + frac * 1.6, 2)
            else:
                selected = None
                for p in PLANETS:
                    px, py = planet_pos(CX, CY, p["orbit"], angles[p["name"]], zoom)
                    if math.hypot(mx - px, my - py) < max(p["size"]*zoom + 4, 12):
                        selected = p["name"]
                        break
                if math.hypot(mx - CX, my - CY) < 38 * zoom + 5:
                    selected = "Sun"

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_speed = False
            dragging_zoom  = False

        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if dragging_speed:
                frac = max(0.0, min(1.0, (mx - slider_bar_x) / slider_bar_w))
                speed_mult = max(0.1, round(frac * 5.0, 1))
            if dragging_zoom:
                frac = max(0.0, min(1.0, (mx - zoom_bar_x) / zoom_bar_w))
                zoom = round(0.4 + frac * 1.6, 2)

    if not paused:
        for p in PLANETS:
            angles[p["name"]] = (angles[p["name"]] + p["speed"] * speed_mult * 0.3) % 360
        moon_angle = (moon_angle + moon["speed"] * speed_mult * 0.3) % 360

    screen.fill((2, 2, 18))

    for sx, sy, sr in stars:
        col_v = random.randint(200, 255) if sr == 2 else 180
        pygame.draw.circle(screen, (col_v, col_v, col_v), (sx, sy), sr)

    if show_orbits:
        for p in PLANETS:
            r = int(p["orbit"] * zoom)
            pygame.draw.circle(screen, (40, 50, 80), (CX, CY), r, 1)
        ex, ey = planet_pos(CX, CY, PLANETS[2]["orbit"], angles["Earth"], zoom)
        mr = int(moon["orbit"] * zoom)
        pygame.draw.circle(screen, (40, 50, 70), (ex, ey), mr, 1)

    draw_sun(screen, CX, CY, zoom)

    earth_x, earth_y = 0, 0
    for p in PLANETS:
        px, py = planet_pos(CX, CY, p["orbit"], angles[p["name"]], zoom)
        r = max(2, int(p["size"] * zoom))

        if p["name"] == "Earth":
            earth_x, earth_y = px, py

        if p["name"] == "Saturn":
            draw_saturn_rings(screen, px, py, r, zoom)

        if p["name"] in ("Jupiter", "Saturn"):
            draw_glow(screen, p["color"], px, py, r, layers=3)

        pygame.draw.circle(screen, p["color"], (px, py), r)

        if p["name"] == "Earth":
            pygame.draw.circle(screen, (180,210,255), (px-r//3, py-r//3), max(1,r//3))

        if p["name"] == "Jupiter":
            for boff in [-r//3, 0, r//3]:
                pygame.draw.line(screen, (180,130,80),
                                 (px-r, py+boff), (px+r, py+boff), 1)

        if show_names:
            lbl = font_small.render(p["name"], True, (180,200,220))
            screen.blit(lbl, (px + r + 3, py - 6))

    if earth_x:
        mx2 = earth_x + int(moon["orbit"] * zoom * math.cos(math.radians(moon_angle)))
        my2 = earth_y + int(moon["orbit"] * zoom * math.sin(math.radians(moon_angle)))
        mr2 = max(2, int(moon["size"] * zoom))
        pygame.draw.circle(screen, moon["color"], (mx2, my2), mr2)
        if show_names:
            lbl = font_small.render("Moon", True, (150,160,170))
            screen.blit(lbl, (mx2 + mr2 + 2, my2 - 5))

    if show_names:
        lbl = font_small.render("Sun", True, (255, 220, 100))
        screen.blit(lbl, (CX + int(38*zoom) + 4, CY - 7))

    title = font_title.render(
        "Solar System - Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn",
        True, (160, 190, 230))
    screen.blit(title, (10, 10))

    draw_panel()

    if selected and selected != "Sun":
        for p in PLANETS:
            if p["name"] == selected:
                px, py = planet_pos(CX, CY, p["orbit"], angles[p["name"]], zoom)
                r = max(2, int(p["size"] * zoom))
                pygame.draw.circle(screen, (255,255,100), (px, py), r+4, 2)
    elif selected == "Sun":
        pygame.draw.circle(screen, (255,255,100), (CX, CY), int(38*zoom)+5, 2)

    hints = font_small.render("SPACE=pause  O=orbits  N=names  ESC=quit", True, (80,100,130))
    screen.blit(hints, (WIDTH - hints.get_width() - 10, HEIGHT - 18))

    pygame.display.flip()

pygame.quit()
sys.exit()