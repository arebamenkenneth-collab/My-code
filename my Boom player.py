import pygame
import os
import random

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption("Music Player")

BG      = (15, 15, 25)
CARD    = (25, 25, 40)
ACCENT  = (100, 220, 255)
ACCENT2 = (180, 100, 255)
WHITE   = (255, 255, 255)
GRAY    = (120, 120, 140)
DARK    = (40, 40, 60)
GREEN   = (80, 220, 120)

font_big   = pygame.font.SysFont("monospace", int(H * 0.030), bold=True)
font_med   = pygame.font.SysFont("monospace", int(H * 0.022))
font_small = pygame.font.SysFont("monospace", int(H * 0.017))

songs = [
    {"title": "7 Years Old",   "artist": "Lukas Graham", "file": "/storage/emulated/0/Xender/audio/7yearsold.mp3"},
    {"title": "Scofield",      "artist": "Unknown",      "file": "/storage/emulated/0/Xender/audio/scofield.mp3"},
    {"title": "Rema Fun",      "artist": "Rema",         "file": "/storage/emulated/0/Xender/audio/Rema fun.mp3"},
    {"title": "Godswill Oyor", "artist": "Unknown",      "file": "/storage/emulated/0/Xender/audio/Godswill oyor banner.mp3"},
    {"title": "Stronger",      "artist": "Unknown",      "file": "/storage/emulated/0/Xender/audio/stronger.mp3"},
]

ART_R      = int(H * 0.10)
ART_CY     = int(H * 0.13)
TITLE_Y    = int(H * 0.25)
ARTIST_Y   = int(H * 0.29)
VIS_BASE   = int(H * 0.38)
VIS_H      = int(H * 0.06)

PROG_BAR   = pygame.Rect(int(W*0.05), int(H*0.40), int(W*0.90), int(H*0.018))
TIME_Y     = int(H * 0.425)

PLAY_R     = int(H * 0.07)
PLAY_CX    = W // 2
PLAY_CY    = int(H * 0.53)
PLAY_BTN   = pygame.Rect(PLAY_CX - PLAY_R, PLAY_CY - PLAY_R, PLAY_R*2, PLAY_R*2)

SB_W       = int(W * 0.20)
SB_H       = int(H * 0.055)
PREV_BTN   = pygame.Rect(PLAY_CX - PLAY_R*2 - SB_W - 5, PLAY_CY - SB_H//2, SB_W, SB_H)
NEXT_BTN   = pygame.Rect(PLAY_CX + PLAY_R*2 + 5,        PLAY_CY - SB_H//2, SB_W, SB_H)

VOL_Y      = int(H * 0.625)
VOL_BAR    = pygame.Rect(int(W*0.18), VOL_Y, int(W*0.65), int(H*0.016))

PLAYLIST_Y = int(H * 0.675)
PLAYLIST_H = int((H - PLAYLIST_Y - 5) // len(songs))

current    = 0
playing    = False
volume     = 0.7
progress   = 0.0
song_len   = 180
start_tick = 0
pause_pos  = 0
pygame.mixer.music.set_volume(volume)

bars        = 28
bar_heights = [random.randint(4, 10) for _ in range(bars)]
bar_targets = [random.randint(4, 10) for _ in range(bars)]


def load_song(idx):
    global song_len, start_tick, pause_pos
    path = songs[idx]["file"]
    if os.path.exists(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        try:
            snd = pygame.mixer.Sound(path)
            song_len = snd.get_length()
            del snd
        except Exception:
            song_len = 180
    else:
        song_len = 180
    start_tick = pygame.time.get_ticks()
    pause_pos  = 0


def play_pause():
    global playing, start_tick, pause_pos
    if not playing:
        if os.path.exists(songs[current]["file"]):
            if pause_pos > 0:
                pygame.mixer.music.unpause()
                start_tick = pygame.time.get_ticks() - int(pause_pos * 1000)
            else:
                load_song(current)
        playing = True
    else:
        pygame.mixer.music.pause()
        pause_pos = (pygame.time.get_ticks() - start_tick) / 1000
        playing = False


def next_song():
    global current, pause_pos
    current = (current + 1) % len(songs)
    pause_pos = 0
    if playing: load_song(current)


def prev_song():
    global current, pause_pos
    current = (current - 1) % len(songs)
    pause_pos = 0
    if playing: load_song(current)


def rr(surf, color, rect, r=10):
    pygame.draw.rect(surf, color, rect, border_radius=r)


def tc(surf, text, font, color, cx, y):
    img = font.render(text, True, color)
    surf.blit(img, (cx - img.get_width()//2, y))


def update_vis():
    global bar_heights, bar_targets
    for i in range(bars):
        if playing:
            if abs(bar_heights[i] - bar_targets[i]) < 2:
                bar_targets[i] = random.randint(6, VIS_H)
            bar_heights[i] += (bar_targets[i] - bar_heights[i]) * 0.15
        else:
            bar_heights[i] = max(4, bar_heights[i] * 0.92)


def draw_vis():
    tw = int(W * 0.90)
    bw = tw / bars
    x0 = int(W * 0.05)
    for i in range(bars):
        h = int(bar_heights[i])
        x = x0 + int(i * bw)
        t = i / bars
        r = int(ACCENT[0]*(1-t) + ACCENT2[0]*t)
        g = int(ACCENT[1]*(1-t) + ACCENT2[1]*t)
        b = int(ACCENT[2]*(1-t) + ACCENT2[2]*t)
        pygame.draw.rect(screen, (r, g, b),
                         (x, VIS_BASE - h, max(2, int(bw)-2), h),
                         border_radius=3)


def draw_art():
    cx, cy, r = W//2, ART_CY, ART_R
    pygame.draw.circle(screen, DARK,   (cx, cy), r)
    pygame.draw.circle(screen, ACCENT, (cx, cy), r, 3)
    for rr2 in [r*0.72, r*0.50, r*0.30]:
        pygame.draw.circle(screen, CARD, (cx, cy), int(rr2), 2)
    pygame.draw.circle(screen, ACCENT2, (cx, cy), int(r*0.12))
    pygame.draw.circle(screen, WHITE,   (cx, cy), int(r*0.06))


def fmt(s):
    s = max(0, int(s))
    return f"{s//60}:{s%60:02d}"


clock  = pygame.time.Clock()
running = True
drag_p = drag_v = False

while running:
    clock.tick(60)

    if playing and not drag_p:
        elapsed  = (pygame.time.get_ticks() - start_tick) / 1000
        progress = min(elapsed / song_len, 1.0)
        if progress >= 1.0:
            next_song()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            mx = int(event.x * W) if event.type == pygame.FINGERDOWN else event.pos[0]
            my = int(event.y * H) if event.type == pygame.FINGERDOWN else event.pos[1]

            if PLAY_BTN.collidepoint(mx, my):
                play_pause()
            elif NEXT_BTN.collidepoint(mx, my):
                next_song()
            elif PREV_BTN.collidepoint(mx, my):
                prev_song()
            elif PROG_BAR.collidepoint(mx, my):
                drag_p   = True
                progress = max(0, min(1, (mx - PROG_BAR.x) / PROG_BAR.width))
                new_pos  = progress * song_len
                if os.path.exists(songs[current]["file"]):
                    pygame.mixer.music.set_pos(new_pos)
                start_tick = pygame.time.get_ticks() - int(new_pos * 1000)
                pause_pos  = 0
            elif VOL_BAR.collidepoint(mx, my):
                drag_v = True
                volume = max(0, min(1, (mx - VOL_BAR.x) / VOL_BAR.width))
                pygame.mixer.music.set_volume(volume)
            else:
                for i in range(len(songs)):
                    pr = pygame.Rect(int(W*0.03),
                                     PLAYLIST_Y + i * PLAYLIST_H,
                                     int(W*0.94), PLAYLIST_H - 4)
                    if pr.collidepoint(mx, my):
                        current = i
                        pause_pos = 0
                        if playing: load_song(current)
                        break

        if event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
            drag_p = drag_v = False

        if event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
            mx = int(event.x * W) if event.type == pygame.FINGERMOTION else event.pos[0]
            my = int(event.y * H) if event.type == pygame.FINGERMOTION else event.pos[1]
            if drag_p:
                progress = max(0, min(1, (mx - PROG_BAR.x) / PROG_BAR.width))
                new_pos  = progress * song_len
                if os.path.exists(songs[current]["file"]):
                    pygame.mixer.music.set_pos(new_pos)
                start_tick = pygame.time.get_ticks() - int(new_pos * 1000)
            if drag_v:
                volume = max(0, min(1, (mx - VOL_BAR.x) / VOL_BAR.width))
                pygame.mixer.music.set_volume(volume)

    # DRAW
    screen.fill(BG)
    draw_art()

    song = songs[current]
    tc(screen, song["title"],  font_big, WHITE, W//2, TITLE_Y)
    tc(screen, song["artist"], font_med, GRAY,  W//2, ARTIST_Y)

    update_vis()
    draw_vis()

    rr(screen, DARK, PROG_BAR, 9)
    fw = int(PROG_BAR.width * progress)
    if fw > 0:
        rr(screen, ACCENT,
           pygame.Rect(PROG_BAR.x, PROG_BAR.y, fw, PROG_BAR.height), 9)
    pygame.draw.circle(screen, WHITE, (PROG_BAR.x + fw, PROG_BAR.centery), 10)

    screen.blit(font_small.render(fmt(progress * song_len), True, GRAY),
                (PROG_BAR.x, TIME_Y))
    ti = font_small.render(fmt(song_len), True, GRAY)
    screen.blit(ti, (PROG_BAR.right - ti.get_width(), TIME_Y))

    rr(screen, CARD, PREV_BTN, 10)
    tc(screen, "|◀", font_med, WHITE, PREV_BTN.centerx, PREV_BTN.y + int(SB_H*0.2))

    pygame.draw.circle(screen, ACCENT if playing else GREEN, (PLAY_CX, PLAY_CY), PLAY_R)
    tc(screen, "▐▌" if playing else " ▶", font_big, BG, PLAY_CX, PLAY_CY - int(PLAY_R*0.4))

    rr(screen, CARD, NEXT_BTN, 10)
    tc(screen, "▶|", font_med, WHITE, NEXT_BTN.centerx, NEXT_BTN.y + int(SB_H*0.2))

    tc(screen, "VOL", font_small, GRAY, int(W*0.10), VOL_Y)
    rr(screen, DARK, VOL_BAR, 8)
    vfw = int(VOL_BAR.width * volume)
    rr(screen, ACCENT2, pygame.Rect(VOL_BAR.x, VOL_BAR.y, vfw, VOL_BAR.height), 8)
    pygame.draw.circle(screen, WHITE, (VOL_BAR.x + vfw, VOL_BAR.centery), 9)

    tc(screen, "— PLAYLIST —", font_small, GRAY, W//2, PLAYLIST_Y - int(H*0.02))
    for i in range(len(songs)):
        py = PLAYLIST_Y + i * PLAYLIST_H
        pr = pygame.Rect(int(W*0.03), py, int(W*0.94), PLAYLIST_H - 4)
        rr(screen, ACCENT if i == current else CARD, pr, 10)
        tc2 = BG if i == current else WHITE
        gc2 = BG if i == current else GRAY
        screen.blit(font_med.render(songs[i]["title"], True, tc2),
                    (pr.x + 12, pr.y + 4))
        screen.blit(font_small.render(songs[i]["artist"], True, gc2),
                    (pr.x + 12, pr.y + int(PLAYLIST_H * 0.52)))

    pygame.display.flip()

pygame.quit()