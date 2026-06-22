import pygame
import sys
import math
import random

pygame.init()
info = pygame.display.Info()
SW, SH = info.current_w, info.current_h
screen = pygame.display.set_mode((SW, SH), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Colors
BG       = (8, 28, 8)
GREEN    = (30, 160, 60)
DARK_G   = (15, 80, 30)
WHITE    = (240, 240, 240)
GOLD     = (220, 180, 40)
RED      = (210, 50, 50)
LIME     = (100, 230, 80)
GRAY     = (110, 120, 110)
STEEL    = (60, 80, 60)
ORANGE   = (230, 130, 30)

def sw(p): return int(SW * p)
def sh(p): return int(SH * p)

fnt_big  = pygame.font.SysFont("monospace", sh(0.06), bold=True)
fnt_med  = pygame.font.SysFont("monospace", sh(0.038), bold=True)
fnt_sm   = pygame.font.SysFont("monospace", sh(0.028))
fnt_tiny = pygame.font.SysFont("monospace", sh(0.021))

QUESTIONS = [
    {
        "q": "Which country has won the FIFA World Cup the most times?",
        "options": ["Germany", "Argentina", "Brazil", "Italy"],
        "answer": 2,
        "fact": "Brazil has won 5 World Cups: 1958, 1962, 1970, 1994 and 2002."
    },
    {
        "q": "Who is the all-time top scorer in FIFA World Cup history?",
        "options": ["Ronaldo (Brazil)", "Miroslav Klose", "Pele", "Just Fontaine"],
        "answer": 1,
        "fact": "Miroslav Klose scored 16 World Cup goals for Germany across 4 tournaments."
    },
    {
        "q": "Which club has won the UEFA Champions League the most times?",
        "options": ["Barcelona", "Bayern Munich", "AC Milan", "Real Madrid"],
        "answer": 3,
        "fact": "Real Madrid have won the Champions League / European Cup 15 times."
    },
    {
        "q": "How many players are on the field per team in football?",
        "options": ["10", "11", "12", "9"],
        "answer": 1,
        "fact": "Each team fields exactly 11 players, including the goalkeeper."
    },
    {
        "q": "Which player has won the most Ballon d'Or awards?",
        "options": ["Cristiano Ronaldo", "Zinedine Zidane", "Lionel Messi", "Ronaldinho"],
        "answer": 2,
        "fact": "Lionel Messi has won the Ballon d'Or 8 times as of 2023."
    },
]

particles = []

def spawn_p(x, y, color, n=12, speed=5):
    for _ in range(n):
        a = random.uniform(0, math.pi * 2)
        s = random.uniform(1, speed)
        particles.append({"x":x,"y":y,"vx":math.cos(a)*s,"vy":math.sin(a)*s,
                          "life":random.randint(25,50),"ml":50,"color":color,
                          "size":random.randint(2,5)})

def draw_particles(surf):
    for p in particles[:]:
        p["x"]+=p["vx"]; p["y"]+=p["vy"]; p["vy"]+=0.1; p["life"]-=1
        if p["life"]<=0: particles.remove(p); continue
        ratio=p["life"]/p["ml"]
        r,g,b=p["color"]
        pygame.draw.circle(surf,(int(r*ratio),int(g*ratio),int(b*ratio)),
                           (int(p["x"]),int(p["y"])),max(1,int(p["size"]*ratio)))

def draw_pitch_bg(surf):
    surf.fill(BG)
    # Pitch stripes
    stripe_w = sw(0.12)
    for i in range(0, SW, stripe_w*2):
        pygame.draw.rect(surf, DARK_G, (i, 0, stripe_w, SH))
    # Centre circle
    pygame.draw.circle(surf, STEEL, (SW//2, SH//2), sh(0.22), 2)
    pygame.draw.line(surf, STEEL, (0, SH//2), (SW, SH//2), 2)
    pygame.draw.rect(surf, STEEL, (sw(0.02), sh(0.02), SW-sw(0.04), SH-sh(0.04)), 2)

def wrap(text, font, max_w):
    words=text.split(); lines=[]; line=""
    for w in words:
        test=(line+" "+w).strip()
        if font.size(test)[0]<=max_w: line=test
        else:
            if line: lines.append(line)
            line=w
    if line: lines.append(line)
    return lines

# ── Title screen ─────────────────────────────────────────
def title_screen():
    frame=0
    while True:
        clock.tick(60); frame+=1
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type in (pygame.FINGERDOWN,pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN):
                return
        draw_pitch_bg(screen)
        # Ball bounce
        by=sh(0.28)+int(math.sin(frame*0.07)*sh(0.04))
        pygame.draw.circle(screen,WHITE,(SW//2,by),sh(0.06))
        pygame.draw.circle(screen,GRAY,(SW//2,by),sh(0.06),3)
        for a in range(0,360,60):
            rad=math.radians(a+frame)
            px2=SW//2+int(math.cos(rad)*sh(0.035))
            py2=by+int(math.sin(rad)*sh(0.035))
            pygame.draw.circle(screen,(30,30,30),(px2,py2),sh(0.015))

        t1=fnt_big.render("FOOTBALL",True,GOLD)
        t2=fnt_big.render("QUIZ",True,WHITE)
        t3=fnt_sm.render("5 Questions — How well do you know football?",True,LIME)
        screen.blit(t1,t1.get_rect(center=(SW//2,sh(0.48))))
        screen.blit(t2,t2.get_rect(center=(SW//2,sh(0.56))))
        screen.blit(t3,t3.get_rect(center=(SW//2,sh(0.65))))

        alpha=int(160+95*math.sin(frame*0.08))
        tp=fnt_sm.render("TAP TO KICK OFF",True,GOLD)
        ts=pygame.Surface(tp.get_size(),pygame.SRCALPHA)
        ts.blit(tp,(0,0)); ts.set_alpha(alpha)
        screen.blit(ts,ts.get_rect(center=(SW//2,sh(0.82))))
        pygame.display.flip()

# ── Results screen ────────────────────────────────────────
def results_screen(score):
    msgs={5:("PERFECT!",GOLD),4:("Great game!",LIME),
          3:("Not bad!",WHITE),2:("Keep training",ORANGE),
          1:("Back to basics",RED),0:("Red card!",RED)}
    msg,col=msgs.get(score,("...",WHITE))
    frame=0
    if score>=4:
        for _ in range(30):
            spawn_p(random.randint(0,SW),sh(0.3),
                    random.choice([GOLD,LIME,WHITE]),4,6)
    while True:
        clock.tick(60); frame+=1
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type in (pygame.FINGERDOWN,pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN):
                return
        draw_pitch_bg(screen)
        draw_particles(screen)

        t1=fnt_big.render(f"{score} / 5",True,col)
        t2=fnt_med.render(msg,True,WHITE)
        screen.blit(t1,t1.get_rect(center=(SW//2,sh(0.38))))
        screen.blit(t2,t2.get_rect(center=(SW//2,sh(0.50))))

        alpha=int(160+95*math.sin(frame*0.08))
        tp=fnt_sm.render("TAP TO PLAY AGAIN",True,GOLD)
        ts=pygame.Surface(tp.get_size(),pygame.SRCALPHA)
        ts.blit(tp,(0,0)); ts.set_alpha(alpha)
        screen.blit(ts,ts.get_rect(center=(SW//2,sh(0.72))))
        pygame.display.flip()

# ── Quiz ─────────────────────────────────────────────────
def run_quiz():
    global particles; particles=[]
    questions=QUESTIONS.copy(); random.shuffle(questions)
    q_idx=0; score=0; TIME_LIMIT=20
    answered=False; chosen=-1; show_fact=False
    fact_timer=0; frame=0; time_left=TIME_LIMIT
    last_tick=pygame.time.get_ticks()

    btn_w=sw(0.44); btn_h=sh(0.1); pad=sw(0.03)
    btn_rects=[
        pygame.Rect(pad,           sh(0.63), btn_w, btn_h),
        pygame.Rect(SW-pad-btn_w,  sh(0.63), btn_w, btn_h),
        pygame.Rect(pad,           sh(0.63)+btn_h+sh(0.025), btn_w, btn_h),
        pygame.Rect(SW-pad-btn_w,  sh(0.63)+btn_h+sh(0.025), btn_w, btn_h),
    ]

    while q_idx < len(questions):
        clock.tick(60); frame+=1
        q=questions[q_idx]
        now=pygame.time.get_ticks()

        if not answered and not show_fact:
            time_left -= (now-last_tick)/1000
            last_tick=now
            if time_left<=0:
                time_left=0; answered=True; chosen=-1
                show_fact=True; fact_timer=100
                spawn_p(SW//2,sh(0.5),RED,12,5)
        else:
            last_tick=now

        if show_fact:
            fact_timer-=1
            if fact_timer<=0:
                q_idx+=1; answered=False; chosen=-1
                show_fact=False; time_left=TIME_LIMIT
                last_tick=pygame.time.get_ticks()
                continue

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                return score
            if not answered and not show_fact:
                pos=None
                if e.type==pygame.FINGERDOWN: pos=(int(e.x*SW),int(e.y*SH))
                elif e.type==pygame.MOUSEBUTTONDOWN: pos=e.pos
                if pos:
                    for i,rect in enumerate(btn_rects):
                        if rect.collidepoint(pos):
                            chosen=i; answered=True
                            if i==q["answer"]:
                                score+=1
                                spawn_p(pos[0],pos[1],LIME,18,7)
                            else:
                                spawn_p(pos[0],pos[1],RED,15,5)
                            show_fact=True; fact_timer=110

        # ── Draw ─────────────────────────────────────
        draw_pitch_bg(screen)
        draw_particles(screen)

        # Progress dots
        for i in range(len(questions)):
            col=GOLD if i<q_idx else (LIME if i==q_idx else STEEL)
            pygame.draw.circle(screen,col,(sw(0.1)+i*sw(0.2),sh(0.04)),sh(0.015))

        # Timer bar
        t_ratio=max(0,time_left/TIME_LIMIT)
        t_col=LIME if t_ratio>0.5 else ORANGE if t_ratio>0.25 else RED
        pygame.draw.rect(screen,STEEL,(sw(0.04),sh(0.07),sw(0.92),sh(0.018)),border_radius=6)
        if t_ratio>0:
            pygame.draw.rect(screen,t_col,(sw(0.04),sh(0.07),int(sw(0.92)*t_ratio),sh(0.018)),border_radius=6)

        # Score
        sc=fnt_tiny.render(f"Score: {score}",True,GOLD)
        screen.blit(sc,sc.get_rect(topright=(SW-sw(0.03),sh(0.01))))

        # Question card
        qcard=pygame.Rect(sw(0.03),sh(0.10),sw(0.94),sh(0.50))
        pygame.draw.rect(screen,(10,40,15),qcard,border_radius=14)
        pygame.draw.rect(screen,GREEN,qcard,2,border_radius=14)

        lines=wrap(q["q"],fnt_sm,sw(0.88))
        total_h=len(lines)*fnt_sm.get_height()*1.3
        sy=qcard.centery-total_h//2
        for i,ln in enumerate(lines):
            lt=fnt_sm.render(ln,True,WHITE)
            screen.blit(lt,lt.get_rect(center=(SW//2,int(sy+i*fnt_sm.get_height()*1.3))))

        # Fact
        if show_fact and q.get("fact"):
            fl=wrap("💡 "+q["fact"],fnt_tiny,sw(0.88))
            fb_h=len(fl)*fnt_tiny.get_height()*1.3+sh(0.02)
            fb=pygame.Rect(sw(0.03),sh(0.585)-fb_h,sw(0.94),fb_h)
            pygame.draw.rect(screen,(5,30,40),fb,border_radius=10)
            pygame.draw.rect(screen,(0,180,200),fb,1,border_radius=10)
            for i,fl2 in enumerate(fl):
                ft=fnt_tiny.render(fl2,True,(0,210,230))
                screen.blit(ft,(fb.x+sw(0.02),int(fb.y+sh(0.01)+i*fnt_tiny.get_height()*1.3)))

        # Buttons
        for i,(rect,opt) in enumerate(zip(btn_rects,q["options"])):
            if not answered:
                fill=(12,50,18); border=GREEN; tc=WHITE
            else:
                if i==q["answer"]:   fill=(10,50,15); border=LIME;  tc=LIME
                elif i==chosen:      fill=(50,10,10); border=RED;   tc=RED
                else:                fill=(10,20,12); border=STEEL; tc=GRAY
            pygame.draw.rect(screen,fill,rect,border_radius=10)
            pygame.draw.rect(screen,border,rect,2,border_radius=10)
            letter=["A","B","C","D"][i]
            lb=pygame.Rect(rect.x+sh(0.008),rect.y+sh(0.008),sh(0.055),sh(0.055))
            pygame.draw.rect(screen,(20,60,25),lb,border_radius=7)
            pygame.draw.rect(screen,border,lb,1,border_radius=7)
            screen.blit(fnt_tiny.render(letter,True,border),
                        fnt_tiny.render(letter,True,border).get_rect(center=lb.center))
            opt_lines=wrap(opt,fnt_tiny,rect.width-sh(0.08))
            oy=rect.centery-len(opt_lines)*fnt_tiny.get_height()*0.6
            for j,ol in enumerate(opt_lines):
                ot=fnt_tiny.render(ol,True,tc)
                screen.blit(ot,(rect.x+sh(0.075),int(oy+j*fnt_tiny.get_height()*1.2)))

        if answered and chosen==-1:
            tm=fnt_sm.render("⏰ TIME'S UP!",True,ORANGE)
            screen.blit(tm,tm.get_rect(center=(SW//2,sh(0.595))))

        pygame.display.flip()

    return score

# ── Launch ────────────────────────────────────────────────
while True:
    title_screen()
    final=run_quiz()
    results_screen(final)